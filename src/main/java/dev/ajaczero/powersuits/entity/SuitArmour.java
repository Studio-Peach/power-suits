package dev.ajaczero.powersuits.entity;

import dev.ajaczero.powersuits.HudAlert;
import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.PowerSuitsConfig;
import dev.ajaczero.powersuits.item.ArmourPiece;
import dev.ajaczero.powersuits.item.ArmourTier;
import dev.ajaczero.powersuits.item.SuitArmourItem;
import dev.ajaczero.powersuits.item.SuitHelmetItem;
import net.minecraft.core.Holder;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.particles.ItemParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.util.Mth;
import net.minecraft.world.Container;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ItemStack;
import org.jetbrains.annotations.Nullable;

/**
 * The armour on the frame (design sec. 10, 2026-11-14): one piece per part, torso, each arm, each leg, in the suit's
 * armour slots (and the helmet in its own). The bare frame has no armour of its own; each piece adds its tier's points
 * (PowerSuitsConfig, "armour"), the helmet its own. The suit is sealed (SuitSeal) only with all five pieces and the
 * helmet on, powered: {@link PowerSuitEntity#isSealed}.
 * <p>
 * The server keeps the protection as one attribute modifier per part. They're transient (not saved), so a loaded suit
 * gets them from its slots, with the config's current numbers: {@link #applyProtection} runs whenever the slots
 * change and once a tick (a cheap compare) to follow config edits. Clients learn what's worn from one synced int
 * (PowerSuitEntity's ARMOUR: each part's tier, to draw the pieces and count the seal).
 */
public final class SuitArmour {
    /** The frame's parts that take armour, each with its slot in the suit's inventory and the piece that fits it. */
    public enum Part {
        TORSO(PowerSuitEntity.TORSO_SLOT, ArmourPiece.TORSO, "torso"),
        LEFT_ARM(PowerSuitEntity.LEFT_ARM_SLOT, ArmourPiece.ARM, "left_arm"),
        RIGHT_ARM(PowerSuitEntity.RIGHT_ARM_SLOT, ArmourPiece.ARM, "right_arm"),
        LEFT_LEG(PowerSuitEntity.LEFT_LEG_SLOT, ArmourPiece.LEG, "left_leg"),
        RIGHT_LEG(PowerSuitEntity.RIGHT_LEG_SLOT, ArmourPiece.LEG, "right_leg");

        public final int slot;
        public final ArmourPiece piece;
        final Identifier modifier;

        Part(int slot, ArmourPiece piece, String name) {
            this.slot = slot;
            this.piece = piece;
            this.modifier = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "armour/" + name);
        }

        /** Whether a stack may go on this part: frame armour of this part's kind (an arm piece fits either arm). */
        public boolean fits(ItemStack stack) {
            SuitArmourItem armour = SuitArmourItem.of(stack);
            return armour != null && armour.piece() == this.piece;
        }

        /** Where the piece sits on the frame, in blocks: sideways (+ = the suit's left) and up from its feet. Only for
         *  the particles of a piece that breaks. */
        double side() {
            return switch (this) {
                case TORSO -> 0;
                case LEFT_ARM -> 0.45;
                case RIGHT_ARM -> -0.45;
                case LEFT_LEG -> 0.18;
                case RIGHT_LEG -> -0.18;
            };
        }

        double height() {
            return this == TORSO ? 1.45 : this.piece == ArmourPiece.ARM ? 1.35 : 0.5;
        }

