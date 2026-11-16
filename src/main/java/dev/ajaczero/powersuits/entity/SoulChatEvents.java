package dev.ajaczero.powersuits.entity;

import dev.ajaczero.powersuits.PowerSuits;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;

/** The soul's one event only the world sees: its owner dies (the nearby suits they own say something to them). */
@EventBusSubscriber(modid = PowerSuits.MODID)
public final class SoulChatEvents {
    @SubscribeEvent
    public static void onDeath(LivingDeathEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) {
            return;
        }
        for (PowerSuitEntity suit : player.level().getEntitiesOfClass(PowerSuitEntity.class, player.getBoundingBox().inflate(64))) {
            if (player.getUUID().equals(suit.brain().getOwnerId())) {
                suit.voice().on(SoulEvent.OWNER_DIED, player);
            }
        }
    }

    private SoulChatEvents() {}
}
