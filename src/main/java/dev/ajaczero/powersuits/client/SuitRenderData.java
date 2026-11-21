package dev.ajaczero.powersuits.client;

import com.geckolib.constant.dataticket.DataTicket;
import com.geckolib.renderer.base.GeoRenderState;
import java.util.function.Consumer;
import net.minecraft.resources.Identifier;

/**
 * What the suit's renderer needs to know about the suit this frame, copied from the entity while Minecraft "extracts"
 * the frame (GeckoLib 5 / Minecraft 1.21.2+ render from a snapshot, the render state, not from the entity itself: by the
 * time the model is drawn the entity may have ticked again). Each value travels in the render state under one of these
 * tickets; PowerSuitRenderer.addRenderData fills them, the renderer and its layers read them.
 */
final class SuitRenderData {
    /** Drawn from inside: the local pilot's own suit in first person (only the legs show). */
    static final DataTicket<Boolean> COCKPIT = DataTicket.create("power_suits_cockpit", Boolean.class);
    /** The pilot's skin texture (a player inside, not in our own first-person view's head), else absent: the frame
     *  stands empty (PilotLayer). */
    static final DataTicket<Identifier> PILOT_SKIN = DataTicket.create("power_suits_pilot_skin", Identifier.class);
    /** The pilot's skin is Alex's slim build: the frame's slim build (narrower chest) and his 3 px arms. */
    static final DataTicket<Boolean> PILOT_SLIM = DataTicket.create("power_suits_pilot_slim", Boolean.class);
    /** 0..1: how far an unpowered suit has slumped (the head bowed, the torso tipped forward). */
    static final DataTicket<Float> SLUMP = DataTicket.create("power_suits_slump", Float.class);
    /** The installed tool's bone id (PowerTool.suitBone), or "" for an empty arm (toggles hand vs socket sleeve). */
    static final DataTicket<String> TOOL_BONE = DataTicket.create("power_suits_tool_bone", String.class);
    static final DataTicket<String> TOOL_BONE_R = DataTicket.create("power_suits_tool_bone_r", String.class);
    /** Extracted standalone render state for each arm's installed tool (ToolLayer / ToolModelRenderer). */
    static final DataTicket<GeoRenderState> TOOL_STATE_L = DataTicket.create("power_suits_tool_state_l", GeoRenderState.class);
    static final DataTicket<GeoRenderState> TOOL_STATE_R = DataTicket.create("power_suits_tool_state_r", GeoRenderState.class);
    static final DataTicket<Float> TOOL_RAISE_R = DataTicket.create("power_suits_tool_raise_r", Float.class);
    static final DataTicket<Float> RECOIL_R = DataTicket.create("power_suits_recoil_r", Float.class);
    /** A helmet is on (seals, visor glow). */
    static final DataTicket<Boolean> HELMET = DataTicket.create("power_suits_helmet", Boolean.class);
    /** AR Glasses are on (helm_glasses bone, left-temple indicator LED glow). */
    static final DataTicket<Boolean> GLASSES = DataTicket.create("power_suits_glasses", Boolean.class);
    /** The worn helmet's style (HelmetStyle ordinal, -1 = standard): which helmet bone is drawn. */
    static final DataTicket<Integer> HELMET_STYLE = DataTicket.create("power_suits_helmet_style", Integer.class);
    /** The armour worn (SuitArmour.wornCode: 3 bits per part, tier ordinal + 1): each part's frame or tier piece (ArmourBones). */
    static final DataTicket<Integer> ARMOUR = DataTicket.create("power_suits_armour", Integer.class);
    /** The installed engine (SuitEngine ordinal, -1 = none): which backpack bone is drawn. */
    static final DataTicket<Integer> ENGINE = DataTicket.create("power_suits_engine", Integer.class);
    /** The plates' paint: a dye id 0..15, or -1 for bare steel (PowerSuitModel picks the texture by it). */
    static final DataTicket<Integer> PAINT = DataTicket.create("power_suits_paint", Integer.class);
    /** Smooths step-ups/downs (PowerSuitEntity.getStepOffset), blocks. */
    static final DataTicket<Float> STEP_OFFSET = DataTicket.create("power_suits_step_offset", Float.class);
    /** Driven and alive: the torso aims and the tool arm can raise (parked suits keep the rest pose). */
    static final DataTicket<Boolean> AIMING = DataTicket.create("power_suits_aiming", Boolean.class);
    /** Fades the aim out while the suit powers down, 0..1. */
    static final DataTicket<Float> AIM_BLEND = DataTicket.create("power_suits_aim_blend", Float.class);
    /** Tool arm raise 0 (hip carry) .. 1 (aiming), and the recoil kick 0..1, both for this frame. */
    static final DataTicket<Float> TOOL_RAISE = DataTicket.create("power_suits_tool_raise", Float.class);
    static final DataTicket<Float> RECOIL = DataTicket.create("power_suits_recoil", Float.class);

    /** Hands the gait's hip height (model pixels) back to the suit when the model is posed, for the cockpit viewmodel's
     *  bob. The only write-back from drawing into the entity (see PowerSuitEntity.setHipHeight); keep it the only one. */
    @SuppressWarnings("unchecked")
    static final DataTicket<Consumer<Float>> HIP_SINK = DataTicket.create("power_suits_hip_sink", (Class<Consumer<Float>>) (Class<?>) Consumer.class);
    /** The lights (SuitGlowLayer): one packed ARGB tint per glowmask, 0 = off. */
    /** The star reactor's light: a tint per glowmask (the steady one, then the segments from the bottom up). */
    static final DataTicket<int[]> STAR = DataTicket.create("power_suits_star", int[].class);
    static final DataTicket<int[]> GLOW = DataTicket.create("power_suits_glow", int[].class);
    /** The robot helmet's visor face (SuitFace.Face ordinal, -1 = none: dark). */
    static final DataTicket<Integer> VISOR_FACE = DataTicket.create("power_suits_visor_face", Integer.class);


    private SuitRenderData() {}
}
