package dev.ajaczero.powersuits.client.dev;

import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.entity.SuitArmour;
import dev.ajaczero.powersuits.registry.ModItems;
import net.minecraft.client.Minecraft;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;

/** Small helpers the dev scripts share (things 1.21.1 had as plain fields). */
final class DevUtil {
    /** F1: hide or show the HUD (the hand pass, i.e. the cockpit viewmodel, is skipped too while hidden). */
    static void hideGui(Minecraft mc, boolean hidden) {
        if (mc.gui.hud.isHidden() != hidden) {
            mc.gui.hud.toggle();
        }
    }

    /** /time set: since 26.1 the time of day is the dimension's default clock. */
    static void setTime(ServerLevel level, long ticks) {
        level.dimensionType().defaultClock().ifPresent(clock -> level.clockManager().setTotalTicks(clock, ticks));
    }

    /** Suits come without an engine: give a scene's suit a firebox (if it has no engine yet) before fuelling it. */
    static void firebox(PowerSuitEntity suit) {
        if (suit.getInventory().getItem(PowerSuitEntity.ENGINE_SLOT).isEmpty()) {
            suit.getInventory().setItem(PowerSuitEntity.ENGINE_SLOT,
                    new ItemStack(ModItems.FIREBOX.get()));
        }
    }

    /** The frame's iron armour on all five parts (2026-11-14): with the helmet it seals the suit (fire, poison, air under
     *  water), as a suit in use is. */
    static void ironArmour(PowerSuitEntity suit) {
        for (SuitArmour.Part part : SuitArmour.Part.values()) {
            suit.getInventory().setItem(part.slot, new ItemStack(switch (part.piece) {
                case TORSO -> ModItems.IRON_TORSO_ARMOUR.get();
                case ARM -> ModItems.IRON_ARM_ARMOUR.get();
                case LEG -> ModItems.IRON_LEG_ARMOUR.get();
            }));
        }
    }

    /** A Robot Helmet with a soul (companion design, 2026-11-16): what lets a friendly mind run on an empty suit. */
    static ItemStack soulHelmet(net.minecraft.world.level.Level level) {
        return soulHelmet(level, "veteran");
    }

    static ItemStack soulHelmet(net.minecraft.world.level.Level level, String soul) {
        ItemStack helmet = new ItemStack(ModItems.ROBOT_HELMET.get());
        helmet.enchant(level.registryAccess().lookupOrThrow(net.minecraft.core.registries.Registries.ENCHANTMENT).getOrThrow(
                net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENCHANTMENT,
                        net.minecraft.resources.Identifier.fromNamespaceAndPath(dev.ajaczero.powersuits.PowerSuits.MODID, soul))), 1);
        return helmet;
    }

    private DevUtil() {}
}
