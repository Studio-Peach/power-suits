package dev.ajaczero.powersuits.entity.ai;

import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import net.minecraft.world.entity.LivingEntity;

/**
 * Rogue mind with a drill (the digger kit): run at the target RogueTarget picked and grind it with the drill (ToolMelee:
 * slow, no knockback, wrecks armour). The drill never digs for a mind. The friendly follow and guard routes have their own
 * (MeleeAttack, HomeGuard).
 */
public class RogueDrillAttack extends AttackGoal {
    public RogueDrillAttack(PowerSuitEntity suit) {
        super(suit);
    }

    @Override
    public boolean canUse() {
        return this.suit.isAiDriven() && this.suit.isRogue() && this.suit.brain().toolUse() == ToolUse.DRILL && this.suit.getTarget() != null
                && this.suit.getTarget().isAlive();
    }

    @Override
    public void tick() {
        LivingEntity target = this.suit.getTarget();
        if (target != null) {
            this.melee(target, true);
        }
    }
}
