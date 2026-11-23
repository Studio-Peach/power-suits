package dev.ajaczero.powersuits.item;



/**
 * The socket tools' lights: each is a glowmask texture (client/SuitGlowLayer maps them to their files, made by
 * tools/make-glowmasks.py from the reserved colours) drawn full-bright over the tool by the suit and the cockpit
 * viewmodel. A tool's ToolEffects sets the brightness of its own lights every frame.
 */
public enum ToolLight {
    /** The chaingun's barrel tips, red- to white-hot with heat. */
    HEAT(true),
    /** The chaingun's barrels behind the tips, only once they're really hot. */
    HEAT_BARREL(true),
    /** The EM projector's lens and cuff capacitor ports (fade by opacity cleanly over unlit dark redstone). */
    EM_CORE(true),
    /** The EM projector's prong arc rails and tips. */
    EM_ARC(true),
    /** The flamethrower's pilot light. */
    PILOT(true),
    /** The rail cannon's core rings, a third each: lit in turn, the energy runs along the core. */
    RAIL_FLOW_0(true),
    RAIL_FLOW_1(true),
    RAIL_FLOW_2(true),
    /** The emitter in the rail cannon's band. */
    RAIL_EMIT(true),
    /** The frame's tools' status lamp (the drill's, chainsaw's and chaingun's base, 2026-11-14): red while the tool is
     *  ready, green while it runs, dark without power (ToolEffects.statusLamp). One mask per colour. */
    LAMP_IDLE(false),
    LAMP_RUN(false),
    /** The frame's chaingun's green muzzle lights (its signature colour): on with the power. */
    GUN_LIGHT(true);

    /** Fades in by opacity instead of brightness: light over cold metal or over nothing (see SuitGlowLayer.energy). The
     *  others are opaque lights whose colour is dimmed (SuitGlowLayer.tint). */
    public final boolean fadesByAlpha;

    ToolLight(boolean fadesByAlpha) {
        this.fadesByAlpha = fadesByAlpha;
    }
}
