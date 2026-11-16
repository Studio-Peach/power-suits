package dev.ajaczero.powersuits.client;

import dev.ajaczero.powersuits.HudAlert;
import dev.ajaczero.powersuits.PowerSuits;
import dev.ajaczero.powersuits.entity.PowerSuitEntity;
import dev.ajaczero.powersuits.entity.SuitArmour;
import dev.ajaczero.powersuits.entity.SuitEngine;
import dev.ajaczero.powersuits.item.PowerSuitItem;
import dev.ajaczero.powersuits.menu.PowerSuitMenu;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.Hud;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.CommonComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.resources.Identifier;
import net.minecraft.util.Mth;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffectUtil;
import net.minecraft.world.entity.player.Inventory;
import org.jetbrains.annotations.Nullable;

/**
 * The picture half of the suit menu (client only). Slots and shift-click live in PowerSuitMenu; this draws the
 * background, a live preview of the suit, the Power and Pack up keys and the status panels beside the menu. Numbers
 * come from the suit's synced entity data, so they update while you watch.
 * <p>
 * Since 2026-11-14 (frame step 6b, user's pick G1) it is vanilla's inventory screen with the suit in it
 * (tools/make-gui.py): the frame's parts like a body round the preview, the tool socket in the off-hand slot, the fuel
 * slot in the crafting corner with vanilla's arrow pointing at the Power key where the result slot was ("fuel in, power
 * out"), the Pack up key small where the recipe book's button sits, the suit's name where "Crafting" is. Inside the
 * suit this is your inventory (E).
 * <p>
 * The status lives beside the menu in panels drawn like the inventory's potion effects (user, 2026-11-14): Hull, Fuel
 * (time at walking pace, or why there's none: no engine, flooded, no fuel), Sealed (only while it is), then the pilot's
 * own effects, which vanilla's inventory screen would have shown. Something wrong reads in gold (a warning) or red.
 * The terminal-style status screen (2026-10-27) and the burn flame went with it.
 */
public class PowerSuitScreen extends AbstractContainerScreen<PowerSuitMenu> {
    private static final Identifier BACKGROUND = Identifier.fromNamespaceAndPath(PowerSuits.MODID, "textures/gui/power_suit.png");
    /** The keys' symbols (tools/make-gui.py). Power is 9 wide for a 1 px stem (user's pick D, 2026-10-27): on an 18 px
     *  key it can't be exactly centred, so it sits half a pixel left, a pixel up (its light goes under it). Pack is 8x8,
     *  centred (x 5..12). */
    private static final SuitKey.Symbol POWER_SYMBOL = new SuitKey.Symbol(sprite("power"), 9, 8, 4, 3);
    private static final SuitKey.Symbol PACK_SYMBOL = new SuitKey.Symbol(sprite("pack"), 8, 8, 5, 4);
    /** Vanilla's preview window. The frame is 2.3 blocks tall (a player 1.8, drawn at 30, fills it to the top): 21 leaves
     *  the frame the margin the player gets. */
    private static final int PREVIEW_X0 = 26, PREVIEW_Y0 = 8, PREVIEW_X1 = 75, PREVIEW_Y1 = 78, PREVIEW_SCALE = 21;
    /** The keys: Power where the crafting result slot was, Pack up where the recipe book's button sits (vanilla's
     *  InventoryScreen: leftPos + 104, 22 above the middle = y 61). Public: the menu scene points the mouse at them. */
    public static final int POWER_X = 153, POWER_Y = 27, PACK_X = 130, PACK_Y = 61;
    /** The title where vanilla writes "Crafting", in vanilla's label grey. */
    private static final int TITLE_X = 97, TITLE_W = 75, LABEL = 0xFF404040;

    // ---- the status panels: vanilla's effect panels (EffectsInInventory), sizes and colours ----
    private static final Identifier PANEL = Identifier.withDefaultNamespace("container/inventory/effect_background");
    private static final Identifier PANEL_AMBIENT = Identifier.withDefaultNamespace("container/inventory/effect_background_ambient");
    private static final Identifier HULL = sprite("status_hull"), SEALED = sprite("status_sealed");
    private static final int PANEL_H = 32, PANEL_STEP = 33, ICON = 18, PAD = 7, TEXT_X = 32, GREY = 0xFF808080;
    /** Chat's red and gold (ChatFormatting.RED / GOLD) for a value that needs attention. */
    private static final int RED = 0xFFFF5555, GOLD = 0xFFFFAA00;

