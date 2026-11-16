package dev.ajaczero.powersuits.entity.ai;

import dev.ajaczero.powersuits.PowerSuitsConfig;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import java.util.Comparator;
import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * The guard route's hand-to-hand fighting (companion design, 2026-11-16): a companion with the drill or the TNT launcher
 * keeps to its home and charges the nearest monster within the guard radius of it. With the drill it grinds the target
 * (ToolMelee: slow, no knockback, wrecks armour); with the TNT launcher it only punches (blowing things up is griefing in
 * a mind's hands). It gives up on one that leaves the radius, and ReturnHome walks it back.
 */
public class HomeGuard extends AttackGoal {
    @Nullable
    private LivingEntity target;
    private int nextSearch;

    public HomeGuard(PowerSuitEntity suit) {
        super(suit);
    }

    @Override
    public boolean canUse() {
        if (!this.suit.isAiDriven() || !this.suit.brain().guardsByMelee() || this.suit.brain().getHome() == null
                || this.suit.tickCount < this.nextSearch) {
            return false;
        }
        this.target = this.pick(0);
        if (this.target == null) {
            this.nextSearch = this.suit.tickCount + SuitGoals.SEARCH_INTERVAL;
        }
        return this.target != null;
    }

    /** The monster nearest home within the radius ({@code slack} blocks more for one already being fought). */
    @Nullable
    private LivingEntity pick(double slack) {
        BlockPos home = this.suit.brain().getHome();
        if (home == null) {
            return null;
        }
        Vec3 centre = Vec3.atBottomCenterOf(home);
        double radius = PowerSuitsConfig.MELEE_GUARD_RADIUS.get() + slack;
        return this.suit.level().getEntitiesOfClass(LivingEntity.class, new AABB(centre, centre).inflate(radius, 8, radius),
                        e -> e instanceof Enemy && e.distanceToSqr(centre) < radius * radius && SuitTargets.canAttack(this.suit, e, false))
                .stream().min(Comparator.comparingDouble(e -> e.distanceToSqr(centre))).orElse(null);
    }

    @Override
    public boolean canContinueToUse() {
        LivingEntity target = this.suit.getTarget();
        BlockPos home = this.suit.brain().getHome();
        if (!this.suit.isAiDriven() || !this.suit.brain().guardsByMelee() || target == null || !target.isAlive() || home == null) {
            return false;
        }
        double radius = PowerSuitsConfig.MELEE_GUARD_RADIUS.get() + 4;
        return target.distanceToSqr(Vec3.atBottomCenterOf(home)) < radius * radius && SuitTargets.canAttack(this.suit, target, false);
    }

    @Override
    public void start() {
        this.suit.setTarget(this.target);
        super.start();
    }

    @Override
    public void tick() {
        LivingEntity target = this.suit.getTarget();
        if (target != null) {
            this.melee(target, this.suit.brain().toolUse() == ToolUse.DRILL);
        }
    }

    @Override
    public void stop() {
        this.suit.setTarget(null);
        this.target = null;
        super.stop();
    }
}
