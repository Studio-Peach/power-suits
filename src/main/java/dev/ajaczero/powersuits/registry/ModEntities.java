package dev.ajaczero.powersuits.registry;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.Bullet;
import dev.ajaczero.powersuits.entity.FlameJet;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.entity.TntShell;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModEntities {
    // createEntities: since 1.21.2 every entity type is built with its registry key; this register fills it in.
    public static final DeferredRegister.Entities ENTITIES = DeferredRegister.createEntities(PowerSuits.MODID);

    public static final DeferredHolder<EntityType<?>, EntityType<PowerSuitEntity>> POWER_SUIT =
            ENTITIES.registerEntityType("power_suit", PowerSuitEntity::new, MobCategory.MISC, builder -> builder
                    // Hitbox in blocks: the frame (model/power_frame.bbmodel) is 36 px tall to the pilot's head, the
                    // helmet half a px more, so 2.3. Under 3, so vanilla's pathfinder (it wants floor(height + 1) free
                    // blocks) walks the machine mind through 3-high gaps. 0.9 wide: the torso is 12 px and the arms
                    // reach 23, and like a player's (0.6 for a 16 px wide model) the box covers the body, not the
                    // arms, so it fits through 1-wide gaps as a player does.
                    // (The big suit before it: 1.4 x 2.95, eyes 2.6, the pilot seated at (0, 1.58, 0.55).)
                    .sized(0.9F, 2.3F)
                    .eyeHeight(1.98F)
                    // Where the pilot is mounted: standing in the frame on its 4 px soles, the camera at his own eyes.
                    // His eyes are 1.62 above his feet, 27.65 model px drawn at vanilla's 0.9375; the frame draws him
                    // at full scale: 4 + 27.65 = 31.65 px = 1.98 blocks up. The player's own vehicle offset is 0.6
                    // (Avatar.DEFAULT_VEHICLE_ATTACHMENT), so the seat is 1.98 - 1.62 + 0.6 = 0.96.
                    .passengerAttachments(new Vec3(0, 0.96, 0))
                    .clientTrackingRange(10));

    /** The chaingun's bullet. Updated every tick so its tracer stays smooth at 80 blocks/s. */
    public static final DeferredHolder<EntityType<?>, EntityType<Bullet>> BULLET =
            ENTITIES.registerEntityType("bullet", Bullet::new, MobCategory.MISC, builder -> builder
                    .sized(0.2F, 0.2F)
                    .clientTrackingRange(8)
                    .updateInterval(1));

    /** The flamethrower's stream: one gob of burning fuel per tick, half a second of life. Updated every tick (fast). */
    public static final DeferredHolder<EntityType<?>, EntityType<FlameJet>> FLAME_JET =
            ENTITIES.registerEntityType("flame_jet", FlameJet::new, MobCategory.MISC, builder -> builder
                    .sized(0.25F, 0.25F)
                    .clientTrackingRange(6)
                    .updateInterval(1));

    /** The TNT launcher's round: a primed TNT block in flight (half a block wide). Updated every tick (it arcs). */
    public static final DeferredHolder<EntityType<?>, EntityType<TntShell>> TNT_SHELL =
            ENTITIES.registerEntityType("tnt_shell", TntShell::new, MobCategory.MISC, builder -> builder
                    .sized(0.5F, 0.5F)
                    .clientTrackingRange(8)
                    .updateInterval(1));

    private ModEntities() {}
}
