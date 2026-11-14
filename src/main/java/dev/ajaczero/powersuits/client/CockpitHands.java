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
import org.joml.Matrix4f;
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

    // Placement rules (tools/viewmodel-fit.py checks and solves them; the hand pass always uses a 70 degree FOV):
    //  - the tool's cut end (its socket face) stays below the bottom edge of the screen, so it reaches in from the corner
    //    instead of floating;
    //  - the raised tool's axis points at the crosshair 10 blocks out (`viewmodel-fit.py aim`), so its barrels line up
    //    with where the shots go (the first poses pointed 20-40 degrees up and the tracers looked off);
    //  - the corners: the hotbar covers the middle of the bottom edge.
    // Not final: the dev view tuner (autopilot "view" mode) reloads them from run/view/tuning.json.
    // Socket tool at rest (lowered: its axis points just below the crosshair, 16 blocks out) and raised (aiming).
    static Vector3f toolPos = new Vector3f(-0.58F, -0.57F, -0.19F);
    static float toolYaw = -2.1F, toolPitch = 88.4F, toolRoll = 15F, toolScale = 1.0F;
    static Vector3f toolRaisedPos = new Vector3f(-0.55F, -0.54F, -0.19F);
    static float toolRaisedYaw = -3.2F, toolRaisedPitch = 93.1F;
    /** The chaingun's muzzle (barrel tips) in the view model (pixels below the socket; the muzzle bone's pivot). */
    private static final float MUZZLE_PX = -15F;
    private static final float RECOIL_TICKS = 6F;

    private static boolean wasShooting;
    private static double shotAt = -100;

    /** The socket tool, low on the left (the off hand's place). */
    static void renderTool(RenderHandEvent event, PowerSuitEntity suit) {
        PoseStack pose = event.getPoseStack();
        CockpitView view = CockpitView.INSTANCE;
        view.suit = suit;
        pollShot(suit, view);
        pose.pushPose();
        toolTransform(pose, suit, event.getPartialTick(), suit.socketVisuals().raise(event.getPartialTick()));
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
        vanillaArmTransform(pose, event.getSwingProgress(), event.getEquipProgress());
        event.getSubmitNodeCollector().submitModelPart(arm(slim), pose, RenderTypes.entityTranslucent(skin.body().texturePath()),
                event.getPackedLight(), OverlayTexture.NO_OVERLAY, null);
        // (Picked 2026-11-14 over his bare arm, vanilla's.) Vanilla's model axes are y-down and x-mirrored; the frame's
        // (GeckoLib's) aren't: turn 180 about Z.
        pose.scale(-1F, -1F, 1F);
        CockpitView.INSTANCE.suit = suit;
        CockpitView.INSTANCE.slim = slim;
        drawPart(pose, event, CockpitViewRenderer.Part.ARM);
        pose.popPose();
    }

    private static @Nullable ModelPart wideArm, slimArm;

    /** The pilot's right arm, vanilla's part with no pose of its own (vanillaArmTransform places it) and no sleeve (the
     *  skin's outer layer lies in the cage's wall planes, as in third person: PilotLayer). */
    private static ModelPart arm(boolean slim) {
        ModelPart arm = slim ? slimArm : wideArm;
        if (arm == null) {
            PlayerModel model = new PlayerModel(Minecraft.getInstance().getEntityModels()
                    .bakeLayer(slim ? ModelLayers.PLAYER_SLIM : ModelLayers.PLAYER), slim);
            model.rightSleeve.visible = false;
            arm = model.rightArm;
            arm.setPos(0F, 0F, 0F);
            arm.setRotation(0F, 0F, 0F);
            if (slim) {
                slimArm = arm;
            } else {
                wideArm = arm;
            }
        }
        return arm;
    }

    private static void drawPart(PoseStack pose, RenderHandEvent event, CockpitViewRenderer.Part part) {
        CockpitView.INSTANCE.part = part;
        // Like everything since 1.21.9, this only queues the drawing ("submits" it); Minecraft draws the queue later.
        RENDERER.performRenderPass(CockpitView.INSTANCE, null, pose, event.getSubmitNodeCollector(),
                Minecraft.getInstance().gameRenderer.gameRenderState().levelRenderState.cameraRenderState,
                event.getPackedLight(), event.getPartialTick());
    }

    /** Tool: low on the left, raised toward the middle while used, bobbing with the gait, kicking back and up when
     *  it fires. */
    private static void toolTransform(PoseStack pose, PowerSuitEntity suit, float partial, float raise) {
        float kick = Math.max(recoil(partial), suit.socketVisuals().recoil(partial)); // EM push / chaingun shots
        Vector3f p = new Vector3f(toolPos).lerp(toolRaisedPos, raise);
        pose.translate(p.x, p.y + bob(suit), p.z + kick * 0.10F);
        pose.rotateDegrees(Axis.YP, Mth.lerp(raise, toolYaw, toolRaisedYaw));
        pose.rotateDegrees(Axis.XP, Mth.lerp(raise, toolPitch, toolRaisedPitch) + kick * 8F);
        pose.rotateDegrees(Axis.YP, toolRoll);
        pose.scale(toolScale, toolScale, toolScale);
    }

    /** Same as toolTransform, as a matrix (no kick), to find the muzzle. */
    private static Matrix4f toolMatrix(PowerSuitEntity suit, float raise) {
        Vector3f p = new Vector3f(toolPos).lerp(toolRaisedPos, raise);
        return new Matrix4f()
                .translate(p.x, p.y + bob(suit), p.z)
                .rotateY(Mth.lerp(raise, toolYaw, toolRaisedYaw) * Mth.DEG_TO_RAD)
                .rotateX(Mth.lerp(raise, toolPitch, toolRaisedPitch) * Mth.DEG_TO_RAD)
                .rotateY(toolRoll * Mth.DEG_TO_RAD)
                .scale(toolScale);
    }

    /** Gait bob (the suit's hip drop, model pixels) plus a slow breathing drift; both off with vanilla's View Bobbing
     *  option, like vanilla's own hand sway. */
    private static float bob(PowerSuitEntity suit) {
        if (!Minecraft.getInstance().options.bobView().get()) {
            return 0F;
        }
        return suit.animator().getHipBob() * 0.008F + Mth.sin((float) ClientUtil.getCurrentTick() * 0.07F) * 0.004F;
    }

    /** Vanilla's right-arm transform (ItemInHandRenderer.renderPlayerArm + PlayerModel's right arm, to its pivot, in
     *  vanilla's model axes: y runs down the arm). */
    private static void vanillaArmTransform(PoseStack pose, float swing, float equip) {
        float sq = Mth.sqrt(swing);
        pose.translate(-0.3F * Mth.sin(sq * Mth.PI) + 0.64F, 0.4F * Mth.sin(sq * Mth.TWO_PI) - 0.6F - equip * 0.6F,
                -0.4F * Mth.sin(swing * Mth.PI) - 0.72F);
        pose.rotateDegrees(Axis.YP, 45.0F);
        pose.rotateDegrees(Axis.YP, Mth.sin(sq * Mth.PI) * 70.0F);
        pose.rotateDegrees(Axis.ZP, Mth.sin(swing * swing * Mth.PI) * -20.0F);
        pose.translate(-1.0F, 3.6F, 3.5F);
        pose.rotateDegrees(Axis.ZP, 120.0F);
        pose.rotateDegrees(Axis.XP, 200.0F);
        pose.rotateDegrees(Axis.YP, -135.0F);
        pose.translate(5.6F, 0.0F, 0.0F);
        // PlayerModel's right arm (wide): pivot (-5, 2, 0) px, idle sway zRot 0.1 rad (AnimationUtils.bobModelPart, age 0).
        // Its box runs x -3..1, y -2..10 (model Y runs down the arm, toward the fist at y 10).
        pose.translate(-5F / 16F, 2F / 16F, 0F);
        pose.rotate(Axis.ZP, 0.1F);
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
        Vector3f p = toolMatrix(suit, suit.socketVisuals().raise(1F)).transformPosition(new Vector3f(0, (MUZZLE_PX + inset) / 16F, -forward / 16F));
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
            if (j.has("toolPos")) toolPos = v.apply("toolPos");
            if (j.has("toolRaisedPos")) toolRaisedPos = v.apply("toolRaisedPos");
            toolRaisedYaw = f.apply("toolRaisedYaw", toolRaisedYaw); toolRaisedPitch = f.apply("toolRaisedPitch", toolRaisedPitch);
            toolYaw = f.apply("toolYaw", toolYaw); toolPitch = f.apply("toolPitch", toolPitch);
            toolRoll = f.apply("toolRoll", toolRoll); toolScale = f.apply("toolScale", toolScale);
        } catch (Exception e) {
            PowerSuits.LOGGER.warn("[view] can't read {}: {}", file, e.toString());
        }
    }

    private CockpitHands() {}
}
