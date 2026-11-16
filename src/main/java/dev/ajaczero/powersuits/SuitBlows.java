package dev.ajaczero.powersuits;

import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.entity.SuitFace;
import net.minecraft.world.entity.Entity;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import org.jspecify.annotations.Nullable;

/**
 * Server: when a suit hurts something living (its punches and stomps, its tools' bullets, beams and flames, the mind's
 * blows), every client watching it hears about it (SuitFace.STRUCK): the robot helmet's visor looks angry for a moment.
 * Clients can't tell who hurt whom, so the server says; the rest of the visor's faces come from data they already have.
 */
@EventBusSubscriber(modid = PowerSuits.MODID)
public final class SuitBlows {
    @SubscribeEvent
    public static void onDamage(LivingDamageEvent.Post event) {
        PowerSuitEntity suit = suitBehind(event.getSource().getEntity());
        Entity victim = event.getEntity();
        if (suit == null || event.getInflictedDamage() <= 0 || victim == suit || victim.getVehicle() == suit) {
            return;
        }
        suit.level().broadcastEntityEvent(suit, SuitFace.STRUCK);
    }

    /** The suit that dealt it: the suit itself, or the pilot inside it (their punches, their tools' shots). */
    private static @Nullable PowerSuitEntity suitBehind(@Nullable Entity attacker) {
        if (attacker instanceof PowerSuitEntity suit) {
            return suit;
        }
        return attacker != null && attacker.getVehicle() instanceof PowerSuitEntity suit ? suit : null;
    }

    private SuitBlows() {}
}
