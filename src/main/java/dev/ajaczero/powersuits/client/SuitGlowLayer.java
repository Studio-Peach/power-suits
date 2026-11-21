package dev.ajaczero.powersuits.client;

import com.geckolib.constant.DataTickets;
import com.geckolib.renderer.base.GeoRenderState;
import com.geckolib.renderer.base.GeoRenderer;
import com.geckolib.renderer.base.RenderPassInfo;
import com.geckolib.renderer.layer.GeoRenderLayer;
import com.geckolib.util.ClientUtil;
import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.entity.SuitEngine;
import dev.ajaczero.powersuits.entity.SuitFace;
import dev.ajaczero.powersuits.entity.SuitLights;
import dev.ajaczero.powersuits.entity.ToolArm;
import dev.ajaczero.powersuits.item.HelmetStyle;
import dev.ajaczero.powersuits.item.ToolLight;
import java.util.Arrays;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.Identifier;
import net.minecraft.util.LightCoordsUtil;
import net.minecraft.util.Mth;
import org.jspecify.annotations.Nullable;

/**
 * The suit's lights: the engine's fire (the tidal engine and the star reactor in their colours), the visor, the tools'
 * status lamp, the chaingun's green lights and the flamethrower's pilot light, drawn on top of the model at full
 * brightness so they glow in the dark. Like GeckoLib's AutoGlowingGeoLayer, the whole model is drawn again with a
 * glowmask texture (empty except the glowing pixels, made from reserved colours by tools/export-frame.py; the big
 * suit's by tools/make-glowmasks.py) in vanilla's "eyes" render type (the one
 * spider and enderman eyes use): it ignores light and draws its colour on top (blended by alpha in 26.3, not added:
 * a dimmed mask is a darker colour, fine over the dark glass and coals it sits on). Unlike AutoGlowingGeoLayer, each mask
 * is tinted every frame, so the fire flickers and fades and the visor changes colour (PowerSuitEntity.tickLights). The
 * socket tool's lights ({@link ToolLight}) are worked out by the installed tool's ToolEffects.
 */
public class SuitGlowLayer extends GeoRenderLayer<PowerSuitEntity, Void, LivingEntityRenderState> {
    /** This frame's tints of one arm's socket tool lights (ToolLight order), used by ToolModelRenderer. */
    static int[] toolTints(PowerSuitEntity suit, ToolArm arm, float time, float partial) {
        return tints(suit.socketVisuals(arm).lights(time, partial));
    }

    private static int[] tints(float[] lights) {
        int[] tints = new int[lights.length];
        ToolLight[] all = ToolLight.values();
        for (int i = 0; i < lights.length; i++) {
            tints[i] = all[i].fadesByAlpha ? energy(lights[i]) : tint(lights[i], 1F, 1F, 1F);
        }
        return tints;
    }

    public SuitGlowLayer(GeoRenderer<PowerSuitEntity, Void, LivingEntityRenderState> renderer) {
        super(renderer);
    }