    public PowerSuitScreen(PowerSuitMenu menu, Inventory playerInventory, Component title) {
        super(menu, playerInventory, title);
    }

    private static Identifier sprite(String name) {
        return Identifier.fromNamespaceAndPath(PowerSuits.MODID, "container/power_suit/" + name);
    }

    @Override
    protected void init() {
        super.init();
        // Buttons in container screens don't need a custom packet: vanilla sends the button id to the
        // server, which calls PowerSuitMenu.clickMenuButton.
        // A key has a symbol, no caption: its tooltip is its name, one word (user, 2026-10-27: the key shows its state).
        SuitKey power = this.addRenderableWidget(new SuitKey(this.leftPos + POWER_X, this.topPos + POWER_Y, POWER_SYMBOL,
                Component.translatable("gui.power_suits.power"), () -> switchedOn(this.menu.getSuit()),
                () -> this.minecraft.gameMode.handleInventoryButtonClick(this.menu.containerId, PowerSuitMenu.BUTTON_POWER)));
        power.setTooltip(Tooltip.create(power.getMessage()));
        SuitKey pack = this.addRenderableWidget(new SuitKey(this.leftPos + PACK_X, this.topPos + PACK_Y, PACK_SYMBOL,
                Component.translatable("gui.power_suits.pack"), null,
                () -> this.minecraft.gameMode.handleInventoryButtonClick(this.menu.containerId, PowerSuitMenu.BUTTON_PACK)));
        // Packing up needs you outside: from inside the key is there but greyed out.
        pack.active = !this.menu.isPiloting(this.minecraft.player);
        pack.setTooltip(Tooltip.create(pack.getMessage()));
    }

    /** Read every frame by the Power key: the switch flips on the server (the key, H), so it follows the synced state. */
    private static boolean switchedOn(PowerSuitEntity suit) {
        return suit == null || suit.power().isSwitchedOn();
    }

    // Since 1.21.6 screens don't draw directly: each frame they "extract" what to draw (a list of quads, text, items)
    // into GuiGraphicsExtractor, and Minecraft draws that list afterwards. Hence the extract* names.
    @Override
    public void extractRenderState(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        this.extractPanels(graphics, mouseX, mouseY); // first, as vanilla's inventory draws its effects
        super.extractRenderState(graphics, mouseX, mouseY, partialTick); // background, slots, labels, item tooltips
        this.renderEmptySlotHints(graphics, mouseX, mouseY);
    }

    /** The panels stand in for vanilla's effect list here: the HUD leaves its effect icons out while there's room. */
    @Override
    public boolean showsActiveEffects() {
        return this.width - (this.leftPos + this.imageWidth + 2) >= PANEL_H;
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        super.extractBackground(graphics, mouseX, mouseY, partialTick);
        int x = this.leftPos, y = this.topPos;
        graphics.blit(RenderPipelines.GUI_TEXTURED, BACKGROUND, x, y, 0F, 0F, this.imageWidth, this.imageHeight, 256, 256);
        PowerSuitEntity suit = this.menu.getSuit();
        if (suit == null) {
            return;
        }
        // The suit itself, turning to follow the mouse (like the player in the inventory screen). The whole of it, also
        // from inside: in first person the renderer would leave out all but the legs (the cockpit view).
        PowerSuitRenderer.inventoryPreview = true;
        try {
            InventoryScreen.extractEntityInInventoryFollowsMouse(graphics, x + PREVIEW_X0, y + PREVIEW_Y0, x + PREVIEW_X1, y + PREVIEW_Y1,
                    PREVIEW_SCALE, 0.0625F, mouseX, mouseY, suit);
        } finally {
            PowerSuitRenderer.inventoryPreview = false;
        }
    }

    /** The suit's name where vanilla's inventory says "Crafting" (a renamed suit shows its own); no "Inventory" label,
     *  as in vanilla's inventory screen. */
    @Override
    protected void extractLabels(GuiGraphicsExtractor graphics, int mouseX, int mouseY) {
        graphics.text(this.font, this.font.plainSubstrByWidth(this.title.getString(), TITLE_W), TITLE_X, this.titleLabelY, LABEL, false);
    }

