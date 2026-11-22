package dev.ajaczero.powersuits.client;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.entity.ToolArm;
import dev.ajaczero.powersuits.item.PowerTool;
import dev.ajaczero.powersuits.network.ToolTriggerPayload;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.world.InteractionHand;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.InputEvent;
import net.neoforged.neoforge.client.network.ClientPacketDistributor;

/**
 * While piloting, a power tool replaces the hand on its arm (2026-11-15: the hands are detachable, either arm can carry
 * one), and works from the button of the hand it replaced, like vanilla's two hands:
 * <ul>
 * <li>the RIGHT arm is the main hand: its tool is the attack button (left click: the fist no longer punches or mines);
 * the main hand's items stay unused;</li>
 * <li>the LEFT arm is the off hand: its tool is the use button (right click), exactly as the socket tool always was: vanilla's
 * {@code startUseItem} tries the main hand, then the off hand, NeoForge fires InteractionKeyMappingTriggered before each,
 * and reaching the off hand means the main hand passed.</li>
 * </ul>
 * An arm without a tool is a plain hand: its items work as in vanilla. Each press is sent to the server (which tool, down
 * or up) and the tool runs for as long as the button is held.
 */
@EventBusSubscriber(modid = PowerSuits.MODID, value = Dist.CLIENT)
public final class ToolInput {
    /** The current press of each arm's button went to its tool, and whether the server was told. */
    private static final boolean[] HELD = new boolean[2], SENT = new boolean[2];

    private static boolean hasTool(PowerSuitEntity suit, ToolArm arm) {
        return suit.getSocketStack(arm).getItem() instanceof PowerTool;
    }

    @SubscribeEvent
    public static void button(InputEvent.InteractionKeyMappingTriggered event) {
        Minecraft mc = Minecraft.getInstance();
        if (mc.player == null || !(mc.player.getVehicle() instanceof PowerSuitEntity suit)) {
            return;
        }
        if (event.isAttack()) {
            if (hasTool(suit, ToolArm.RIGHT)) {
                HELD[ToolArm.RIGHT.ordinal()] = true; // the main hand is a tool: left click is its button
                event.setCanceled(true);
                event.setSwingHand(false);
            }
            return;
        }
        if (!event.isUseItem()) {
            return;
        }
        boolean main = event.getHand() == InteractionHand.MAIN_HAND;
        if (main && hasTool(suit, ToolArm.RIGHT)) {
            if (hasTool(suit, ToolArm.LEFT)) {
                // Dual-wielding two tools: right-click always goes straight to the off-hand tool.
                HELD[ToolArm.LEFT.ordinal()] = true;
                event.setCanceled(true);
                event.setSwingHand(false);
            }
            // Otherwise (only main hand holds a power tool): don't cancel so doors, chests and off-hand items (shield/torch) work.
            return;
        }
        if (!main && hasTool(suit, ToolArm.LEFT)) {
            HELD[ToolArm.LEFT.ordinal()] = true;      // the main hand passed: the tool takes this press
        }
        if (HELD[ToolArm.LEFT.ordinal()]) {
            // Also swallows vanilla's repeats (every 4 ticks while held), so a drill doesn't start placing the blocks
            // in your hand when the crosshair moves onto a block face.
            event.setCanceled(true);
            event.setSwingHand(false);
        }
    }

    /** Release, and send a message only when a tool's state changes (not every tick). */
    @SubscribeEvent
    public static void trigger(ClientTickEvent.Post event) {
        Minecraft mc = Minecraft.getInstance();
        boolean piloting = mc.player != null && mc.player.getVehicle() instanceof PowerSuitEntity;
        for (ToolArm arm : ToolArm.values()) {
            KeyMapping key = arm == ToolArm.LEFT ? mc.options.keyUse : mc.options.keyAttack;
            int i = arm.ordinal();
            if (!piloting || mc.gui.screen() != null || !key.isDown()) {
                HELD[i] = false;
            }
            if (HELD[i] != SENT[i] && mc.getConnection() != null) {
                SENT[i] = HELD[i];
                ClientPacketDistributor.sendToServer(new ToolTriggerPayload(HELD[i], arm));
            }
        }
    }

    private ToolInput() {}
}
