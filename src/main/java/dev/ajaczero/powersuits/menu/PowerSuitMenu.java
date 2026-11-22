package dev.ajaczero.powersuits.menu;

import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.entity.SuitArmour;
import dev.ajaczero.powersuits.entity.SuitFuel;
import dev.ajaczero.powersuits.item.ArGlassesItem;
import dev.ajaczero.powersuits.item.EngineItem;
import dev.ajaczero.powersuits.item.PowerTool;
import dev.ajaczero.powersuits.item.SuitHelmetItem;
import dev.ajaczero.powersuits.registry.ModItems;
import dev.ajaczero.powersuits.registry.ModMenus;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.resources.Identifier;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import org.jetbrains.annotations.Nullable;

/**
 * The suit's inventory screen, server side. A "menu" is the logic half of a GUI: which slots exist,
 * what may go in them and what shift-click does. It exists on both sides; the server's copy is the
 * real one and Minecraft keeps the client's copy in sync slot by slot. The picture is drawn by
 * {@code client/PowerSuitScreen}.
 * <p>
 * Since 2026-10-27 (user) it's the player's inventory with the suit in it: the pilot opens it with the inventory key (E)
 * from inside, like a horse's (PowerSuitEntity.openCustomInventoryScreen), and sneak + right-click opens it on a parked
 * suit. Since 2026-11-14 (frame step 6b, user's pick G1) it is vanilla's inventory screen slot for slot: the frame's
 * parts like a body round the preview (the armour column: helmet, right arm, right leg, engine; above the off-hand slot:
 * torso, left arm, left leg; the suit faces you, so its right side is on your left), the tool socket in the off-hand
 * slot (the tool is the suit's off hand: the swap-hands key moves it, see {@link #clicked}), the fuel slot in the
 * crafting corner before the arrow to the Power key (tools/make-gui.py draws the frames).
 */
public class PowerSuitMenu extends AbstractContainerMenu {
    // Two numberings, don't mix them up: the suit's own slots (PowerSuitEntity.FUEL_SLOT etc.: where an item lives in
    // the suit's inventory, and in saves) and the menu's slots (MENU_*: the order they were added here, which is what
    // clicks and shift-clicks talk about). The menu shows the suit's slots in this order, then the player's inventory.
    public static final int MENU_SOCKET = 0, MENU_FUEL = 1, MENU_HELMET = 2, MENU_ENGINE = 3;
    /** The armour (frame step 6b): menu slot MENU_ARMOUR + i is SuitArmour.Part i (torso, left arm, right arm, left
     *  leg, right leg). */
    public static final int MENU_ARMOUR = 4;
    private static final int SUIT_SLOTS = MENU_ARMOUR + SuitArmour.Part.values().length;
    /** Menu slots of the player's inventory (27, top-left first) and hotbar (9). */
    public static final int INV_START = SUIT_SLOTS, HOTBAR_START = INV_START + 27, END = HOTBAR_START + 9;
    /** Where a shift-click from the player's side tries to put an item, first that takes it and has room (the fuel slot
     *  last: it takes the most; the right arm and leg before the left: reading order). MENU_SOCKET is skipped while
     *  piloting (then it is the pilot's real off-hand slot). */
    private static final int[] SHIFT_CLICK_ORDER = {MENU_SOCKET, MENU_HELMET, MENU_ARMOUR, MENU_ARMOUR + 2, MENU_ARMOUR + 1,
            MENU_ARMOUR + 4, MENU_ARMOUR + 3, MENU_ENGINE, MENU_FUEL};
    /** Button ids sent by the "Pack up" and power switch buttons (vanilla's built-in menu button packet carries them). */
    public static final int BUTTON_PACK = 0, BUTTON_POWER = 1;

