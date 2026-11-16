package dev.ajaczero.powersuits.client.dev;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.entity.SuitFace;
import dev.ajaczero.powersuits.entity.SuitMind;
import dev.ajaczero.powersuits.item.HelmetStyle;
import dev.ajaczero.powersuits.registry.ModDataComponents;
import dev.ajaczero.powersuits.registry.ModEntities;
import dev.ajaczero.powersuits.registry.ModItems;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Locale;
import net.minecraft.client.CameraType;
import net.minecraft.client.Minecraft;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.Mth;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.animal.cow.Cow;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.gamerules.GameRules;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.Vec3;
import net.neoforged.fml.loading.FMLPaths;

/**
 * Autopilot scene for the robot helmet's visor faces (entity/SuitFace, 2026-11-15): one robot-helmet suit (gold, a drill
 * in the socket, no AI: a statue) filmed close from the front while things happen to it, each face shot a few ticks
 * after its cause ({@code ap_robot_face_<phase>.png}): parked with nothing happening (dark), hit, a pilot climbing in
 * (amber from here), refuelled, the drill held (effort), the pilot punching a cow (a blow landed: the server's struck
 * event), the pilot out (green), lightning (knocked out: dizzy through the dead visor), the helmet broken, repaired, a
 * rogue (red), and the rogue at night. Log run/autopilot_robot_face.csv: the client's face each tick beside what it
 * reads (power, knock-out, pilot, the tool, the helmet, the mind, the hurt flash) and the visor's colour. Runs after
 * StyleScene in ./gradlew runAutopilotStyles.
 */
final class RobotFaceScene {
    /** Phase starts (ticks from the scene's start) and their shots' delays. */
    private static final int SETUP = 50, EACH = 30;
    private static final String[] PHASES = {"idle", "hit", "happy", "love", "effort", "angry", "out", "dizzy", "broken",
            "repaired", "rogue", "night"};
    /** Ticks after a phase's start its shot is taken (the face must have arrived and the camera settled). */
    private static final int[] SHOT_AT = {6, 12, 8, 6, 20, 8, 10, 40, 8, 6, 16, 12};   // (effort: after the refuel's
    // hearts; dizzy: after the bolt's flash)   // (hit: after the red flash)
    /** The lightning's knock-out runs a few seconds: the dizzy phase gets longer before the helmet breaks. */
    private static final int DIZZY_EXTRA = 180;   // (and its restart's stutter: the visor flickers a while)
    private static volatile BlockPos base;
    private static volatile PowerSuitEntity suit;
    private static volatile Cow cow;
    private static BufferedWriter csv;
    private static String phase = "setup";

    static boolean step(Minecraft mc, int s) {
        if (s == 0) {
            setup(mc);
            open();
        }
        if (s == SETUP - 10) {
            front(mc); // (not earlier: the suit is spawned on the server a tick or two after the setup)
        }
        int k = s - SETUP;
        if (k >= 0) {
            int i = phaseAt(k), t = k - startOf(i);
            if (i >= PHASES.length) {
                close();
                mc.setCameraEntity(mc.player);
                mc.options.setCameraType(CameraType.FIRST_PERSON);
                DevUtil.hideGui(mc, false);
                return false;
            }
            if (t == 0) {
                phase = PHASES[i];
                start(mc, PHASES[i]);
                front(mc); // (again: climbing in and out moves the player's camera back)
            }
            if (t == 3 || t == SHOT_AT[i] - 3) {
                front(mc); // (and once the client has caught up with the pilot getting in or out)
            }
            if (t == SHOT_AT[i]) {
                AutoPilot.shot(mc, "robot_face_" + PHASES[i]);
            }
            if (PHASES[i].equals("effort") && t == EACH - 2) {
                AutoPilot.onServer(mc, p -> { if (suit != null) suit.socket().setTriggerHeld(p, false); });
            }
        }
        if (s >= 2) {
            log(mc, s);
        }
        return true;
    }

    private static int startOf(int i) {
        int dizzy = indexOf("dizzy");
        return i * EACH + (i > dizzy ? DIZZY_EXTRA : 0);
    }

