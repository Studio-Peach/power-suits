package dev.ajaczero.powersuits.client;

import com.geckolib.cache.model.GeoBone;
import com.geckolib.renderer.base.GeoRenderer;
import com.geckolib.renderer.base.PerBoneRender;
import com.geckolib.renderer.base.RenderPassInfo;
import com.geckolib.renderer.layer.GeoRenderLayer;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import java.util.Map;
import java.util.function.BiConsumer;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.player.PlayerModel;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.Identifier;

/**
 * The pilot inside the frame: the player's own skin, drawn with vanilla's player model parts (Steve's wide arms or
 * Alex's slim ones, as the skin asks) at the frame's pilot_* bones. Each pilot bone rides its frame bone (pilot_right_arm
 * under right_arm...), so his limbs swing with the frame's and stay inside their cages. tools/export-frame.py puts each
 * pilot bone where vanilla's part has its pivot, so a part drawn there with no offset of its own covers the cube the
 * design file has for it (st_*).
 *
 * Only the skin's base layer: the outer layer (jacket, sleeves, trousers) sits 0.25 px out, in the planes of the
 * frame's cage walls, and would flicker through them. The hat layer stays (the frame has no head cage).
 * In the pilot's own first-person view only his legs (you see them looking down, like the frame's); never anyone else
 * in a suit (mobs ride without a skin: the frame stands empty).
 */
public class PilotLayer extends GeoRenderLayer<PowerSuitEntity, Void, LivingEntityRenderState> {
    /** Per build, the frame bone -> the vanilla part drawn there. Our own model instances: their poses are set once. */
    private final Map<String, ModelPart> wide, slim;

    public PilotLayer(EntityRendererProvider.Context context, GeoRenderer<PowerSuitEntity, Void, LivingEntityRenderState> renderer) {
        super(renderer);
        this.wide = parts(new PlayerModel(context.bakeLayer(ModelLayers.PLAYER), false));
        this.slim = parts(new PlayerModel(context.bakeLayer(ModelLayers.PLAYER_SLIM), true));
    }

    private static Map<String, ModelPart> parts(PlayerModel model) {
        model.jacket.visible = model.leftSleeve.visible = model.rightSleeve.visible = false;
        model.leftPants.visible = model.rightPants.visible = false;
        Map<String, ModelPart> parts = Map.of("pilot_head", model.head, "pilot_torso", model.body,
                "pilot_right_arm", model.rightArm, "pilot_left_arm", model.leftArm,
                "pilot_right_leg", model.rightLeg, "pilot_left_leg", model.leftLeg);
        // No offset or turn of their own: the bone is the pivot, the frame's bones do the posing. (Set once, since the
        // parts are drawn later than they are submitted: a per-suit change here would reach every suit this frame.)
        parts.values().forEach(part -> {
            part.setPos(0F, 0F, 0F);
            part.setRotation(0F, 0F, 0F);
        });
        return parts;
    }

    /** Draws from the render state only: PowerSuitRenderer.addRenderData puts the skin and the build in it. */
    @Override
    public void addPerBoneRender(RenderPassInfo<LivingEntityRenderState> info, BiConsumer<GeoBone, PerBoneRender<LivingEntityRenderState>> consumer) {
        Identifier skin = info.renderState().getGeckolibData(SuitRenderData.PILOT_SKIN);
        if (skin == null || !info.willRender()) {
            return;
        }
        boolean cockpit = info.getOrDefaultGeckolibData(SuitRenderData.COCKPIT, false);
        Map<String, ModelPart> parts = info.getOrDefaultGeckolibData(SuitRenderData.PILOT_SLIM, false) ? this.slim : this.wide;
        parts.forEach((boneName, part) -> {
            if (cockpit && (CockpitDrafts.down == 0 || boneName.equals("pilot_head") || boneName.endsWith("_arm")
                    || (CockpitDrafts.down == 1 && boneName.equals("pilot_torso")))) {
                return; // the camera is in his head; his arms are the cockpit viewmodel's
            }
            info.model().getBone(boneName).ifPresent(bone -> consumer.accept(bone, (pass, b, tasks) -> {
                var poseStack = pass.poseStack(); // at the bone's pivot, in the frame's model space
                // Vanilla models are built y-down and drawn through scale(-1, -1, 1) (LivingEntityRenderer does the same).
                poseStack.scale(-1F, -1F, 1F);
                tasks.submitModelPart(part, poseStack, RenderTypes.entityTranslucent(skin), pass.packedLight(),
                        OverlayTexture.NO_OVERLAY, null, -1, pass.renderState().outlineColor);
            }));
        });
    }
}
