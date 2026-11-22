package dev.ajaczero.powersuits.client;

import com.geckolib.animatable.GeoAnimatable;
import com.geckolib.animatable.instance.AnimatableInstanceCache;
import com.geckolib.animatable.manager.AnimatableManager;
import com.geckolib.constant.DataTickets;
import com.geckolib.constant.dataticket.DataTicket;
import com.geckolib.model.GeoModel;
import com.geckolib.renderer.GeoObjectRenderer;
import com.geckolib.renderer.base.BoneSnapshots;
import com.geckolib.renderer.base.GeoRenderState;
import com.geckolib.renderer.base.RenderPassInfo;
import com.geckolib.renderer.layer.GeoRenderLayer;
import com.geckolib.util.ClientUtil;
import com.geckolib.util.GeckoLibUtil;
import com.mojang.blaze3d.vertex.PoseStack;
import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.entity.ToolArm;
import dev.ajaczero.powersuits.item.PowerTool;
import dev.ajaczero.powersuits.item.ToolLight;
import java.util.Map;
import java.util.Set;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.rendertype.RenderType;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.resources.Identifier;
import org.jspecify.annotations.Nullable;

/**
 * Draws any standalone power tool model ({@code geckolib/models/tool/<id>(_r).geo.json}, exported by
 * {@code tools/export-tools.py} with its socket pivot at {@code (0, 0, 0)}) and its own per-tool glowmasks.
 * Shared by both third-person suits ({@link ToolLayer}) and the first-person cockpit ({@link CockpitViewRenderer}):
 * each arm extracts its own snapshot, so dual-wielding tools spin, shake and glow completely independently.
 */
final class ToolModelRenderer extends GeoObjectRenderer<ToolModelRenderer.Dummy, ToolModelRenderer.Context, GeoRenderState> {
    static final ToolModelRenderer INSTANCE = new ToolModelRenderer();

    /** Tools whose art is handed (left/right mirror uses a separate _r geo sharing the same texture). */
    private static final Set<String> HANDED = Set.of("drill", "chainsaw", "flamethrower");
    /** Tools with standalone exported models; any later tool without one falls back to the drill. */
    private static final Set<String> KNOWN = Set.of("drill", "chainsaw", "chaingun", "flamethrower", "rail_cannon", "tnt_launcher", "em_projector");
    private static final String STAND_IN = "drill";

    private static final DataTicket<String> TOOL_ID = DataTicket.create("power_suits_tool_id", String.class);
    private static final DataTicket<Boolean> RIGHT_ARM = DataTicket.create("power_suits_tool_right", Boolean.class);
    private static final DataTicket<Float> ROTOR_ANGLE = DataTicket.create("power_suits_tool_rotor", Float.class);
    private static final DataTicket<Boolean> RUNNING = DataTicket.create("power_suits_tool_running", Boolean.class);
    private static final DataTicket<Float> TIME = DataTicket.create("power_suits_tool_time", Float.class);
    private static final DataTicket<Float> RAIL_SHAKE = DataTicket.create("power_suits_tool_rail_shake", Float.class);
    private static final DataTicket<int[]> GLOW = DataTicket.create("power_suits_tool_glow", int[].class);

    /** Per-tool glowmask tables indexed by ToolLight.ordinal() (null for lights a tool does not use). */
    private static final Map<String, Identifier[]> GLOW_MASKS = Map.of(
            "drill", masks("drill", Map.of(ToolLight.LAMP_IDLE, "lamp_idle", ToolLight.LAMP_RUN, "lamp_run")),
            "chainsaw", masks("chainsaw", Map.of(ToolLight.LAMP_IDLE, "lamp_idle", ToolLight.LAMP_RUN, "lamp_run")),
            "chaingun", masks("chaingun", Map.of(ToolLight.GUN_LIGHT, "gun_light", ToolLight.HEAT, "heat", ToolLight.HEAT_BARREL, "heat_barrel")),
            "flamethrower", masks("flamethrower", Map.of(ToolLight.PILOT, "pilot")),
            "rail_cannon", masks("rail_cannon", Map.of(
                    ToolLight.RAIL_FLOW_0, "rail_flow_0", ToolLight.RAIL_FLOW_1, "rail_flow_1",
                    ToolLight.RAIL_FLOW_2, "rail_flow_2", ToolLight.RAIL_EMIT, "rail_emit")),
            "em_projector", masks("em_projector", Map.of(ToolLight.EM_CORE, "em_core", ToolLight.EM_ARC, "em_arc")));

    private static final Dummy DUMMY = new Dummy();

    private static Identifier[] masks(String tool, Map<ToolLight, String> entries) {
        Identifier[] out = new Identifier[ToolLight.values().length];
        entries.forEach((light, suffix) -> out[light.ordinal()] = Identifier.fromNamespaceAndPath(
                PowerSuits.MODID, "textures/tool/" + tool + "_glow_" + suffix + ".png"));
        return out;
    }

    private ToolModelRenderer() {
        super(new Model());
        this.withRenderLayer(new ToolGlow(this));
    }

