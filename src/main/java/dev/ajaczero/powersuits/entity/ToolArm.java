package dev.ajaczero.powersuits.entity;

/**
 * Which of the frame's two arms a socket belongs to (2026-11-15: either hand can be swapped for a power tool, so both arms
 * have a socket). The left arm's socket is the original ({@link PowerSuitEntity#SOCKET_SLOT}); the right arm's is added after
 * the armour slots, so saves keep their numbers.
 */
public enum ToolArm {
    LEFT(PowerSuitEntity.SOCKET_SLOT), RIGHT(PowerSuitEntity.RIGHT_SOCKET_SLOT);

    /** The suit's inventory slot of this arm's socket. */
    public final int slot;

    ToolArm(int slot) {
        this.slot = slot;
    }

    public ToolArm other() {
        return this == LEFT ? RIGHT : LEFT;
    }

    public static ToolArm byIndex(int index) {
        return index == 1 ? RIGHT : LEFT;
    }
}
