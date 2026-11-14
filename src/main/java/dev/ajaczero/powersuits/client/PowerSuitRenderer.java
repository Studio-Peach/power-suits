package dev.ajaczero.powersuits.client;

import com.geckolib.renderer.GeoEntityRenderer;
import com.geckolib.renderer.base.BoneSnapshots;
import com.geckolib.renderer.base.RenderPassInfo;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.item.HelmetStyle;
import dev.ajaczero.powersuits.item.PowerTool;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.AbstractClientPlayer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.player.PlayerModelType;
import net.minecraft.world.entity.player.PlayerSkin;
import org.jspecify.annotations.Nullable;

/**
 * Draws the suit with GeckoLib. Rendering happens in two steps since Minecraft 1.21.2: first the frame is "extracted"
 * (addRenderData copies what we need from the entity into the render state, see SuitRenderData), then the model is
 * posed and drawn from that snapshot alone (adjustModelBonesForRender, the layers).
 */
public class PowerSuitRenderer extends GeoEntityRenderer<PowerSuitEntity, LivingEntityRenderState> {
    /** Each engine's backpack (design sec. 4b), in SuitEngine order: the firebox (with its exhausts), the tidal engine's
     *  tanks, the star reactor's canisters. Only the installed engine's is drawn; none without an engine. */
    private static final String[] ENGINE_BONES = {"backpack_parts", "pack_tidal", "pack_reactor"};

    public PowerSuitRenderer(EntityRendererProvider.Context context) {
        super(context, new PowerSuitModel());
        this.shadowRadius = 0.6F;
        this.withRenderLayer(new HeldItemLayer(context, this)); // the pilot's selected item in the right hand
        this.withRenderLayer(new PilotLayer(context, this));    // the pilot himself, in his own skin
        // (SuitGlowLayer, the engine / visor / tool lights, comes back with the frame's engine and helmet: its glowmasks
        // are the big suit's texture layout and would light random texels of the frame's.)
    }

    // ---- extract: entity -> render state ------------------------------------------------------------------------

    @Override
    public void addRenderData(PowerSuitEntity suit, @Nullable Void ignored, LivingEntityRenderState state, float partialTick) {
        boolean cockpit = isCockpitView(suit);
        state.addGeckolibData(SuitRenderData.COCKPIT, cockpit);
        if (suit.getControllingPassenger() instanceof AbstractClientPlayer pilot) {
            PlayerSkin skin = pilot.getSkin();
            state.addGeckolibData(SuitRenderData.PILOT_SKIN, skin.body().texturePath());
            state.addGeckolibData(SuitRenderData.PILOT_SLIM, skin.model() == PlayerModelType.SLIM);
        }
        state.addGeckolibData(SuitRenderData.SLUMP, suit.isPowered() ? 0F : 1F - suit.animator().getAimBlend());
        state.addGeckolibData(SuitRenderData.TOOL_BONE, suit.getSocketStack().getItem() instanceof PowerTool tool ? tool.suitBone() : "");
        state.addGeckolibData(SuitRenderData.HELMET, suit.hasHelmet());
        state.addGeckolibData(SuitRenderData.HELMET_STYLE, suit.getHelmetStyle() == null ? -1 : suit.getHelmetStyle().ordinal());
        state.addGeckolibData(SuitRenderData.ENGINE, suit.getEngine() == null ? -1 : suit.getEngine().ordinal());
        state.addGeckolibData(SuitRenderData.PAINT, suit.getPaint() == null ? -1 : suit.getPaint().getId());
        state.addGeckolibData(SuitRenderData.STEP_OFFSET, (float) suit.animator().getStepOffset(partialTick));
        state.addGeckolibData(SuitRenderData.AIMING, suit.isDriven() && !suit.isDeadOrDying());
        state.addGeckolibData(SuitRenderData.AIM_BLEND, suit.animator().getAimBlend());
        state.addGeckolibData(SuitRenderData.TOOL_RAISE, suit.socketVisuals().raise(partialTick));
        state.addGeckolibData(SuitRenderData.RECOIL, suit.socketVisuals().recoil(partialTick));
        state.addGeckolibData(SuitRenderData.BARREL_ANGLE, suit.socketVisuals().rotorAngle(partialTick));
        state.addGeckolibData(SuitRenderData.HIP_SINK, suit.animator()::setHipHeight);
    }

