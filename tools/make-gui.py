"""Builds the suit menu background (textures/gui/power_suit.png) and its sprites from vanilla's inventory screen.

    uv run --with pillow python3 tools/make-gui.py

Since 2026-10-27 the suit's menu is the player's inventory with the suit in it (user): E inside the suit opens it, like
a horse's. Since 2026-11-14 (frame step 6b, user's pick G1 of .scratch/menu6b) it IS vanilla's inventory screen, slot for
slot, with the suit's things in vanilla's places:
- the armour column (left of the preview) and the column above the off-hand slot (right of it) hold the frame's parts
  like a body round the preview (the suit faces you, so its right side is on your left): helmet / right arm / right leg
  / engine (the backpack: worn too) on the left, torso / left arm / left leg on the right;
- the off-hand slot is the pilot's real off-hand slot while piloting (or the companion's tool slot when opened from
  outside); the engine sits at the foot of the left column (2026-11-22: power tool sockets removed for pilots);
- the crafting corner: the suit's name where "Crafting" is, the fuel slot where the grid was, vanilla's arrow, the Power
  key in the result slot's place (fuel in, power out); the Pack up key small where the recipe book's button sits.
The status (hull, fuel, sealed) moved out of the menu into panels beside it, drawn like the inventory's potion effects
(PowerSuitScreen); no burn flame (not every engine burns).
Coordinates must match PowerSuitMenu (slots) and PowerSuitScreen (keys, preview).
"""
import io
import os
import zipfile
from glob import glob
from PIL import Image

jar = glob('build/moddev/artifacts/minecraft-patched-*-merged.jar')[0]
with zipfile.ZipFile(jar) as z:
    inventory = Image.open(io.BytesIO(z.read('assets/minecraft/textures/gui/container/inventory.png'))).convert('RGBA')

DARK, LIGHT, PANEL, SLOT = (55, 55, 55, 255), (255, 255, 255, 255), (198, 198, 198, 255), (139, 139, 139, 255)
HINT = (85, 85, 85, 255)  # vanilla's empty-slot outlines (container/slot/chestplate...)
img = inventory.copy()


def fill(x0, y0, x1, y1, c):
    for x in range(x0, x1):
        for y in range(y0, y1):
            img.putpixel((x, y), c)


slot_frame = img.crop((76, 61, 94, 79))     # vanilla's off-hand slot frame (18x18)
fill(97, 17, 133, 53, PANEL)                # the 2x2 crafting grid goes...
fill(152, 26, 172, 46, PANEL)               # ...and the result slot (the Power key covers its place)
for y in (7, 25, 43):                       # three slots above the off-hand slot: torso, left arm, left leg
    img.paste(slot_frame, (76, y))
img.paste(slot_frame, (111, 27))            # the fuel slot, before vanilla's arrow (x 135..150)
img.save('src/main/resources/assets/power_suits/textures/gui/power_suit.png')
print('wrote textures/gui/power_suit.png')


def sprite(name, rows, colour=LIGHT, size=None):
    """A sprite from rows of '.'/'X' (X = colour), padded to size (centred) if given."""
    w, h = len(rows[0]), len(rows)
    im = Image.new('RGBA', size or (w, h), (0, 0, 0, 0))
    ox, oy = ((size[0] - w) // 2, (size[1] - h) // 2) if size else (0, 0)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == 'X':
                im.putpixel((ox + x, oy + y), colour)
    path = f'src/main/resources/assets/power_suits/textures/gui/sprites/{name}.png'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)
    print('wrote', path)


# The keys' symbols, white (the screen tints them: grey, or green when the Power key is on), positioned by
# PowerSuitScreen. Power, 9x8 (user's pick D, 2026-10-27, over 2 px stems that looked too heavy): a 1 px stem in a ring
# open at the top; an odd width can't be exactly centred on the 18 px key, it sits half a pixel left. Pack, 8x8 and
# centred: an arrow into a tray, a pixel of air between the arrow's tip and the tray's floor.
sprite('container/power_suit/power', ["....X....",
                                      ".X..X..X.",
                                      "X...X...X",
                                      "X...X...X",
                                      "X.......X",
                                      "X.......X",
                                      ".X.....X.",
                                      "..XXXXX.."])
