package dev.ajaczero.powersuits.entity;

import dev.ajaczero.powersuits.PowerSuitsConfig;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.MoverType;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * How the suit moves (design sec. 3): the pilot's keys, walking and sprinting speeds, stepping down ledges, sinking and
 * walking along the bottom of water and lava, the instant jump, crawling in an EM field, and the legs turning under the
 * torso. The pilot's or the mind's: both drive the same legs.
 *
 * One of the suit's parts (see PowerSuitEntity): {@code suit.driving()}. Vanilla calls its movement hooks on the entity
 * (travel, tickRidden, tickHeadTurn...: the ones horses use); the entity passes them on to here. Ridden movement is
 * client-authoritative: for a piloted suit these run on the pilot's client, for an empty one on the server
 * ({@code isLocalInstanceAuthoritative}); the turning runs on every side, from synced values only, so all agree.
 */
public final class SuitDriving {
    // ---- Speed -----------------------------------------------------------------------------
    // Attribute speed -> blocks per second on flat ground for ridden entities. Measured in game with
    // ./gradlew runAutopilot: 42.14 on 1.21.1; on 26.3 the same speed attribute went 2.4% further (0.11865 gave
    // 5.12 blocks/s instead of 5.00), so x43.15.
    private static final double BLOCKS_PER_SECOND_PER_SPEED = 43.15;
    // Powered brisk walk and sprint (2026-11-22: 4.8 / 6.8 blocks/s; a player walks at 4.3 and sprints at 5.6).
    // The old big mech walked at 3.0 to stay close to its baked Blockbench cycle; the frame uses vanilla's procedural
    // limb swing, so the walk isn't tied to an authored cadence.
    /** The walk on flat ground, blocks/s (tests compare against it). */
    public static final double WALK_BLOCKS_PER_SECOND = 4.8;
    /** The movement speed attribute for that walk (PowerSuitEntity.BASE_STATS). */
    static final double WALK_SPEED = WALK_BLOCKS_PER_SECOND / BLOCKS_PER_SECOND_PER_SPEED;
    /** The sprint on flat ground, blocks/s. */
    public static final double SPRINT_BLOCKS_PER_SECOND = 6.8;
    /** Sprint / walk multiplier: 6.8 blocks/s sprint. */
    public static final float SPRINT_MULTIPLIER = (float) (SPRINT_BLOCKS_PER_SECOND / WALK_BLOCKS_PER_SECOND);
    /** Ground speed (blocks/s) between the walk and the sprint: the mind, which has no sprint key, runs above it. */
    static final double RUN_THRESHOLD = 5.8;
    /** A suit held in an EM field crawls: a quarter of its speed. */
    private static final float FIELD_HELD_SPEED = 0.25F;

    // ---- Terrain ----------------------------------------------------------------------------
    /** Walking off a ledge up to this high keeps the suit planted (steps down instead of falling).
     *  2 blocks: a 3-block-tall mech steps down mountain terraces; the step easing smooths it. */
    static final double STEP_DOWN = 2.1;

    // ---- Water (Fallout-style: the suit sinks and walks along the bottom) ----------------------
    /** Speed on the bottom relative to dry land. */
    static final float UNDERWATER_SPEED = 0.5F;
    /** Lava is thicker: the suit wades through it (and its hull burns) at a third of its speed. */
    static final float LAVA_SPEED = 0.35F;
    /** Steering while sinking / rising, relative to UNDERWATER_SPEED. */
    private static final float UNDERWATER_AIR_CONTROL = 0.3F;
    /** Downward acceleration per tick and the vertical drag: terminal sink ~2.8 blocks/s. */
    private static final double SINK_ACCEL = 0.025;
    private static final double WATER_DRAG_Y = 0.85;
    /** Horizontal drag per tick on the bottom (same as dry ground, so it feels like walking). */
    private static final double WATER_DRAG_XZ = 0.546;
    /** Jumps underwater are pushing off against water. */
    private static final double UNDERWATER_JUMP_SCALE = 0.6;

    // ---- Jumping ---------------------------------------------------------------------------
    /** Instant jump vertical velocity (blocks/tick): ~2.30 blocks peak on land (clears 2-block ledges cleanly, stays
     *  below the 3.5-block stomp threshold; the suit already auto-steps 1-block ledges). */
    static final double JUMP_VELOCITY = 0.59;
    /** Matches vanilla LivingEntity.noJumpDelay: holding Space re-jumps on landing without double-firing under a low
     *  ceiling; releasing Space resets it to 0 immediately. */
    private static final int JUMP_COOLDOWN_TICKS = 10;

