package dev.ajaczero.powersuits.item;

import java.util.function.Consumer;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/**
 * Early-game head item (2026-11-20, user): fits in the suit's helmet slot, projects the floating HUD readouts and night
 * vision without the heavy steel visor frame, and carries a tiny power indicator LED on its left temple arm. Unlike a
 * helmet it gives no armour, never seals the suit, runs no machine mind and takes no wear.
 */
public class ArGlassesItem extends Item implements ModTooltip {
    public ArGlassesItem(Properties properties) {
        super(properties);
    }

    public static boolean isGlasses(ItemStack stack) {
        return stack.getItem() instanceof ArGlassesItem;
    }

    @Override
    public void addTooltip(ItemStack stack, TooltipContext context, Consumer<Component> tooltip, TooltipFlag flag) {
        tooltip.accept(Component.translatable("item.power_suits.ar_glasses.tooltip").withStyle(ChatFormatting.GRAY));
    }
}
