package dev.ajaczero.powersuits.item;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import java.util.Comparator;
import java.util.List;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageType;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * The chainsaw and the drill as melee weapons (2026-11-16): while a pilot holds the trigger with a mob in front of the
 * tool, the tool grinds it instead of mining. Steady damage like the chaingun's spin (no hit immunity: their damage types
 * are in {@code bypasses_cooldown}), no knockback (the {@code no_knockback} tag: you stay locked on it) and a slowness
 * that is renewed every tick. The two differ in numbers only: the saw hurts more, the drill wears the target's armour
 * ({@link #wearArmour}). A pilot grinds what is under their crosshair; the companion mind (2026-11-16) only its own chosen
 * target, so a hit on its owner or a pet can't happen.
 */
public final class ToolMelee {
    /** "power_suits:saw" / "power_suits:drill" (data/power_suits/damage_type): sawn apart, drilled through. */
    static final ResourceKey<DamageType> SAW = key("saw");
    static final ResourceKey<DamageType> DRILL = key("drill");
    /** How far the bit reaches: a suit's arm is long, but this is still a melee. */
    private static final double REACH = 4.0;
    /** Mobs are a little easier to hit than their boxes. */
    private static final double SLACK = 0.25;

    private ToolMelee() {
    }

    private static ResourceKey<DamageType> key(String name) {
        return ResourceKey.create(Registries.DAMAGE_TYPE, Identifier.fromNamespaceAndPath(PowerSuits.MODID, name));
    }

    /** The mind's target is in reach: from the eye to its box, within the melee reach. */
    public static boolean inReach(PowerSuitEntity suit, LivingEntity target) {
        Vec3 eye = suit.getEyePosition();
        AABB box = target.getBoundingBox();
        double dx = Math.max(Math.max(box.minX - eye.x, 0), eye.x - box.maxX), dy = Math.max(Math.max(box.minY - eye.y, 0), eye.y - box.maxY),
                dz = Math.max(Math.max(box.minZ - eye.z, 0), eye.z - box.maxZ);
        return dx * dx + dy * dy + dz * dz <= (REACH - 0.5) * (REACH - 0.5);
    }

    /** What the tool grinds: a pilot's is the nearest living thing under the crosshair within reach and not behind a block;
     *  a mind's is only the target it picked (it must never hit its owner or a pet that stands in front of it). */
    @Nullable
    static LivingEntity target(PowerSuitEntity suit, LivingEntity operator) {
        if (!(operator instanceof Player)) {
            LivingEntity chosen = suit.getTarget();
            return chosen != null && chosen.isAlive() && inReach(suit, chosen) && suit.getSensing().hasLineOfSight(chosen) ? chosen : null;
        }
        Vec3 eye = operator.getEyePosition();
        Vec3 end = eye.add(operator.getViewVector(1F).scale(REACH));
        List<Entity> near = suit.level().getEntities(suit, new AABB(eye, end).inflate(1.0),
                e -> e instanceof LivingEntity && e.isAlive() && e != operator && !e.isSpectator() && !suit.hasPassenger(e) && e.isPickable());
        HitResult block = suit.level().clip(new ClipContext(eye, end, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, operator));
        double wall = block.getType() == HitResult.Type.BLOCK ? eye.distanceToSqr(block.getLocation()) : Double.MAX_VALUE;
        return near.stream()
                .filter(e -> {
                    AABB box = e.getBoundingBox().inflate(SLACK);
                    return box.contains(eye) || box.clip(eye, end).map(p -> eye.distanceToSqr(p) < wall).orElse(false);
                })
                .min(Comparator.comparingDouble(e -> e.distanceToSqr(eye)))
                .map(e -> (LivingEntity) e).orElse(null);
    }

    /**
     * One tick of grinding on a pilot's target: pays {@code energy} (nothing happens without it), slows it, and every
     * {@code interval} ticks hurts it by {@code damage} and wears its armour by {@code armourWear}.
     * Returns false when there is nothing to grind (the tool goes on mining) .
     */
    static boolean grind(PowerSuitEntity suit, LivingEntity operator, ResourceKey<DamageType> type, float damage, int interval,
                         int energy, int slowLevel, int armourWear) {
        if (!(suit.level() instanceof ServerLevel level)) {
            return false;
        }
        LivingEntity target = target(suit, operator);
        if (target == null) {
            return false;
        }
        if (!suit.power().hasEnergyFor(energy)) {
            return true; // out of fuel: neither grinds nor digs
        }
        suit.power().tryUseEnergy(energy);
        if (slowLevel > 0) {
            target.addEffect(new MobEffectInstance(MobEffects.SLOWNESS, 10, slowLevel - 1, false, false, true), operator);
        }
        Vec3 at = target.getBoundingBox().getCenter();
        if (suit.tickCount % interval != 0) {
            return true;
        }
        DamageSource source = level.damageSources().source(type, operator);
        if (target.hurtServer(level, source, damage)) {
            operator.setLastHurtMob(target);
            wearArmour(level, source, target, armourWear);
            level.sendParticles(ParticleTypes.CRIT, at.x, at.y, at.z, 2, 0.2, 0.3, 0.2, 0.2);
            level.sendParticles(ParticleTypes.CRIT, at.x, at.y, at.z, 1, 0.1, 0.1, 0.1, 0.1);
        }
        return true;
    }

    /** Extra durability loss on whatever the target wears: a suit's armour pieces, or a mob's / player's armour slots. */
    private static void wearArmour(ServerLevel level, DamageSource source, LivingEntity target, int amount) {
        if (amount <= 0) {
            return;
        }
        if (target instanceof PowerSuitEntity other) {
            other.wearArmour(level, source, amount);
            return;
        }
        for (EquipmentSlot slot : EquipmentSlot.VALUES) {
            if (slot.getType() != EquipmentSlot.Type.HUMANOID_ARMOR) {
                continue;
            }
            ItemStack stack = target.getItemBySlot(slot);
            if (!stack.isEmpty() && stack.isDamageableItem() && stack.canBeHurtBy(source)) {
                stack.hurtAndBreak(amount, target, slot);
            }
        }
    }
}
