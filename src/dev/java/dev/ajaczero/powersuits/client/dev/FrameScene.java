package dev.ajaczero.powersuits.client.dev;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.client.CockpitDrafts;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.registry.ModEntities;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Locale;
import net.minecraft.client.CameraType;
import net.minecraft.client.Minecraft;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec3;
import net.neoforged.fml.loading.FMLPaths;

/**
 * Autopilot scene for the frame in game (2026-11-14, ./gradlew runAutopilotFrame, ~25 s): the frame with the player
 * inside, drawn in his own skin, from the front, the back and the side (GUI hidden), the game's own third-person view,
 * the cockpit looking down at his legs, a walk and a sprint from the front (the limbs swing like a player's), the head
 * following the view (45 right: the head only; 80 left: the torso turns the last 30; up 40), and an empty frame
 * without an engine beside it (it slumps: head bowed, torso tipped). Shots ap_frame_*.png.
 * Log run/autopilot_frame.csv per tick: the suit's hitbox, how high the pilot's eyes ride above the suit (1.98: his
 * own eyes in the frame, ModEntities), the client's walk animation (position, speed), the parked frame's power and
 * the pilot's skin model (wide / slim: which frame build is drawn).
 */
final class FrameScene {
    private static BufferedWriter csv;
    private static Vec3 home;
    private static volatile PowerSuitEntity parked;
    private static String phase = "setup";

    static boolean step(Minecraft mc, int s) {
        var o = mc.options;
        switch (s) {
            case 0 -> setup(mc);
            case 6 -> { phase = "front"; camera(mc, home.add(0.6, 1.3, 3.6), home.add(-0.6, 1.15, 0)); }
            case 20 -> AutoPilot.shot(mc, "frame_front");
            case 22 -> { phase = "back"; camera(mc, home.add(0, 1.4, -3.4), home.add(0, 1.15, 0)); }
            case 36 -> AutoPilot.shot(mc, "frame_back");
            case 38 -> { phase = "side"; camera(mc, home.add(3.6, 1.2, 0), home.add(0, 1.15, 0)); }
            case 52 -> AutoPilot.shot(mc, "frame_side");
            case 54 -> { phase = "third_person"; mc.setCameraEntity(mc.player); DevUtil.hideGui(mc, false); o.setCameraType(CameraType.THIRD_PERSON_BACK); }
            case 70 -> AutoPilot.shot(mc, "frame_tp_back");
            case 72 -> { phase = "cockpit_down"; o.setCameraType(CameraType.FIRST_PERSON); AutoPilot.setView(0, 70); }
            case 88 -> AutoPilot.shot(mc, "frame_fp_down");
            // The player only moves while the camera is his own (vanilla reads the keys for the camera entity), so the
            // walk is shot with the game's front view (F5 twice), GUI hidden.
            case 90 -> { phase = "walk"; AutoPilot.setView(0, 0); mc.setCameraEntity(mc.player); DevUtil.hideGui(mc, true); o.setCameraType(CameraType.THIRD_PERSON_FRONT); AutoPilot.hold(o.keyUp, true); }
            case 104, 107, 110, 113 -> AutoPilot.shot(mc, "frame_walk_" + s);
            case 116 -> AutoPilot.hold(o.keyUp, false);
            case 130 -> { phase = "sprint"; AutoPilot.hold(o.keyUp, true); AutoPilot.hold(o.keySprint, true); }
            case 146, 148, 150 -> AutoPilot.shot(mc, "frame_sprint_" + s);
            case 152 -> { AutoPilot.hold(o.keyUp, false); AutoPilot.hold(o.keySprint, false); mc.player.setSprinting(false); }
            case 170 -> { phase = "look"; Vec3 at = mc.player.getVehicle().position(); camera(mc, at.add(0, 1.4, 3.6), at.add(0, 1.3, 0)); AutoPilot.setView(45, 0); }
            case 186 -> AutoPilot.shot(mc, "frame_look_right45");
            case 188 -> AutoPilot.setView(-80, 0);
            case 204 -> AutoPilot.shot(mc, "frame_look_left80");
            case 206 -> AutoPilot.setView(0, -40);
            case 222 -> AutoPilot.shot(mc, "frame_look_up40");
            case 224 -> { phase = "parked"; AutoPilot.setView(0, 0); camera(mc, home.add(-3.6, 1.3, 3.2), home.add(-3, 1.1, 0)); }
            case 240 -> AutoPilot.shot(mc, "frame_parked");
            // Step 2 drafts (CockpitDrafts): the empty right hand, looking down, the third-person distance.
            case 244 -> { phase = "cockpit"; mc.setCameraEntity(mc.player); DevUtil.hideGui(mc, false); o.setCameraType(CameraType.FIRST_PERSON); CockpitDrafts.armCage = true; }
            case 258 -> AutoPilot.shot(mc, "frame_cockpit_arm_cage");
            case 260 -> CockpitDrafts.armCage = false;
            case 272 -> AutoPilot.shot(mc, "frame_cockpit_arm_bare");
            case 274 -> CockpitDrafts.armCage = true;
            case 280 -> { phase = "cockpit_down"; AutoPilot.setView(0, 60); CockpitDrafts.down = 0; }
            case 296 -> AutoPilot.shot(mc, "frame_cockpit_down_0");
            case 298 -> CockpitDrafts.down = 1;
            case 306 -> AutoPilot.shot(mc, "frame_cockpit_down_1");
            case 308 -> CockpitDrafts.down = 2;
            case 316 -> AutoPilot.shot(mc, "frame_cockpit_down_2");
            case 318 -> AutoPilot.setView(0, 35);
            case 332 -> AutoPilot.shot(mc, "frame_cockpit_down_2_35");
            case 334 -> CockpitDrafts.down = 1;
            case 340 -> AutoPilot.shot(mc, "frame_cockpit_down_1_35");
            case 342 -> { phase = "distance"; CockpitDrafts.down = 1; AutoPilot.setView(0, 15); o.setCameraType(CameraType.THIRD_PERSON_BACK); CockpitDrafts.cameraDistance = 4F; }
            case 356 -> AutoPilot.shot(mc, "frame_tp_4");
            case 358 -> CockpitDrafts.cameraDistance = 5F;
            case 372 -> AutoPilot.shot(mc, "frame_tp_5");
            case 374 -> CockpitDrafts.cameraDistance = 6.5F;
            case 388 -> AutoPilot.shot(mc, "frame_tp_6_5");
            case 390 -> { CockpitDrafts.cameraDistance = 5F; AutoPilot.setView(0, 0); close(); return false; }
            default -> {}
        }
        if (s >= 1) {
            log(mc, s);
        }
        return true;
    }