    /** Set while the suit's menu draws its preview (PowerSuitScreen): the whole suit, even the one you sit in. */
    static boolean inventoryPreview;

    /** True when we're drawing the suit the local player sits in, from inside (first person). */
    static boolean isCockpitView(PowerSuitEntity suit) {
        if (inventoryPreview) {
            return false;
        }
        Minecraft mc = Minecraft.getInstance();
        // The camera must also be the pilot: a scripted camera (another entity, e.g. the autopilot's close-ups) sees
        // the whole suit even while the view is set to first person.
        return suit.isPilotedBy(mc.player) && mc.options.getCameraType().isFirstPerson() && mc.getCameraEntity() == mc.player;
    }

    // ---- render: render state -> model ---------------------------------------------------------------------------

    @Override
    public void adjustRenderPose(RenderPassInfo<LivingEntityRenderState> info) {
        info.poseStack().translate(0, info.getOrDefaultGeckolibData(SuitRenderData.STEP_OFFSET, 0F), 0); // glide over steps
        super.adjustRenderPose(info);
    }

    /**
     * Runs every frame after the keyframe animations have posed the bones. GeckoLib 5 hands us a fresh snapshot per bone
     * each frame holding the animation's offset from the bone's rest pose, so we add to it (nothing piles up: the next
     * frame starts from the animation again).
     */
    @Override
    public void adjustModelBonesForRender(RenderPassInfo<LivingEntityRenderState> info, BoneSnapshots bones) {
        // In first person the camera sits in the pilot's head and, like vanilla, he sees nothing of his own body: the
        // arms are the cockpit viewmodel (CockpitHands), which lines up with the view. (Drafts 2026-11-14, user picked
        // nothing: the legs alone floated a block under the view as two loose squares, and the chest's top, 4 px under
        // his eyes, filled the view like a table top.)
        boolean cockpit = info.getOrDefaultGeckolibData(SuitRenderData.COCKPIT, false);
        bones.ifPresent("marine", root -> root.skipRender(cockpit).skipChildrenRender(cockpit));
        // Socket: show the installed tool's bone and hide the others; the bare coupling only when empty.
        String installed = info.getOrDefaultGeckolibData(SuitRenderData.TOOL_BONE, "");
        for (String toolBone : ToolBones.all()) {
            boolean hide = !toolBone.equals(installed);
            bones.ifPresent(toolBone, bone -> bone.skipRender(hide).skipChildrenRender(hide));
        }
        boolean socketHidden = !installed.isEmpty();
        bones.ifPresent("socket", bone -> bone.skipRender(socketHidden));
        // Helmet slot: no helmet, no helmet bone (the pilot's own head shows: PilotLayer). Each helmet style (design sec. 4c) is a whole helmet of its own under the head bone: draw only the worn one.
        boolean helmet = info.getOrDefaultGeckolibData(SuitRenderData.HELMET, true);
        int style = info.getOrDefaultGeckolibData(SuitRenderData.HELMET_STYLE, -1);
        boolean standard = helmet && style < 0;
        bones.ifPresent("helmet", bone -> bone.skipRender(!standard).skipChildrenRender(!standard));
        for (HelmetStyle each : HelmetStyle.values()) {
            boolean show = helmet && style == each.ordinal();
            bones.ifPresent(each.bone(), bone -> bone.skipRender(!show).skipChildrenRender(!show));
        }
        // Engine slot: the installed engine's backpack only (the glowmasks follow: a hidden bone isn't drawn again).
        int engine = info.getOrDefaultGeckolibData(SuitRenderData.ENGINE, 0);
        for (int i = 0; i < ENGINE_BONES.length; i++) {
            boolean hide = i != engine;
            bones.ifPresent(ENGINE_BONES[i], bone -> bone.skipRender(hide).skipChildrenRender(hide));
        }
        ToolRotors.pose(bones, info.getOrDefaultGeckolibData(SuitRenderData.BARREL_ANGLE, 0F)); // turn (and coast) always
        float[] shake = info.getGeckolibData(SuitRenderData.RAIL_SHAKE);
        if (shake != null) {
            ToolRotors.railShake(bones, shake[0], shake[1]);
        }
        aim(info, bones);
    }