        public static @Nullable Part ofSlot(int slot) {
            for (Part part : values()) {
                if (part.slot == slot) {
                    return part;
                }
            }
            return null;
        }
    }

    /** The helmet's height on the frame, in blocks (its break particles). */
    private static final double HELMET_HEIGHT = 2.0;
    private static final Identifier HELMET_MODIFIER = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "armour/helmet");
    /** Bits per part in the synced int: the tier's ordinal + 1, 0 = nothing worn (7 tiers fit). */
    private static final int BITS = 3;

    private final PowerSuitEntity suit;

    SuitArmour(PowerSuitEntity suit) {
        this.suit = suit;
    }

    /** Server: what the slots hold, packed for the synced copy (each part's tier ordinal + 1 in its 3 bits). */
    static int encode(Container slots) {
        int worn = 0;
        for (Part part : Part.values()) {
            SuitArmourItem armour = SuitArmourItem.of(slots.getItem(part.slot));
            if (armour != null && armour.piece() == part.piece) {
                worn |= (armour.tier().ordinal() + 1) << (part.ordinal() * BITS);
            }
        }
        return worn;
    }

    /** Server: how worn each piece is, packed for the synced copy: 2 bits per part (then the helmet's), the piece's
     *  {@link HudAlert} from what is left of its durability (fine / half gone / last 15%): the visor's figure shows it. A
     *  broken helmet counts as nothing left. */
    static int encodeWear(Container slots) {
        int wear = 0;
        for (Part part : Part.values()) {
            ItemStack stack = slots.getItem(part.slot);
            if (part.fits(stack)) {
                wear |= left(stack).ordinal() << (part.ordinal() * 2);
            }
        }
        ItemStack helmet = slots.getItem(PowerSuitEntity.HELMET_SLOT);
        if (helmet.getItem() instanceof SuitHelmetItem) {
            wear |= left(helmet).ordinal() << (Part.values().length * 2);
        }
        return wear;
    }

    private static HudAlert left(ItemStack stack) {
        return stack.isDamageableItem() ? HudAlert.ofLeft(1F - (float) stack.getDamageValue() / stack.getMaxDamage()) : HudAlert.NONE;
    }

    /** Both sides: how worn the piece on this part is (NONE for a bare part too: see {@link #worn}). */
    public HudAlert condition(Part part) {
        return alert(this.suit.getEntityData().get(PowerSuitEntity.ARMOUR_WEAR) >> (part.ordinal() * 2));
    }

    /** Both sides: how worn the helmet is. */
    public HudAlert helmetCondition() {
        return alert(this.suit.getEntityData().get(PowerSuitEntity.ARMOUR_WEAR) >> (Part.values().length * 2));
    }

    private static HudAlert alert(int bits) {
        return HudAlert.values()[Math.min(bits & 3, HudAlert.values().length - 1)];
    }

    /** Both sides: the tier of the piece on this part, or null for a bare part. */
    public @Nullable ArmourTier worn(Part part) {
        int id = (this.suit.getEntityData().get(PowerSuitEntity.ARMOUR) >> (part.ordinal() * BITS)) & ((1 << BITS) - 1);
        return ArmourTier.byId(id - 1);
    }

    /** Both sides: which parts are armoured, one bit per Part (1 << ordinal): what the renderer shows. */
    public int wornMask() {
        int mask = 0;
        for (Part part : Part.values()) {
            if (this.worn(part) != null) {
                mask |= 1 << part.ordinal();
            }
        }
        return mask;
    }

    /** Both sides: how many of the five parts are armoured. */
    public int pieces() {
        int count = 0;
        for (Part part : Part.values()) {
            if (this.worn(part) != null) {
                count++;
            }
        }
        return count;
    }

    /** Both sides: every part armoured (any tiers, mixed too): with the helmet, what the seal needs. */
    public boolean fullSet() {
        return this.pieces() == Part.values().length;
    }

    /**
     * Server: one armour modifier per part (its piece's points, none when bare) and one for the helmet, set to the
     * config's current numbers. Only touches a modifier whose amount changed, so it's cheap to call every tick.
     */
    void applyProtection() {
        AttributeInstance armour = this.suit.getAttribute(Attributes.ARMOR);
        if (armour == null) {
            return;
        }
        Container slots = this.suit.getInventory();
        for (Part part : Part.values()) {
            SuitArmourItem piece = SuitArmourItem.of(slots.getItem(part.slot));
            set(armour, part.modifier, piece != null && piece.piece() == part.piece ? piece.tier().protection(part.piece) : 0);
        }
        ItemStack helmet = slots.getItem(PowerSuitEntity.HELMET_SLOT);
        set(armour, HELMET_MODIFIER, helmet.isEmpty() || SuitHelmetItem.isBroken(helmet) ? 0 : PowerSuitsConfig.HELMET_ARMOUR.get());
    }

    /**
     * Server, from the suit's hurtArmor (vanilla calls it for every hit that armour reduces: not /kill, the void,
     * starving...): every worn piece wears like vanilla armour, max(1, damage / 4) durability a hit (times the config's
     * wear). A piece worn out breaks like vanilla armour (its break sound, bits of it
     * flying) and is gone: the part is bare, its protection and the seal with it (design sec. 10, 2026-11-14).
     * The helmet wears the same but stays on when worn out: broken (SuitHelmetItem.isBroken, user 2026-11-14).
     */
    void wear(ServerLevel level, DamageSource source, float damage) {
        double wear = PowerSuitsConfig.ARMOUR_WEAR.get();
        if (damage <= 0 || wear <= 0) {
            return;
        }
        int amount = Math.max(1, (int) (damage / 4.0F * wear));
        Container slots = this.suit.getInventory();
        boolean changed = false;
        for (Part part : Part.values()) {
            ItemStack stack = slots.getItem(part.slot);
            if (!part.fits(stack) || !stack.isDamageableItem() || !stack.canBeHurtBy(source)) {
                continue;
            }
            // The suit as the owner: vanilla skips the wear only for players in creative (a mob never is).
            stack.hurtAndBreak(amount, level, this.suit, broken -> this.breakEffects(level, part.side(), part.height(), broken));
            if (stack.isEmpty()) {
                slots.setItem(part.slot, ItemStack.EMPTY); // tells the container: syncSlots drops its protection, the seal
            }
            changed = true;
        }
        ItemStack helmet = slots.getItem(PowerSuitEntity.HELMET_SLOT);
        if (helmet.getItem() instanceof SuitHelmetItem && helmet.isDamageableItem() && !helmet.isBroken() && helmet.canBeHurtBy(source)) {
            // not hurtAndBreak: that would use it up at its max damage; it stops there instead (like an elytra)
            helmet.setDamageValue(Math.min(helmet.getMaxDamage(), helmet.getDamageValue() + amount));
            if (helmet.isBroken()) {
                this.breakEffects(level, 0, HELMET_HEIGHT, helmet);
            }
            changed = true;
        }
        if (changed) {
            // a stack damaged in place doesn't tell its container (the menu's durability bars follow the slots anyway)
            slots.setChanged();
        }
    }

    /** What vanilla shows when a worn piece breaks (LivingEntity.breakItem: a client-side entity event for equipment
     *  slots, which the suit's pieces aren't in), sent from the server at the piece's place on the frame. */
    private void breakEffects(ServerLevel level, double side, double height, ItemStack broken) {
        float yaw = this.suit.yBodyRot * Mth.DEG_TO_RAD;
        // the suit's left in the world: yaw 0 faces +z, so its left is +x
        double x = this.suit.getX() + Mth.cos(yaw) * side;
        double z = this.suit.getZ() + Mth.sin(yaw) * side;
        double y = this.suit.getY() + height;
        Holder<SoundEvent> sound = broken.get(DataComponents.BREAK_SOUND);
        if (sound != null && !this.suit.isSilent()) {
            level.playSound(null, x, y, z, sound.value(), this.suit.getSoundSource(), 0.8F, 0.8F + this.suit.getRandom().nextFloat() * 0.4F);
        }
        level.sendParticles(new ItemParticleOption(ParticleTypes.ITEM, broken.getItem()), x, y, z, 12, 0.15, 0.2, 0.15, 0.08);
    }

    private static void set(AttributeInstance attribute, Identifier id, double amount) {
        AttributeModifier current = attribute.getModifier(id);
        if (amount == 0) {
            if (current != null) {
                attribute.removeModifier(id);
            }
        } else if (current == null || current.amount() != amount) {
            attribute.addOrUpdateTransientModifier(new AttributeModifier(id, amount, AttributeModifier.Operation.ADD_VALUE));
        }
    }
}
