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
    private static final DataTicket<Boolean> HIDE_ARM = DataTicket.create("power_suits_view_hide_arm", Boolean.class);
    private static final DataTicket<String> TOOL_BONE = DataTicket.create("power_suits_view_tool_bone", String.class);
    private static final DataTicket<Float> BARREL_ANGLE = DataTicket.create("power_suits_view_barrel_angle", Float.class);
    /** The rail cannon's charge and the time (ticks), for its shake. */
    private static final DataTicket<float[]> RAIL_SHAKE = DataTicket.create("power_suits_view_rail_shake", float[].class);
    private static final DataTicket<int[]> GLOW = DataTicket.create("power_suits_view_glow", int[].class);
    /** The suit's armour (SuitArmour.wornMask): the arm in view shows its piece or its bare frame (ArmourBones). */
    private static final DataTicket<Integer> ARMOUR = DataTicket.create("power_suits_view_armour", Integer.class);
    /** The suit's paint (a dye id, -1 bare): the arm's piece in its colour, as on the suit. */
    private static final DataTicket<Integer> PAINT = DataTicket.create("power_suits_view_paint", Integer.class);


    CockpitViewRenderer() {
        super(new Model());
        this.withRenderLayer(new ToolGlow(this));
    }

    @Override
    public void addRenderData(CockpitView view, @Nullable Void ignored, GeoRenderState state, float partialTick) {
        state.addGeckolibData(PART, view.part);
        state.addGeckolibData(SLIM, view.slim);
        state.addGeckolibData(HIDE_ARM, view.hideArm);
        var suit = view.suit;
        state.addGeckolibData(TOOL_BONE, suit != null && suit.getSocketStack().getItem() instanceof PowerTool tool ? tool.suitBone() : "");
        state.addGeckolibData(BARREL_ANGLE, suit == null ? 0F : suit.socketVisuals().rotorAngle(partialTick));
        state.addGeckolibData(ARMOUR, suit == null ? 0 : suit.armour().wornMask());
        state.addGeckolibData(PAINT, suit == null || suit.getPaint() == null ? -1 : suit.getPaint().getId());
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
        // The installed tool (one without frame art: the drill's body, as on the frame, PowerSuitRenderer).
        String installed = info.getOrDefaultGeckolibData(TOOL_BONE, "");
        String shown = installed.isEmpty() || info.model().getBone(installed).isPresent() ? installed : "drill";
        for (String name : ToolBones.all()) {
            boolean show = name.equals(shown);
            bones.ifPresent(name, b -> b.skipRender(!show).skipChildrenRender(!show));
        }
        ArmourBones.show(bones, info.getOrDefaultGeckolibData(ARMOUR, 0), info.getOrDefaultGeckolibData(PART, Part.TOOL) == Part.TOOL ? 1 : 0); // the arm's piece, or its bare frame
        if (info.getOrDefaultGeckolibData(PART, Part.TOOL) == Part.TOOL && info.getOrDefaultGeckolibData(HIDE_ARM, false)) {
            // The tool is the subject, drawn like a held item (user, 2026-11-15): its arm's cubes stay out of the view
            // (their own bones only: the tool bones are children of view_tool).
            for (String arm : new String[] {"view_tool", "frame_left_arm", "armor_left_arm", "frame_left_arm_socket", "armor_left_arm_socket"}) {
                bones.ifPresent(arm, b -> b.skipRender(true));
            }
        }
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
        // The frame's tools about the socket (tools/export-frame.py), per build; the frame's animations (the tools' run loops).
        private static final Identifier TOOL = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "view/frame_tool");
        private static final Identifier TOOL_SLIM = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "view/frame_tool_slim");
        private static final Identifier ANIMATIONS = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "entity/power_frame");
        // The frame's arm (tools/export-frame.py), per build.
        private static final Identifier ARM = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "view/frame_arm");
        private static final Identifier ARM_SLIM = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "view/frame_arm_slim");

        private static boolean arm(GeoRenderState state) {
            return state.getOrDefaultGeckolibData(PART, Part.TOOL) == Part.ARM;
        }

        private static boolean slim(GeoRenderState state) {
            return state.getOrDefaultGeckolibData(SLIM, false);
        }

        @Override
        public Identifier getModelResource(GeoRenderState state) {
            return arm(state) ? (slim(state) ? ARM_SLIM : ARM) : slim(state) ? TOOL_SLIM : TOOL;
        }

        @Override
        public Identifier getTextureResource(GeoRenderState state) {
            return PowerSuitModel.texture(slim(state), state.getOrDefaultGeckolibData(PAINT, -1)); // the suit's, painted too
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
            // The tool's lights, like on the suit (SuitGlowLayer: one mask per ToolLight, per build).
            if (info.willRender() && tints != null && info.getOrDefaultGeckolibData(PART, Part.TOOL) == Part.TOOL) {
                boolean slim = info.getOrDefaultGeckolibData(SLIM, false);
                SuitGlowLayer.drawMasks(this.renderer, info, renderTasks,
                        slim ? SuitGlowLayer.FRAME_TOOL_MASKS_SLIM : SuitGlowLayer.FRAME_TOOL_MASKS, tints);
            }
        }
    }
}
