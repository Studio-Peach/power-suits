package dev.ajaczero.powersuits.entity.ai;

import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.item.RailCannonItem;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.phys.Vec3;

/**
 * Rogue mind with a rail cannon (the hunter kit): walk until it sees the target RogueTarget picked, aim the head, hold the
 * trigger until the cannon is charged (the core between the prongs glows brighter: the warning), let go once the head is
 * within 2 degrees of the target, charge again. No friend-on-the-beam check: a rogue hurts what it hits. It never breaks
 * blocks (the beam breaks them only for a pilot). Its damage is its own config (rogue_rail_damage).
 */
public class RogueRailAttack extends AttackGoal {
    private static final double MAX_AIM_ERROR = 2.0;
    /** Shoots from up to this far (the rogue's sight is 24). */
    private static final double RANGE = 26;

    public RogueRailAttack(PowerSuitEntity suit) {
        super(suit);
    }

    @Override
    public boolean canUse() {
        return this.suit.isAiDriven() && this.suit.isRogue() && this.suit.brain().toolUse() == ToolUse.RAIL && this.suit.getTarget() != null
                && this.suit.getTarget().isAlive();
    }

    @Override
    public void tick() {
        LivingEntity target = this.suit.getTarget();
        if (target == null) {
            return;
        }
        Vec3 aim = target.getBoundingBox().getCenter();
        this.suit.brain().setAim(aim);
        boolean sees = this.suit.getSensing().hasLineOfSight(target);
        if (!sees || this.suit.distanceTo(target) > RANGE) {
            this.suit.socket().setAiTrigger(false);
            RailCannonItem.disarm(this.suit);
            this.approach(target, 1.0);
            return;
        }
        this.suit.getNavigation().stop(); // plant the feet and shoot
        this.suit.socket().setAiTrigger(true); // charge (it holds a full charge while the trigger stays down)
        if (!RailCannonItem.isCharged(this.suit)) {
            return;
        }
        Vec3 view = this.suit.getViewVector(1F);
        Vec3 want = aim.subtract(this.suit.getEyePosition()).normalize();
        if (Math.toDegrees(Math.acos(Mth.clamp(view.dot(want), -1, 1))) <= MAX_AIM_ERROR) {
            this.suit.socket().setAiTrigger(false); // let go: it fires this tick (SuitSocket.tick), then charges again
        }
    }
}
