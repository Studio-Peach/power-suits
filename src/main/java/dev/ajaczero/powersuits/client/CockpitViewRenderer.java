package dev.ajaczero.powersuits.client;

import com.geckolib.cache.model.GeoBone;
import com.geckolib.constant.dataticket.DataTicket;
import com.geckolib.model.GeoModel;
import com.geckolib.renderer.GeoObjectRenderer;
import com.geckolib.renderer.base.BoneSnapshots;
import com.geckolib.renderer.base.GeoRenderState;
import com.geckolib.renderer.base.PerBoneRender;
import com.geckolib.renderer.base.RenderPassInfo;
import com.geckolib.renderer.layer.GeoRenderLayer;
import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.ToolArm;
import java.util.function.BiConsumer;
import net.minecraft.client.renderer.rendertype.RenderType;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.resources.Identifier;
import org.jspecify.annotations.Nullable;

/**
 * Draws one arm of the cockpit viewmodel (CockpitView): the frame's sleeve around the pilot's skin arm
 * ({@code view/frame_arm(_l)(_slim).geo.json}), plus the standalone socket tool attached onto its
 * {@code left_socket} / {@code right_socket} bone via {@link ToolModelRenderer}.
 */
final class CockpitViewRenderer extends GeoObjectRenderer<CockpitView, Void, GeoRenderState> {
    enum Part { TOOL, ARM }

    private static final DataTicket<Part> PART = DataTicket.create("power_suits_view_part", Part.class);
    private static final DataTicket<ToolArm> ARM = DataTicket.create("power_suits_view_arm", ToolArm.class);
    private static final DataTicket<Boolean> SLIM = DataTicket.create("power_suits_view_slim", Boolean.class);
    private static final DataTicket<Boolean> HIDE_ARM = DataTicket.create("power_suits_view_hide_arm", Boolean.class);
    private static final DataTicket<Integer> ARMOUR = DataTicket.create("power_suits_view_armour", Integer.class);
    private static final DataTicket<Integer> PAINT = DataTicket.create("power_suits_view_paint", Integer.class);
    private static final DataTicket<GeoRenderState> TOOL_STATE = DataTicket.create("power_suits_view_tool_state", GeoRenderState.class);

    CockpitViewRenderer() {
        super(new Model());
        this.withRenderLayer(new CockpitToolLayer(this));
    }

    @Override
    public void addRenderData(CockpitView view, @Nullable Void ignored, GeoRenderState state, float partialTick) {
        state.addGeckolibData(PART, view.part);
        state.addGeckolibData(ARM, view.arm);
        state.addGeckolibData(SLIM, view.slim);
        state.addGeckolibData(HIDE_ARM, view.hideArm);
        var suit = view.suit;
        state.addGeckolibData(ARMOUR, suit == null ? 0 : suit.armour().wornCode());
        state.addGeckolibData(PAINT, suit == null || suit.getPaint() == null ? -1 : suit.getPaint().getId());
        if (suit != null && view.part == Part.TOOL) {
            GeoRenderState toolState = ToolModelRenderer.INSTANCE.extract(suit, view.arm, partialTick);
            if (toolState != null) {
                state.addGeckolibData(TOOL_STATE, toolState);
            }
        }
    }

    /** No centring in a block (GeoObjectRenderer's default translates by 0.5): CockpitHands places the model itself. */
    @Override
    public void adjustRenderPose(RenderPassInfo<GeoRenderState> info) {
    }

    @Override
    public void adjustModelBonesForRender(RenderPassInfo<GeoRenderState> info, BoneSnapshots bones) {
        ToolArm toolArm = info.getOrDefaultGeckolibData(ARM, ToolArm.LEFT);
        int toolMask = info.getOrDefaultGeckolibData(PART, Part.TOOL) == Part.TOOL ? (toolArm == ToolArm.RIGHT ? 2 : 1) : 0;
        ArmourBones.show(bones, info.getOrDefaultGeckolibData(ARMOUR, 0), toolMask);
        if (info.getOrDefaultGeckolibData(PART, Part.TOOL) == Part.TOOL && info.getOrDefaultGeckolibData(HIDE_ARM, false)) {
            // Hide sleeve cubes only (not children) so left_socket / right_socket still renders the standalone tool.
            for (String arm : new String[] {"view_arm", "frame_left_arm", "armor_left_arm", "copper_left_arm",
                    "frame_left_arm_socket", "armor_left_arm_socket", "copper_left_arm_socket",
                    "frame_right_arm", "armor_right_arm", "copper_right_arm",
                    "frame_right_arm_socket", "armor_right_arm_socket", "copper_right_arm_socket"}) {
                bones.ifPresent(arm, b -> b.skipRender(true));
            }
        }
    }

    @Override
    public @Nullable RenderType getRenderType(GeoRenderState state, Identifier texture) {
        return RenderTypes.entityCutout(texture);
    }

    private static final class Model extends GeoModel<CockpitView> {
        private static final Identifier ANIMATIONS = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "entity/power_frame");
        private static final Identifier ARM_R = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "view/frame_arm");
        private static final Identifier ARM_R_SLIM = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "view/frame_arm_slim");
        private static final Identifier ARM_L = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "view/frame_arm_l");
        private static final Identifier ARM_L_SLIM = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "view/frame_arm_l_slim");

        private static boolean slim(GeoRenderState state) {
            return state.getOrDefaultGeckolibData(SLIM, false);
        }

        @Override
        public Identifier getModelResource(GeoRenderState state) {
            boolean slim = slim(state);
            boolean left = state.getOrDefaultGeckolibData(PART, Part.TOOL) == Part.TOOL
                    && state.getOrDefaultGeckolibData(ARM, ToolArm.LEFT) == ToolArm.LEFT;
            return left ? (slim ? ARM_L_SLIM : ARM_L) : (slim ? ARM_R_SLIM : ARM_R);
        }

        @Override
        public Identifier getTextureResource(GeoRenderState state) {
            return PowerSuitModel.texture(slim(state), state.getOrDefaultGeckolibData(PAINT, -1));
        }

        @Override
        public Identifier getAnimationResource(CockpitView view) {
            return ANIMATIONS;
        }
    }

    private static final class CockpitToolLayer extends GeoRenderLayer<CockpitView, Void, GeoRenderState> {
        CockpitToolLayer(CockpitViewRenderer renderer) {
            super(renderer);
        }

        @Override
        public void addPerBoneRender(RenderPassInfo<GeoRenderState> info, BiConsumer<GeoBone, PerBoneRender<GeoRenderState>> consumer) {
            GeoRenderState toolState = info.getGeckolibData(TOOL_STATE);
            if (!info.willRender() || toolState == null) {
                return;
            }
            String socket = info.getOrDefaultGeckolibData(ARM, ToolArm.LEFT) == ToolArm.RIGHT ? "right_socket" : "left_socket";
            info.model().getBone(socket).ifPresent(bone -> consumer.accept(bone, (pass, b, tasks) ->
                    ToolModelRenderer.INSTANCE.render(toolState, pass.poseStack(), tasks, pass.cameraState(),
                            pass.packedLight(), pass.packedOverlay(), pass.renderColor())));
        }
    }
}
