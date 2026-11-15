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
    /** What a tool without frame art shows in the socket (see adjustModelBonesForRender). */
    private static final String STAND_IN_TOOL = "drill";
    /** The standard helmet's bone, under armor_head beside the styles' (helm_<style>). */
    private static final String STANDARD_HELMET = "helm_standard";

    public PowerSuitRenderer(EntityRendererProvider.Context context) {
        super(context, new PowerSuitModel());
        this.shadowRadius = 0.6F;
        this.withRenderLayer(new HeldItemLayer(context, this)); // the pilot's selected item in the right hand
        this.withRenderLayer(new PilotLayer(context, this));    // the pilot himself, in his own skin
        this.withRenderLayer(new HelmetGlassLayer(this));       // the visor's glass, over his face
        this.withRenderLayer(new SuitGlowLayer(this));          // the lights: so far the visor
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
        state.addGeckolibData(SuitRenderData.ARMOUR, suit.armour().wornMask());
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
        // Socket (the left arm's end): show the installed tool's bone and hide the others; empty, the socket plate painted
        // on the arm's underside shows. The frame has the drill, chainsaw, chaingun and flamethrower so far; a tool
        // without frame art (the EM projector, rail cannon, TNT launcher) shows the drill's body until it gets its own
        // (user, 2026-11-14: "reuse the drill model or something, whatever is easiest").
        String installed = info.getOrDefaultGeckolibData(SuitRenderData.TOOL_BONE, "");
        String shown = installed.isEmpty() || info.model().getBone(installed).isPresent() ? installed : STAND_IN_TOOL;
        for (String toolBone : ToolBones.all()) {
            boolean hide = !toolBone.equals(shown);
            bones.ifPresent(toolBone, bone -> bone.skipRender(hide).skipChildrenRender(hide));
        }
        // Helmet slot: the frame's helmet (armor_head) only when one is worn; without it the pilot's own head shows
        // (PilotLayer). Inside it one helmet at a time (frame step 7b, design sec. 4c): the worn style's (helm_<style>,
        // HelmetStyle.bone) or the standard one (helm_standard: the box, its glass, the outer layer with the radio and
        // camera), which also stands in for a style without frame art yet.
        boolean helmet = info.getOrDefaultGeckolibData(SuitRenderData.HELMET, true);
        bones.ifPresent("armor_head", bone -> bone.skipRender(!helmet).skipChildrenRender(!helmet));
        HelmetStyle style = HelmetStyle.byId(info.getOrDefaultGeckolibData(SuitRenderData.HELMET_STYLE, -1));
        String helm = style != null && info.model().getBone(style.bone()).isPresent() ? style.bone() : STANDARD_HELMET;
        bones.ifPresent(STANDARD_HELMET, bone -> bone.skipRender(!helm.equals(STANDARD_HELMET)).skipChildrenRender(!helm.equals(STANDARD_HELMET)));
        for (HelmetStyle each : HelmetStyle.values()) {
            boolean hide = !each.bone().equals(helm);
            bones.ifPresent(each.bone(), bone -> bone.skipRender(hide).skipChildrenRender(hide));
        }
        // Engine slot (design sec. 4b): the frame's engine (the heart: core and hoses on the front, the blower on the back)
        // only with one installed; none without (the glowmasks follow: a hidden bone isn't drawn again). Every engine
        // shows the heart for now: the tidal engine and the star reactor light its fire in their own colours
        // (SuitGlowLayer) until they get frame art of their own.
        boolean engine = info.getOrDefaultGeckolibData(SuitRenderData.ENGINE, -1) >= 0;
        bones.ifPresent("engine", bone -> bone.skipRender(!engine).skipChildrenRender(!engine));
        // Armour slots (frame step 6c): each part shows its piece while worn, its bare frame otherwise (ArmourBones);
        // the breastplate also swaps the engine's front for its armoured one.
        ArmourBones.show(bones, info.getOrDefaultGeckolibData(SuitRenderData.ARMOUR, 0));
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
        boolean aiming = info.getOrDefaultGeckolibData(SuitRenderData.AIMING, false);
        float raise = aiming ? info.getOrDefaultGeckolibData(SuitRenderData.TOOL_RAISE, 0F) : 0F;
        walk(state, bones, raise);
        float slump = info.getOrDefaultGeckolibData(SuitRenderData.SLUMP, 0F);
        if (slump > 0F) {
            // Out of power the pilot's weight hangs in the frame: head down, the torso tipped a little forward.
            bones.ifPresent("head", head -> head.setRotX(head.getRotX() - 25F * slump * Mth.DEG_TO_RAD));
            bones.ifPresent("torso", torso -> torso.setRotX(torso.getRotX() - 6F * slump * Mth.DEG_TO_RAD));
        }
        if (!aiming) {
            return; // parked: rest pose
        }
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
        if (raise > 0F) {
            raiseTool(info, bones, raise, headYaw, pitch);
        }
    }

    /**
     * Using the tool raises the tool arm by the suit's toolRaise blend (SocketVisuals: like raising a shield) until the
     * tool points along the view: the arm swings forward 90 degrees less the view's pitch (looking straight down, it hangs;
     * looking up, it points up), then turns with the head (the torso has already turned the rest). The frame's arm is
     * one rigid bone, like a player's, so this is a player's aiming pose (a bow's, one-armed); SocketAim fires from where
     * it puts the muzzle. Each shot kicks the muzzle up a little (recoil; at full spin a shudder).
     */
    private static void raiseTool(RenderPassInfo<LivingEntityRenderState> info, BoneSnapshots bones, float w, float headYaw, float pitch) {
        float kick = info.getOrDefaultGeckolibData(SuitRenderData.RECOIL, 0F) * w;
        bones.ifPresent("left_arm", arm -> {
            arm.setRotX(arm.getRotX() + ((90F - pitch) * w + 4F * kick) * Mth.DEG_TO_RAD);
            arm.setRotY(arm.getRotY() - headYaw * w * Mth.DEG_TO_RAD);
        });
    }

    /**
     * Vanilla's walk (HumanoidModel.setupAnim): arms and legs swing opposite, by the entity's own walk animation (its
     * distance walked and speed, which Minecraft keeps for every mob, ridden ones too). Vanilla's x turns are the other
     * way round (its models are y-down, x-mirrored), hence the minus.
     */
    private static void walk(LivingEntityRenderState state, BoneSnapshots bones, float raise) {
        float pos = state.walkAnimationPos * 0.6662F, speed = state.walkAnimationSpeed;
        if (speed <= 0F) {
            return;
        }
        float swing = Mth.cos(pos) * speed, counter = Mth.cos(pos + Mth.PI) * speed;
        bones.ifPresent("right_arm", arm -> arm.setRotX(arm.getRotX() - counter));
        bones.ifPresent("left_arm", arm -> arm.setRotX(arm.getRotX() - swing * (1F - raise))); // a raised tool stays on aim
        bones.ifPresent("right_leg", leg -> leg.setRotX(leg.getRotX() - 1.4F * swing));
        bones.ifPresent("left_leg", leg -> leg.setRotX(leg.getRotX() - 1.4F * counter));
    }


}
