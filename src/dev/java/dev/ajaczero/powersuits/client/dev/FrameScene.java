package dev.ajaczero.powersuits.client.dev;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.registry.ModEntities;
import dev.ajaczero.powersuits.registry.ModItems;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;
import java.util.Locale;
import java.util.function.Supplier;
import net.minecraft.client.CameraType;
import net.minecraft.client.Minecraft;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.util.Mth;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.phys.Vec3;
import net.neoforged.fml.loading.FMLPaths;

/**
 * Autopilot scene for the frame in game (2026-11-14, ./gradlew runAutopilotFrame, ~25 s): the frame with the player
 * inside, drawn in his own skin, from the front, the back and the side (GUI hidden), the game's own third-person view,
 * a walk and a sprint from the front (the limbs swing like a player's), the head
 * following the view (45 right: the head only; 80 left: the torso turns the last 30; up 40), and an empty frame
 * without an engine beside it (it slumps: head bowed, torso tipped; its helmet's visor dark), the helmet up close (his
 * face behind the visor glass, lit in the visor's colour; at night; the parked frame's dark visor; without a helmet:
 * his own head and hat layer), the engine (the blower on the back, the core and hoses on the front, by day and by night:
 * fire lit, smoke from the caps; a star reactor frame, its light violet on the same heart), every socket tool (the
 * EM projector, TNT launcher and rail cannon stand in with the drill's body), the drill and chaingun running, then the cockpit: the empty right hand (his arm in
 * the frame's arm) and looking down (nothing of his body, like vanilla). Shots ap_frame_*.png.
 * Log run/autopilot_frame.csv per tick: the suit's hitbox, how high the pilot's eyes ride above the suit (1.98: his
 * own eyes in the frame, ModEntities), the client's walk animation (position, speed), the parked frame's power and
 * the pilot's skin model (wide / slim: which frame build is drawn).
 */