    // =========================================================================================
    // The status panels (beside the menu, like the inventory's potion effects)
    // =========================================================================================

    /** One panel: a suit status (sprite in the visor's colour, a hint for its tooltip) or one of the pilot's effects. */
    private record Panel(Identifier icon, boolean tinted, boolean ambient, Component name, Component value, int valueColour,
            @Nullable Component hint) {}

    /** What the panels say now: Hull, Fuel, Sealed (only while sealed), then the pilot's own effects. */
    private List<Panel> panels(PowerSuitEntity suit) {
        List<Panel> panels = new ArrayList<>();
        var power = suit.power();
        // Hull: its % (gold from half, red in the last 15%, like the HUD), or knocked out by lightning.
        float hull = Mth.clamp(suit.getHealth() / suit.getMaxHealth(), 0F, 1F);
        panels.add(suit.isStunned()
                ? panel(HULL, "hull", Component.translatable("gui.power_suits.status.knocked_out"), HudAlert.CRITICAL)
                : panel(HULL, "hull", Component.translatable("hud.power_suits.percent", Math.round(hull * 100)), HudAlert.ofLeft(hull)));
        // Fuel: time left at walking pace (endless on a wet tidal engine or a star reactor), or why there's none.
        SuitEngine engine = suit.getEngine();
        Identifier fuelIcon = sprite("status_fuel_" + (engine == SuitEngine.TIDAL ? "tidal" : engine == SuitEngine.REACTOR ? "reactor" : "firebox"));
        int energy = power.getTotalEnergy();
        Panel fuel;
        if (engine == null) {
            fuel = panel(fuelIcon, "fuel", Component.translatable("gui.power_suits.status.no_engine"), HudAlert.CRITICAL);
        } else if (power.isFlooded()) {
            fuel = panel(fuelIcon, "fuel", Component.translatable("gui.power_suits.status.flooded"), HudAlert.CRITICAL);
        } else if (power.hasFreePower()) {
            fuel = panel(fuelIcon, "fuel", Component.translatable("hud.power_suits.endless"), HudAlert.NONE);
        } else if (energy == 0) {
            fuel = panel(fuelIcon, "fuel", Component.translatable("gui.power_suits.status.no_fuel"), HudAlert.CRITICAL);
        } else {
            fuel = panel(fuelIcon, "fuel", Component.literal(PowerSuitItem.formatWalkTime(energy)),
                    power.isLowOnFuel() ? HudAlert.WARNING : HudAlert.NONE);
        }
        panels.add(fuel);
        // Sealed: there or not (user: binary).
        if (suit.isSealed()) {
            panels.add(panel(SEALED, "sealed", CommonComponents.EMPTY, HudAlert.NONE));
        }
        // The pilot's own effects, as vanilla's inventory screen lists them (it isn't open while the suit's is).
        List<MobEffectInstance> effects = this.minecraft.player.getActiveEffects().stream()
                .filter(net.neoforged.neoforge.client.ClientHooks::shouldRenderEffect).sorted().toList();
        for (MobEffectInstance effect : effects) {
            panels.add(new Panel(Hud.getMobEffectSprite(effect.getEffect()), false, effect.isAmbient(), effectName(effect),
                    MobEffectUtil.formatDuration(effect, 1.0F, this.minecraft.level.tickRateManager().tickrate()), GREY, null));
        }
        return panels;
    }

    private static Panel panel(Identifier icon, String key, Component value, HudAlert alert) {
        int colour = alert == HudAlert.CRITICAL ? RED : alert == HudAlert.WARNING ? GOLD : GREY;
        return new Panel(icon, true, false, Component.translatable("gui.power_suits.status." + key), value, colour,
                Component.translatable("gui.power_suits.status." + key + ".hint"));
    }

    /** "Speed II", as vanilla's list names an effect. */
    private static Component effectName(MobEffectInstance effect) {
        MutableComponent name = effect.getEffect().value().getDisplayName().copy();
        if (effect.getAmplifier() >= 1 && effect.getAmplifier() <= 9) {
            name.append(CommonComponents.SPACE).append(Component.translatable("enchantment.level." + (effect.getAmplifier() + 1)));
        }
        return name;
    }

