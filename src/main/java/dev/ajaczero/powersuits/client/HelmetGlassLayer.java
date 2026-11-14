package dev.ajaczero.powersuits.client;

import com.geckolib.renderer.base.GeoRenderer;
import com.geckolib.renderer.base.RenderPassInfo;
import com.geckolib.renderer.layer.GeoRenderLayer;
import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.resources.Identifier;

/**
 * The helmet's visor glass: its partly see-through texels (the frame's design: 80 % smoked glass with a faint glint),
 * so the pilot's face shows behind it. The frame itself is drawn in a cutout pass, where a texel is either opaque or not
 * drawn at all, so tools/export-frame.py moves the glass into a texture of its own (power_frame_glass) and this layer
 * draws the model once more with it, translucent. Ordered after the main pass and the pilot (renderTasks.order(1)):
 * translucent glass drawn first would hide his face behind it. The visor's light goes on top (SuitGlowLayer).
 */
public class HelmetGlassLayer extends GeoRenderLayer<PowerSuitEntity, Void, LivingEntityRenderState> {
    private static final Identifier WIDE = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "textures/entity/power_frame_glass.png");
    private static final Identifier SLIM = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "textures/entity/power_frame_glass_slim.png");

    public HelmetGlassLayer(GeoRenderer<PowerSuitEntity, Void, LivingEntityRenderState> renderer) {
        super(renderer);
    }

    @Override
    public void submitRenderTask(RenderPassInfo<LivingEntityRenderState> info, SubmitNodeCollector renderTasks) {
        if (!info.willRender() || !info.getOrDefaultGeckolibData(SuitRenderData.HELMET, false)
                || info.getOrDefaultGeckolibData(SuitRenderData.COCKPIT, false)) {
            return;
        }
        boolean slim = info.getOrDefaultGeckolibData(SuitRenderData.PILOT_SLIM, false);
        this.renderer.submitRenderTasks(info, renderTasks.order(1), RenderTypes.entityTranslucent(slim ? SLIM : WIDE));
    }
}
