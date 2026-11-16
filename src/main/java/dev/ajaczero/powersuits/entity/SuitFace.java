package dev.ajaczero.powersuits.entity;

import java.util.Locale;
import org.jspecify.annotations.Nullable;

/**
 * Client: the robot helmet's visor face (design sec. 4c, user 2026-11-15). The robot's visor doesn't light up as the
 * other helmets' do (its big glass lit amber read as one block with the gold): it shows simple faces instead, eyes
 * only, as reactions to what happens to the suit, in the visor's colour (who is in control: amber a pilot, green the
 * friendly mind, red a rogue; SuitLights), and stays dark when nothing is happening. The faces' art is
 * model/art/frame_helmet_art.py ROBOT_FACES; tools/export-frame.py makes a glowmask of each, SuitGlowLayer draws the one
 * picked here.
 *
 * What shows, strongest first: nothing without a helmet, or without power unless knocked out; x x while the helmet is
 * broken; @ @ while dizzy (knocked out by lightning: the suit is off, but the dizzy face shows through it; or held in
 * another suit's EM field); then the latest reaction while it lasts: > < for a hit, ^^ when a pilot climbs in, heart eyes when
 * it's refuelled or its helmet repaired, angry when the suit lands a blow (its punches, stomps and tools' hits on a
 * living thing: the server tells the clients, {@link #STRUCK}); then half-lidded effort while a socket tool works; a
 * rogue's lasting angry face; else dark.
 *
 * One of the suit's parts through {@code suit.lights().face()}. It only reads what every client already has (the
 * synced data, the hurt flash) apart from the struck event, and the choice itself ({@link #pick}) and the reactions
 * ({@link #tick}) take plain inputs, so the GameTests check them without a client.
 */
public final class SuitFace {
    /** The faces (frame_helmet_art.py ROBOT_FACES, same names): each has a glowmask power_frame_glow_robot_<id>. */
    public enum Face {
        HIT, BROKEN, DIZZY, HAPPY, ANGRY, LOVE, EFFORT;

        /** Its name in the art and the glowmask's file name. */
        public String id() {
            return this.name().toLowerCase(Locale.ROOT);
        }
    }

    /** The entity event the server sends when the suit (or its pilot through it) hurts something living: the visor
     *  shows angry for a moment. Above vanilla's own events (EntityEvent, 0..72). */
    public static final byte STRUCK = 112;
    /** How long each reaction shows, in ticks. */
    public static final int HIT_TICKS = 20, CHEER_TICKS = 40, ANGRY_TICKS = 30;

    /**
     * What the face reads each tick. knockedOut: lightning tripped the electrics (unpowered for a few seconds);
     * fieldHeld: another suit's EM field holds it; hurtTime: the suit's hurt flash (vanilla's, set on every client by
     * the damage event, counting down); fuel: how many items in the fuel slot.
     */
    public record Inputs(boolean helmet, boolean powered, boolean broken, boolean knockedOut, boolean fieldHeld, boolean piloted,
                         int hurtTime, int fuel, boolean toolActive, boolean rogue) {
        static Inputs of(PowerSuitEntity suit) {
            return new Inputs(suit.hasHelmet(), suit.isPowered(), suit.isHelmetBroken(), suit.isStunned(), suit.driving().isFieldHeld(),
                    suit.isVehicle(), suit.hurtTime, suit.getFuelStack().getCount(), suit.socket().isActive(), suit.isRogue());
        }
    }

    private @Nullable Inputs last;
    private @Nullable Face reaction;
    private int reactionTicks;
    private @Nullable Face shown;

    /** Client, every tick (from SuitLights). */
    void tick(PowerSuitEntity suit) {
        this.shown = this.tick(Inputs.of(suit));
    }

    /** One tick with these inputs: notices what changed since the last tick, starts its reaction, counts the reaction
     *  down, and returns the face to show. */
    public @Nullable Face tick(Inputs now) {
        if (this.reactionTicks > 0 && --this.reactionTicks == 0) {
            this.reaction = null;
        }
        Inputs before = this.last;
        this.last = now;
        if (before != null) { // (the first tick only learns the state: a suit coming into view doesn't react to it)
            if (now.hurtTime() > before.hurtTime()) {
                this.react(Face.HIT, HIT_TICKS);
            } else if (now.piloted() && !before.piloted()) {
                this.react(Face.HAPPY, CHEER_TICKS);
            } else if (now.fuel() > before.fuel() || (before.broken() && !now.broken())) {
                this.react(Face.LOVE, CHEER_TICKS);
            }
        }
        return pick(now, this.reaction);
    }

    /** Client: the suit landed a blow (the server's STRUCK event). */
    public void struck() {
        this.react(Face.ANGRY, ANGRY_TICKS);
    }

    private void react(Face face, int ticks) {
        this.reaction = face;
        this.reactionTicks = ticks;
    }

    /** The face for this state with this reaction running (null: none), strongest first (see the class comment). */
    public static @Nullable Face pick(Inputs now, @Nullable Face reaction) {
        if (!now.helmet() || !(now.powered() || now.knockedOut())) {
            return null;
        }
        if (now.broken()) {
            return Face.BROKEN;
        }
        if (now.knockedOut() || now.fieldHeld()) {
            return Face.DIZZY;
        }
        if (reaction != null) {
            return reaction;
        }
        if (now.toolActive()) {
            return Face.EFFORT;
        }
        return now.rogue() ? Face.ANGRY : null;
    }

    /** Client: the face showing now (null: the visor is dark). */
    public @Nullable Face shown() {
        return this.shown;
    }
}