    /**
     * Vanilla's effect list, re-done for our panels (EffectsInInventory only lists the player's effects): right of the
     * menu, from its top, 33 px apart (closer with more than five); wide with names when there's 120 px of room, icons
     * only (name and value in a tooltip) down to 32 px, none below that.
     */
    private void extractPanels(GuiGraphicsExtractor graphics, int mouseX, int mouseY) {
        PowerSuitEntity suit = this.menu.getSuit();
        int x0 = this.leftPos + this.imageWidth + 2;
        int room = this.width - x0;
        if (suit == null || room < PANEL_H) {
            return;
        }
        boolean wide = room >= 120;
        List<Panel> panels = this.panels(suit);
        int step = panels.size() > 5 ? 132 / (panels.size() - 1) : PANEL_STEP;
        int y = this.topPos;
        int tint = 0xFF000000 | VisorConfig.colour();
        for (Panel p : panels) {
            int w = wide ? Math.min(room - PAD, Math.max(TEXT_X + this.font.width(p.name()), TEXT_X + this.font.width(p.value())) + PAD) : PANEL_H;
            graphics.blitSprite(RenderPipelines.GUI_TEXTURED, p.ambient() ? PANEL_AMBIENT : PANEL, x0, y, w, PANEL_H);
            if (p.tinted()) {
                graphics.blitSprite(RenderPipelines.GUI_TEXTURED, p.icon(), x0 + PAD, y + PAD, ICON, ICON, tint);
            } else {
                graphics.blitSprite(RenderPipelines.GUI_TEXTURED, p.icon(), x0 + PAD, y + PAD, ICON, ICON);
            }
            if (wide) {
                if (p.value().getString().isEmpty()) {
                    graphics.text(this.font, p.name(), x0 + TEXT_X, y + 12, -1); // one line (Sealed): centred
                } else {
                    graphics.text(this.font, p.name(), x0 + TEXT_X, y + PAD, -1);
                    graphics.text(this.font, p.value(), x0 + TEXT_X, y + PAD + 9, p.valueColour());
                }
            }
            if (mouseX >= x0 && mouseX < x0 + w && mouseY >= y && mouseY < y + Math.min(step, PANEL_H)) {
                List<Component> lines = new ArrayList<>();
                if (!wide) {
                    lines.add(p.name());
                    if (!p.value().getString().isEmpty()) {
                        lines.add(p.value().copy().withColor(p.valueColour()));
                    }
                }
                if (p.hint() != null) {
                    lines.add(p.hint().copy().withStyle(ChatFormatting.GRAY));
                }
                if (!lines.isEmpty()) {
                    graphics.setComponentTooltipForNextFrame(this.font, lines, mouseX, mouseY);
                }
            }
            y += step;
        }
    }

    /** Explain the suit's slots while they're empty. */
    private void renderEmptySlotHints(GuiGraphicsExtractor graphics, int mouseX, int mouseY) {
        if (this.hoveredSlot == null || this.hoveredSlot.hasItem() || !this.menu.getCarried().isEmpty()) {
            return;
        }
        int index = this.menu.slots.indexOf(this.hoveredSlot);
        int armour = index - PowerSuitMenu.MENU_ARMOUR;
        String key = index == PowerSuitMenu.MENU_SOCKET ? "gui.power_suits.socket_slot"
                : index == PowerSuitMenu.MENU_RIGHT_SOCKET ? "gui.power_suits.right_socket_slot"
                : index == PowerSuitMenu.MENU_FUEL ? "gui.power_suits.fuel_slot"
                : index == PowerSuitMenu.MENU_HELMET ? "gui.power_suits.helmet_slot"
                : index == PowerSuitMenu.MENU_ENGINE ? "gui.power_suits.engine_slot"
                : armour >= 0 && armour < SuitArmour.Part.values().length
                        ? "gui.power_suits.armour_slot." + SuitArmour.Part.values()[armour].piece.getName() : null;
        if (key != null) {
            graphics.setComponentTooltipForNextFrame(this.font, List.of(Component.translatable(key),
                    Component.translatable(key + ".hint").withStyle(ChatFormatting.GRAY)), mouseX, mouseY);
        }
    }
}