    /** Extract: work out this frame's tint of every light while we still have the suit. */
    @Override
    public void addRenderData(PowerSuitEntity suit, @Nullable Void ignored, LivingEntityRenderState state, float partialTick) {
        float time = (float) ClientUtil.getCurrentTick(partialTick);
        // Coals: a slow uneven flicker (two sines that never line up), deeper when the engine works hard.
        float fire = suit.lights().getFireGlow() * (0.86F + 0.08F * Mth.sin(time * 0.37F + suit.getId()) + 0.06F * Mth.sin(time * 1.31F));
        float[] visor = suit.lights().getVisorColor();
        float on = suit.lights().getVisorFlicker(time);
        // The robot helmet's visor shows a face instead of its light: opaque, at the visor's full brightness and colour.
        boolean robot = suit.getHelmetStyle() == HelmetStyle.ROBOT;
        SuitFace.Face face = robot ? suit.lights().face().shown() : null;
        state.addGeckolibData(SuitRenderData.VISOR_FACE, face == null ? -1 : face.ordinal());
        // Knocked out by lightning the visor is off, but the dizzy face shows through it, stuttering.
        float faceLevel = suit.isStunned() ? (Mth.sin(time * 1.7F) + Mth.sin(time * 4.1F) < -0.6F ? 0.25F : 0.85F) : on;
        boolean glasses = suit.hasGlasses();
        int[] suitTints = {
                tint(fire, 1F, 1F, 1F),
                robot ? tint(faceLevel, visor[0], visor[1], visor[2])
                        : glasses ? tint(on, visor[0], visor[1], visor[2])
                        : glass(on * VISOR_GLOW, visor[0], visor[1], visor[2]),
                tint(suit.lights().getTidalGlow(time), TIDAL_TINT[0], TIDAL_TINT[1], TIDAL_TINT[2]),
                tint(suit.lights().getReactorGlow(time), REACTOR_TINT[0], REACTOR_TINT[1], REACTOR_TINT[2])};
        state.addGeckolibData(SuitRenderData.GLOW, suitTints);
        float[] chain = suit.lights().getStarSegments(time);
        int[] star = new int[1 + chain.length];
        star[0] = tint(suit.lights().getReactorGlow(time), 1F, 1F, 1F);   // the lines, the links, the lens: steady
        for (int i = 0; i < chain.length; i++) {
            star[1 + i] = tint(chain[i], 1F, 1F, 1F);
        }
        state.addGeckolibData(SuitRenderData.STAR, star);
    }

    /** The frame's visor glowmask per build (tools/export-frame.py: its glass texels). */
    private static final Identifier FRAME_VISOR = frameMask("visor"), FRAME_VISOR_SLIM = frameMask("visor_slim");
    /** The AR glasses' left-temple power indicator LED glowmask per build (lenses stay dark). */
    private static final Identifier FRAME_GLASSES_LED = frameMask("glasses_led"), FRAME_GLASSES_LED_SLIM = frameMask("glasses_led_slim");
    /** The robot helmet's faces per build (tools/export-frame.py, from frame_helmet_art.py ROBOT_FACES), by
     *  SuitFace.Face ordinal: white texels on its visor's front, tinted in the visor's colour. */
    private static final Identifier[] ROBOT_FACES = faceMasks(""), ROBOT_FACES_SLIM = faceMasks("_slim");

    private static Identifier[] faceMasks(String build) {
        return Arrays.stream(SuitFace.Face.values()).map(f -> frameMask("robot_" + f.id() + build)).toArray(Identifier[]::new);
    }

    /** The frame's engine fire per build (tools/export-frame.py: its reserved coal colours). Anything painted in those
     *  colours lights with the engine: the radiator guard's slats, the protector helmet's cheek lamps (its lamps are
     *  "on when the suit is powered", so they borrow the fire's light). */
    private static final Identifier FRAME_FIRE = frameMask("fire"), FRAME_FIRE_SLIM = frameMask("fire_slim");
    /** The same texels in white -> grey (FRAME_CORE): the star reactor's light on the heart until it has frame art of its
     *  own, in the big suit's violet core (tinting the fire's yellow -> red mask instead came out a muddy pink). */
    private static final Identifier FRAME_CORE = frameMask("core"), FRAME_CORE_SLIM = frameMask("core_slim");
    /** The tidal engine's glass (tools/export-frame.py: its reserved dark teals, painted in their lit teals): white tint,
     *  scaled by the tidal glow's shimmer. */
    private static final Identifier FRAME_SEA = frameMask("sea"), FRAME_SEA_SLIM = frameMask("sea_slim");
    private static final float[] TIDAL_TINT = {1F, 1F, 1F}, REACTOR_TINT = {0.85F, 0.45F, 1F};
    /** The star reactor's glowmasks per build (tools/export-frame.py star_masks): the steady one, then the pulse's segments
     *  from the hip up (the violet is painted in them: white tint, scaled by the level). */
    private static final Identifier[] STAR = starMasks(""), STAR_SLIM = starMasks("_slim");

