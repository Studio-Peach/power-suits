package dev.ajaczero.powersuits.client.dev;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.client.PowerSuitScreen;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.menu.PowerSuitMenu;
import dev.ajaczero.powersuits.registry.ModEntities;
import dev.ajaczero.powersuits.registry.ModItems;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Locale;
import com.mojang.blaze3d.platform.InputConstants;
import net.minecraft.client.CameraType;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.protocol.game.ServerboundPlayerActionPacket;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.ContainerInput;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.levelgen.Heightmap;
import net.neoforged.fml.loading.FMLPaths;

/**
 * Autopilot scene for the suit's inventory screen (user, 2026-10-27): the player's inventory with the suit in it.
 * A survival pilot sits in a fuelled suit with the chaingun in its socket, a drill and a chainsaw on the hotbar and
 * ammo and coal in the inventory.
 * <ol>
 *   <li>The inventory key from inside (what vanilla does for E when the vehicle has its own screen:
 *   {@code sendOpenInventory}): the suit's menu (vanilla's inventory screen with the suit in it: the armour round the
 *   preview, the socket in the off-hand slot, fuel -> Power), no Pack up, and beside it the status panels (Hull, Fuel,
 *   Sealed) over the pilot's own Speed effect ({@code ap_menu_inside}).</li>
 *   <li>The right leg's piece shift-clicked off: no Sealed panel ({@code ap_menu_unsealed}); the mouse over its empty
 *   slot ({@code ap_menu_hover_leg}); shift-clicked back on.</li>
 *   <li>F over the drill on the hotbar: the drill goes into the socket, the chaingun comes out ({@code ap_menu_swapped}).</li>
 *   <li>The Power key: switched off, it pops out ({@code ap_menu_off}); closed, the visor is completely
 *   dark, nothing on the glass ({@code ap_menu_hud_off}).</li>
 *   <li>The power switch key (H): on again, the visor warms up ({@code ap_menu_hud_on}).</li>
 *   <li>F outside the screen with the chainsaw selected: the chainsaw goes into the socket ({@code ap_menu_f_back},
 *   the in-game back view).</li>
 *   <li>Out of the suit, sneak + right-click: the same screen from outside, with Pack up ({@code ap_menu_outside}).</li>
 *   <li>Still open, the fuel taken out: the Fuel panel reads No fuel, red ({@code ap_menu_no_fuel}); the engine taken
 *   out: No engine ({@code ap_menu_no_engine}). The menu is the only place that says why a suit is dark (SuitHud draws nothing).</li>
 *   <li>The mouse over the keys: Power ({@code ap_menu_hover_power}), Pack up from outside ({@code ap_menu_hover_pack})
 *   and, at the start, greyed out from inside ({@code ap_menu_hover_pack_inside}).</li>
 * </ol>
 * Log run/autopilot_menu.csv: per tick the screen open on the client, the server's and the client's socket tool, the
 * switch and power on both sides, the pilot's hand, whether vanilla treats the inventory key as the vehicle's, and the
 * client's armour pieces and seal.
 * Runs alone with ./gradlew runAutopilotMenu (~26 s) and at the end of runAutopilotMech.
 */
final class MenuScene {
    private static volatile BlockPos base;
    private static volatile PowerSuitEntity suit;
    private static BufferedWriter csv;
    private static String phase = "-";

