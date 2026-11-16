package dev.ajaczero.powersuits.entity;

import dev.ajaczero.powersuits.item.HelmetStyle;
import dev.ajaczero.powersuits.registry.ModDataComponents;
import dev.ajaczero.powersuits.registry.ModItems;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

/**
 * The three kits rogue suits come in (design sec. 8, user 2026-11-16): a painted frame, a styled helmet and one tool each,
 * rare and dangerous on purpose. They drop their tool and their helmet's template when defeated
 * (PowerSuitEntity.dropCustomDeathLoot). Armour is rolled apart (SuitBrain.equipRogue: bare to full, per piece).
 */
public enum RogueKit {
    /** Brown, the diver helmet, the drill: closes in and grinds you (slow, no knockback, wrecks your armour). */
    DIGGER(DyeColor.BROWN, HelmetStyle.PROTECTOR, 40),
    /** Red, the hunter helmet, the rail cannon: charges and shoots you from range. */
    HUNTER(DyeColor.RED, HelmetStyle.HUNTER, 20),
    /** Green, the spartan helmet, the chaingun: shoots you. */
    LINE(DyeColor.GREEN, HelmetStyle.SPARTAN, 40);

    private final DyeColor paint;
    private final HelmetStyle helmet;
    private final int weight;

    RogueKit(DyeColor paint, HelmetStyle helmet, int weight) {
        this.paint = paint;
        this.helmet = helmet;
        this.weight = weight;
    }

    /** The odds: 40 / 20 / 40 (the rail one is the deadliest). */
    public static RogueKit roll(RandomSource random) {
        int total = 0;
        for (RogueKit kit : values()) {
            total += kit.weight;
        }
        int pick = random.nextInt(total);
        for (RogueKit kit : values()) {
            pick -= kit.weight;
            if (pick < 0) {
                return kit;
            }
        }
        return LINE;
    }

    public DyeColor paint() {
        return this.paint;
    }

    public HelmetStyle helmet() {
        return this.helmet;
    }

    public Item tool() {
        return switch (this) {
            case DIGGER -> ModItems.DRILL.get();
            case HUNTER -> ModItems.RAIL_CANNON.get();
            case LINE -> ModItems.CHAINGUN.get();
        };
    }

    /** Make this suit a rogue of this kit: its mind, tool, styled helmet and paint. */
    public void apply(PowerSuitEntity suit) {
        suit.setMind(SuitMind.ROGUE);
        suit.getInventory().setItem(PowerSuitEntity.SOCKET_SLOT, new ItemStack(this.tool()));
        ItemStack helmet = new ItemStack(ModItems.SUIT_HELMET.get());
        helmet.set(ModDataComponents.HELMET_STYLE.get(), this.helmet);
        suit.getInventory().setItem(PowerSuitEntity.HELMET_SLOT, helmet);
        suit.setPaint(this.paint);
    }
}
