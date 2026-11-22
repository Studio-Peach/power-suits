package dev.ajaczero.powersuits.entity;

import java.util.function.Predicate;
import net.minecraft.world.entity.player.Player;

/**
 * What shared code (this package runs on both sides) may ask about the local player's view.
 *
 * Classes like {@code net.minecraft.client.Minecraft} only exist in the game client: a dedicated server doesn't ship
 * them, and code that touches one there crashes with NoClassDefFoundError the moment it runs. So shared code never calls
 * the client directly; it asks through these hooks, which hold safe defaults (no camera, nobody looking) until
 * {@code client/ClientSetup} fills them in on the client. Same idea as {@code SocketAim.visualMuzzle}.
 */
public final class ClientView {
    /** Is this client looking out of this suit's cockpit (it's our own suit, first person, the camera on the pilot)?
     *  Always false on a server. */
    public static Predicate<PowerSuitEntity> inCockpit = suit -> false;
    /** Tell the server the local pilot's suit just jumped (no-op on a server). */
    public static Runnable sendJump = () -> {};
    /** Is the local client holding Space right now? Checked directly so the suit jumps on the same tick Space is
     *  pressed instead of waiting one tick for LocalPlayer.rideTick to copy the key into pilot.jumping. */
    public static Predicate<Player> jumpPressed = pilot -> false;

    private ClientView() {}
}
