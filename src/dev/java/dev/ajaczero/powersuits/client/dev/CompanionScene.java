package dev.ajaczero.powersuits.client.dev;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.entity.SoulEvent;
import dev.ajaczero.powersuits.registry.ModEntities;
import dev.ajaczero.powersuits.registry.ModItems;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.CopyOnWriteArrayList;
import net.minecraft.client.CameraType;
import net.minecraft.client.Minecraft;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.Vec3;

/**
 * Autopilot scene for the companion's two routes (companion design, 2026-11-16), run at the end of the mech scene
 * (AutoPilot.mechanics) in place of the old workers' scene. Four phases, each a suit with a soul helmet and a husk that
 * stands still (no AI) in front of it, filmed from a side view:
 * <ul>
 *   <li>chainsaw (follow route): the owner stands by; the suit runs at the husk and shreds it;</li>
 *   <li>drill (guard route): the suit keeps to home and grinds the husk that comes within its radius;</li>
 *   <li>flamethrower (follow) and TNT launcher (guard): carried, never fired: they punch the husk.</li>
 * </ul>
 * Logs run/autopilot_companion.csv (husk health, the suit's goals, the tool's uses, fire blocks seen).
 */
final class CompanionScene {
    private static final String[] PHASES = {"saw", "drill", "flame", "tnt", "voice"};
    private static final int PHASE_TICKS = 170;
    private static volatile BlockPos base;
    private static final List<PowerSuitEntity> suits = new CopyOnWriteArrayList<>();
    private static final List<LivingEntity> husks = new CopyOnWriteArrayList<>();
    private static BufferedWriter csv;
    private static boolean fire;

    /** Scene step {@code s} (ticks since it started). Returns false once it's over. */
    static boolean step(Minecraft mc, int s) {
        int phase = s / PHASE_TICKS, at = s % PHASE_TICKS;
        if (phase >= PHASES.length) {
            close();
            return false;
        }
        if (phase == 4) { // the souls' chat: four suits, one soul each, the GUI up so the chat shows
            switch (at) {
                case 0 -> voiceSetup(mc);
                case 6 -> { mc.options.setCameraType(CameraType.THIRD_PERSON_BACK); DevUtil.hideGui(mc, false); }
                case 20 -> AutoPilot.onServer(mc, p -> speak(SoulEvent.FIRST_WORDS));
                case 60 -> { AutoPilot.shot(mc, "companion_voice_first"); AutoPilot.onServer(mc, p -> speak(SoulEvent.HELMET_BROKEN)); }
                case 100 -> { AutoPilot.shot(mc, "companion_voice_broken"); AutoPilot.onServer(mc, p -> speak(SoulEvent.OWNER_DIED)); }
                case 140 -> AutoPilot.shot(mc, "companion_voice_died");
                default -> {}
            }
            return true;
        }
        switch (at) {
            case 0 -> { setup(mc, phase); if (phase == 0) { open(mc); } }
            case 6 -> camera(mc, new Vec3(-9, 4, 3), new Vec3(0, 1.5, 4));
            case 40, 80, 120, 160 -> AutoPilot.shot(mc, "companion_" + PHASES[phase] + "_" + at);
            default -> {}
        }
        if (s >= 5) {
            log(mc, s, phase);
        }
        return true;
    }