    static boolean step(Minecraft mc, int s) {
        switch (s) {
            case 0 -> { setup(mc); open(); }
            case 40 -> { phase = "inside"; mc.options.setCameraType(CameraType.FIRST_PERSON); DevUtil.hideGui(mc, false);
                         // what Minecraft.handleKeybinds does for the inventory key
                         if (mc.gameMode.isServerControlledInventory()) {
                             mc.player.sendOpenInventory();
                         } }
            case 50 -> AutoPilot.shot(mc, "menu_inside");
            // the mouse over the Pack up key from inside: greyed out, its name as the tooltip
            case 51 -> pointAt(mc, PowerSuitScreen.PACK_X + 9, PowerSuitScreen.PACK_Y + 9);
            case 53 -> AutoPilot.shot(mc, "menu_hover_pack_inside");
            // The armour (frame step 6b): the right leg's piece shift-clicked off: the Sealed panel goes; the mouse over its
            // empty slot (the leggings outline, its hint); the piece shift-clicked back on.
            case 54 -> { phase = "armour_off"; pointAt(mc, -100, -100); click(mc, PowerSuitMenu.MENU_ARMOUR + 4, 0, ContainerInput.QUICK_MOVE); }
            case 64 -> AutoPilot.shot(mc, "menu_unsealed");
            case 65 -> pointAt(mc, PowerSuitMenu.LEFT_X + 8, PowerSuitMenu.ROW_Y + 2 * PowerSuitMenu.ROW + 8);
            case 67 -> AutoPilot.shot(mc, "menu_hover_leg");
            case 68 -> { phase = "armour_on"; pointAt(mc, -100, -100);
                         if (mc.player.containerMenu instanceof PowerSuitMenu m) {
                             for (int i = PowerSuitMenu.INV_START; i < PowerSuitMenu.END; i++) {
                                 if (m.getSlot(i).getItem().is(ModItems.IRON_LEG_ARMOUR.get())) {
                                     click(mc, i, 0, ContainerInput.QUICK_MOVE);
                                     break;
                                 }
                             }
                         } }
            // F over the drill (hotbar slot 1): the screen's own swap-hands click
            case 84 -> { phase = "swap"; pointAt(mc, -100, -100); click(mc, PowerSuitMenu.HOTBAR_START + 1, Inventory.SLOT_OFFHAND, ContainerInput.SWAP); }
            case 90 -> AutoPilot.shot(mc, "menu_swapped");
            case 94 -> { phase = "off"; if (mc.player.containerMenu instanceof PowerSuitMenu m) {
                             mc.gameMode.handleInventoryButtonClick(m.containerId, PowerSuitMenu.BUTTON_POWER);
                         } }
            case 104 -> AutoPilot.shot(mc, "menu_off");
            case 108 -> mc.player.closeContainer();
            case 140 -> AutoPilot.shot(mc, "menu_hud_off");
            // the power switch key: a press of H, through the key binding itself (SuitKeys sends the message)
            case 144 -> { phase = "on"; KeyMapping.click(InputConstants.Type.KEYBOARD.getOrCreate(InputConstants.KEY_H)); }
            case 190 -> AutoPilot.shot(mc, "menu_hud_on");
            // F outside the screen, the chainsaw selected: vanilla's swap packet, which the suit takes over (PilotHands)
            case 194 -> { phase = "f_key"; mc.player.getInventory().setSelectedSlot(2); // (the client tells the server next tick)
                          AutoPilot.onServer(mc, p -> p.getInventory().setSelectedSlot(2)); }
            case 196 -> { mc.getConnection().send(new ServerboundPlayerActionPacket(ServerboundPlayerActionPacket.Action.SWAP_ITEM_WITH_OFFHAND,
                                  BlockPos.ZERO, Direction.DOWN)); }
            case 200 -> { mc.options.setCameraType(CameraType.THIRD_PERSON_BACK); DevUtil.hideGui(mc, true); }
            case 210 -> AutoPilot.shot(mc, "menu_f_back");
            // out of the suit: sneak + right-click opens the same screen, with Pack up
            case 214 -> { phase = "outside"; mc.options.setCameraType(CameraType.FIRST_PERSON); DevUtil.hideGui(mc, false);
                          AutoPilot.onServer(mc, p -> {
                              PowerSuitEntity x = suit;
                              if (x == null) {
                                  return;
                              }
                              p.stopRiding();
                              p.teleportTo(x.getX() - 2, x.getY(), x.getZ() - 2);
                              p.setShiftKeyDown(true);
                              x.interact(p, InteractionHand.MAIN_HAND, x.position());
                              p.setShiftKeyDown(false);
                          }); }
            case 226 -> AutoPilot.shot(mc, "menu_outside");
            // the menu is the only place that says why a suit is dark (the visor shows nothing): out of fuel, then no engine
            case 230 -> { phase = "no_fuel"; AutoPilot.onServer(mc, p -> {
                              PowerSuitEntity x = suit;
                              if (x != null) {
                                  x.getInventory().setItem(PowerSuitEntity.FUEL_SLOT, ItemStack.EMPTY);
                                  x.power().setBurn(0, 0);
                              }
                          }); }
            case 240 -> AutoPilot.shot(mc, "menu_no_fuel");
            case 244 -> { phase = "no_engine"; AutoPilot.onServer(mc, p -> {
                              PowerSuitEntity x = suit;
                              if (x != null) {
                                  x.getInventory().setItem(PowerSuitEntity.ENGINE_SLOT, ItemStack.EMPTY);
                              }
                          }); }
            case 254 -> AutoPilot.shot(mc, "menu_no_engine");
            // the keys under the mouse: highlighted, with their tooltips (Power names its state)
            case 255 -> pointAt(mc, PowerSuitScreen.POWER_X + 9, PowerSuitScreen.POWER_Y + 9);
            case 257 -> AutoPilot.shot(mc, "menu_hover_power");
            case 259 -> pointAt(mc, PowerSuitScreen.PACK_X + 9, PowerSuitScreen.PACK_Y + 9);
            case 261 -> AutoPilot.shot(mc, "menu_hover_pack");
            // Robot companion menu (A2, 2026-11-22): put a souled Robot Helmet on, stock ammo/spare fuel in its pack, reopen
            case 264 -> { phase = "robot"; pointAt(mc, -100, -100); mc.player.closeContainer();
                          AutoPilot.onServer(mc, p -> {
                              PowerSuitEntity x = suit;
                              if (x == null) {
                                  return;
                              }
                              DevUtil.firebox(x);
                              x.getInventory().setItem(PowerSuitEntity.FUEL_SLOT, new ItemStack(Items.COAL, 16));
                              x.getInventory().setItem(PowerSuitEntity.HELMET_SLOT, DevUtil.soulHelmet(x.level()));
                              x.getInventory().setItem(PowerSuitEntity.PACK_START, new ItemStack(Items.FIRE_CHARGE, 48));
                              x.getInventory().setItem(PowerSuitEntity.PACK_START + 1, new ItemStack(Items.AMETHYST_SHARD, 16));
                              x.getInventory().setItem(PowerSuitEntity.PACK_START + 2, new ItemStack(Items.COAL, 32));
                              x.getInventory().setItem(PowerSuitEntity.PACK_START + 4, new ItemStack(Items.IRON_INGOT, 12));
                              p.setShiftKeyDown(true);
                              x.interact(p, InteractionHand.MAIN_HAND, x.position());
                              p.setShiftKeyDown(false);
                          }); }
            case 276 -> AutoPilot.shot(mc, "menu_robot");
            case 277 -> pointAt(mc, PowerSuitMenu.PACK_X + 3 * 18 + 8, PowerSuitMenu.PACK_Y + 18 + 8);
            case 279 -> AutoPilot.shot(mc, "menu_robot_hover");
            case 282 -> { pointAt(mc, -100, -100); mc.player.closeContainer(); close(); return false; }
            default -> {}
        }
        if (s >= 2) {
            log(mc, s);
        }
        return true;
    }

