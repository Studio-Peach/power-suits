package dev.ajaczero.powersuits.entity;

import dev.ajaczero.powersuits.PowerSuitsConfig;
import dev.ajaczero.powersuits.item.Soul;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.monster.Creeper;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * The soul's voice (companion design, 2026-11-16, section 5): the Robot Helmet's soul comments on what happens, in the
 * chat, in lines written beforehand (the language file: {@link SoulEvent}). Flavour only: it changes nothing else. One of
 * the suit's parts: {@code suit.voice()}, server only.
 *
 * It speaks to the owner (if near) and the pilot, as {@code <Veteran> line}. Whether an event speaks: the soul is on a
 * helmet that isn't broken (but the helmet breaking is the broken helmet's own last words), the suit is a companion or
 * piloted, a chance (the event's, times the config's frequency), the event's own cooldown and the global one (a priority
 * event skips that one). It never says the same line twice running for one event.
 *
 * It watches for its events itself (state changes in {@link #tick}); the few things only the entity sees come in through
 * {@link #on}. Chat messages are marked (MARK) so a player can mute them on their own client (client/SoulChatMute).
 */
public final class SuitVoice {
    /** The marker on a soul's chat message (in its style's insertion): the client's mute config looks for it. */
    public static final String MARK = "power_suits:soul";
    /** The night starts at 13000 and ends at 23000 of the day (vanilla's own bed rule). */
    private static final int NIGHT_FROM = 13000, NIGHT_TO = 23000;
    private static final double OWNER_LOW_HEALTH = 6.0;
    private static final double TALK_RANGE = 48;

    private final PowerSuitEntity suit;
    private long lastSpoke = Long.MIN_VALUE / 2;
    private final EnumMap<SoulEvent, Long> last = new EnumMap<>(SoulEvent.class);
    private final EnumMap<SoulEvent, Integer> lastLine = new EnumMap<>(SoulEvent.class);
    // what was true last tick (edge detection); not set until the first tick, so loading a world says nothing
    private boolean seen;
    @Nullable
    private Soul soul;
    private boolean ai, vehicle, broken, lowFuel, hadTarget, night, raining, ownerLow;
    /** Tests: the key of the last line spoken and how many were (the chat itself can't be read back). */
    public String lastKey = "";
    public int spoken;

    SuitVoice(PowerSuitEntity suit) {
        this.suit = suit;
    }

    /** Server, every tick: the soul's own events. */
    void tick() {
        Soul now = this.suit.getHelmetSoul();
        boolean companion = this.suit.isCompanion(), ai = this.suit.isAiDriven(), vehicle = this.suit.isVehicle(), broken = this.suit.isHelmetBroken(), lowFuel = this.suit.power().isLowOnFuel();
        boolean target = this.suit.getTarget() != null;
        ServerLevel level = (ServerLevel) this.suit.level();
        long day = level.getOverworldClockTime() % 24000L;
        boolean night = level.dimension() == Level.OVERWORLD && day >= NIGHT_FROM && day < NIGHT_TO;
        boolean raining = level.isRaining() && level.dimension() == Level.OVERWORLD;
        Player owner = this.suit.brain().getOwner();
        boolean ownerLow = owner != null && owner.getHealth() <= OWNER_LOW_HEALTH;
        if (!this.seen) {
            this.seen = true;
        } else if (now != null) {
            if (this.soul == null) {
                this.on(SoulEvent.FIRST_WORDS);
            } else if (ai && !this.ai && !this.vehicle) {
                this.on(this.broken ? SoulEvent.REPAIRED : SoulEvent.WAKE); // (a pilot climbing out is EXIT's, not a wake-up)
            }
            if (broken && !this.broken) {
                this.on(SoulEvent.HELMET_BROKEN);
            }
            if (lowFuel && !this.lowFuel) {
                this.on(SoulEvent.FUEL_LOW);
            }
            if (target && !this.hadTarget && companion) {
                this.on(this.suit.getTarget() instanceof Creeper ? SoulEvent.CREEPER : SoulEvent.SPOTS);
            }
            if (night && !this.night) {
                this.on(SoulEvent.NIGHT);
            } else if (!night && this.night) {
                this.on(SoulEvent.DAWN);
            }
            if (raining && !this.raining) {
                this.on(SoulEvent.STORM);
            }
            if (ownerLow && !this.ownerLow) {
                this.on(SoulEvent.OWNER_LOW);
            }
            if (companion && this.suit.tickCount % 200 == 0 && owner != null && owner.distanceTo(this.suit) < 16
                    && this.suit.getRandom().nextFloat() < 0.15F) {
                this.on(SoulEvent.IDLE);
            }
        }
        this.soul = now;
        this.ai = ai;
        this.vehicle = vehicle;
        this.broken = broken;
        this.lowFuel = lowFuel;
        this.hadTarget = target;
        this.night = night;
        this.raining = raining;
        this.ownerLow = ownerLow;
    }

    /** Something happened that the soul may comment on. */
    public void on(SoulEvent event) {
        this.on(event, null);
    }

    /** The same, also to {@code extra} (the owner who just died is no longer "the owner"). */
    public void on(SoulEvent event, @Nullable Player extra) {
        Soul soul = this.suit.getHelmetSoul();
        if (soul == null || !(this.suit.level() instanceof ServerLevel level) || !PowerSuitsConfig.SOUL_CHAT.get()) {
            return;
        }
        boolean piloted = this.suit.getControllingPassenger() instanceof Player;
        boolean allowed = event == SoulEvent.HELMET_BROKEN || event == SoulEvent.FIRST_WORDS || event == SoulEvent.OWNER_DIED && extra != null
                || !this.suit.isHelmetBroken() && (this.suit.isCompanion() || piloted);
        if (!allowed) {
            return;
        }
        long now = level.getGameTime();
        double chance = Mth.clamp(event.chance() * PowerSuitsConfig.SOUL_CHAT_FREQUENCY.get(), 0, 1);
        if (this.suit.getRandom().nextDouble() >= chance
                || now - this.last.getOrDefault(event, Long.MIN_VALUE / 2) < event.cooldownSeconds() * 20L
                || !event.priority() && now - this.lastSpoke < PowerSuitsConfig.SOUL_CHAT_COOLDOWN.get() * 20L) {
            return;
        }
        List<Player> hearers = this.hearers(extra, event == SoulEvent.FIRST_WORDS);
        if (hearers.isEmpty()) {
            return;
        }
        int line = this.suit.getRandom().nextInt(SoulEvent.LINES);
        if (line == this.lastLine.getOrDefault(event, -1)) {
            line = (line + 1) % SoulEvent.LINES; // never the same line twice running
        }
        String key = soul.lineKey(event, line);
        Component message = Component.empty().withStyle(style -> style.withInsertion(MARK))
                .append(Component.literal("<")).append(Component.translatable(soul.nameKey()).withStyle(soul.colour()))
                .append(Component.literal("> ")).append(Component.translatable(key));
        for (Player hearer : hearers) {
            if (hearer instanceof ServerPlayer player) {
                player.sendSystemMessage(message);
            }
        }
        this.last.put(event, now);
        this.lastLine.put(event, line);
        this.lastSpoke = now;
        this.lastKey = key;
        this.spoken++;
    }

    /** Who hears it: the pilot, the owner when near, {@code extra}; the nearest player when the soul has just been given
     *  to a suit nobody owns. */
    private List<Player> hearers(@Nullable Player extra, boolean firstWords) {
        List<Player> out = new ArrayList<>(3);
        if (this.suit.getControllingPassenger() instanceof Player pilot) {
            out.add(pilot);
        }
        Player owner = this.suit.brain().getOwner();
        if (owner != null && owner.distanceTo(this.suit) < TALK_RANGE && !out.contains(owner)) {
            out.add(owner);
        }
        if (extra != null && !out.contains(extra)) {
            out.add(extra);
        }
        if (out.isEmpty() && firstWords) {
            Player near = this.suit.level().getNearestPlayer(this.suit, 16);
            if (near != null) {
                out.add(near);
            }
        }
        return out;
    }
}
