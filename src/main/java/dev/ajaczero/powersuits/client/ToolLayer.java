package dev.ajaczero.powersuits.client;

import com.geckolib.cache.model.GeoBone;
import com.geckolib.renderer.base.GeoRenderState;
import com.geckolib.renderer.base.GeoRenderer;
import com.geckolib.renderer.base.PerBoneRender;
import com.geckolib.renderer.base.RenderPassInfo;
import com.geckolib.renderer.layer.GeoRenderLayer;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.entity.ToolArm;
import java.util.function.BiConsumer;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import org.jspecify.annotations.Nullable;

/**
 * Draws the installed power tools on the suit's {@code left_socket} and {@code right_socket} bones using
 * {@link ToolModelRenderer}. Each arm renders its own standalone tool model and independent glowmasks.
 */
public class ToolLayer extends GeoRenderLayer<PowerSuitEntity, Void, LivingEntityRenderState> {
    public ToolLayer(GeoRenderer<PowerSuitEntity, Void, LivingEntityRenderState> renderer) {
        super(renderer);
    }

    @Override
    public void addRenderData(PowerSuitEntity suit, @Nullable Void ignored, LivingEntityRenderState state, float partialTick) {
        GeoRenderState left = ToolModelRenderer.INSTANCE.extract(suit, ToolArm.LEFT, partialTick);
        if (left != null) {
            state.addGeckolibData(SuitRenderData.TOOL_STATE_L, left);
        }
        GeoRenderState right = ToolModelRenderer.INSTANCE.extract(suit, ToolArm.RIGHT, partialTick);
        if (right != null) {
            state.addGeckolibData(SuitRenderData.TOOL_STATE_R, right);
        }
    }

    @Override
    public void addPerBoneRender(RenderPassInfo<LivingEntityRenderState> info, BiConsumer<GeoBone, PerBoneRender<LivingEntityRenderState>> consumer) {
        if (!info.willRender() || info.getOrDefaultGeckolibData(SuitRenderData.COCKPIT, false)) {
            return;
        }
        attach(info, consumer, "left_socket", info.getGeckolibData(SuitRenderData.TOOL_STATE_L));
        attach(info, consumer, "right_socket", info.getGeckolibData(SuitRenderData.TOOL_STATE_R));
    }

    private static void attach(RenderPassInfo<LivingEntityRenderState> info, BiConsumer<GeoBone, PerBoneRender<LivingEntityRenderState>> consumer,
                               String boneName, @Nullable GeoRenderState toolState) {
        if (toolState == null) {
            return;
        }
        info.model().getBone(boneName).ifPresent(bone -> consumer.accept(bone, (pass, b, tasks) ->
                ToolModelRenderer.INSTANCE.render(toolState, pass.poseStack(), tasks, pass.cameraState(),
                        pass.packedLight(), pass.packedOverlay(), pass.renderColor())));
    }
}