final class FrameScene {
    private static BufferedWriter csv;
    private static Vec3 home;
    private static volatile PowerSuitEntity parked, reactor;
    /** The socket tools, in the order shot (ModItems), from tick TOOLS_AT, 16 ticks each. */
    private static final int TOOLS_AT = 420;
    private static final String[] TOOL_NAMES = {"chaingun", "em_projector", "drill", "chainsaw", "flamethrower", "tnt_launcher", "rail_cannon"};
    private static final List<Supplier<? extends Item>> TOOLS = List.of(
            ModItems.CHAINGUN, ModItems.EM_PROJECTOR, ModItems.DRILL, ModItems.CHAINSAW, ModItems.FLAMETHROWER, ModItems.TNT_LAUNCHER,
            ModItems.RAIL_CANNON);
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
            // The helmet up close: his face behind the visor glass, lit in the visor's colour; at night; without it.
            case 242 -> { phase = "helmet"; Vec3 at = mc.player.getVehicle().position(); camera(mc, at.add(0.9, 2.0, 1.5), at.add(0, 1.95, 0)); }
            case 256 -> AutoPilot.shot(mc, "frame_helmet_front");
            case 258 -> { Vec3 at = mc.player.getVehicle().position(); camera(mc, at.add(1.7, 2.0, 0.2), at.add(0, 1.95, 0)); }
            case 272 -> AutoPilot.shot(mc, "frame_helmet_side");
            case 274 -> { phase = "helmet_night"; AutoPilot.onServer(mc, p -> DevUtil.setTime(p.level(), 18000)); Vec3 at = mc.player.getVehicle().position(); camera(mc, at.add(0.9, 2.0, 1.5), at.add(0, 1.95, 0)); }
            case 290 -> AutoPilot.shot(mc, "frame_helmet_night");
            case 292 -> { Vec3 at = parked.position(); camera(mc, at.add(0.9, 1.9, 1.6), at.add(0, 1.85, 0)); }
            case 306 -> AutoPilot.shot(mc, "frame_helmet_night_parked"); // no power: a dark visor
            case 308 -> { phase = "no_helmet"; AutoPilot.onServer(mc, p -> DevUtil.setTime(p.level(), 6000)); helmet(mc, false); Vec3 at = mc.player.getVehicle().position(); camera(mc, at.add(0.9, 2.0, 1.5), at.add(0, 1.95, 0)); }
            case 322 -> AutoPilot.shot(mc, "frame_no_helmet");
            case 324 -> helmet(mc, true);
            // The engine (the pilot's firebox): the blower on the back, the core and hoses on the front, by day and by night
            // (the fire lit, smoke from the caps); a star reactor frame (its light violet on the same heart).
            case 330 -> { phase = "engine"; Vec3 at = mc.player.getVehicle().position(); camera(mc, at.add(1.4, 2.1, -2.2), at.add(0, 1.4, 0)); }
            case 344 -> AutoPilot.shot(mc, "frame_engine_back");
            case 346 -> { Vec3 at = mc.player.getVehicle().position(); camera(mc, at.add(-1.2, 1.6, 2.2), at.add(0, 1.35, 0)); }
            case 360 -> AutoPilot.shot(mc, "frame_engine_front");
            case 362 -> { phase = "engine_night"; AutoPilot.onServer(mc, p -> DevUtil.setTime(p.level(), 18000)); Vec3 at = mc.player.getVehicle().position(); camera(mc, at.add(1.4, 2.1, -2.2), at.add(0, 1.4, 0)); }
            case 380 -> AutoPilot.shot(mc, "frame_engine_night_back");
            case 382 -> { Vec3 at = mc.player.getVehicle().position(); camera(mc, at.add(-1.2, 1.6, 2.2), at.add(0, 1.35, 0)); }
            case 396 -> AutoPilot.shot(mc, "frame_engine_night_front");
            case 398 -> around(mc, reactor, -2.4);     // its mind turns it about: shoot by its own facing
            case 410 -> AutoPilot.shot(mc, "frame_engine_reactor_back");
            case 411 -> around(mc, reactor, 2.4);
            case 417 -> AutoPilot.shot(mc, "frame_engine_reactor_front");
            case 418 -> AutoPilot.onServer(mc, p -> DevUtil.setTime(p.level(), 6000));
            default -> {}
        }
        // The tools in the left arm's socket, one after another (the last three stand in with the drill's body).
        int k = s - TOOLS_AT;
        if (k >= 0 && k < TOOLS.size() * 16) {
            int i = k / 16;
            switch (k % 16) {
                case 0 -> { phase = "tool_" + TOOL_NAMES[i]; socket(mc, i); Vec3 at = mc.player.getVehicle().position();
                            camera(mc, at.add(1.9, 1.35, 1.7), at.add(0.45, 0.8, 0)); }
                case 12 -> AutoPilot.shot(mc, "frame_tool_" + TOOL_NAMES[i]);
                default -> {}
            }
        }
        // The drill and the chaingun running (third person: the player's keys only work with his own camera): the bit
        // spins, the barrels turn (the CSV's tool_running and rotor columns).
        switch (s) {
            case 534 -> { phase = "tool_run_drill"; socket(mc, 2); mc.setCameraEntity(mc.player); o.setCameraType(CameraType.THIRD_PERSON_BACK);
                          DevUtil.hideGui(mc, true); AutoPilot.setView(0, 50); AutoPilot.hold(o.keyUse, true); }
            case 550 -> AutoPilot.shot(mc, "frame_tool_run_drill");
            case 552 -> { AutoPilot.hold(o.keyUse, false); phase = "tool_run_chaingun"; socket(mc, 0); AutoPilot.setView(0, 0); }
            case 556 -> AutoPilot.hold(o.keyUse, true);
            case 576 -> AutoPilot.shot(mc, "frame_tool_run_chaingun");
            case 578 -> { AutoPilot.hold(o.keyUse, false); socket(mc, -1); }
            // The cockpit: the empty right hand (his arm in the frame's), nothing of the body looking down.
            case 590 -> { phase = "cockpit"; mc.setCameraEntity(mc.player); DevUtil.hideGui(mc, false); o.setCameraType(CameraType.FIRST_PERSON); }
            case 604 -> AutoPilot.shot(mc, "frame_cockpit_arm");
            case 606 -> AutoPilot.setView(0, 60);
            case 622 -> AutoPilot.shot(mc, "frame_cockpit_down");
            case 624 -> { AutoPilot.setView(0, 0); close(); return false; }
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
            s.getInventory().setItem(PowerSuitEntity.HELMET_SLOT, new ItemStack(ModItems.SUIT_HELMET.get())); // its visor dark: no power
            p.level().addFreshEntity(s);
            parked = s;
            // a star reactor frame (a nether star: free power; its mind keeps it standing, looking about) 3 blocks behind the pilot
            PowerSuitEntity r = ModEntities.POWER_SUIT.get().create(p.level(), EntitySpawnReason.COMMAND);
            r.getInventory().setItem(PowerSuitEntity.ENGINE_SLOT, new ItemStack(ModItems.STAR_REACTOR.get()));
            r.getInventory().setItem(PowerSuitEntity.HELMET_SLOT, new ItemStack(ModItems.SUIT_HELMET.get()));
            r.getInventory().setItem(PowerSuitEntity.FUEL_SLOT, new ItemStack(Items.NETHER_STAR)); // the reactor's core
            r.snapTo(home.x + 3, home.y, home.z - 3, 0, 0);
            r.setYBodyRot(0);
            r.setYHeadRot(0);
            r.brain().setOwnerId(p.getUUID());
            p.level().addFreshEntity(r);
            reactor = r;
        });
        try {
            csv = Files.newBufferedWriter(FMLPaths.GAMEDIR.get().resolve("autopilot_frame.csv"));
            csv.write("tick,phase,bb_width,bb_height,eye_above_suit,walk_pos,walk_speed,speed,parked_powered,pilot_skin,tool,tool_running,rotor\n");
        } catch (IOException e) {
            PowerSuits.LOGGER.error("frame csv", e);
        }
    }

    /** Puts TOOLS[i] in the pilot's suit's socket (-1: empties it), on the server. */
    private static void socket(Minecraft mc, int i) {
        AutoPilot.onServer(mc, p -> {
            if (p.getVehicle() instanceof PowerSuitEntity suit) {
                suit.getInventory().setItem(PowerSuitEntity.SOCKET_SLOT, i < 0 ? ItemStack.EMPTY : new ItemStack(TOOLS.get(i).get()));
            }
        });
    }

    /** Puts the pilot's suit's helmet on or takes it off (on the server; the slot syncs). */
    private static void helmet(Minecraft mc, boolean on) {
        AutoPilot.onServer(mc, p -> {
            if (p.getVehicle() instanceof PowerSuitEntity suit) {
                suit.getInventory().setItem(PowerSuitEntity.HELMET_SLOT, on ? new ItemStack(ModItems.SUIT_HELMET.get()) : ItemStack.EMPTY);
            }
        });
    }

    /** A camera {@code ahead} blocks in front of a suit (negative: behind it) by the way its body faces now, a little to
     *  its side and above, looking at its chest (the client's copy: what is drawn). */
    private static void around(Minecraft mc, PowerSuitEntity suit, double ahead) {
        var c = mc.level.getEntity(suit.getId());
        if (!(c instanceof PowerSuitEntity drawn)) {
            return;
        }
        float yaw = drawn.yBodyRot * Mth.DEG_TO_RAD;
        Vec3 forward = new Vec3(-Mth.sin(yaw), 0, Mth.cos(yaw)), side = new Vec3(-forward.z, 0, forward.x);
        Vec3 at = drawn.position();
        camera(mc, at.add(forward.scale(ahead)).add(side.scale(0.8)).add(0, 1.9, 0), at.add(0, 1.4, 0));
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
            csv.write(String.format(Locale.ROOT, "%d,%s,%.3f,%.3f,%.3f,%.3f,%.3f,%.2f,%s,%s,%s,%s,%.1f%n", s, phase, suit.getBbWidth(), suit.getBbHeight(),
                    mc.player.getEyeY() - suit.getY(), suit.walkAnimation.position(), suit.walkAnimation.speed(),
                    suit.animator().getVisualSpeed(), parkedClient instanceof PowerSuitEntity c ? c.isPowered() : "-",
                    mc.player.getSkin().model().getSerializedName(), // slim = the frame's slim build
                    suit.getSocketStack().isEmpty() ? "-" : BuiltInRegistries.ITEM.getKey(suit.getSocketStack().getItem()).getPath(),
                    suit.socket().isRunning(), suit.socketVisuals().rotorAngle(1F)));
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
