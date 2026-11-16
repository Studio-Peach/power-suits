package dev.ajaczero.powersuits.item;

import dev.ajaczero.powersuits.PowerSuits;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.Enchantment;
import org.jetbrains.annotations.Nullable;

/**
 * The Robot Helmet's soul (companion design, 2026-11-16): a personality, flavour only. Each soul is an enchantment
 * ({@code data/power_suits/enchantment/<id>.json}) so the vanilla enchanting table offers them (three slots, the player
 * picks one), an exclusive set keeps it to one, the helmet glints, and a grindstone takes it off again. The enchantments
 * have no effects of their own: this enum is what the game reads them as.
 */
public enum Soul {
    /** Gruff and terse, has seen it all. */
    VETERAN("veteran", ChatFormatting.GRAY),
    /** Cheerful, delighted by everything. */
    OPTIMIST("optimist", ChatFormatting.YELLOW),
    /** Dry, formal, politely sarcastic. */
    BUTLER("butler", ChatFormatting.AQUA),
    /** Anxious, sees danger everywhere, brave anyway. */
    NERVOUS("nervous", ChatFormatting.LIGHT_PURPLE);

    private final String name;
    private final Identifier id;
    private final ChatFormatting colour;

    Soul(String name, ChatFormatting colour) {
        this.colour = colour;
        this.name = name;
        this.id = Identifier.fromNamespaceAndPath(PowerSuits.MODID, name);
    }

    public String id() {
        return this.name;
    }

    /** The colour of its name in the chat. */
    public ChatFormatting colour() {
        return this.colour;
    }

    /** "soul.power_suits.veteran.name": what the chat calls it. */
    public String nameKey() {
        return "soul.power_suits." + this.name + ".name";
    }

    /** "soul.power_suits.veteran.kill.1": one of its lines for an event. */
    public String lineKey(dev.ajaczero.powersuits.entity.SoulEvent event, int n) {
        return "soul.power_suits." + this.name + "." + event.id() + "." + n;
    }

    /** The soul on this helmet, or null if it has none (or isn't a Robot Helmet). */
    public static @Nullable Soul of(ItemStack stack) {
        if (!(stack.getItem() instanceof RobotHelmetItem)) {
            return null;
        }
        for (var entry : stack.getTagEnchantments().entrySet()) {
            Holder<Enchantment> enchantment = entry.getKey();
            for (Soul soul : values()) {
                if (enchantment.unwrapKey().map(k -> k.identifier().equals(soul.id)).orElse(false)) {
                    return soul;
                }
            }
        }
        return null;
    }
}
