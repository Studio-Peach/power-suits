package dev.ajaczero.powersuits.client;

import com.geckolib.renderer.base.BoneSnapshots;
import dev.ajaczero.powersuits.entity.SuitArmour;

/**
 * Which of the frame's two looks each part shows (frame step 6c, 2026-11-14): its bare frame or its armour piece. The
 * frame's files hold both (model/art/frame_model.py, ARMOR=game): a part's frame cubes in {@code frame_<bone>}, its
 * piece in {@code armor_<bone>}; a piece takes its frame's place, so exactly one of the two is drawn. The torso piece
 * also covers the engine's front (the open hoses and core, {@code engine_open}; under the breastplate the lower hoses and
 * the radiator grille, {@code engine_armored}); the belt and its piece, the hip, go with the legs (the hip with either
 * leg piece on). Bones a model hasn't (the cockpit's arm has only its arm) are left alone.
 */
final class ArmourBones {
    private ArmourBones() {}

    /** worn: SuitArmour.wornMask (a bit per Part). */
    static void show(BoneSnapshots bones, int worn) {
        boolean torso = worn(worn, SuitArmour.Part.TORSO);
        pair(bones, "torso", torso);
        pair(bones, "right_arm", worn(worn, SuitArmour.Part.RIGHT_ARM));
        pair(bones, "left_arm", worn(worn, SuitArmour.Part.LEFT_ARM));
        pair(bones, "right_leg", worn(worn, SuitArmour.Part.RIGHT_LEG));
        pair(bones, "left_leg", worn(worn, SuitArmour.Part.LEFT_LEG));
        pair(bones, "body", worn(worn, SuitArmour.Part.RIGHT_LEG) || worn(worn, SuitArmour.Part.LEFT_LEG));
        hide(bones, "engine_open", torso);
        hide(bones, "engine_armored", !torso);
    }

    static boolean worn(int mask, SuitArmour.Part part) {
        return (mask & 1 << part.ordinal()) != 0;
    }

    private static void pair(BoneSnapshots bones, String bone, boolean armoured) {
        hide(bones, "frame_" + bone, armoured);
        hide(bones, "armor_" + bone, !armoured);
    }

    private static void hide(BoneSnapshots bones, String bone, boolean hide) {
        bones.ifPresent(bone, b -> b.skipRender(hide).skipChildrenRender(hide));
    }
}
