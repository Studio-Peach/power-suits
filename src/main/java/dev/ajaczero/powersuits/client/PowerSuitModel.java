package dev.ajaczero.powersuits.client;

import com.geckolib.model.GeoModel;
import com.geckolib.renderer.base.GeoRenderState;
import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.DyeColor;

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
    /** A painted frame's texture per build and dye (by DyeColor id): the frame's texture with the painted texels in the
     *  dye's colours, built by tools/make-frame-paint.py (design sec. 4d, frame step 7: the armour pieces and the helmet's
     *  shell, user 2026-11-14; the bare frame stays steel). Only a texture swap: same model, same glowmasks. */
    private static final Identifier[] PAINTED = new Identifier[DyeColor.values().length];
    private static final Identifier[] PAINTED_SLIM = new Identifier[DyeColor.values().length];

    static {
        for (DyeColor dye : DyeColor.values()) {
            PAINTED[dye.getId()] = id("textures/entity/paint/power_frame_" + dye.getName() + ".png");
            PAINTED_SLIM[dye.getId()] = id("textures/entity/paint/power_frame_slim_" + dye.getName() + ".png");
        }
    }

    /** The frame's texture for a build and a paint (a dye id, -1 for bare steel): the suit's and the cockpit's arm. */
    static Identifier texture(boolean slim, int paint) {
        if (paint >= 0 && paint < PAINTED.length) {
            return slim ? PAINTED_SLIM[paint] : PAINTED[paint];
        }
        return slim ? SLIM_TEXTURE : WIDE_TEXTURE;
    }

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
        return texture(slim(state), state.getOrDefaultGeckolibData(SuitRenderData.PAINT, -1));
    }

    @Override
    public Identifier getAnimationResource(PowerSuitEntity suit) {
        return WIDE;
    }
}
