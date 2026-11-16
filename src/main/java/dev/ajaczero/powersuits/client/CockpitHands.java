package dev.ajaczero.powersuits.client;

import com.geckolib.animation.AnimationController;
import com.geckolib.util.ClientUtil;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.item.PowerTool;
import dev.ajaczero.powersuits.item.SocketAim;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.function.BiFunction;
import java.util.function.Function;
import net.minecraft.client.Camera;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.player.PlayerModel;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.PlayerModelType;
import net.minecraft.world.entity.player.PlayerSkin;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.client.event.RenderHandEvent;
import org.joml.Matrix3f;
import org.joml.Matrix4f;
import org.joml.Quaternionf;
import org.joml.Vector3f;
import org.joml.Vector3fc;
import org.jspecify.annotations.Nullable;

/**
 * What the pilot sees of the suit's arms, drawn in the hand pass like vanilla's first-person hands. The suit's own
 * upper body is hidden in the cockpit (only the legs are drawn), because looking at its arms from inside never lined
 * up with the view: the arm raised a hand where your hand isn't, the tool hid behind its own base, pads clipped.
 * Instead: the socket tool low on the left (CockpitView, animated like the suit's tool), and on the right your main
 * hand exactly as vanilla draws it: a held item is vanilla's own first-person item (same place, swing, eat / bow /
 * shield / crossbow motions; no arm, as in vanilla), and an empty hand is your own arm in the frame's arm (renderArm;
 * the big suit's gauntlet until 2026-11-14). PilotView decides which.
 *
 * <p>Positions are in view space (blocks; x right, y up, -z forward), like vanilla's hand transforms.
 */
public final class CockpitHands {
    private static final CockpitViewRenderer RENDERER = new CockpitViewRenderer();

    // The tool arm (2026-11-14, the frame): his left arm in the frame's left arm, the socket tool at its end, drawn where
    // vanilla draws a left hand (vanillaArmTransform mirrored), like the right arm. Raised to aim, the arm turns about its
    // shoulder until the tool's axis points at the crosshair TOOL_AIM_DISTANCE out (the shots go there; a tool pointing
    // elsewhere looked off, the big suit's first poses taught), the hotbar left clear. At rest the arm keeps vanilla's
    // pose, turned toward REST_AIM (a point low and left of the crosshair) by REST_TURN of the way.
    // Not final: the dev view tuner (autopilot "view" mode) reloads them from run/view/tuning.json.
    static float toolAimDistance = 10F;
    static Vector3f restAim = new Vector3f(-1.5F, -3.5F, -10F);
    static float restTurn = 0.45F;
    /** Both arms are drawn at this scale about their shoulder pivot (user, 2026-11-15: in first person they were too big and
     *  too extended: the frame's arm shell is 5 px wide and 16 long round the skin's 4 x 12 arm, vanilla's hand places
     *  it close to the camera). Scaling about the pivot shortens the reach as it shrinks the arm. */
    static float armScale = 0.75F;
    /** The tool arm's own scale (it turns toward the aim, so the same scale hides more of it than the plain right arm). */
    static float toolArmScale = 0.85F;
    /** The chaingun's muzzle about the pilot's left arm pivot, in vanilla's arm space (y down the arm, x mirrored; px):
     *  the socket is 10 px down the arm and 1.25 px off its pivot's axis (tools/export-frame.py), the muzzle block's
     *  bottom 8.5 px under the socket. */
    private static final Vector3f MUZZLE_PX = new Vector3f(1.25F, 18.5F, 0F);
    private static final float RECOIL_TICKS = 6F;

    private static boolean wasShooting;
    private static double shotAt = -100;