    /** Extract phase: snapshots the tool installed on {@code arm}, or null if that arm has no tool. */
    @Nullable
    GeoRenderState extract(PowerSuitEntity suit, ToolArm arm, float partialTick) {
        if (!(suit.getSocketStack(arm).getItem() instanceof PowerTool tool)) {
            return null;
        }
        String id = tool.suitBone();
        if (id.isEmpty()) {
            return null;
        }
        return fillRenderState(DUMMY, new Context(suit, arm, KNOWN.contains(id) ? id : STAND_IN),
                createRenderState(DUMMY, null), partialTick);
    }

    /** Render phase: draws a previously extracted tool state at the current PoseStack origin (the socket bone). */
    void render(GeoRenderState toolState, PoseStack poseStack, SubmitNodeCollector tasks, CameraRenderState camera,
                int packedLight, int packedOverlay, int renderColor) {
        toolState.addGeckolibData(DataTickets.PACKED_LIGHT, packedLight);
        toolState.addGeckolibData(DataTickets.PACKED_OVERLAY, packedOverlay);
        toolState.addGeckolibData(DataTickets.RENDER_COLOR, renderColor);
        performRenderPass(toolState, poseStack, tasks, camera);
    }

    @Override
    public void addRenderData(Dummy animatable, @Nullable Context ctx, GeoRenderState state, float partialTick) {
        if (ctx == null) {
            return;
        }
        float time = (float) ClientUtil.getCurrentTick(partialTick);
        state.addGeckolibData(TOOL_ID, ctx.toolId);
        state.addGeckolibData(RIGHT_ARM, ctx.arm == ToolArm.RIGHT);
        state.addGeckolibData(ROTOR_ANGLE, ctx.suit.socketVisuals(ctx.arm).rotorAngle(partialTick));
        state.addGeckolibData(RUNNING, ctx.suit.socket(ctx.arm).isRunning());
        state.addGeckolibData(TIME, time);
        state.addGeckolibData(RAIL_SHAKE, ctx.suit.socketVisuals(ctx.arm).shake());
        state.addGeckolibData(GLOW, SuitGlowLayer.toolTints(ctx.suit, ctx.arm, time, partialTick));
    }

    /** No 0.5 block centring: the socket bone is already at the tool's (0, 0, 0) pivot. */
    @Override
    public void adjustRenderPose(RenderPassInfo<GeoRenderState> info) {
    }

    @Override
    public void adjustModelBonesForRender(RenderPassInfo<GeoRenderState> info, BoneSnapshots bones) {
        float angle = info.getOrDefaultGeckolibData(ROTOR_ANGLE, 0F);
        boolean running = info.getOrDefaultGeckolibData(RUNNING, false);
        float time = info.getOrDefaultGeckolibData(TIME, 0F);
        ToolRotors.pose(bones, angle, running, time);
        float shake = info.getOrDefaultGeckolibData(RAIL_SHAKE, 0F);
        if (shake > 0F) {
            ToolRotors.railShake(bones, shake, time);
        }
    }

    @Override
    public @Nullable RenderType getRenderType(GeoRenderState state, Identifier texture) {
        // In MC 26.3 entityCutout is already no-cull (culled is entityCutoutCull), so thin 2D outer cutout layers draw cleanly.
        return RenderTypes.entityCutout(texture);
    }

    record Context(PowerSuitEntity suit, ToolArm arm, String toolId) {}

    /** Stateless animatable handle (all tool motion is driven per-frame in ToolRotors from extracted state). */
    static final class Dummy implements GeoAnimatable {
        private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

        @Override
        public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        }

        @Override
        public AnimatableInstanceCache getAnimatableInstanceCache() {
            return this.cache;
        }
    }

    private static final class Model extends GeoModel<Dummy> {
        private static final Identifier EMPTY_ANIM = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "entity/power_frame");

        @Override
        public Identifier getModelResource(GeoRenderState state) {
            String id = state.getOrDefaultGeckolibData(TOOL_ID, STAND_IN);
            boolean right = state.getOrDefaultGeckolibData(RIGHT_ARM, false);
            String path = right && HANDED.contains(id) ? id + "_r" : id;
            return Identifier.fromNamespaceAndPath(PowerSuits.MODID, "tool/" + path);
        }

        @Override
        public Identifier getTextureResource(GeoRenderState state) {
            String id = state.getOrDefaultGeckolibData(TOOL_ID, STAND_IN);
            return Identifier.fromNamespaceAndPath(PowerSuits.MODID, "textures/tool/" + id + ".png");
        }

        @Override
        public Identifier getAnimationResource(Dummy animatable) {
            return EMPTY_ANIM;
        }
    }

    private static final class ToolGlow extends GeoRenderLayer<Dummy, Context, GeoRenderState> {
        ToolGlow(ToolModelRenderer renderer) {
            super(renderer);
        }

        @Override
        public void submitRenderTask(RenderPassInfo<GeoRenderState> info, SubmitNodeCollector renderTasks) {
            if (!info.willRender()) {
                return;
            }
            int[] tints = info.getGeckolibData(GLOW);
            Identifier[] masks = GLOW_MASKS.get(info.getOrDefaultGeckolibData(TOOL_ID, ""));
            if (tints != null && masks != null) {
                SuitGlowLayer.drawMasks(this.renderer, info, renderTasks, masks, tints);
            }
        }
    }
}
