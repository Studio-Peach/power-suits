package dev.ajaczero.powersuits.client;

import com.geckolib.model.GeoModel;
import com.geckolib.renderer.base.GeoRenderState;
import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import net.minecraft.resources.Identifier;

/**
 * Points GeckoLib at the frame's files (written by tools/export-frame.py from model/power_frame*.bbmodel):
 *   geckolib/models/entity/power_frame.geo.json (or power_frame_slim, for a pilot with Alex's slim arms: its chest is
 *   1 px narrower so the arms hang beside his), textures/entity/power_frame(_slim).png, and
 *   geckolib/animations/entity/power_frame.animation.json (every animation name, all empty: the frame is posed in code,
 *   PowerSuitRenderer.adjustModelBonesForRender).
 * Both builds have the same bones, so animations, layers and code poses work on either.
 */
public class PowerSuitModel extends GeoModel<PowerSuitEntity> {
    private static final Identifier WIDE = id("entity/power_frame"), SLIM = id("entity/power_frame_slim");
    private static final Identifier WIDE_TEXTURE = id("textures/entity/power_frame.png");
    private static final Identifier SLIM_TEXTURE = id("textures/entity/power_frame_slim.png");
    // (Paint, design sec. 4d, comes back with the frame's armour: the painted textures in textures/entity/paint are
    // the big suit's.)

    private static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(PowerSuits.MODID, path);
    }

    private static boolean slim(GeoRenderState state) {
        return state.getOrDefaultGeckolibData(SuitRenderData.PILOT_SLIM, false);
    }

    @Override
    public Identifier getModelResource(GeoRenderState state) {
        return slim(state) ? SLIM : WIDE;
    }

    @Override
    public Identifier getTextureResource(GeoRenderState state) {
        return slim(state) ? SLIM_TEXTURE : WIDE_TEXTURE;
    }

    @Override
    public Identifier getAnimationResource(PowerSuitEntity suit) {
        return WIDE;
    }
}
