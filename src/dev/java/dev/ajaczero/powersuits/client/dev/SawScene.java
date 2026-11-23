package dev.ajaczero.powersuits.client.dev;

import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.registry.ModItems;
import net.minecraft.client.CameraType;
import net.minecraft.client.Minecraft;
import net.minecraft.core.BlockPos;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.client.event.InputEvent;
import net.neoforged.neoforge.common.NeoForge;

/**
 * Fast autopilot showcase for the chainsaw: close-up 3P side/front3q/back, raised running on an oak trunk,
 * and 1P cockpit at rest and running ({@code ap_saw_*.png}). Runs alone with ./gradlew runAutopilotSaw (~20 s).
 */
final class SawScene {
    private static volatile Vec3 home;

    static boolean step(Minecraft mc, int s) {
        var o = mc.options;
        switch (s) {
            case 0 -> { AutoPilot.releaseAll(); AutoPilot.aimTarget = null; setup(mc); }
            case 8 -> {
                Vec3 at = home != null ? home : mc.player.getVehicle().position();
                camera(mc, at.add(-1.55, 1.0, 0.0), at.add(-0.5, 0.85, 0.0));
            }
            case 16 -> AutoPilot.shot(mc, "saw_3p_side");
            case 18 -> {
                Vec3 at = home != null ? home : mc.player.getVehicle().position();
                camera(mc, at.add(-1.35, 1.25, 1.35), at.add(-0.4, 0.9, 0.0));
            }
            case 26 -> AutoPilot.shot(mc, "saw_3p_front3q");
            case 28 -> {
                mc.setCameraEntity(mc.player);
                o.setCameraType(CameraType.THIRD_PERSON_BACK);
                DevUtil.hideGui(mc, false);
                AutoPilot.setView(0, 12);
            }
            case 36 -> AutoPilot.shot(mc, "saw_3p_back");
            case 38 -> {
                o.setCameraType(CameraType.FIRST_PERSON);
                DevUtil.hideGui(mc, false);
                AutoPilot.setView(0, 6);
            }
            case 48 -> AutoPilot.shot(mc, "saw_fp_rest");
            case 50 -> {
                AutoPilot.setView(0, 10);
                AutoPilot.hold(o.keyAttack, true);
                NeoForge.EVENT_BUS.post(new InputEvent.InteractionKeyMappingTriggered(0, o.keyAttack, InteractionHand.MAIN_HAND));
            }
            case 62 -> AutoPilot.shot(mc, "saw_fp_run_a");
            case 63 -> AutoPilot.shot(mc, "saw_fp_run_b");
            case 65 -> {
                Vec3 at = home != null ? home : mc.player.getVehicle().position();
                camera(mc, at.add(-1.85, 1.5, 1.85), at.add(-0.35, 1.35, 0.6));
            }
            case 74 -> AutoPilot.shot(mc, "saw_3p_raised_a");
            case 75 -> AutoPilot.shot(mc, "saw_3p_raised_b");
            case 77 -> {
                AutoPilot.hold(o.keyAttack, false);
                mc.setCameraEntity(mc.player);
                DevUtil.hideGui(mc, false);
                return false;
            }
            default -> {}
        }
        return true;
    }

    private static void setup(Minecraft mc) {
        AutoPilot.onServer(mc, p -> {
            DevUtil.setTime(p.level(), 6000);
            if (!(p.getVehicle() instanceof PowerSuitEntity suit)) {
                return;
            }
            home = suit.position();
            DevUtil.ironArmour(suit);
            suit.setYRot(0);
            suit.setYBodyRot(0);
            suit.setYHeadRot(0);
            p.setItemInHand(InteractionHand.OFF_HAND, ItemStack.EMPTY);
            p.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(ModItems.CHAINSAW.get()));
            // Oak log column 3 blocks ahead (+Z) for cutting shots (no leaves so it won't auto-fell on tick 1)
            BlockPos base = suit.blockPosition().offset(0, 0, 3);
            for (int y = 0; y < 5; y++) {
                p.level().setBlockAndUpdate(base.above(y), Blocks.OAK_LOG.defaultBlockState());
            }
        });
    }

    private static void camera(Minecraft mc, Vec3 from, Vec3 to) {
        mc.options.setCameraType(CameraType.FIRST_PERSON);
        DevUtil.hideGui(mc, true);
        Vec3 drop = new Vec3(0, EntityTypes.ARMOR_STAND.getDimensions().eyeHeight(), 0);
        AutoPilot.lookCamera(mc, from.subtract(drop), to.subtract(drop));
    }

    private SawScene() {}
}