    /** Move the mouse to (x, y) in the menu's background (GUI pixels from its top-left corner): what GLFW's cursor
     *  callback would tell the mouse handler (window coordinates), twice, as the first move after a screen opens only
     *  sets the position. */
    private static void pointAt(Minecraft mc, int x, int y) {
        var window = mc.getWindow();
        int left = (window.getGuiScaledWidth() - 176) / 2, top = (window.getGuiScaledHeight() - 166) / 2;
        double sx = (left + x + 0.5) * window.getScreenWidth() / window.getGuiScaledWidth();
        double sy = (top + y + 0.5) * window.getScreenHeight() / window.getGuiScaledHeight();
        mc.mouseHandler.onMove(window.handle(), sx, sy, 0, 0);
        mc.mouseHandler.onMove(window.handle(), sx, sy, 0, 0);
    }

    private static void click(Minecraft mc, int slot, int button, ContainerInput input) {
        if (mc.player.containerMenu instanceof PowerSuitMenu m) {
            mc.gameMode.handleContainerInput(m.containerId, slot, button, input, mc.player);
        }
    }

    /** Flat ground 140 blocks east by day; the suit (firebox, coal, helmet, chaingun) with a survival pilot carrying a
     *  drill and a chainsaw on the hotbar (slot 0, the selected one, empty) and nuggets and coal in the inventory. */
    private static void setup(Minecraft mc) {
        AutoPilot.onServer(mc, player -> {
            ServerLevel level = player.level();
            DevUtil.setTime(level, 6000);
            player.stopRiding();
            int x = player.getBlockX() + 140, z = player.getBlockZ();
            int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING, x, z);
            base = new BlockPos(x, y, z);
            PowerSuitEntity s = ModEntities.POWER_SUIT.get().create(level, EntitySpawnReason.COMMAND);
            DevUtil.firebox(s);
            s.getInventory().setItem(PowerSuitEntity.FUEL_SLOT, new ItemStack(Items.COAL, 16));
            s.getInventory().setItem(PowerSuitEntity.HELMET_SLOT, new ItemStack(ModItems.SUIT_HELMET.get())); DevUtil.ironArmour(s);
            s.getInventory().setItem(PowerSuitEntity.SOCKET_SLOT, new ItemStack(ModItems.CHAINGUN.get()));
            s.snapTo(x + 0.5, y, z + 0.5, 0, 0);
            s.setYBodyRot(0);
            s.setYHeadRot(0);
            s.brain().setOwnerId(player.getUUID());
            level.addFreshEntity(s);
            suit = s;
            player.setGameMode(GameType.SURVIVAL);
            Inventory inv = player.getInventory();
            inv.clearContent();
            inv.setSelectedSlot(0);
            player.setItemInHand(InteractionHand.OFF_HAND, new ItemStack(ModItems.CHAINGUN.get()));
            inv.setItem(1, new ItemStack(ModItems.DRILL.get()));
            inv.setItem(2, new ItemStack(ModItems.CHAINSAW.get()));
            inv.setItem(9, new ItemStack(Items.FIRE_CHARGE, 64));
            inv.setItem(10, new ItemStack(Items.TNT, 12));
            inv.setItem(11, new ItemStack(Items.COAL, 32));
            player.addEffect(new MobEffectInstance(MobEffects.SPEED, 20 * 600)); // listed under the suit's status panels
            player.setShiftKeyDown(false);
            player.teleportTo(x + 0.5, y, z - 1.5);
            player.startRiding(s, true, true);
        });
    }

    private static void open() {
        try {
            csv = Files.newBufferedWriter(FMLPaths.GAMEDIR.get().resolve("autopilot_menu.csv"));
            csv.write("tick,phase,screen,vehicle_inventory,server_socket,client_socket,server_on,client_on,server_powered,client_powered,hand,client_armour,client_sealed\n");
        } catch (IOException e) {
            PowerSuits.LOGGER.error("menu csv", e);
        }
    }

    private static void log(Minecraft mc, int s) {
        PowerSuitEntity x = suit;
        BufferedWriter w = csv;
        if (x == null || w == null) {
            return;
        }
        String p = phase;
        PowerSuitEntity client = mc.level == null ? null : mc.level.getEntity(x.getId()) instanceof PowerSuitEntity c ? c : null;
        var open = mc.gui.screen();
        String screen = open == null ? "-" : open instanceof PowerSuitScreen ? "suit" : open.getClass().getSimpleName();
        boolean vehicleInventory = mc.gameMode.isServerControlledInventory();
        String clientSocket = client == null ? "?" : id(client.getSocketStack());
        boolean clientOn = client != null && client.power().isSwitchedOn();
        boolean clientPowered = client != null && client.isPowered();
        int armour = client == null ? -1 : client.armour().pieces();
        boolean sealed = client != null && client.isSealed();
        AutoPilot.onServer(mc, player -> {
            try {
                w.write(String.format(Locale.ROOT, "%d,%s,%s,%b,%s,%s,%b,%b,%b,%b,%s,%d,%b%n", s, p, screen, vehicleInventory,
                        id(x.getSocketStack()), clientSocket, x.power().isSwitchedOn(), clientOn,
                        x.isPowered(), clientPowered, id(player.getMainHandItem()), armour, sealed));
            } catch (IOException ignored) {
                // closed at the end of the scene
            }
        });
    }

    private static String id(ItemStack stack) {
        return stack.isEmpty() ? "-" : BuiltInRegistries.ITEM.getKey(stack.getItem()).getPath();
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
}
