package dev.ajaczero.powersuits.entity;

/**
 * Which arm of the suit carries a power tool (2026-11-22: for a pilot, power tools live in the normal off-hand and
 * hotbar main hand instead of dedicated suit slots — LEFT is the off-hand, RIGHT is the selected hotbar slot; for an
 * unpiloted companion or rogue, LEFT is the suit's stored tool slot {@link PowerSuitEntity#SOCKET_SLOT}).
 */
public enum ToolArm {
    LEFT, RIGHT;

    public ToolArm other() {
        return this == LEFT ? RIGHT : LEFT;
    }

    public static ToolArm byIndex(int index) {
        return index == 1 ? RIGHT : LEFT;
    }
}