    /** The socket tool, low on the left (the off hand's place). */
    static void renderTool(RenderHandEvent event, PowerSuitEntity suit) {
        PoseStack pose = event.getPoseStack();
        CockpitView view = CockpitView.INSTANCE;
        view.suit = suit;
        view.slim = Minecraft.getInstance().player != null && Minecraft.getInstance().player.getSkin().model() == PlayerModelType.SLIM;
        pollShot(suit, view);
        float partial = event.getPartialTick();
        float kick = Math.max(recoil(partial), suit.socketVisuals().recoil(partial)); // EM push / chaingun shots
        pose.pushPose();
        toolArmTransform(pose, suit, suit.socketVisuals().raise(partial), kick);
        PlayerSkin skin = Minecraft.getInstance().player != null ? Minecraft.getInstance().player.getSkin() : null;
        if (skin != null) {
            event.getSubmitNodeCollector().submitModelPart(arm(view.slim, true), pose, RenderTypes.entityTranslucent(skin.body().texturePath()),
                    event.getPackedLight(), OverlayTexture.NO_OVERLAY, null);
        }
        pose.scale(-1F, -1F, 1F); // into the frame's axes (see renderArm)
        drawPart(pose, event, CockpitViewRenderer.Part.TOOL);
        pose.popPose();
    }

    /** The frame's right arm: the pilot's own skin arm exactly where vanilla draws an empty right hand (its swing and
     *  equip motion too), with the frame's arm shell round it (tools/export-frame.py: the same cubes about the same
     *  pivot as on the frame), so the cage and the fist under his hand move with it. */
    static void renderArm(RenderHandEvent event, PowerSuitEntity suit) {
        Minecraft mc = Minecraft.getInstance();
        if (mc.player == null) {
            return;
        }
        PlayerSkin skin = mc.player.getSkin();
        boolean slim = skin.model() == PlayerModelType.SLIM;
        PoseStack pose = event.getPoseStack();
        pose.pushPose();
        vanillaArmTransform(pose, event.getSwingProgress(), event.getEquipProgress(), 1F);
        pose.scale(armScale, armScale, armScale);
        event.getSubmitNodeCollector().submitModelPart(arm(slim, false), pose, RenderTypes.entityTranslucent(skin.body().texturePath()),
                event.getPackedLight(), OverlayTexture.NO_OVERLAY, null);
        // (Picked 2026-11-14 over his bare arm, vanilla's.) Vanilla's model axes are y-down and x-mirrored; the frame's
        // (GeckoLib's) aren't: turn 180 about Z.
        pose.scale(-1F, -1F, 1F);
        CockpitView.INSTANCE.suit = suit;
        CockpitView.INSTANCE.slim = slim;
        drawPart(pose, event, CockpitViewRenderer.Part.ARM);
        pose.popPose();
    }

    /** Our own player models, wide and slim (their arms' poses are set once). */
    private static final PlayerModel[] MODELS = new PlayerModel[2];

    /** The pilot's right or left arm, vanilla's part with no pose of its own (vanillaArmTransform places it) and no
     *  sleeve (the skin's outer layer lies in the cage's wall planes, as in third person: PilotLayer). */
    private static ModelPart arm(boolean slim, boolean left) {
        int i = slim ? 1 : 0;
        if (MODELS[i] == null) {
            PlayerModel model = new PlayerModel(Minecraft.getInstance().getEntityModels()
                    .bakeLayer(slim ? ModelLayers.PLAYER_SLIM : ModelLayers.PLAYER), slim);
            model.rightSleeve.visible = model.leftSleeve.visible = false;
            for (ModelPart arm : new ModelPart[] {model.rightArm, model.leftArm}) {
                arm.setPos(0F, 0F, 0F);
                arm.setRotation(0F, 0F, 0F);
            }
            MODELS[i] = model;
        }
        return left ? MODELS[i].leftArm : MODELS[i].rightArm;
    }

    private static void drawPart(PoseStack pose, RenderHandEvent event, CockpitViewRenderer.Part part) {
        CockpitView.INSTANCE.part = part;
        // Like everything since 1.21.9, this only queues the drawing ("submits" it); Minecraft draws the queue later.
        RENDERER.performRenderPass(CockpitView.INSTANCE, null, pose, event.getSubmitNodeCollector(),
                Minecraft.getInstance().gameRenderer.gameRenderState().levelRenderState.cameraRenderState,
                event.getPackedLight(), event.getPartialTick());
    }