    private static Identifier[] starMasks(String build) {
        Identifier[] masks = new Identifier[1 + SuitLights.STAR_SEGMENTS];
        masks[0] = frameMask("star" + build);
        for (int i = 0; i < SuitLights.STAR_SEGMENTS; i++) {
            masks[1 + i] = frameMask("star_" + i + build);
        }
        return masks;
    }
    /** How strongly the lit visor covers the glass: part strength, so the pilot's face still shows through. */
    private static final float VISOR_GLOW = 0.45F;

    private static Identifier frameMask(String name) {
        return Identifier.fromNamespaceAndPath(PowerSuits.MODID, "textures/entity/power_frame_glow_" + name + ".png");
    }

    /**
     * Render: draw the model once per lit mask, after (on top of) the suit itself: the frame's engine fire (for each
     * engine, see TIDAL_TINT), the visor, and the socket tool's lights (FRAME_TOOL_MASKS; a hidden tool's bone isn't
     * drawn again, so only the installed tool's texels light).
     * The frame's visor is glass with his face behind it, so its light fades by opacity in the visor's colour
     * (energy-style, see energy()), not by darkening an opaque colour as on the big suit's dark visor.
     */
    @Override
    public void submitRenderTask(RenderPassInfo<LivingEntityRenderState> info, SubmitNodeCollector renderTasks) {
        int[] tints = info.getGeckolibData(SuitRenderData.GLOW);
        if (!info.willRender() || info.getOrDefaultGeckolibData(SuitRenderData.COCKPIT, false) || tints == null) {
            return; // nothing is drawn from inside
        }
        boolean slim = info.getOrDefaultGeckolibData(SuitRenderData.PILOT_SLIM, false);
        // The fire, in the installed engine's light (the fire's glow follows the power for any engine, so pick by the
        // engine; none installed: the engine isn't drawn, nor its mask).
        int engine = info.getOrDefaultGeckolibData(SuitRenderData.ENGINE, -1);
        boolean sea = engine == SuitEngine.TIDAL.ordinal();
        boolean star = engine == SuitEngine.REACTOR.ordinal();
        boolean firebox = !sea && !star;
        int fire = engine == SuitEngine.TIDAL.ordinal() ? tints[2] : engine == SuitEngine.REACTOR.ordinal() ? tints[3] : tints[0];
        Identifier fireMask = firebox ? (slim ? FRAME_FIRE_SLIM : FRAME_FIRE)
                : sea ? (slim ? FRAME_SEA_SLIM : FRAME_SEA) : null;   // (the reactor's own masks: below)
        // No helmet or AR glasses, no visor / LED glow (its tint stays on with the power).
        boolean hasHelmet = info.getOrDefaultGeckolibData(SuitRenderData.HELMET, false);
        boolean hasGlasses = info.getOrDefaultGeckolibData(SuitRenderData.GLASSES, false);
        int visor = (hasHelmet || hasGlasses) ? tints[1] : 0xFF000000;
        // Suit lights only (tools draw their own independent glowmasks via ToolModelRenderer).
        Identifier[] masks = new Identifier[2];
        int[] all = {fire, visor};
        masks[0] = fireMask;
        masks[1] = hasGlasses ? (slim ? FRAME_GLASSES_LED_SLIM : FRAME_GLASSES_LED) : (slim ? FRAME_VISOR_SLIM : FRAME_VISOR);
        Identifier face = null;
        if (info.getOrDefaultGeckolibData(SuitRenderData.HELMET_STYLE, -1) == HelmetStyle.ROBOT.ordinal()) {
            int shown = info.getOrDefaultGeckolibData(SuitRenderData.VISOR_FACE, -1);   // its face, or nothing (dark)
            face = shown < 0 ? null : (slim ? ROBOT_FACES_SLIM : ROBOT_FACES)[shown];
            masks[1] = null;
        }
        drawMasks(this.renderer, info, renderTasks, masks, all, 1);
        int[] chain = info.getGeckolibData(SuitRenderData.STAR);
        if (star && chain != null) {
            drawMasks(this.renderer, info, renderTasks, slim ? STAR_SLIM : STAR, chain, 1);   // the star reactor's pulse
        }
        if (face != null) {
            // The robot's face: on top of the glass (HelmetGlassLayer, order 1). In the same order the passes' sort
            // depended on the texture, so some faces showed through the smoked glass at a fifth of their light.
            drawMasks(this.renderer, info, renderTasks, new Identifier[] {face}, new int[] {visor}, 2);
        }
    }

