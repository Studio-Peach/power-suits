package dev.ajaczero.powersuits.entity.ai;

import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import net.minecraft.world.entity.LivingEntity;

/**
 * The follow route's hand-to-hand fighting (companion design, 2026-11-16): a companion with the chainsaw, the flamethrower
 * or no tool runs at the target DefendOwner picked. With the chainsaw it holds the trigger once the target is in reach
 * (ToolMelee shreds it: slow, no knockback); with the flamethrower or nothing it punches. Never the flame (fire is
 * griefing in a mind's hands). The chaingun has its own goal (GunAttack).
 */
public class MeleeAttack extends AttackGoal {
    public MeleeAttack(PowerSuitEntity suit) {
        super(suit);
    }

    @Override
    public boolean canUse() {
        var brain = this.suit.brain();
        return this.suit.isAiDriven() && brain.followsOwner() && !brain.hasGun() && this.suit.getTarget() != null
                && this.suit.getTarget().isAlive();
    }

    @Override
    public void tick() {
        LivingEntity target = this.suit.getTarget();
        if (target != null) {
            this.melee(target, this.suit.brain().toolUse() == ToolUse.SAW);
        }
    }
}
