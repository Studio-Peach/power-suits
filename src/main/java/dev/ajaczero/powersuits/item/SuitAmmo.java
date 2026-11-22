package dev.ajaczero.powersuits.item;

import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import java.util.function.Predicate;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import org.jetbrains.annotations.Nullable;

/**
 * Where the power tools' ammo comes from:
 * <ul>
 *   <li>A pilot pays from their own inventory (off-hand first, then the rest; free in creative).</li>
 *   <li>A friendly companion (a non-rogue {@link PowerSuitEntity} operating on its own) draws from its 8-slot robot
 *       pack ({@link PowerSuitEntity#PACK_START}..{@code +PACK_SLOTS}; 2026-11-22).</li>
 *   <li>A rogue suit still fires for free.</li>
 * </ul>
 * Each tool says what a round is ({@code fits}): a fire charge for the chaingun, TNT for the TNT launcher, an amethyst
 * shard for the rail cannon.
 */
public final class SuitAmmo {
    /** What {@link #count} returns for a pilot who never runs out (creative). */
    public static final int ENDLESS = -1;

    private SuitAmmo() {
    }

    /** Server: use up one round for this operator. */
    public static boolean take(@Nullable LivingEntity operator, Predicate<ItemStack> fits) {
        if (operator instanceof PowerSuitEntity suit) {
            if (suit.isRogue()) {
                return true;
            }
            SimpleContainer inv = suit.getInventory();
            for (int i = PowerSuitEntity.PACK_START; i < PowerSuitEntity.PACK_START + PowerSuitEntity.PACK_SLOTS; i++) {
                ItemStack stack = inv.getItem(i);
                if (!stack.isEmpty() && fits.test(stack)) {
                    stack.shrink(1);
                    inv.setChanged();
                    return true;
                }
            }
            return false;
        }
        if (!(operator instanceof Player player)) {
            return true;
        }
        if (player.hasInfiniteMaterials()) {
            return true;
        }
        ItemStack offhand = player.getOffhandItem();
        if (!offhand.isEmpty() && fits.test(offhand)) {
            offhand.shrink(1);
            return true;
        }
        Inventory inventory = player.getInventory();
        for (int i = 0; i < inventory.getContainerSize(); i++) {
            ItemStack stack = inventory.getItem(i);
            if (!stack.isEmpty() && fits.test(stack)) {
                stack.shrink(1);
                inventory.setChanged();
                return true;
            }
        }
        return false;
    }

    /** Both sides: does this operator have a round to fire? */
    public static boolean has(@Nullable LivingEntity operator, Predicate<ItemStack> fits) {
        if (operator instanceof PowerSuitEntity suit) {
            if (suit.isRogue()) {
                return true;
            }
            SimpleContainer inv = suit.getInventory();
            for (int i = PowerSuitEntity.PACK_START; i < PowerSuitEntity.PACK_START + PowerSuitEntity.PACK_SLOTS; i++) {
                ItemStack stack = inv.getItem(i);
                if (!stack.isEmpty() && fits.test(stack)) {
                    return true;
                }
            }
            return false;
        }
        return !(operator instanceof Player player) || count(player, fits) != 0;
    }

    /** Both sides: the rounds this pilot carries, or {@link #ENDLESS} in creative. A client knows its own player's
     *  inventory, so the HUD can count without asking the server. */
    public static int count(Player player, Predicate<ItemStack> fits) {
        if (player.hasInfiniteMaterials()) {
            return ENDLESS;
        }
        Inventory inventory = player.getInventory();
        int n = 0;
        for (int i = 0; i < inventory.getContainerSize(); i++) {
            ItemStack stack = inventory.getItem(i);
            if (!stack.isEmpty() && fits.test(stack)) {
                n += stack.getCount();
            }
        }
        return n;
    }
}
