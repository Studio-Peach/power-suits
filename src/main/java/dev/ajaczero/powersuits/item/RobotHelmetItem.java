package dev.ajaczero.powersuits.item;

/**
 * The Robot Helmet (companion design, 2026-11-16): a helmet of its own, solid gold, never crafted and never a smithing
 * style. It is found broken in piglin strongholds, mended with gold at an anvil and (later) given a soul at an enchanting
 * table. Worn on a suit it is an ordinary helmet (same seal, same wear) with the robot's face on the visor.
 *
 * It extends the suit helmet, so everything that asks "is this the suit's helmet" (the slot, the wear, the seal, the
 * broken state) treats it alike; its look is {@link HelmetStyle#ROBOT}, which {@link SuitHelmetItem#style} reports for it
 * instead of reading a component (the smithing table can't give that look to any other helmet).
 */
public class RobotHelmetItem extends SuitHelmetItem {
    public RobotHelmetItem(Properties properties) {
        super(properties);
    }
}