    /**
     * The tool arm: vanilla's left-hand pose (no swing: the off hand), then turned about the shoulder toward the aim: at
     * rest REST_TURN of the way to REST_AIM, raised (the suit's toolRaise blend) until the tool points at the crosshair,
     * a kick lifting it with each shot. The turn is worked out in view space (where the arm's pivot is and where its
     * axis points now) and put in front of the arm's transform.
     */
    private static void toolArmTransform(PoseStack pose, PowerSuitEntity suit, float raise, float kick) {
        // The hand pass's pose stack doesn't start at identity (26.3: it holds a half turn about y), so the turn is
        // worked out in the hand space under it: the space vanilla's arm numbers are in (x right, y up, -z forward).
        Matrix4f base = new Matrix4f(pose.last().pose());
        Matrix3f baseNormal = new Matrix3f(pose.last().normal());
        pose.translate(0F, bob(suit), 0F);
        vanillaArmTransform(pose, 0F, 0F, -1F);
        Matrix4f local = new Matrix4f(base).invert().mul(pose.last().pose());
        Vector3f pivot = local.transformPosition(new Vector3f());
        Vector3f axis = local.transformDirection(new Vector3f(0F, 1F, 0F)).normalize(); // down vanilla's arm, to the tool
        Quaternionf rest = new Quaternionf().slerp(new Quaternionf().rotationTo(axis, new Vector3f(restAim).sub(pivot).normalize()), restTurn);
        Vector3f target = new Vector3f(0F, kick * 0.8F, -toolAimDistance);
        Quaternionf aimed = new Quaternionf().rotationTo(axis, target.sub(pivot).normalize());
        Quaternionf turn = rest.slerp(aimed, raise);
        pose.last().pose().set(new Matrix4f(base).translate(pivot).rotate(turn).translate(-pivot.x, -pivot.y, -pivot.z).mul(local)
                .scale(toolArmScale));
        Matrix3f localNormal = new Matrix3f(baseNormal).invert().mul(pose.last().normal());
        pose.last().normal().set(new Matrix3f(baseNormal).rotate(turn).mul(localNormal));
    }

    /** Gait bob (the suit's hip drop, model pixels) plus a slow breathing drift; both off with vanilla's View Bobbing
     *  option, like vanilla's own hand sway. */
    private static float bob(PowerSuitEntity suit) {
        if (!Minecraft.getInstance().options.bobView().get()) {
            return 0F;
        }
        return suit.animator().getHipBob() * 0.008F + Mth.sin((float) ClientUtil.getCurrentTick() * 0.07F) * 0.004F;
    }

    /** Vanilla's arm transform (ItemInHandRenderer.renderPlayerArm + PlayerModel's arm, to its pivot, in vanilla's
     *  model axes: y runs down the arm); side 1 the right arm, -1 the left (vanilla mirrors it the same way). */
    private static void vanillaArmTransform(PoseStack pose, float swing, float equip, float side) {
        float sq = Mth.sqrt(swing);
        pose.translate(side * (-0.3F * Mth.sin(sq * Mth.PI) + 0.64F), 0.4F * Mth.sin(sq * Mth.TWO_PI) - 0.6F - equip * 0.6F,
                -0.4F * Mth.sin(swing * Mth.PI) - 0.72F);
        pose.rotateDegrees(Axis.YP, side * 45.0F);
        pose.rotateDegrees(Axis.YP, side * Mth.sin(sq * Mth.PI) * 70.0F);
        pose.rotateDegrees(Axis.ZP, side * Mth.sin(swing * swing * Mth.PI) * -20.0F);
        pose.translate(side * -1.0F, 3.6F, 3.5F);
        pose.rotateDegrees(Axis.ZP, side * 120.0F);
        pose.rotateDegrees(Axis.XP, 200.0F);
        pose.rotateDegrees(Axis.YP, side * -135.0F);
        pose.translate(side * 5.6F, 0.0F, 0.0F);
        // PlayerModel's arm (wide): pivot (-5, 2, 0) px for the right, (5, 2, 0) the left, idle sway zRot +-0.1 rad
        // (AvatarRenderer.renderHand). Its box runs y -2..10 (model Y runs down the arm, toward the fist at y 10).
        pose.translate(side * -5F / 16F, 2F / 16F, 0F);
        pose.rotate(Axis.ZP, side * 0.1F);
    }

