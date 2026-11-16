package dev.ajaczero.powersuits.client;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.SuitVoice;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientChatReceivedEvent;

/** Client: drops the soul's chat remarks when the player muted them (VisorConfig.MUTE_SOUL_CHAT). The server marks them
 *  (SuitVoice.MARK, in the style's insertion), so nothing else is touched. */
@EventBusSubscriber(modid = PowerSuits.MODID, value = Dist.CLIENT)
public final class SoulChatMute {
    @SubscribeEvent
    public static void onChat(ClientChatReceivedEvent event) {
        if (VisorConfig.MUTE_SOUL_CHAT.get() && SuitVoice.MARK.equals(event.getMessage().getStyle().getInsertion())) {
            event.setCanceled(true);
        }
    }

    private SoulChatMute() {}
}
