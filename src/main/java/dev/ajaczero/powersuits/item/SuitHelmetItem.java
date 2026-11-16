package dev.ajaczero.powersuits.item;

import dev.ajaczero.powersuits.registry.ModDataComponents;
import java.util.function.Consumer;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import org.jetbrains.annotations.Nullable;

/**
 * The suit's helmet (its helmet slot: seals the suit, carries its mind). Its look is a data component, so one item has
 * every style (design sec. 4c): a smithing table gives a helmet a style (template + helmet + style object) or takes it
 * off again (helmet + iron block). The style changes the name ("Spartan Helmet") and adds a flavour line, nothing else.
 *
 * A data component is a typed piece of data stored on one ItemStack (like a sword's enchantments or a renamed item's
 * name): the item type stays power_suits:suit_helmet, so the suit, the menu and the recipes need nothing new.
 */
public class SuitHelmetItem extends SuitPartItem {
    /** Its durability: vanilla's iron helmet (design sec. 10, 2026-11-14). An item property, so not in the config. */
    public static final int DURABILITY = 165;

    public SuitHelmetItem(Properties properties) {
        super(properties, "item.power_suits.suit_helmet.tooltip");
    }

    /** The helmet's style, or null for the standard helmet. */
    public static @Nullable HelmetStyle style(ItemStack stack) {
        if (stack.getItem() instanceof RobotHelmetItem) {
            return HelmetStyle.ROBOT; // its own item, not a style a smithing table can give
        }
        return stack.get(ModDataComponents.HELMET_STYLE.get());
    }

    /**
     * Worn out (design sec. 10, user 2026-11-14): a helmet doesn't break off like the armour pieces (SuitArmour.wear
     * stops its damage at the max), it stays on, broken: no armour points and no seal, but the machine mind still runs
     * (a parked suit mustn't die from scratches). An anvil with iron ingots repairs it.
     */
    public static boolean isBroken(ItemStack stack) {
        return stack.getItem() instanceof SuitHelmetItem && stack.isBroken();
    }

    @Override
    public Component getName(ItemStack stack) {
        // A name typed in at an anvil still wins: vanilla draws the custom name over this one (the tooltip still says
        // it's broken).
        HelmetStyle style = style(stack);
        Component name = style == null ? super.getName(stack) : Component.translatable("item.power_suits.suit_helmet." + style.getSerializedName());
        return isBroken(stack) ? Component.translatable("item.power_suits.suit_helmet.broken", name) : name; // "Spartan Helmet (broken)"
    }

    @Override
    public void addTooltip(ItemStack stack, TooltipContext context, Consumer<Component> tooltip, TooltipFlag flag) {
        if (isBroken(stack)) {
            tooltip.accept(Component.translatable("item.power_suits.suit_helmet.broken.tooltip").withStyle(ChatFormatting.RED));
        }
        super.addTooltip(stack, context, tooltip, flag);
        HelmetStyle style = style(stack);
        if (style != null) {
            // a line that hints at the helmet's inspiration, in the grey italics vanilla uses for flavour text
            tooltip.accept(Component.translatable("item.power_suits.suit_helmet." + style.getSerializedName() + ".flavour")
                    .withStyle(ChatFormatting.DARK_GRAY, ChatFormatting.ITALIC));
        }
    }
}
