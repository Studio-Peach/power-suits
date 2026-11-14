package dev.ajaczero.powersuits.item;

import java.util.function.Consumer;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import org.jetbrains.annotations.Nullable;

/**
 * A piece of frame armour (design sec. 10, 2026-11-14): goes on a deployed suit, one per part (torso, each arm, each
 * leg: the suit's armour slots, entity/SuitArmour). It isn't vanilla armour (the player can't wear it): it adds its
 * tier's protection to the suit, and a full set with the helmet seals a running suit.
 */
public class SuitArmourItem extends Item implements ModTooltip {
    private final ArmourPiece piece;
    private final ArmourTier tier;

    public SuitArmourItem(Properties properties, ArmourPiece piece, ArmourTier tier) {
        super(properties);
        this.piece = piece;
        this.tier = tier;
    }

    public ArmourPiece piece() {
        return this.piece;
    }

    public ArmourTier tier() {
        return this.tier;
    }

    /** The piece a stack is, or null if it isn't frame armour. */
    public static @Nullable SuitArmourItem of(ItemStack stack) {
        return stack.getItem() instanceof SuitArmourItem armour ? armour : null;
    }

    @Override
    public void addTooltip(ItemStack stack, TooltipContext context, Consumer<Component> tooltip, TooltipFlag flag) {
        // "Armour for a Power Suit's arm (either one)." + "+2 Armour on the suit" (the config's number, so it stays true)
        tooltip.accept(Component.translatable("item.power_suits.suit_armour." + this.piece.getName() + ".tooltip").withStyle(ChatFormatting.GRAY));
        tooltip.accept(Component.translatable("item.power_suits.suit_armour.protection",
                number(this.tier.protection(this.piece))).withStyle(ChatFormatting.BLUE));
        tooltip.accept(Component.translatable("item.power_suits.suit_armour.seal").withStyle(ChatFormatting.GRAY));
    }

    /** 6 -> "6", 2.5 -> "2.5" (vanilla's armour lines drop a whole number's ".0" too). */
    private static String number(double value) {
        return value == Math.rint(value) ? Long.toString((long) value) : String.format(java.util.Locale.ROOT, "%.1f", value);
    }
}