    /** Noon, an empty hand, the view ahead (+Z); an engineless frame 3 blocks to the pilot's right, facing the same way. */
    private static void setup(Minecraft mc) {
        AutoPilot.setView(0, 0);
        home = mc.player.getVehicle().position();
        AutoPilot.onServer(mc, p -> {
            DevUtil.setTime(p.level(), 6000);
            p.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY);
            PowerSuitEntity s = ModEntities.POWER_SUIT.get().create(p.level(), EntitySpawnReason.COMMAND);
            s.snapTo(home.x - 3, home.y, home.z, 0, 0);
            s.setYBodyRot(0);
            s.setYHeadRot(0);
            p.level().addFreshEntity(s);
            parked = s;
        });
        try {
            csv = Files.newBufferedWriter(FMLPaths.GAMEDIR.get().resolve("autopilot_frame.csv"));
            csv.write("tick,phase,bb_width,bb_height,eye_above_suit,walk_pos,walk_speed,speed,parked_powered,pilot_skin\n");
        } catch (IOException e) {
            PowerSuits.LOGGER.error("frame csv", e);
        }
    }

    /** A still camera (GUI hidden: the screenshot shows the frame, not the visor). */
    private static void camera(Minecraft mc, Vec3 from, Vec3 to) {
        mc.options.setCameraType(CameraType.FIRST_PERSON);
        DevUtil.hideGui(mc, true);
        // the camera is an armor stand's eye: place the stand that much lower
        Vec3 drop = new Vec3(0, EntityTypes.ARMOR_STAND.getDimensions().eyeHeight(), 0);
        AutoPilot.lookCamera(mc, from.subtract(drop), to.subtract(drop));
    }

    private static void log(Minecraft mc, int s) {
        if (csv == null || !(mc.player.getVehicle() instanceof PowerSuitEntity suit)) {
            return;
        }
        PowerSuitEntity p = parked;
        var parkedClient = p == null || mc.level == null ? null : mc.level.getEntity(p.getId());
        try {
            csv.write(String.format(Locale.ROOT, "%d,%s,%.3f,%.3f,%.3f,%.3f,%.3f,%.2f,%s,%s%n", s, phase, suit.getBbWidth(), suit.getBbHeight(),
                    mc.player.getEyeY() - suit.getY(), suit.walkAnimation.position(), suit.walkAnimation.speed(),
                    suit.animator().getVisualSpeed(), parkedClient instanceof PowerSuitEntity c ? c.isPowered() : "-",
                    mc.player.getSkin().model().getSerializedName())); // slim = the frame's slim build
        } catch (IOException ignored) {
            // closed
        }
    }

    private static void close() {
        try {
            if (csv != null) {
                csv.close();
            }
        } catch (IOException ignored) {
            // nothing to do
        }
        csv = null;
    }

    private FrameScene() {}
}