    /** The suit plays tool_recoil when the EM projector pushes; start the kick here too. (Chaingun shots kick through
     *  the suit's synced shot counter, SocketVisuals.recoil.) */
    private static void pollShot(PowerSuitEntity suit, CockpitView view) {
        AnimationController<?> action = suit.getAnimatableInstanceCache().getManagerForId(suit.getId()).getAnimationControllers().get("action");
        var triggered = action == null ? null : action.getCurrentRawAnimation();
        boolean shooting = action != null && action.isPlayingTriggeredAnimation() && triggered != null
                && triggered.getAnimationStages().get(0).animationName().endsWith("tool_recoil");
        if (shooting && !wasShooting) {
            shotAt = ClientUtil.getCurrentTick();
        }
        wasShooting = shooting;
    }

    /** 1 right after a shot, easing back to 0. */
    private static float recoil(float partial) {
        double age = ClientUtil.getCurrentTick() - shotAt;
        if (age < 0 || age > RECOIL_TICKS) {
            return 0F;
        }
        float t = (float) (age / RECOIL_TICKS);
        return t < 0.15F ? t / 0.15F : (1 - t) / 0.85F * (1 - t);
    }

    /**
     * Where the tool's muzzle appears in the world for the local pilot in first person: bolts and the EM beam start
     * there on their screen. The hand pass uses a fixed 70 degree FOV, so the view-space point is rescaled to the
     * world FOV to land on the same spot of the screen.
     */
    static Vec3 visualMuzzle(PowerSuitEntity suit, LivingEntity operator) {
        Minecraft mc = Minecraft.getInstance();
        if (operator != mc.player || !PowerSuitRenderer.isCockpitView(suit)) {
            return SocketAim.muzzlePosition(suit, operator); // also when a scripted camera watches the suit from outside
        }
        PowerTool tool = suit.getSocketStack().getItem() instanceof PowerTool t ? t : null;
        float inset = tool != null ? tool.muzzleInsetPixels() : 0F;
        float forward = tool != null ? tool.barrelForwardPixels() : 0F; // the model's front is -z
        PoseStack arm = new PoseStack();
        toolArmTransform(arm, suit, suit.socketVisuals().raise(1F), 0F);
        Vector3f p = arm.last().pose().transformPosition(new Vector3f(MUZZLE_PX.x, MUZZLE_PX.y - inset, -forward).div(16F));
        double k = Math.tan(Math.toRadians(mc.options.fov().get()) / 2) / Math.tan(Math.toRadians(70) / 2);
        Camera camera = mc.gameRenderer.mainCamera();
        Vector3fc look = camera.forwardVector(), up = camera.upVector(), left = camera.leftVector();
        double x = p.x * k, y = p.y * k, z = p.z;
        return camera.position()
                .add(-left.x() * x, -left.y() * x, -left.z() * x)
                .add(up.x() * y, up.y() * y, up.z() * y)
                .add(-look.x() * z, -look.y() * z, -look.z() * z);
    }

    /** Dev: reload the placement from a JSON file (keys as the fields above; positions as [x, y, z]). */
    public static void loadTuning(Path file) {
        try (var reader = Files.newBufferedReader(file)) {
            JsonObject j = JsonParser.parseReader(reader).getAsJsonObject();
            BiFunction<String, Float, Float> f = (k, d) -> j.has(k) ? j.get(k).getAsFloat() : d;
            Function<String, Vector3f> v = k -> {
                var a = j.getAsJsonArray(k);
                return new Vector3f(a.get(0).getAsFloat(), a.get(1).getAsFloat(), a.get(2).getAsFloat());
            };
            toolAimDistance = f.apply("toolAimDistance", toolAimDistance);
            if (j.has("restAim")) restAim = v.apply("restAim");
            restTurn = f.apply("restTurn", restTurn);
            armScale = f.apply("armScale", armScale);
            toolArmScale = f.apply("toolArmScale", toolArmScale);
        } catch (Exception e) {
            PowerSuits.LOGGER.warn("[view] can't read {}: {}", file, e.toString());
        }
    }

    private CockpitHands() {}
}