    /** Slot positions in the 176x166 background (top-left of the 16x16 item area), vanilla's inventory screen's: its
     *  armour column (x 8: helmet, right arm, right leg, engine) and the column right of the preview (x 77: torso, left
     *  arm, left leg, off-hand / companion tool), rows 18 apart from y 8; fuel in the crafting corner. */
    public static final int LEFT_X = 8, RIGHT_X = 77, ROW_Y = 8, ROW = 18, FUEL_X = 112, FUEL_Y = 28;
    /** Empty-slot outlines: vanilla's for the helmet, chest (the torso), legs and off-hand shield, ours for an arm. */
    private static final Identifier EMPTY_HELMET = Identifier.withDefaultNamespace("container/slot/helmet");
    private static final Identifier EMPTY_TORSO = Identifier.withDefaultNamespace("container/slot/chestplate");
    private static final Identifier EMPTY_LEG = Identifier.withDefaultNamespace("container/slot/leggings");
    private static final Identifier EMPTY_SHIELD = Identifier.withDefaultNamespace("container/slot/shield");
    private static final Identifier EMPTY_ARM = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "container/slot/suit_arm");

    @Nullable
    private final PowerSuitEntity suit;
    /** True when opened from inside the suit (pilot): MENU_SOCKET is the player's real off-hand slot; false when opened
     *  from outside (parked / companion): MENU_SOCKET is the suit's companion tool slot (SOCKET_SLOT). */
    private final boolean piloting;

    public PowerSuitMenu(int containerId, Inventory playerInventory, Container suitInventory, @Nullable PowerSuitEntity suit) {
        this(containerId, playerInventory, suitInventory, suit, suit != null && playerInventory.player.getVehicle() == suit);
    }

    public PowerSuitMenu(int containerId, Inventory playerInventory, Container suitInventory, @Nullable PowerSuitEntity suit, boolean piloting) {
        super(ModMenus.POWER_SUIT.get(), containerId);
        this.suit = suit;
        this.piloting = piloting;
        checkContainerSize(suitInventory, PowerSuitEntity.SLOTS);
        suitInventory.startOpen(playerInventory.player);

        // Added in MENU_* order: the n-th addSlot is menu slot n.
        if (this.piloting) {
            this.addSlot(new Slot(playerInventory, Inventory.SLOT_OFFHAND, RIGHT_X, ROW_Y + 3 * ROW) { // pilot's real off-hand
                @Override
                public Identifier getNoItemIcon() {
                    return EMPTY_SHIELD;
                }
            });
        } else {
            this.addSlot(new Slot(suitInventory, PowerSuitEntity.SOCKET_SLOT, RIGHT_X, ROW_Y + 3 * ROW) { // companion's tool slot
                @Override
                public boolean mayPlace(ItemStack stack) {
                    return stack.getItem() instanceof PowerTool;
                }

                @Override
                public int getMaxStackSize() {
                    return 1;
                }
            });
        }
        this.addSlot(new Slot(suitInventory, PowerSuitEntity.FUEL_SLOT, FUEL_X, FUEL_Y) {
            @Override
            public boolean mayPlace(ItemStack stack) {
                // Any engine's fuel, like a furnace's slot (what the installed engine can't use just sits there), and
                // what burnt fuel leaves (the empty bucket / glass bottle).
                return SuitFuel.fitsFuelSlot(stack);
            }
        });
        this.addSlot(new Slot(suitInventory, PowerSuitEntity.HELMET_SLOT, LEFT_X, ROW_Y) {
            @Override
            public boolean mayPlace(ItemStack stack) {
                return stack.getItem() instanceof SuitHelmetItem || ArGlassesItem.isGlasses(stack);
            }

            @Override
            public Identifier getNoItemIcon() {
                return EMPTY_HELMET;
            }

            @Override
            public int getMaxStackSize() {
                return 1;
            }
        });
        this.addSlot(new Slot(suitInventory, PowerSuitEntity.ENGINE_SLOT, LEFT_X, ROW_Y + 3 * ROW) { // the backpack: foot of left column
            @Override
            public boolean mayPlace(ItemStack stack) {
                return stack.getItem() instanceof EngineItem;
            }

            @Override
            public int getMaxStackSize() {
                return 1;
            }
        });
        // The armour, like a body round the preview (it faces you: the suit's right side on your left). Each slot takes
        // its part's piece only (an arm piece either arm), one at a time.
        for (SuitArmour.Part part : SuitArmour.Part.values()) {
            this.addSlot(new Slot(suitInventory, part.slot, armourX(part), armourY(part)) {
                @Override
                public boolean mayPlace(ItemStack stack) {
                    return part.fits(stack);
                }

                @Override
                public int getMaxStackSize() {
                    return 1;
                }

                @Override
                public Identifier getNoItemIcon() {
                    return switch (part.piece) {
                        case TORSO -> EMPTY_TORSO;
                        case ARM -> EMPTY_ARM;
                        case LEG -> EMPTY_LEG;
                    };
                }
            });
        }
        // Player inventory and hotbar, where vanilla's inventory screen has them.
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                this.addSlot(new Slot(playerInventory, col + row * 9 + 9, 8 + col * 18, 84 + row * 18));
            }
        }
        for (int col = 0; col < 9; col++) {
            this.addSlot(new Slot(playerInventory, col, 8 + col * 18, 142));
        }
    }

    /** Left column: helmet, right arm, right leg (engine); right column: torso, left arm, left leg (socket). */
    private static int armourX(SuitArmour.Part part) {
        return part == SuitArmour.Part.RIGHT_ARM || part == SuitArmour.Part.RIGHT_LEG ? LEFT_X : RIGHT_X;
    }

    private static int armourY(SuitArmour.Part part) {
        return ROW_Y + ROW * switch (part) {
            case TORSO -> 0;
            case LEFT_ARM, RIGHT_ARM -> 1;
            case LEFT_LEG, RIGHT_LEG -> 2;
        };
    }

    /** Client side: the server told us which suit (entity id). Slot contents arrive separately. */
    public static PowerSuitMenu fromNetwork(int containerId, Inventory playerInventory, RegistryFriendlyByteBuf buf) {
        PowerSuitEntity suit = playerInventory.player.level().getEntity(buf.readVarInt()) instanceof PowerSuitEntity s ? s : null;
        boolean piloting = buf.readBoolean();
        return new PowerSuitMenu(containerId, playerInventory, new SimpleContainer(PowerSuitEntity.SLOTS), suit, piloting);
    }

    @Nullable
    public PowerSuitEntity getSuit() {
        return this.suit;
    }

    /** Both sides: was this menu opened from inside the suit (pilot)? Then MENU_SOCKET is their real off-hand and
     *  there's no Pack up: climb out first. */
    public boolean isPiloting(Player player) {
        return this.piloting || this.suit != null && player.getVehicle() == this.suit;
    }

    /** Usable by the pilot from inside, or on a parked suit you're standing next to (not one somebody else is in). */
    @Override
    public boolean stillValid(Player player) {
        return this.suit != null && this.suit.isAlive()
                && (this.isPiloting(player) || !this.suit.isVehicle() && player.distanceToSqr(this.suit) < 8 * 8);
    }

    /** Runs on the server when a screen button is clicked. */
    @Override
    public boolean clickMenuButton(Player player, int id) {
        if (this.suit == null || !this.stillValid(player)) {
            return false;
        }
        if (id == BUTTON_PACK && !this.isPiloting(player)) {
            return this.suit.packUp(player); // refused while the firebox is flooded
        }
        if (id == BUTTON_POWER) {
            this.suit.flipPowerSwitch();
            return true;
        }
        return false;
    }

    /** The suit's menu slot a shift-click from the player's side sends this item to, or -1 (then it hops between
     *  inventory and hotbar, as in vanilla). The first slot that takes it and has room (an arm piece goes to the free
     *  arm); none with room: the first that takes it (nothing moves, like a furnace's full slot). The empty bucket and
     *  glass bottle burnt fuel leaves behind may sit in the fuel slot but are never shift-clicked into it. */
    private int shiftClickTarget(ItemStack stack) {
        int first = -1;
        for (int target : SHIFT_CLICK_ORDER) {
            if (target == MENU_SOCKET && this.piloting) {
                continue; // while piloting this is the player's real off-hand slot (vanilla doesn't shift-click into it)
            }
            if (target == MENU_FUEL && (stack.is(Items.BUCKET) || stack.is(Items.GLASS_BOTTLE))) {
                continue;
            }
            Slot slot = this.slots.get(target);
            if (slot.mayPlace(stack)) {
                ItemStack in = slot.getItem();
                if (in.isEmpty() || ItemStack.isSameItemSameComponents(in, stack) && in.getCount() < slot.getMaxStackSize(in)) {
                    return target;
                }
                first = first < 0 ? target : first;
            }
        }
        return first;
    }

    /** Shift-click: suit slots -> player; player -> socket (tools), helmet slot (a helmet), armour slots (a piece),
     *  engine slot (an engine) or fuel slot (fuel). */
    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        Slot slot = this.slots.get(index);
        if (!slot.hasItem()) {
            return ItemStack.EMPTY;
        }
        ItemStack stack = slot.getItem();
        ItemStack original = stack.copy();
        if (index < SUIT_SLOTS) {
            if (!this.moveItemStackTo(stack, INV_START, END, true)) {
                return ItemStack.EMPTY;
            }
        } else {
            int target = this.shiftClickTarget(stack);
            if (target >= 0) {
                if (!this.moveItemStackTo(stack, target, target + 1, false)) {
                    return ItemStack.EMPTY; // that slot is full: nothing moves (like a furnace)
                }
            } else if (index < HOTBAR_START) {
                if (!this.moveItemStackTo(stack, HOTBAR_START, END, false)) {
                    return ItemStack.EMPTY;
                }
            } else if (!this.moveItemStackTo(stack, INV_START, HOTBAR_START, false)) {
                return ItemStack.EMPTY;
            }
        }
        if (stack.isEmpty()) {
            slot.setByPlayer(ItemStack.EMPTY);
        } else {
            slot.setChanged();
        }
        return original;
    }
}