    /** Server: flat ground 60 blocks east (by day, normal difficulty: the husks are statues, but a monster is a monster).
     *  The suit (soul helmet, fuel, the phase's tool, home here, the player as owner) and a husk 6 blocks in front. */
    private static void setup(Minecraft mc, int phase) {
        AutoPilot.onServer(mc, player -> {
            ServerLevel level = player.level();
            DevUtil.setTime(level, 6000);
            player.setGameMode(GameType.CREATIVE);
            player.getInventory().clearContent();
            for (PowerSuitEntity old : suits) {
                old.discard();
            }
            for (LivingEntity old : husks) {
                old.discard();
            }
            suits.clear();
            husks.clear();
            int x = player.getBlockX() + 60, z = player.getBlockZ() + 20 * phase;
            int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING, x, z);
            BlockPos home = new BlockPos(x, y, z);
            base = home;
            Item tool = switch (phase) {
                case 0 -> ModItems.CHAINSAW.get();
                case 1 -> ModItems.DRILL.get();
                case 2 -> ModItems.FLAMETHROWER.get();
                default -> ModItems.TNT_LAUNCHER.get();
            };
            PowerSuitEntity s = ModEntities.POWER_SUIT.get().create(level, EntitySpawnReason.COMMAND);
            DevUtil.firebox(s);
            s.getInventory().setItem(PowerSuitEntity.FUEL_SLOT, new ItemStack(Items.BLAZE_ROD, 16));
            s.getInventory().setItem(PowerSuitEntity.HELMET_SLOT, DevUtil.soulHelmet(level));
            DevUtil.ironArmour(s);
            s.getInventory().setItem(PowerSuitEntity.SOCKET_SLOT, new ItemStack(tool));
            s.snapTo(x + 0.5, y, z + 0.5, 0, 0);
            s.brain().setOwnerId(player.getUUID());
            s.brain().setHome(home);
            level.addFreshEntity(s);
            var husk = EntityTypes.HUSK.create(level, EntitySpawnReason.COMMAND);
            husk.setNoAi(true);
            husk.snapTo(x + 0.5, y, z + 6.5, 180, 0);
            level.addFreshEntity(husk);
            suits.add(s);
            husks.add(husk);
            player.teleportTo(x - 4.5, y, z - 2.5); // the owner, out of the picture
            fire = false;
        });
    }

    /** Server: four suits in a row east of the scene, each wearing a different soul, the player their owner beside them. */
    private static void voiceSetup(Minecraft mc) {
        AutoPilot.onServer(mc, player -> {
            ServerLevel level = player.level();
            DevUtil.setTime(level, 6000);
            player.setGameMode(GameType.CREATIVE);
            for (PowerSuitEntity old : suits) {
                old.discard();
            }
            for (LivingEntity old : husks) {
                old.discard();
            }
            suits.clear();
            husks.clear();
            int x = player.getBlockX() + 60, z = player.getBlockZ() + 100;
            int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING, x, z);
            String[] souls = {"veteran", "optimist", "butler", "nervous"};
            for (int i = 0; i < souls.length; i++) {
                PowerSuitEntity s = ModEntities.POWER_SUIT.get().create(level, EntitySpawnReason.COMMAND);
                DevUtil.firebox(s);
                s.getInventory().setItem(PowerSuitEntity.FUEL_SLOT, new ItemStack(Items.BLAZE_ROD, 16));
                s.getInventory().setItem(PowerSuitEntity.HELMET_SLOT, DevUtil.soulHelmet(level, souls[i]));
                DevUtil.ironArmour(s);
                s.snapTo(x + 0.5 + 3 * i, y, z + 0.5, 180, 0);
                s.brain().setOwnerId(player.getUUID());
                level.addFreshEntity(s);
                suits.add(s);
            }
            player.teleportTo(x + 5, y, z - 4);
        });
    }

    private static void speak(SoulEvent event) {
        for (PowerSuitEntity s : suits) {
            s.voice().on(event);
        }
    }

    private static void camera(Minecraft mc, Vec3 from, Vec3 at) {
        BlockPos b = base;
        if (b == null) {
            return;
        }
        mc.options.setCameraType(CameraType.FIRST_PERSON);
        DevUtil.hideGui(mc, true);
        Vec3 drop = new Vec3(0, EntityTypes.ARMOR_STAND.getDimensions().eyeHeight(), 0); // lookCamera places the stand's feet
        AutoPilot.lookCamera(mc, Vec3.atBottomCenterOf(b).add(from).subtract(drop), Vec3.atBottomCenterOf(b).add(at).subtract(drop));
    }

    private static void open(Minecraft mc) {
        try {
            csv = Files.newBufferedWriter(mc.gameDirectory.toPath().resolve("autopilot_companion.csv"));
            csv.write("tick,phase,suitDz,goals,target,uses,huskHealth,huskAlive,fireSeen,energy,companion\n");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static void log(Minecraft mc, int s, int phase) {
        PowerSuitEntity suit = suits.isEmpty() ? null : suits.get(0);
        LivingEntity husk = husks.isEmpty() ? null : husks.get(0);
        BlockPos b = base;
        var player = mc.getSingleplayerServer() == null ? null : mc.getSingleplayerServer().getPlayerList().getPlayer(mc.player.getUUID());
        if (csv == null || suit == null || husk == null || b == null || player == null) {
            return;
        }
        ServerLevel level = player.level();
        for (BlockPos p : BlockPos.betweenClosed(b.offset(-4, 0, -2), b.offset(4, 3, 9))) {
            fire |= level.getBlockState(p).is(BlockTags.FIRE);
        }
        try {
            csv.write(String.format(Locale.ROOT, "%d,%s,%.2f,%s,%s,%d,%.1f,%b,%b,%d,%b%n", s, PHASES[phase], suit.getZ() - b.getZ() - 0.5,
                    suit.brain().runningGoalNames(), suit.getTarget() == null ? "-" : suit.getTarget().getType().toShortString(),
                    suit.socket().getUses(), husk.getHealth(), husk.isAlive(), fire, suit.power().getTotalEnergy(), suit.isCompanion()));
        } catch (IOException e) {
            PowerSuits.LOGGER.error("[autopilot] companion csv", e);
        }
    }

    private static void close() {
        try {
            if (csv != null) {
                csv.close();
            }
        } catch (IOException ignored) {
        }
    }

    private CompanionScene() {}
}
