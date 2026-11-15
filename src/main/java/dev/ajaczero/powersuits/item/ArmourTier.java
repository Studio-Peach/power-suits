package dev.ajaczero.powersuits.item;

import dev.ajaczero.powersuits.PowerSuitsConfig;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import org.jetbrains.annotations.Nullable;

/**
 * The material of a set of frame armour (design sec. 10: "tiers from the start", 2026-11-14). Iron is the only one so
 * far; copper is planned. A new tier is a new constant here, its three items (ModItems) and its numbers in the config:
 * the slots, the seal and the synced worn state take any tier.
 * <p>
 * Synced to clients by ordinal (PowerSuitEntity's ARMOUR, 3 bits a slot: see SuitArmour): add new tiers at the end.
 */
public enum ArmourTier {
    IRON("iron");

    private final String name;

    ArmourTier(String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }

    /** Armour points this tier's piece adds to the suit (read from the config each time: it's hot-reloaded). */
    public double protection(ArmourPiece piece) {
        return switch (this) {
            case IRON -> switch (piece) {
                case TORSO -> PowerSuitsConfig.IRON_TORSO_ARMOUR.get();
                case ARM -> PowerSuitsConfig.IRON_ARM_ARMOUR.get();
                case LEG -> PowerSuitsConfig.IRON_LEG_ARMOUR.get();
            };
        };
    }

    /**
     * How many hits' worth of wear this tier's piece takes (its item's max damage, set at registration, so not in the
     * config: that loads later; PowerSuitsConfig's armour_wear scales the wear instead). Iron as vanilla's iron armour:
     * the torso a chestplate's 240, the legs leggings' 225, an arm a helmet's 165 (the smallest piece).
     */
    public int durability(ArmourPiece piece) {
        return switch (this) {
            case IRON -> switch (piece) {
                case TORSO -> 240;
                case ARM -> 165;
                case LEG -> 225;
            };
        };
    }

    /** What repairs this tier's pieces at an anvil (vanilla armour's own material). */
    public Item repairItem() {
        return switch (this) {
            case IRON -> Items.IRON_INGOT;
        };
    }

    public static @Nullable ArmourTier byId(int id) {
        return id >= 0 && id < values().length ? values()[id] : null;
    }
}
