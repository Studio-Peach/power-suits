package dev.ajaczero.powersuits.client;

import com.geckolib.renderer.base.BoneSnapshots;
import dev.ajaczero.powersuits.entity.SuitArmour;
import dev.ajaczero.powersuits.item.ArmourTier;
import org.jetbrains.annotations.Nullable;

/**
 * Which of the frame's looks each part shows (frame step 6c, 2026-11-14; copper tier, 2026-11-20): its bare frame
 * ({@code frame_<bone>}), its iron piece ({@code armor_<bone>}) or its copper piece ({@code copper_<bone>}). A piece
 * takes its frame's place, so exactly one of the three is drawn per part (tiers mix freely on one suit). Any torso
 * armour (iron or copper) also covers the engine's open front ({@code engine_open} -> {@code engine_armored}, and the
 * tidal engine's / star reactor's equivalents); the belt ({@code frame_body}) gives way to the hip block
 * ({@code armor_body}) whenever either leg is armoured. Bones a model hasn't (the cockpit's arm has only its arm) are
 * left alone.
 */
final class ArmourBones {
    private ArmourBones() {}

    /** wornCode: SuitArmour.wornCode (3 bits per Part: tier ordinal + 1, 0 = bare); tools: which arms carry a power tool
     *  (bit 0 the left, bit 1 the right): an arm shows its hand look or, with a tool fitted, its socket look. */
    static void show(BoneSnapshots bones, int wornCode, int tools) {
        ArmourTier torso = SuitArmour.tierAt(wornCode, SuitArmour.Part.TORSO);
        ArmourTier rightArm = SuitArmour.tierAt(wornCode, SuitArmour.Part.RIGHT_ARM);
        ArmourTier leftArm = SuitArmour.tierAt(wornCode, SuitArmour.Part.LEFT_ARM);
        ArmourTier rightLeg = SuitArmour.tierAt(wornCode, SuitArmour.Part.RIGHT_LEG);
        ArmourTier leftLeg = SuitArmour.tierAt(wornCode, SuitArmour.Part.LEFT_LEG);
        part(bones, "torso", torso);
        arm(bones, "right_arm", rightArm, (tools & 2) != 0);
        arm(bones, "left_arm", leftArm, (tools & 1) != 0);
        part(bones, "right_leg", rightLeg);
        part(bones, "left_leg", leftLeg);
        boolean anyLeg = rightLeg != null || leftLeg != null;
        hide(bones, "frame_body", anyLeg);
        hide(bones, "armor_body", !anyLeg);
        boolean torsoArmoured = torso != null;
        hide(bones, "engine_open", torsoArmoured);
        hide(bones, "engine_armored", !torsoArmoured);
        hide(bones, "sea_open", torsoArmoured);
        hide(bones, "sea_armored", !torsoArmoured);
        hide(bones, "star_open", torsoArmoured);
        hide(bones, "star_armored", !torsoArmoured);
    }

    /** An arm's six looks: frame / iron / copper, with its hand / with the socket: exactly one is drawn. */
    private static void arm(BoneSnapshots bones, String bone, @Nullable ArmourTier tier, boolean socket) {
        hide(bones, "frame_" + bone, tier != null || socket);
        hide(bones, "armor_" + bone, tier != ArmourTier.IRON || socket);
        hide(bones, "copper_" + bone, tier != ArmourTier.COPPER || socket);
        hide(bones, "frame_" + bone + "_socket", tier != null || !socket);
        hide(bones, "armor_" + bone + "_socket", tier != ArmourTier.IRON || !socket);
        hide(bones, "copper_" + bone + "_socket", tier != ArmourTier.COPPER || !socket);
    }

    private static void part(BoneSnapshots bones, String bone, @Nullable ArmourTier tier) {
        hide(bones, "frame_" + bone, tier != null);
        hide(bones, "armor_" + bone, tier != ArmourTier.IRON);
        hide(bones, "copper_" + bone, tier != ArmourTier.COPPER);
    }

    private static void hide(BoneSnapshots bones, String bone, boolean hide) {
        bones.ifPresent(bone, b -> b.skipRender(hide).skipChildrenRender(hide));
    }
}
