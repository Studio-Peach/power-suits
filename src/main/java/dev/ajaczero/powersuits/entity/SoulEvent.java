package dev.ajaczero.powersuits.entity;

/**
 * Things a soul comments on (companion design, 2026-11-16, section 5): each has a chance to fire when it happens and a
 * cooldown of its own, on top of the global one (SuitVoice). Its lines are in the language file as
 * {@code soul.power_suits.<soul>.<event>.<n>}, {@link #LINES} of them per soul. A priority event ignores the global
 * cooldown (the helmet breaking, the owner dying: never swallowed by an idle remark a moment before).
 */
public enum SoulEvent {
    /** The soul was just given (first words). */
    FIRST_WORDS("first_words", 1.0, 0, true),
    /** The companion boots (refuelled, helmet mended, stun over). */
    WAKE("wake", 0.5, 60, false),
    HELMET_BROKEN("helmet_broken", 1.0, 30, true),
    REPAIRED("repaired", 1.0, 30, false),
    FUEL_LOW("fuel_low", 0.8, 120, false),
    /** It picked a hostile target. */
    SPOTS("spots", 0.25, 60, false),
    /** The target is a creeper (instead of SPOTS). */
    CREEPER("creeper", 0.8, 60, false),
    KILL("kill", 0.25, 45, false),
    HURT("hurt", 0.3, 45, false),
    OWNER_LOW("owner_low", 0.7, 90, false),
    OWNER_DIED("owner_died", 1.0, 0, true),
    NIGHT("night", 0.6, 600, false),
    DAWN("dawn", 0.5, 600, false),
    STORM("storm", 0.6, 300, false),
    /** Rare chatter while it walks with its owner. */
    IDLE("idle", 1.0, 120, false),
    /** The owner climbs in / out. */
    BOARD("board", 0.5, 60, false),
    EXIT("exit", 0.5, 60, false);

    /** Lines per soul per event. */
    public static final int LINES = 2;

    private final String id;
    private final double chance;
    private final int cooldownSeconds;
    private final boolean priority;

    SoulEvent(String id, double chance, int cooldownSeconds, boolean priority) {
        this.id = id;
        this.chance = chance;
        this.cooldownSeconds = cooldownSeconds;
        this.priority = priority;
    }

    public String id() {
        return this.id;
    }

    /** The chance it speaks when this happens (before the config's frequency). */
    public double chance() {
        return this.chance;
    }

    public int cooldownSeconds() {
        return this.cooldownSeconds;
    }

    public boolean priority() {
        return this.priority;
    }
}
