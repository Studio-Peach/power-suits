package dev.ajaczero.powersuits.entity.ai;

/**
 * How the companion mind uses the tool in its socket (design sec. 8, rewritten 2026-11-16): each tool says which
 * (PowerTool.mindUse). The kind picks the route: the follow route (a gunner: it follows its owner like a tamed wolf and
 * defends them) or the guard route (it keeps to its home, the block where the pilot got out, and deals with what comes
 * near); the tool's own goals do the fighting (PowerTool.mindGoals). A rogue only fights, with the weapons rogues carry.
 *
 * Nothing destructive ever runs in a mind's hands: the flamethrower and the TNT launcher are carried but the mind only
 * punches with them, and the drill and the chainsaw only ever grind a target (they never mine or fell for a mind).
 */
public enum ToolUse {
    /** No tool: follow route, fists. */
    NONE,
    /** Aim and hold the trigger (chaingun): follow route. */
    GUN,
    /** Chainsaw: follow route, runs at the target and shreds it (ToolMelee). */
    SAW,
    /** Flamethrower: follow route, fists only (fire is griefing). */
    FLAME,
    /** Grab and throw with the EM projector: guard route (EmGuard). */
    EM,
    /** Snipe with the rail cannon: guard route (RailGuard). */
    RAIL,
    /** Drill: guard route, charges what comes near home and grinds it (ToolMelee). */
    DRILL,
    /** TNT launcher: guard route, fists only (blowing things up is griefing). */
    TNT
}