    // ---- Turning (legs vs torso) ---------------------------------------------------------------
    /** The torso can twist this far from the legs before the legs are dragged along. */
    static final float MAX_TWIST = 90F;
    /** Standing still, the legs shuffle round once the view is this far off... */
    private static final float IDLE_REALIGN_START = 50F;
    /** ...and stop once they're this close. */
    private static final float IDLE_REALIGN_END = 8F;
    /** Leg turn rates, degrees per tick. */
    private static final float LEG_TURN_MOVING = 18F;
    private static final float LEG_TURN_IDLE = 7F;

    private final PowerSuitEntity suit;
    /** Ticks before holding Space can trigger another jump (reset to 0 as soon as Space is released). */
    private int jumpCooldown;
    /** True on the tick a jump launched, so travel()'s ledge step-down doesn't snap back down under a low ceiling. */
    private boolean jumpedThisTick;
    /** Legs are turning to catch up with the torso while standing still. */
    private boolean realigning;
    /** Server: tick the suit was last held by an EM field (EmProjectorItem refreshes it every tick it holds us). */
    private int fieldHeldUntil;

    SuitDriving(PowerSuitEntity suit) {
        this.suit = suit;
    }

    /**
     * The pilot's WASD as (strafe, 0, forward), each -1..1 (+x = left, +z = forward, like the player's xxa / zza).
     * The pilot's own client moves the suit with its xxa / zza. The server learns the keys from the input packet vanilla
     * sends for every passenger (that's how a boat knows you're paddling); since 1.21.2 that packet no longer fills the
     * server player's xxa / zza, only its "last client input" (keys pressed). GameTests' mock players set xxa / zza.
     */
    public static Vec3 pilotInput(Player pilot) {
        if (pilot instanceof ServerPlayer sp) {
            var keys = sp.getLastClientInput();
            float strafe = keys.left() == keys.right() ? 0F : keys.left() ? 1F : -1F;
            float forward = keys.forward() == keys.backward() ? 0F : keys.forward() ? 1F : -1F;
            if (strafe != 0F || forward != 0F) {
                return new Vec3(strafe, 0, forward);
            }
        }
        return new Vec3(pilot.xxa, 0, pilot.zza);
    }

    /** True while the pilot holds Space. On the local client we read keyJump directly via ClientView so the suit
     *  jumps on the very tick Space is pressed (the suit ticks before its passenger's LocalPlayer.rideTick). */
    public static boolean pilotJumping(Player pilot) {
        if (pilot.level().isClientSide()) {
            return ClientView.jumpPressed.test(pilot);
        }
        if (pilot instanceof ServerPlayer sp && sp.getLastClientInput().jump()) {
            return true;
        }
        return pilot.isJumping();
    }

    // ---- Driving: the pilot's keys ---------------------------------------------------------------

    /** The pilot's keys as the suit's travel input (PowerSuitEntity.getRiddenInput). */
    Vec3 riddenInput(Player pilot) {
        if (!this.suit.canOperate()) {
            return Vec3.ZERO; // out of fuel (or still booting): the legs don't move
        }
        // A/D: full speed since 2026-10-20 (was half). The legs turn to face the way the suit walks, so a strafe is a
        // walk sideways with the torso twisted toward the view; at half speed its steps played in slow motion.
        float strafe = pilot.xxa;
        float forward = pilot.zza;         // W/S
        if (forward < 0) {
            forward *= 0.5F;               // backing up is slow
        }
        return new Vec3(strafe, 0, forward);
    }

    /** The walk, or the sprint while the pilot sprints (PowerSuitEntity.getRiddenSpeed). */
    float riddenSpeed(Player pilot) {
        float speed = (float) this.suit.getAttributeValue(Attributes.MOVEMENT_SPEED);
        return pilot.isSprinting() ? speed * SPRINT_MULTIPLIER : speed;
    }

