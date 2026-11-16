package dev.ajaczero.powersuits.client;

import com.geckolib.renderer.base.BoneSnapshots;
import dev.ajaczero.powersuits.entity.SuitArmour;

/**
 * Which of the frame's two looks each part shows (frame step 6c, 2026-11-14): its bare frame or its armour piece. The
 * frame's files hold both (model/art/frame_model.py, ARMOR=game): a part's frame cubes in {@code frame_<bone>}, its
 * piece in {@code armor_<bone>}; a piece takes its frame's place, so exactly one of the two is drawn. The torso piece
 * also covers the engine's front (the open hoses and core, {@code engine_open}; under the breastplate the lower hoses and
 * the radiator grille, {@code engine_armored}; the tidal engine's two, {@code sea_open} / {@code sea_armored}); the belt and its piece, the hip, go with the legs (the hip with either
 * leg piece on). Bones a model hasn't (the cockpit's arm has only its arm) are left alone.
 */
final class ArmourBones {
    private ArmourBones() {}

    /** worn: SuitArmour.wornMask (a bit per Part); tools: which arms carry a power tool (bit 0 the left, bit 1 the right):
     *  an arm shows its hand look or, with a tool fitted, its socket look (2026-11-15). */
    static void show(BoneSnapshots bones, int worn, int tools) {
        boolean torso = worn(worn, SuitArmour.Part.TORSO);
        pair(bones, "torso", torso);
        arm(bones, "right_arm", worn(worn, SuitArmour.Part.RIGHT_ARM), (tools & 2) != 0);
        arm(bones, "left_arm", worn(worn, SuitArmour.Part.LEFT_ARM), (tools & 1) != 0);
        pair(bones, "right_leg", worn(worn, SuitArmour.Part.RIGHT_LEG));
        pair(bones, "left_leg", worn(worn, SuitArmour.Part.LEFT_LEG));
        pair(bones, "body", worn(worn, SuitArmour.Part.RIGHT_LEG) || worn(worn, SuitArmour.Part.LEFT_LEG));
        hide(bones, "engine_open", torso);
        hide(bones, "engine_armored", !torso);
        hide(bones, "sea_open", torso);   // the tidal engine's own (its group engine_sea is shown by the renderer)
        hide(bones, "sea_armored", !torso);
    }

    static boolean worn(int mask, SuitArmour.Part part) {
        return (mask & 1 << part.ordinal()) != 0;
    }

    /** An arm's four looks: frame / armour, with its hand / with the socket (frame_<arm>_socket): exactly one is drawn. */
    private static void arm(BoneSnapshots bones, String bone, boolean armoured, boolean socket) {
        hide(bones, "frame_" + bone, armoured || socket);
        hide(bones, "armor_" + bone, !armoured || socket);
        hide(bones, "frame_" + bone + "_socket", armoured || !socket);
        hide(bones, "armor_" + bone + "_socket", !armoured || !socket);
    }

    private static void pair(BoneSnapshots bones, String bone, boolean armoured) {
        hide(bones, "frame_" + bone, armoured);
        hide(bones, "armor_" + bone, !armoured);
    }

    private static void hide(BoneSnapshots bones, String bone, boolean hide) {
        bones.ifPresent(bone, b -> b.skipRender(hide).skipChildrenRender(hide));
    }
}
