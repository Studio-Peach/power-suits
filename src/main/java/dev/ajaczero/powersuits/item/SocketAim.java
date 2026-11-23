package dev.ajaczero.powersuits.item;

import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import java.util.function.BiFunction;
import java.util.function.Predicate;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.ProjectileUtil;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * Where socket tools fire from and what their operator is aiming at. Works on both sides. The operator is the pilot,
 * or the suit itself while its machine mind drives (then its head is the "camera": eye height 1.98, head yaw and pitch).
 */
public final class SocketAim {
    // The frame (2026-11-14, step 5b): the tool arm swings up from its shoulder until the tool points along the view
    // (PowerSuitRenderer.raiseTool, which it always is while a tool works), so the muzzle is the shoulder plus the arm's
    // reach along the view. The shoulder pivot (model/power_frame.bbmodel, left_arm): 8.25 px left of the centre, 28 px up
    // from the feet; with the +3 px sleeved tool socket (built y 19), the reach to the chaingun's muzzle (its muzzle
    // block's bottom, y 10.5 under the shoulder's 28) is 17.5 px. The other tools end within a px or two of it (drill/TNT/
    // flamethrower 18, rail 19, chainsaw 22 (felling_taper), EM 16 with its 2 px inset). The shoulder turns with the torso, which faces
    // the view within the head's 50 degrees: taking the view's yaw puts it at most ~0.2 blocks off, for a shot that goes
    // for the crosshair anyway (aimPoint).
    // (The big suit's: its raised elbow's muzzle 0.709 left, 2.226 up, 1.738 forward of the feet, the torso pivot
    // 1.695 up, pitching with the view at 55%.)
    // That's where everyone else sees the gun; the pilot's own first-person view draws its bullets from the cockpit
    // viewmodel's muzzle instead (visualMuzzle + Bullet.visualOffset).
    private static final double SHOULDER_LEFT = 8.25 / 16, SHOULDER_UP = 28.0 / 16, REACH = 17.5 / 16;

    /** Where muzzle effects (EM beam particles) start on this client. The client points it at the cockpit viewmodel's
     *  muzzle for its own pilot in first person (CockpitHands); everywhere else it's the suit's muzzle. */
    public static BiFunction<PowerSuitEntity, LivingEntity, Vec3> visualMuzzle = SocketAim::muzzlePosition;

    public static Vec3 muzzlePosition(PowerSuitEntity suit, LivingEntity operator) {
        float yaw = aimYaw(operator) * Mth.DEG_TO_RAD;
        float pitch = operator.getXRot() * Mth.DEG_TO_RAD; // + = looking down
        double reach = REACH - (suit.getSocketStack().getItem() instanceof PowerTool tool ? tool.muzzleInsetPixels() / 16.0 : 0);
        double shoulder = suit.arm() == dev.ajaczero.powersuits.entity.ToolArm.LEFT ? SHOULDER_LEFT : -SHOULDER_LEFT; // the arm shooting
        Vec3 view = new Vec3(-Mth.sin(yaw) * Mth.cos(pitch), -Mth.sin(pitch), Mth.cos(yaw) * Mth.cos(pitch));
        Vec3 left = new Vec3(Mth.cos(yaw), 0, Mth.sin(yaw));
        return suit.position().add(0, SHOULDER_UP, 0).add(left.scale(shoulder)).add(view.scale(reach));
    }

    /** Which way the operator faces. A player's yaw is their view; a mob's view is its head (yRot is where it walks). */
    public static float aimYaw(LivingEntity operator) {
        return operator instanceof Player ? operator.getYRot() : operator.getYHeadRot();
    }

    /** What's under the operator's crosshair: the first entity or block along the view, or a far point. */
    public static Vec3 aimPoint(PowerSuitEntity suit, LivingEntity operator, double range) {
        return aimPoint(suit, operator, range, 1F);
    }

    /** The same between two ticks ({@code partial}: 0 last tick .. 1 this one): a client drawing the aim every frame
     *  (the TNT launcher's arc on the HUD) follows the view smoothly. At 1 it's exactly the server's. */
    public static Vec3 aimPoint(PowerSuitEntity suit, LivingEntity operator, double range, float partial) {
        Vec3 eye = operator.getEyePosition(partial);
        Vec3 blockEnd = blockHit(suit, operator, range, partial);
        EntityHitResult entityHit = ProjectileUtil.getEntityHitResult(suit.level(), operator, eye, blockEnd,
                new AABB(eye, blockEnd).inflate(1), e -> e != suit && e != operator && e.isPickable() && !e.isSpectator(), 0.3F);
        return entityHit != null ? entityHit.getLocation() : blockEnd;
    }

    /** The first entity along the view (not behind a wall) that passes the filter. Hit boxes are grown
     *  by {@code inflate} so small things like dropped items are easy to point at. */
    @Nullable
    public static Entity entityInView(PowerSuitEntity suit, LivingEntity operator, double range, Predicate<Entity> filter, float inflate) {
        Vec3 eye = operator.getEyePosition();
        Vec3 blockEnd = blockHit(suit, operator, range, 1F);
        EntityHitResult hit = ProjectileUtil.getEntityHitResult(suit.level(), operator, eye, blockEnd,
                new AABB(eye, blockEnd).inflate(inflate + 1), e -> e != suit && e != operator && filter.test(e), inflate);
        return hit == null ? null : hit.getEntity();
    }

    private static Vec3 blockHit(PowerSuitEntity suit, LivingEntity operator, double range, float partial) {
        Vec3 eye = operator.getEyePosition(partial);
        Vec3 end = eye.add(operator.getViewVector(partial).scale(range));
        return suit.level().clip(new ClipContext(eye, end, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, operator)).getLocation();
    }

    private SocketAim() {}
}