    /**
     * Movement for the side that moves the suit. After vanilla moves us, if we just walked off a small ledge (and aren't
     * jumping), drop straight onto the ground below: stepping down instead of falling keeps full speed and avoids a fall
     * pose on every block of a slope.
     */
    void travel(Vec3 travelVector) {
        if (!this.suit.isVehicle() && !this.suit.canOperate()) {
            travelVector = Vec3.ZERO; // off (or booting): the legs don't move, whatever the AI's controls still say
        } else if (!this.suit.isVehicle() && travelVector.horizontalDistanceSqr() > 1.0E-6) {
            // Driven by the mind: vanilla's MoveControl passes its speed as the forward input (zza), and the speed is
            // applied again in moveRelative, so mobs move at speed squared. Pushing the stick all the way instead makes
            // the mind's suit walk exactly like a piloted one: 1.0 = the pilot's jog, 2.0 = sprint (walk animation sync).
            Vec3 flat = new Vec3(travelVector.x, 0, travelVector.z).normalize();
            travelVector = new Vec3(flat.x, travelVector.y, flat.z);
        }
        if (this.isFieldHeld()) {
            travelVector = travelVector.multiply(FIELD_HELD_SPEED, 1, FIELD_HELD_SPEED); // the pilot's or the mind's push
        }
        if ((this.suit.isInWater() || this.suit.isInLava()) && this.suit.isLocalInstanceAuthoritative()) {
            this.travelUnderwater(travelVector); // lava too: vanilla's lava swimming crawled at 0.4 blocks/s
            return;
        }
        boolean wasOnGround = this.suit.onGround();
        this.suit.vanillaTravel(travelVector);
        if (this.suit.isVehicle() && this.suit.isLocalInstanceAuthoritative() && wasOnGround && !this.suit.onGround()
                && this.suit.getDeltaMovement().y <= 0 && !this.jumpedThisTick) {
            AABB below = this.suit.getBoundingBox().expandTowards(0, -STEP_DOWN, 0);
            if (!this.suit.level().noCollision(this.suit, below)) {
                this.suit.move(MoverType.SELF, new Vec3(0, -STEP_DOWN, 0)); // stops at the ground
                this.suit.setDeltaMovement(this.suit.getDeltaMovement().multiply(1, 0, 1));
            }
        }
    }

    /**
     * Vanilla makes living things float and paddle in water. The suit is a ton of steel instead:
     * no buoyancy, it sinks to the bottom and walks there at reduced speed. Runs on whichever side
     * controls the suit (the pilot's client, or the server for an empty suit).
     */
    private void travelUnderwater(Vec3 input) {
        float fluidSpeed = this.suit.isInLava() ? LAVA_SPEED : UNDERWATER_SPEED;
        float speed = this.suit.getSpeed() * fluidSpeed * (this.suit.onGround() ? 1.0F : UNDERWATER_AIR_CONTROL);
        this.suit.moveRelative(speed, input);
        this.suit.move(MoverType.SELF, this.suit.getDeltaMovement());
        Vec3 v = this.suit.getDeltaMovement();
        double vy = (v.y - SINK_ACCEL) * WATER_DRAG_Y;
        // Vanilla's "climb out at the edge" help: pushing into a bank near the surface lifts us over.
        if (this.suit.horizontalCollision && this.suit.isFree(v.x, v.y + 0.6 - this.suit.getY() + this.suit.yo, v.z)) {
            vy = 0.3;
        }
        this.suit.setDeltaMovement(v.x * WATER_DRAG_XZ, vy, v.z * WATER_DRAG_XZ);
        // LivingEntity.aiStep calls calculateEntityAnimation after travel() on 26.3: calling it here too doubled it underwater.
    }

    // ---- Jumping: instant Space-to-jump (2026-11-22; replaced the horse jump bar and 2-tick launch delay) ----

    /** Every ridden tick while the suit can operate: launch immediately when Space is held on the ground. */
    void tryJump(Player pilot) {
        this.jumpedThisTick = false;
        if (!this.suit.isLocalInstanceAuthoritative()) {
            return;
        }
        if (this.jumpCooldown > 0) {
            this.jumpCooldown--;
        }
        if (!pilotJumping(pilot)) {
            this.jumpCooldown = 0;
            return;
        }
        if (this.suit.onGround() && this.jumpCooldown == 0) {
            Vec3 motion = this.suit.getDeltaMovement();
            boolean inFluid = this.suit.isInWater() || this.suit.isInLava();
            double launch = JUMP_VELOCITY * (inFluid ? UNDERWATER_JUMP_SCALE : 1.0);
            this.suit.setDeltaMovement(motion.x, launch, motion.z); // ~2.30 blocks on land
            this.suit.needsSync = true; // (was hasImpulse) send the new motion right away
            this.jumpCooldown = JUMP_COOLDOWN_TICKS;
            this.jumpedThisTick = true;
            if (this.suit.level().isClientSide()) {
                this.suit.animator().jumpStarted();
                this.suit.playSound(SoundEvents.PISTON_EXTEND, 0.8F, 0.6F);
                ClientView.sendJump.run();
            } else {
                this.onServerJump();
            }
        }
    }