    // ---- the frame's pose (code, not keyframes: the frame's limbs are rigid like a player's) -------------------------

    /** The helmet's turn limit off the torso (design: the head yaws +-50); the torso twists the rest, up to 40 more. */
    private static final float HEAD_YAW = 50F, TORSO_YAW = 40F;

    /**
     * Poses the frame like vanilla poses a player: the limbs swing with the walk, the head follows the pilot's view
     * (or the machine mind's), and a suit without power slumps. Bone rotations here have Blockbench's signs on all three
     * axes (the Bedrock export negates X and Y, GeckoLib negates them back; the GeckoLib 4 rule of subtracting them
     * survived the port once and twisted the old torso away from the view): +X swings a hanging limb forward and tips the torso or head back, +Y turns the front to the suit's left.
     */
    private void aim(RenderPassInfo<LivingEntityRenderState> info, BoneSnapshots bones) {
        LivingEntityRenderState state = info.renderState();
        walk(state, bones);
        float slump = info.getOrDefaultGeckolibData(SuitRenderData.SLUMP, 0F);
        if (slump > 0F) {
            // Out of power the pilot's weight hangs in the frame: head down, the torso tipped a little forward.
            bones.ifPresent("head", head -> head.setRotX(head.getRotX() - 25F * slump * Mth.DEG_TO_RAD));
            bones.ifPresent("torso", torso -> torso.setRotX(torso.getRotX() - 6F * slump * Mth.DEG_TO_RAD));
        }
        if (!info.getOrDefaultGeckolibData(SuitRenderData.AIMING, false)) {
            return; // parked: rest pose
        }
        // (The tool arm's raise comes back with the frame's tools: the big suit's raised an elbow the frame hasn't.)
        // aimBlend fades the aiming out when the suit powers down and back in after it boots up.
        float aim = info.getOrDefaultGeckolibData(SuitRenderData.AIM_BLEND, 1F);
        // Look yaw relative to the legs (Minecraft already wraps it to -180..180; unwrapped, a pilot who had turned round
        // twice twisted the torso the wrong way). The head turns first; past its limit the torso turns with it.
        float yaw = Mth.clamp(Mth.wrapDegrees(state.yRot), -HEAD_YAW - TORSO_YAW, HEAD_YAW + TORSO_YAW) * aim; // + = right
        float headYaw = Mth.clamp(yaw, -HEAD_YAW, HEAD_YAW);
        float pitch = state.xRot * aim; // + = looking down
        bones.ifPresent("torso", torso -> torso.setRotY(torso.getRotY() - (yaw - headYaw) * Mth.DEG_TO_RAD));
        bones.ifPresent("head", head -> {
            head.setRotY(head.getRotY() - headYaw * Mth.DEG_TO_RAD);
            head.setRotX(head.getRotX() - pitch * Mth.DEG_TO_RAD); // the whole look, like a player's head
        });
    }

    /**
     * Vanilla's walk (HumanoidModel.setupAnim): arms and legs swing opposite, by the entity's own walk animation (its
     * distance walked and speed, which Minecraft keeps for every mob, ridden ones too). Vanilla's x turns are the other
     * way round (its models are y-down, x-mirrored), hence the minus.
     */
    private static void walk(LivingEntityRenderState state, BoneSnapshots bones) {
        float pos = state.walkAnimationPos * 0.6662F, speed = state.walkAnimationSpeed;
        if (speed <= 0F) {
            return;
        }
        float swing = Mth.cos(pos) * speed, counter = Mth.cos(pos + Mth.PI) * speed;
        bones.ifPresent("right_arm", arm -> arm.setRotX(arm.getRotX() - counter));
        bones.ifPresent("left_arm", arm -> arm.setRotX(arm.getRotX() - swing));
        bones.ifPresent("right_leg", leg -> leg.setRotX(leg.getRotX() - 1.4F * swing));
        bones.ifPresent("left_leg", leg -> leg.setRotX(leg.getRotX() - 1.4F * counter));
    }


}