    /** Draws the model again in the "eyes" render type for each mask whose tint isn't black. The tint, light
     *  and overlay are read from the render state when a pass is submitted, so they're swapped in for each pass and put
     *  back afterwards. */
    static <R extends GeoRenderState> void drawMasks(GeoRenderer<?, ?, R> renderer, RenderPassInfo<R> info, SubmitNodeCollector renderTasks,
                                                     Identifier[] masks, int[] tints) {
        drawMasks(renderer, info, renderTasks, masks, tints, 1);
    }

    /** The same in the given submit order (later orders draw over earlier ones). */
    static <R extends GeoRenderState> void drawMasks(GeoRenderer<?, ?, R> renderer, RenderPassInfo<R> info, SubmitNodeCollector renderTasks,
                                                     Identifier[] masks, int[] tints, int order) {
        R state = info.renderState();
        int colour = info.renderColor(), light = info.packedLight(), overlay = info.packedOverlay();
        for (int i = 0; i < masks.length; i++) {
            if (masks[i] == null || (tints[i] & 0xFFFFFF) == 0) {
                continue; // off, or a light without a mask
            }
            state.addGeckolibData(DataTickets.RENDER_COLOR, tints[i]); // scaling the colour down dims the glow
            state.addGeckolibData(DataTickets.PACKED_LIGHT, LightCoordsUtil.FULL_BRIGHT);
            state.addGeckolibData(DataTickets.PACKED_OVERLAY, OverlayTexture.NO_OVERLAY);
            renderer.submitRenderTasks(info, renderTasks.order(order), RenderTypes.eyes(masks[i]));
        }
        state.addGeckolibData(DataTickets.RENDER_COLOR, colour);
        state.addGeckolibData(DataTickets.PACKED_LIGHT, light);
        state.addGeckolibData(DataTickets.PACKED_OVERLAY, overlay);
    }

    /** Light that fades in over the model or over nothing (the chaingun's heat, the rail cannon's core, see-through
     *  when off: its pixels are cleared from the texture): the mask's own colour, faded by its opacity instead of darkened.
     *  The "eyes" pipeline blends by alpha (it isn't additive), so a dimmed opaque colour would draw a dark core where
     *  there should be air (the chaingun's warming barrels showed a dark smudge until 2026-10-26). */
    static int energy(float brightness) {
        if (brightness <= 0.01F) {
            return 0xFF000000;
        }
        return channel(brightness) << 24 | 0xFFFFFF;
    }

    /** (r, g, b) at full colour, faded in by opacity (light over glass); black (= nothing to draw) below 1%. */
    static int glass(float opacity, float r, float g, float b) {
        if (opacity <= 0.01F) {
            return 0xFF000000;
        }
        return channel(opacity) << 24 | channel(r) << 16 | channel(g) << 8 | channel(b);
    }

    /** Opaque ARGB of (r, g, b) x brightness; black (= nothing to draw) below 1%. */
    static int tint(float brightness, float r, float g, float b) {
        if (brightness <= 0.01F) {
            return 0xFF000000;
        }
        return 0xFF000000 | channel(r * brightness) << 16 | channel(g * brightness) << 8 | channel(b * brightness);
    }

    private static int channel(float v) {
        return Mth.clamp((int) (v * 255F), 0, 255);
    }
}