    /** Server, when the pilot's suit jumps (SuitJumpPayload): notify other clients and pay the jump's fuel. */
    public void onServerJump() {
        this.suit.getEntityData().set(PowerSuitEntity.JUMP_COUNTER, this.suit.getEntityData().get(PowerSuitEntity.JUMP_COUNTER) + 1);
        this.suit.power().consume(PowerSuitsConfig.JUMP_ENERGY.get()); // nothing for a wet tidal engine or a reactor
    }

    /** Power lost (or still booting): clear any jump bookkeeping. */
    void resetJump() {
        this.jumpCooldown = 0;
        this.jumpedThisTick = false;
    }

    // ---- Turning: the legs under the torso -----------------------------------------------------

    /**
     * Vanilla turns the body every tick (server and clients, PowerSuitEntity.tickHeadTurn). For a driven suit (pilot or
     * mind) we turn the legs ourselves: toward the direction of travel while moving (or away from it when backing up),
     * and in small catch-up shuffles when standing still. The renderer then twists the torso by (look - legs), so the
     * upper body always faces where the pilot (or the mind) looks.
     * The mind used vanilla's mob rule until 2026-10-19: it lets the head get past the torso's 90 degree twist before
     * the body follows (the suit drilled a block while facing away from it), and each client works a mob's body yaw out
     * from tiny position changes (the torso swung from side to side while it chased and punched). This rule depends
     * only on the synced head yaw and the movement, so every side agrees.
     * Returns false for a suit nobody drives: vanilla's rule then.
     */
    boolean turnLegs() {
        if (!this.suit.isVehicle() && !this.suit.isAiDriven()) {
            this.realigning = false;
            return false;
        }
        float look = this.suit.getYHeadRot();
        double dx = this.suit.getX() - this.suit.xo, dz = this.suit.getZ() - this.suit.zo;
        boolean moving = dx * dx + dz * dz > 0.0004; // > 0.4 blocks/s
        float target = this.suit.yBodyRot;
        float step = LEG_TURN_IDLE;
        if (moving) {
            float heading = (float) (Mth.atan2(dz, dx) * Mth.RAD_TO_DEG) - 90F;
            if (Math.abs(Mth.wrapDegrees(heading - look)) > 100F) {
                heading += 180F; // backing up: legs keep facing forward
            }
            target = heading;
            step = LEG_TURN_MOVING;
            this.realigning = false;
        } else {
            float twist = Math.abs(Mth.wrapDegrees(look - this.suit.yBodyRot));
            if (twist > IDLE_REALIGN_START) {
                this.realigning = true;
            } else if (twist < IDLE_REALIGN_END) {
                this.realigning = false;
            }
            if (this.realigning) {
                target = look;
            }
        }
        this.suit.yBodyRot = Mth.approachDegrees(this.suit.yBodyRot, target, step);
        // Never let the torso twist past its limit: drag the legs along instead.
        float twist = Mth.wrapDegrees(look - this.suit.yBodyRot);
        if (Math.abs(twist) > MAX_TWIST) {
            this.suit.yBodyRot = look - Math.signum(twist) * MAX_TWIST;
        }
        return true;
    }

    /** True while the legs are shuffling round to face the view (plays a step cycle). */
    public boolean isRealigning() {
        return this.realigning;
    }

    // ---- Held in an EM field -----------------------------------------------------------------------

    /** Server: another suit's EM field holds us this tick. Too heavy to lift, the suit fights the field: it can only
     *  crawl (a quarter of its speed) while held. */
    public void holdInField() {
        this.fieldHeldUntil = this.suit.tickCount + 2;
        this.suit.getEntityData().set(PowerSuitEntity.FIELD_HELD, true);
    }

    /** Both sides: held in an EM field right now (synced: the pilot's client moves a piloted suit, so it must know). */
    public boolean isFieldHeld() {
        return this.suit.getEntityData().get(PowerSuitEntity.FIELD_HELD);
    }

    /** Server, every tick: the field let go when nothing refreshed it. */
    void tick() {
        if (this.isFieldHeld() && this.suit.tickCount > this.fieldHeldUntil) {
            this.suit.getEntityData().set(PowerSuitEntity.FIELD_HELD, false);
        }
    }
}
