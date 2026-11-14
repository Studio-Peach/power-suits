package dev.ajaczero.powersuits.client;

import com.geckolib.constant.dataticket.DataTicket;
import com.geckolib.model.GeoModel;
import com.geckolib.renderer.GeoObjectRenderer;
import com.geckolib.renderer.base.BoneSnapshots;
import com.geckolib.renderer.base.GeoRenderState;
import com.geckolib.renderer.base.RenderPassInfo;
import com.geckolib.renderer.layer.GeoRenderLayer;
import com.geckolib.util.ClientUtil;
import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.item.PowerTool;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.rendertype.RenderType;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.resources.Identifier;
import org.jspecify.annotations.Nullable;

/** Draws one part of the cockpit viewmodel (CockpitView): the socket tool, or the frame's right arm round the pilot's
 *  own (CockpitHands). */
final class CockpitViewRenderer extends GeoObjectRenderer<CockpitView, Void, GeoRenderState> {
    enum Part { TOOL, ARM }


    // Copied from CockpitView / its suit when the frame is extracted (the model is posed and drawn later).
    private static final DataTicket<Part> PART = DataTicket.create("power_suits_view_part", Part.class);
    /** The pilot's skin is Alex's: the frame's slim arm (the same cubes about his arm, the slim build's texture). */
    private static final DataTicket<Boolean> SLIM = DataTicket.create("power_suits_view_slim", Boolean.class);
    private static final DataTicket<String> TOOL_BONE = DataTicket.create("power_suits_view_tool_bone", String.class);
    private static final DataTicket<Float> BARREL_ANGLE = DataTicket.create("power_suits_view_barrel_angle", Float.class);
    /** The rail cannon's charge and the time (ticks), for its shake. */
    private static final DataTicket<float[]> RAIL_SHAKE = DataTicket.create("power_suits_view_rail_shake", float[].class);
    private static final DataTicket<int[]> GLOW = DataTicket.create("power_suits_view_glow", int[].class);
    /** The tool's lights, like on the suit (SuitGlowLayer: one mask per ToolLight). */
    private static final Identifier[] MASKS = SuitGlowLayer.TOOL_MASKS;

    CockpitViewRenderer() {
        super(new Model());
        this.withRenderLayer(new ToolGlow(this));
    }

    @Override
    public void addRenderData(CockpitView view, @Nullable Void ignored, GeoRenderState state, float partialTick) {
        state.addGeckolibData(PART, view.part);
        state.addGeckolibData(SLIM, view.slim);
        var suit = view.suit;
        state.addGeckolibData(TOOL_BONE, suit != null && suit.getSocketStack().getItem() instanceof PowerTool tool ? tool.suitBone() : "");
        state.addGeckolibData(BARREL_ANGLE, suit == null ? 0F : suit.socketVisuals().rotorAngle(partialTick));
        if (suit != null && view.part == Part.TOOL) {
            float time = (float) ClientUtil.getCurrentTick(partialTick);
            state.addGeckolibData(GLOW, SuitGlowLayer.toolTints(suit, time, partialTick));
            state.addGeckolibData(RAIL_SHAKE, new float[] {suit.socketVisuals().effects().shake(suit), time});
        }
    }

    /** No centring in a block (GeoObjectRenderer's default translates by 0.5): CockpitHands places the model itself. */
    @Override
    public void adjustRenderPose(RenderPassInfo<GeoRenderState> info) {
    }

    @Override
    public void adjustModelBonesForRender(RenderPassInfo<GeoRenderState> info, BoneSnapshots bones) {
        boolean tool = info.getOrDefaultGeckolibData(PART, Part.TOOL) == Part.TOOL;
        bones.ifPresent("view_tool", b -> b.skipRender(!tool).skipChildrenRender(!tool));
        bones.ifPresent("view_gauntlet", b -> b.skipRender(true).skipChildrenRender(true)); // the big suit's (the frame's arm: ARM)
        String installed = info.getOrDefaultGeckolibData(TOOL_BONE, "");
        for (String name : ToolBones.all()) {
            boolean show = name.equals(installed);
            bones.ifPresent(name, b -> b.skipRender(!show).skipChildrenRender(!show));
        }
        boolean bare = installed.isEmpty();
        bones.ifPresent("socket", b -> b.skipRender(!bare).skipChildrenRender(!bare));
        ToolRotors.pose(bones, info.getOrDefaultGeckolibData(BARREL_ANGLE, 0F)); // turns with the suit's spin
        float[] shake = info.getGeckolibData(RAIL_SHAKE);
        if (shake != null) {
            ToolRotors.railShake(bones, shake[0], shake[1]);
        }
    }

    /** Both faces, like GeckoLib's default: in this render path the cubes wind the other way, so culling hid them all. */
    @Override
    public @Nullable RenderType getRenderType(GeoRenderState state, Identifier texture) {
        return RenderTypes.entityCutout(texture);
    }

    private static final class Model extends GeoModel<CockpitView> {
        // GeckoLib 5 ids: assets/power_suits/geckolib/models/<id>.geo.json and geckolib/animations/<id>.animation.json.
        private static final Identifier GEO = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "view/power_suit_view");
        private static final Identifier TEXTURE = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "textures/entity/power_suit.png");
        private static final Identifier ANIMATIONS = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "entity/power_suit");
        // The frame's arm (tools/export-frame.py), per build.
        private static final Identifier ARM = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "view/frame_arm");
        private static final Identifier ARM_SLIM = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "view/frame_arm_slim");
        private static final Identifier FRAME = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "textures/entity/power_frame.png");
        private static final Identifier FRAME_SLIM = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "textures/entity/power_frame_slim.png");

        private static boolean arm(GeoRenderState state) {
            return state.getOrDefaultGeckolibData(PART, Part.TOOL) == Part.ARM;
        }

        private static boolean slim(GeoRenderState state) {
            return state.getOrDefaultGeckolibData(SLIM, false);
        }

        @Override
        public Identifier getModelResource(GeoRenderState state) {
            return arm(state) ? (slim(state) ? ARM_SLIM : ARM) : GEO;
        }

        @Override
        public Identifier getTextureResource(GeoRenderState state) {
            return arm(state) ? (slim(state) ? FRAME_SLIM : FRAME) : TEXTURE;
        }

        @Override
        public Identifier getAnimationResource(CockpitView view) {
            return ANIMATIONS;
        }
    }

    private static final class ToolGlow extends GeoRenderLayer<CockpitView, Void, GeoRenderState> {
        ToolGlow(CockpitViewRenderer renderer) {
            super(renderer);
        }

        @Override
        public void submitRenderTask(RenderPassInfo<GeoRenderState> info, SubmitNodeCollector renderTasks) {
            int[] tints = info.getGeckolibData(GLOW);
            if (info.willRender() && tints != null && info.getOrDefaultGeckolibData(PART, Part.TOOL) == Part.TOOL) {
                SuitGlowLayer.drawMasks(this.renderer, info, renderTasks, MASKS, tints);
            }
        }
    }
}