sprite('container/power_suit/pack', ["...XX...",
                                     "...XX...",
                                     "...XX...",
                                     ".XXXXXX.",
                                     "..XXXX..",
                                     "X..XX..X",
                                     "X......X",
                                     "XXXXXXXX"])

# The status panels' icons (18x18, white masks: drawn in the visor's colour like the HUD's). Hull: the HUD's little
# suit; fuel: what the engine runs on (the firebox's flame, the tidal engine's drop, the star reactor's star); sealed:
# the HUD's shield, twice its size.
sprite('container/power_suit/status_hull', ["....XXXX....",
                                            "....XXXX....",
                                            "....XXXX....",
                                            "....XXXX....",
                                            "............",
                                            "XX.XXXXXX.XX",
                                            "XX.XXXXXX.XX",
                                            "XX.XXXXXX.XX",
                                            "XX.XXXXXX.XX",
                                            "XX.XXXXXX.XX",
                                            "XX.XXXXXX.XX",
                                            "...XXX.XXX..",
                                            "...XXX.XXX..",
                                            "...XXX.XXX..",
                                            "...XXX.XXX..",
                                            "...XXX.XXX.."], size=(18, 18))
sprite('container/power_suit/status_fuel_firebox', ["....X.......",
                                                    "....XX......",
                                                    "...XXX......",
                                                    "...XXXX.....",
                                                    "..XXXXX...X.",
                                                    "..XXXXXX..X.",
                                                    ".XXXXXXX.XX.",
                                                    ".XXXX.XXXXX.",
                                                    "XXXX...XXXX.",
                                                    "XXX.....XXX.",
                                                    "XXX.....XXX.",
                                                    ".XXX...XXX..",
                                                    "..XXXXXXX...",
                                                    "...XXXXX...."], size=(18, 18))
sprite('container/power_suit/status_fuel_tidal', ["....XX....",
                                                  "....XX....",
                                                  "...XXXX...",
                                                  "...XXXX...",
                                                  "..XXXXXX..",
                                                  "..XXXXXX..",
                                                  ".XXXXXXXX.",
                                                  ".XXXXXXXX.",
                                                  "XXXXXXXXXX",
                                                  "XXXXXXXXXX",
                                                  "XX.XXXXXXX",
                                                  "XX.XXXXXXX",
                                                  ".XX.XXXXX.",
                                                  "..XXXXXX..",
                                                  "...XXXX..."], size=(18, 18))
sprite('container/power_suit/status_fuel_reactor', ["........X........",
                                                    "........X........",
                                                    ".......XXX.......",
                                                    ".......XXX.......",
                                                    "......XXXXX......",
                                                    "....XXXXXXXXX....",
                                                    "XXXXXXXXXXXXXXXXX",
                                                    "....XXXXXXXXX....",
                                                    "......XXXXX......",
                                                    ".......XXX.......",
                                                    ".......XXX.......",
                                                    "........X........",
                                                    "........X........"], size=(18, 18))
seal = Image.open('src/main/resources/assets/power_suits/textures/gui/hud/seal.png').convert('RGBA')
sprite('container/power_suit/status_sealed',
       [''.join('X' if seal.getpixel((x // 2, y // 2))[3] > 0 else '.' for x in range(seal.width * 2)) for y in range(seal.height * 2)],
       size=(18, 18))

# The empty arm slot's outline (vanilla has outlines for the chest and legs, none for an arm): a pauldron over the
# arm, in vanilla's outline grey.
sprite('container/slot/suit_arm', ["................",
                                   "................",
                                   "...XXXXXXXXXX...",
                                   "..X..........X..",
                                   "..X..........X..",
                                   "...XXXXXXXXXX...",
                                   ".....X....X.....",
                                   ".....X....X.....",
                                   ".....X....X.....",
                                   ".....XXXXXX.....",
                                   ".....X....X.....",
                                   ".....X....X.....",
                                   ".....X....X.....",
                                   ".....XXXXXX.....",
                                   "................",
                                   "................"], colour=HINT)
