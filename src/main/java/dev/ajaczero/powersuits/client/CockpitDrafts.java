package dev.ajaczero.powersuits.client;

/**
 * Draft knobs for the frame's cockpit (step 2, 2026-11-14): FrameScene shoots every option, the user picks, and this
 * class goes (the picks stay as plain code). Public so the dev scenes can switch them.
 */
public final class CockpitDrafts {
    /** The empty right hand: the frame's arm shell round his skin arm (true) or his bare arm, as vanilla's (false). */
    public static boolean armCage = true;
    /** Looking down from the cockpit: 0 nothing (vanilla), 1 the legs (frame + his), 2 the legs and the torso under the
     *  neck (chest, waist, belt, his body; not the arms: the hand pass draws them). */
    public static int down = 1;
    /** The third-person camera's distance (blocks; vanilla 4, the big suit 6.5). */
    public static float cameraDistance = 5F;

    private CockpitDrafts() {}
}