    private static int phaseAt(int k) {
        int i = 0;
        while (i < PHASES.length && k >= startOf(i + 1)) {
            i++;
        }
        return i;
    }

    private static int indexOf(String name) {
        for (int i = 0; i < PHASES.length; i++) {
            if (PHASES[i].equals(name)) {
                return i;
            }
        }
        return -1;
    }

    /** Flat ground 100 blocks east (StyleScene's row is 100 west), daytime; a gold robot suit facing north. */
    private static void setup(Minecraft mc) {
        AutoPilot.onServer(mc, player -> {
            ServerLevel level = player.level();
            DevUtil.setTime(level, 6000);
            player.stopRiding();
            player.setGameMode(GameType.SURVIVAL);
            player.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY); // (scripts that use a tool empty the hand)
            int x = player.getBlockX() + 100, z = player.getBlockZ();
            int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING, x, z);
            base = new BlockPos(x, y, z);
            // the player's own suits follow them (a friendly mind walks after its owner, and it would fight our rogue):
            // send them away first
            for (var e : level.getAllEntities()) {
                if (e instanceof PowerSuitEntity other && !other.isNoAi()) {
                    other.discard();
                }
            }
            player.teleportTo(x + 0.5, y, z + 3.5); // behind it, out of the front shots
            PowerSuitEntity s = ModEntities.POWER_SUIT.get().create(level, EntitySpawnReason.COMMAND);
            ItemStack helmet = new ItemStack(ModItems.SUIT_HELMET.get());
            helmet.set(ModDataComponents.HELMET_STYLE.get(), HelmetStyle.ROBOT);
            DevUtil.firebox(s);
            s.getInventory().setItem(PowerSuitEntity.FUEL_SLOT, new ItemStack(Items.BLAZE_ROD, 4));
            s.getInventory().setItem(PowerSuitEntity.HELMET_SLOT, helmet);
            s.getInventory().setItem(PowerSuitEntity.SOCKET_SLOT, new ItemStack(ModItems.DRILL.get()));
            DevUtil.ironArmour(s);
            s.snapTo(x + 0.5, y, z + 0.5, 180, 0);
            s.setYBodyRot(180);
            s.setYHeadRot(180);
            s.brain().setOwnerId(player.getUUID());
            s.setNoAi(true);
            level.addFreshEntity(s);
            suit = s;
        });
    }

    /** What each phase does to the suit (on the server). */
    private static void start(Minecraft mc, String name) {
        AutoPilot.onServer(mc, p -> {
            PowerSuitEntity s = suit;
            if (s == null) {
                return;
            }
            ServerLevel level = p.level();
            switch (name) {
                case "hit" -> s.hurtServer(level, s.damageSources().generic(), 1F);
                case "happy" -> {
                    p.snapTo(s.getX(), s.getY(), s.getZ(), 180, 0); // facing north as the suit does: it turns to its pilot
                    p.setYHeadRot(180);
                    p.startRiding(s, true, true); // (forced, as the other scenes do)
                }
                case "love" -> s.getInventory().setItem(PowerSuitEntity.FUEL_SLOT, new ItemStack(Items.BLAZE_ROD, 8));
                case "effort" -> s.socket().setTriggerHeld(p, true); // the drill spins in the air
                case "angry" -> punch(p, level, s);
                case "out" -> {
                    p.stopRiding();
                    p.teleportTo(s.getX(), s.getY(), s.getZ() + 3);
                    s.snapTo(s.getX(), s.getY(), s.getZ(), 180, 0);
                    s.setYBodyRot(180);
                    s.setYHeadRot(180);
                    if (cow != null) {
                        cow.discard();
                    }
                }
                case "dizzy" -> {
                    level.getGameRules().set(GameRules.FIRE_SPREAD_RADIUS_AROUND_PLAYER, 0, level.getServer());
                    var bolt = EntityTypes.LIGHTNING_BOLT.create(level, EntitySpawnReason.COMMAND);
                    bolt.snapTo(s.position());
                    level.addFreshEntity(bolt);
                }
                case "broken" -> {
                    s.clearFire();
                    ItemStack helmet = s.getInventory().getItem(PowerSuitEntity.HELMET_SLOT);
                    helmet.setDamageValue(helmet.getMaxDamage()); // worn out: it stays on, broken
                    s.getInventory().setChanged();
                }
                case "repaired" -> {
                    s.getInventory().getItem(PowerSuitEntity.HELMET_SLOT).setDamageValue(0);
                    s.getInventory().setChanged();
                }
                case "rogue" -> s.setMind(SuitMind.ROGUE);
                case "night" -> DevUtil.setTime(level, 18000);
                default -> {}
            }
        });
    }

    /** The pilot hits a cow standing beside the suit, as their own punch from inside (SuitBlows: the suit's). A cow:
     *  the autopilot's world is peaceful, a zombie would vanish. */
    private static void punch(ServerPlayer pilot, ServerLevel level, PowerSuitEntity s) {
        Cow c = EntityTypes.COW.create(level, EntitySpawnReason.COMMAND);
        if (c == null) {
            return;
        }
        c.snapTo(s.getX() + 2.5, s.getY(), s.getZ() - 1, 0, 0);
        c.setNoAi(true);
        level.addFreshEntity(c);
        cow = c;
        c.hurtServer(level, pilot.damageSources().playerAttack(pilot), 2F);
    }

    /** Close in front of the helmet, a little to the side (its visor wraps round), wherever the helmet faces (the
     *  client's head yaw: with a pilot in, the suit looks where the pilot looks). */
    private static void front(Minecraft mc) {
        PowerSuitEntity server = suit;
        if (server == null || mc.level == null || !(mc.level.getEntity(server.getId()) instanceof PowerSuitEntity c)) {
            return;
        }
        mc.options.setCameraType(CameraType.FIRST_PERSON);
        DevUtil.hideGui(mc, true);
        float yaw = c.getYHeadRot() * Mth.DEG_TO_RAD;
        Vec3 forward = new Vec3(-Mth.sin(yaw), 0, Mth.cos(yaw)), right = new Vec3(-forward.z, 0, forward.x);
        Vec3 drop = new Vec3(0, EntityTypes.ARMOR_STAND.getDimensions().eyeHeight(), 0);
        // the helmet is 1.72-2.28 blocks up (raw 25.5-34.5 px + the 2 px soles)
        Vec3 from = c.position().add(forward.scale(1.7)).add(right.scale(0.45)).add(0, 2.15, 0);
        AutoPilot.lookCamera(mc, from.subtract(drop), c.position().add(0, 1.98, 0).subtract(drop));
    }

    private static void open() {
        try {
            csv = Files.newBufferedWriter(FMLPaths.GAMEDIR.get().resolve("autopilot_robot_face.csv"));
            csv.write("tick,phase,face,visor_rgb,visor_level,powered,knocked_out,piloted,tool_active,helmet_broken,mind,hurt_time,suit_yaw,body_yaw,pilot_yaw\n");
        } catch (IOException e) {
            PowerSuits.LOGGER.error("robot face csv", e);
        }
    }

    /** The client's copy of the suit: what its visor shows and what the face read. */
    private static void log(Minecraft mc, int s) {
        BufferedWriter w = csv;
        PowerSuitEntity server = suit;
        if (w == null || server == null || mc.level == null || !(mc.level.getEntity(server.getId()) instanceof PowerSuitEntity c)) {
            return;
        }
        SuitFace.Face face = c.lights().face().shown();
        float[] v = c.lights().getVisorColor();
        try {
            w.write(String.format(Locale.ROOT, "%d,%s,%s,%.2f %.2f %.2f,%.2f,%b,%b,%b,%b,%b,%s,%d,%.0f,%.0f,%.0f%n", s, phase,
                    face == null ? "none" : face.id(), v[0], v[1], v[2], c.lights().getVisorFlicker(c.tickCount), c.isPowered(), c.isStunned(), c.isVehicle(),
                    c.socket().isActive(), c.isHelmetBroken(), c.getMind().name(), c.hurtTime, c.getYRot(), c.yBodyRot, mc.player.getYRot()));
        } catch (IOException ignored) {
            // closed at the scene's end
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

    private RobotFaceScene() {}
}
