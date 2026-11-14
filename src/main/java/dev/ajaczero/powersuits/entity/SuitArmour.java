package dev.ajaczero.powersuits.entity;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.PowerSuitsConfig;
import dev.ajaczero.powersuits.item.ArmourPiece;
import dev.ajaczero.powersuits.item.ArmourTier;
import dev.ajaczero.powersuits.item.SuitArmourItem;
import net.minecraft.resources.Identifier;
import net.minecraft.world.Container;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ItemStack;
import org.jetbrains.annotations.Nullable;

/**
 * The armour on the frame (design sec. 10, 2026-11-14): one piece per part, torso, each arm, each leg, in the suit's
 * armour slots (and the helmet in its own). The bare frame has no armour of its own; each piece adds its tier's points
 * (PowerSuitsConfig, "armour"), the helmet its own. The suit is sealed (SuitSeal) only with all five pieces and the
 * helmet on, powered: {@link PowerSuitEntity#isSealed}.
 * <p>
 * The server keeps the protection as one attribute modifier per part. They're transient (not saved), so a loaded suit
 * gets them from its slots, with the config's current numbers: {@link #applyProtection} runs whenever the slots
 * change and once a tick (a cheap compare) to follow config edits. Clients learn what's worn from one synced int
 * (PowerSuitEntity's ARMOUR: each part's tier, to draw the pieces and count the seal).
 */
public final class SuitArmour {
    /** The frame's parts that take armour, each with its slot in the suit's inventory and the piece that fits it. */
    public enum Part {
        TORSO(PowerSuitEntity.TORSO_SLOT, ArmourPiece.TORSO, "torso"),
        LEFT_ARM(PowerSuitEntity.LEFT_ARM_SLOT, ArmourPiece.ARM, "left_arm"),
        RIGHT_ARM(PowerSuitEntity.RIGHT_ARM_SLOT, ArmourPiece.ARM, "right_arm"),
        LEFT_LEG(PowerSuitEntity.LEFT_LEG_SLOT, ArmourPiece.LEG, "left_leg"),
        RIGHT_LEG(PowerSuitEntity.RIGHT_LEG_SLOT, ArmourPiece.LEG, "right_leg");

        public final int slot;
        public final ArmourPiece piece;
        final Identifier modifier;

        Part(int slot, ArmourPiece piece, String name) {
            this.slot = slot;
            this.piece = piece;
            this.modifier = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "armour/" + name);
        }

        /** Whether a stack may go on this part: frame armour of this part's kind (an arm piece fits either arm). */
        public boolean fits(ItemStack stack) {
            SuitArmourItem armour = SuitArmourItem.of(stack);
            return armour != null && armour.piece() == this.piece;
        }

        public static @Nullable Part ofSlot(int slot) {
            for (Part part : values()) {
                if (part.slot == slot) {
                    return part;
                }
            }
            return null;
        }
    }

    private static final Identifier HELMET_MODIFIER = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "armour/helmet");
    /** Bits per part in the synced int: the tier's ordinal + 1, 0 = nothing worn (7 tiers fit). */
    private static final int BITS = 3;

    private final PowerSuitEntity suit;

    SuitArmour(PowerSuitEntity suit) {
        this.suit = suit;
    }

    /** Server: what the slots hold, packed for the synced copy (each part's tier ordinal + 1 in its 3 bits). */
    static int encode(Container slots) {
        int worn = 0;
        for (Part part : Part.values()) {
            SuitArmourItem armour = SuitArmourItem.of(slots.getItem(part.slot));
            if (armour != null && armour.piece() == part.piece) {
                worn |= (armour.tier().ordinal() + 1) << (part.ordinal() * BITS);
            }
        }
        return worn;
    }

    /** Both sides: the tier of the piece on this part, or null for a bare part. */
    public @Nullable ArmourTier worn(Part part) {
        int id = (this.suit.getEntityData().get(PowerSuitEntity.ARMOUR) >> (part.ordinal() * BITS)) & ((1 << BITS) - 1);
        return ArmourTier.byId(id - 1);
    }

    /** Both sides: which parts are armoured, one bit per Part (1 << ordinal): what the renderer shows. */
    public int wornMask() {
        int mask = 0;
        for (Part part : Part.values()) {
            if (this.worn(part) != null) {
                mask |= 1 << part.ordinal();
            }
        }
        return mask;
    }

    /** Both sides: how many of the five parts are armoured. */
    public int pieces() {
        int count = 0;
        for (Part part : Part.values()) {
            if (this.worn(part) != null) {
                count++;
            }
        }
        return count;
    }

    /** Both sides: every part armoured (any tiers, mixed too): with the helmet, what the seal needs. */
    public boolean fullSet() {
        return this.pieces() == Part.values().length;
    }

    /**
     * Server: one armour modifier per part (its piece's points, none when bare) and one for the helmet, set to the
     * config's current numbers. Only touches a modifier whose amount changed, so it's cheap to call every tick.
     */
    void applyProtection() {
        AttributeInstance armour = this.suit.getAttribute(Attributes.ARMOR);
        if (armour == null) {
            return;
        }
        Container slots = this.suit.getInventory();
        for (Part part : Part.values()) {
            SuitArmourItem piece = SuitArmourItem.of(slots.getItem(part.slot));
            set(armour, part.modifier, piece != null && piece.piece() == part.piece ? piece.tier().protection(part.piece) : 0);
        }
        set(armour, HELMET_MODIFIER, slots.getItem(PowerSuitEntity.HELMET_SLOT).isEmpty() ? 0 : PowerSuitsConfig.HELMET_ARMOUR.get());
    }

    private static void set(AttributeInstance attribute, Identifier id, double amount) {
        AttributeModifier current = attribute.getModifier(id);
        if (amount == 0) {
            if (current != null) {
                attribute.removeModifier(id);
            }
        } else if (current == null || current.amount() != amount) {
            attribute.addOrUpdateTransientModifier(new AttributeModifier(id, amount, AttributeModifier.Operation.ADD_VALUE));
        }
    }
}
