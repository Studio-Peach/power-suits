package dev.ajaczero.powersuits.network;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;

/**
 * Client -> server: "the pilot's suit just jumped" (SuitDriving.tryJump). Ridden movement is client-authoritative, so
 * the pilot's client launches the suit on the tick Space is pressed and sends this empty message so the server charges
 * the jump's fuel and notifies other clients (via JUMP_COUNTER).
 */
public record SuitJumpPayload() implements CustomPacketPayload {
    public static final Type<SuitJumpPayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath(PowerSuits.MODID, "suit_jump"));
    public static final StreamCodec<ByteBuf, SuitJumpPayload> STREAM_CODEC = StreamCodec.unit(new SuitJumpPayload());

    @Override
    public Type<SuitJumpPayload> type() {
        return TYPE;
    }

    /** Mod-bus event: declare the message ("1": the protocol version, both sides must match). */
    public static void register(RegisterPayloadHandlersEvent event) {
        event.registrar("1").playToServer(TYPE, STREAM_CODEC, SuitJumpPayload::handle);
    }

    /** Server, main thread. Never trust the client: only the suit's pilot while the suit can operate. */
    private static void handle(SuitJumpPayload payload, IPayloadContext context) {
        if (context.player().getVehicle() instanceof PowerSuitEntity suit
                && suit.getControllingPassenger() == context.player()
                && suit.canOperate()) {
            suit.driving().onServerJump();
        }
    }
}
