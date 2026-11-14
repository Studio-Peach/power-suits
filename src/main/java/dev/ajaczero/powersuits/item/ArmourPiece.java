package dev.ajaczero.powersuits.item;

/**
 * What a frame armour piece covers (design sec. 10, 2026-11-14): one item per kind, fitting either side (an arm piece
 * goes on the left or the right arm, like the frame's own arm parts). The helmet isn't one: it keeps its own item and
 * slot. Each kind's protection per tier is in the balance config ({@link ArmourTier#protection}).
 */
public enum ArmourPiece {
    TORSO("torso"),
    ARM("arm"),
    LEG("leg");

    private final String name;

    ArmourPiece(String name) {
        this.name = name;
    }

    /** "torso", "arm", "leg": item ids (iron_torso_armour) and translation keys. */
    public String getName() {
        return this.name;
    }
}
