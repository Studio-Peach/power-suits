"""The star reactor for the frame (frame_model.py, knob STAR: 'A' the default, 'none'): its own back and front, not the
heart's (2026-11-16, after the tidal engine's diver, frame_sea_art.py: "the light and particles are good but they
shouldn't follow the firebox's shape": a 3D component on the back, flat painted decals on the front).

How it was found (eight rounds of drafts, each in git, "Star reactor drafts round N"; the user's words):
- discs, cages, halos, pylons: "too far out there ... more grounded in technology, and don't do wheels anymore"; of the
  fronts, "I prefer C": the lens, no lines;
- a cell housing with a window: "I like A the best", but no steel cap; an accelerator box with a spinning star;
- "lean into the exoskeleton vibe for the back ... do you know what a Sandevistan is?" (the Cyberpunk 2077 / Edgerunners
  spinal implant): vertebrae, then "more mechanical and less boney, this isn't a horror mod", then "drop the white tones
  and make it more slick black and purple" with a photo of the prop (blasters4masters.com, .scratch/sand/ref.jpg: a
  chain of black wedge modules with a small lit screen each, thin lit connectors between, button pods either side of
  every module, a boxy unit at the neck end, a rounded one at the hip end; its light green): "Go with A".

What it is: the chain. Down the back, under the helmet (raw y 16 .. 25.5): a base unit at the hip, four wedge modules
(a wide slab and a narrow ridge carrying its screen), a head unit with a wide screen at the neck, a lit rod through all
of them and a pod on a short stalk either side of each module. Glossy black ($ 8 9, violet-tinged), the light only the
star's violet. On the chest the lens (open: a plate on the chest; under the breastplate: in a steel ring).
The module screens, the head and the base are the SEGMENTS: the game lights them one after another up the spine
(tools/export-frame.py makes a glowmask of each from its part's texels; SuitLights.getStarSegments paces them).

Light: the glass is the letters & % * = (lit: EXTRA; in the texture dark reserved colours, STAR_DARK, lit by glowmasks as
the sea engine's); STAR_GLOW=lit paints it lit for a review.

Coordinates raw (frame_model.py adds FY), right side +x, front -z, back +z; 2 texels per px. Faces as frame_sea_art.py.
"""
import math
from frame_radial_art import part, grid, disc, K
import frame_sea_art as sea

EXTRA = {'&': (0xe6, 0xb4, 0xff),   # the core: light violet (not white: user, round 8)
         '%': (0xc0, 0x7c, 0xff),   # glass, bright
         '*': (0x80, 0x40, 0xd0),   # glass, mid
         '=': (0x4c, 0x2a, 0x82),   # glass, deep
         '$': (0x12, 0x0d, 0x1a),   # obsidian, darkest
         '8': (0x1c, 0x14, 0x28),   # obsidian
         '9': (0x2e, 0x22, 0x44)}   # obsidian, lit edge
STAR_DARK = {'&': (0x38, 0x26, 0x50), '%': (0x2e, 0x1e, 0x44), '*': (0x26, 0x18, 0x3a), '=': (0x1e, 0x12, 0x2e)}
STYLE = dict(HR=0.5, tube=('%', '*', '='), band=('9', '$'), bubbles=True, spark='&')


# ---------------------------------------------------------------- the chest's lens (8 x 8 texels, centred on x 0, y 23)
def lens_glyph():
    g = grid(8, 8, '.')
    disc(g, 4, 4, 4, '$', ring='9', rw=1)
    disc(g, 4, 4, 3, '*')
    disc(g, 4, 4, 2, '%')
    disc(g, 4, 4, 1, '&')
    return g


def glyph_plate(el):
    """The chest's glyph alone (no lines): a 4 x 4 px plate on the chest, ink round it, the rest see-through."""
    hx, y0, y1 = 2.0, 21, 25
    def front(x, y):
        e = el(x, y)
        if e: return e
        return 'X' if max(abs(x), abs(y - 23)) < 2.5 else '.'
    def paint(f, w, h):
        if f == 'north': return [[front(hx - (i + 0.5) / K, y1 - (j + 0.5) / K) for i in range(w)] for j in range(h)]
        return grid(w, h, '.')
    return part('glyph', ((-hx, y0, -3.5), (hx, y1, -3)), paint)


# ---------------------------------------------------------------- the back: the chain
def blk(f, w, h):
    """Glossy black: a violet-tinged edge light along the top and left, the base dark."""
    g = [['8'] * w for _ in range(h)]
    g[0] = ['9'] * w
    g[-1] = ['$'] * w
    for j in range(h): g[j][0] = '9' if f in ('south', 'north', 'up') else g[j][0]
    return g


def screen(f, w, h):
    """A small lit screen on a module's ridge: a row of light over a dim row, a black bezel round it."""
    g = blk(f, w, h)
    if f == 'south':
        for i in range(1, w - 1):
            g[h // 2 - 1][i] = '&' if i % 2 else '%'
            g[h // 2][i] = '*'
    return g


def pod(f, w, h):
    """A button pod (a box): black with a dark slot across its face and a thin violet rim."""
    g = blk(f, w, h)
    if f == 'south':
        for i in range(w): g[h // 2][i] = '$'
        for i in range(1, w - 1): g[h // 2 - 1][i] = '='
    return g


def rodfill(f, w, h):
    g = [['*'] * w for _ in range(h)]
    if f in ('south', 'north'):
        for j in range(h): g[j][w // 2 - 1] = g[j][w // 2] = '%'
    return g


def lit_bar(narrow):
    """The hip unit's lit bit / the head unit's wide screen."""
    def paint(f, w, h):
        g = blk(f, w, h)
        if f == 'south':
            for i in range(2, w - 2):
                if narrow: g[h // 2][i] = '%'
                else: g[h // 2 - 1][i], g[h // 2][i] = ('&' if i % 2 else '%'), '*'
        return g
    return paint


MODS = (18, 19.5, 21, 22.5)                                              # four wedge modules, 1 px tall, 0.5 gaps
# The parts that carry a light of their own, from the hip up: the game lights them in this order, one after another
# (tools/export-frame.py SEGMENTS reads this); the rod, the pods and the lens keep the engine's steady light.
SEGMENTS = ['base', 'ridge0', 'ridge1', 'ridge2', 'ridge3', 'head']


def chain():
    P = [part('rod', ((-0.5, 16, 3), (0.5, 25.5, 4.5)), rodfill),
         part('base', ((-2, 16, 3), (2, 17.5, 5)), lit_bar(True)),
         part('head', ((-2.5, 24, 3), (2.5, 25.5, 5.5)), lit_bar(False))]
    for k, y in enumerate(MODS):
        P.append(part(f'slab{k}', ((-1.5, y, 3), (1.5, y + 1, 4)), blk))
        P.append(part(f'ridge{k}', ((-0.75, y, 4), (0.75, y + 1, 5)), screen))
        P.append(part(f'stalk{k}', ((1.5, y + 0.25, 3), (2, y + 0.75, 3.5)), blk, mirror=True))
        P.append(part(f'pod{k}', ((2, y, 3), (3.5, y + 1, 4)), pod, mirror=True))
    return P


# ---------------------------------------------------------------- B: the jetpack (2026-11-16: the star grants flight)
# User: the star engine gives flight, new reference the Fortnite "Alien Jetpack" (.scratch/star/ref_jet.png): a faceted
# grey-black shell, a big round glyph plate on its face, a dome on top, violet slits down the sides, two fins at the
# foot with a lit stripe. The front stays the lens. Raw coordinates as above; the shell is stepped boxes for the facets.
def shell(f, w, h):
    return blk(f, w, h)


def belly(f, w, h):
    """The jetpack's body; on its back a round window (a dark well in a violet ring) for the star to spin in."""
    g = blk(f, w, h)
    if f != 'south': return g
    cx, cy, R = w / 2, h / 2, 4.6
    for j in range(h):
        for i in range(w):
            d = math.hypot(i + 0.5 - cx, j + 0.5 - cy)
            if d <= R + 0.5: g[j][i] = '$'
            if R - 0.5 <= d <= R + 0.5: g[j][i] = '*'
    return g


def hub(f, w, h):
    return [['&'] * w for _ in range(h)]


def slit(f, w, h):
    """The side face of the main shell: black with one slanted violet slit."""
    g = blk(f, w, h)
    if f in ('east', 'west'):
        for i in range(2, w - 1):
            j = h // 2 + (1 if (i < w // 2) == (f == 'east') else 0)
            if 0 < j < h - 1: g[j][i] = '%'; g[j - 1][i] = '*' if g[j - 1][i] != '9' else g[j - 1][i]
    return g


def fin(f, w, h):
    """A foot fin: black, a lit stripe down its outer face."""
    g = blk(f, w, h)
    if f in ('east', 'west', 'south', 'north'):
        for j in range(1, h - 1):
            for i in range(w // 2 - 1, w // 2 + 1): g[j][i] = '%'
    return g


def dome(f, w, h):
    g = [['=' if f != 'down' else '$'] * w for _ in range(h)]
    if f != 'down': g[0] = ['*'] * w
    return g


BONE_ORIGIN = {'star_core': (0, 21.5, 5.5)}   # raw; the star's spin pivot (the window's middle). The game draws the fuel slot's
                                                # nether star there and turns the bone fast.


# Steel as the firebox's and the tidal engine's housings are drawn (letters of frame_model.PAL: W V U G steel light -> dark,
# O N X gunmetal): a light bevel on top and left, a dark one below and right, ink round every inset, bolts, vent slots; the
# light is only the star's violet (& % * =), as the tidal engine's glass is teal. User, 2026-11-16: "look at the firebox and
# tidal engines ... textures are important and were the real detail lies. Currently your textures are flat and give no
# shape": the boxes stay few and plain, the shape is painted.
def px(paint):
    """Paint at one pixel per block-pixel, the way vanilla textures are: paint(face, w_px, h_px) -> grid, each cell drawn as
    2 x 2 texels (the frame's texture is 2 texels to the px). User, 2026-11-16: "the texels are too fine"."""
    def up(f, w, h):
        small = paint(f, w // 2, h // 2)
        return [[small[j // 2][i // 2] for i in range(w)] for j in range(h)]
    return up


def bevel(w, h, base='U'):
    """A steel plate: W lit top row, V lit left column, G dark right column, X ink bottom row."""
    g = [[base] * w for _ in range(h)]
    if h == 1: return [['V'] + ['U'] * (w - 2) + ['G']]               # a 1 px step: no room for both bevels
    for i in range(w): g[0][i] = 'W'; g[h - 1][i] = 'X'
    for j in range(1, h - 1): g[j][0] = 'V'; g[j][w - 1] = 'G'
    g[0][w - 1] = 'V'
    return g


def window_disc(g, cx, cy, R):
    """The star's window in px cells: a violet rim, a deep well, a brighter heart."""
    for j in range(len(g)):
        for i in range(len(g[0])):
            d = math.hypot(i + 0.5 - cx, j + 0.5 - cy)
            if d <= R: g[j][i] = 'X' if d > R - 0.9 else '*' if d > R - 1.9 else '%'


def mid_art(f, w, h):
    g = bevel(w, h)
    if f == 'south':
        window_disc(g, w / 2, h / 2, 3.0)
        for j in range(1, h - 1):                                    # vent slots down both sides of the window
            for i in (1, w - 2): g[j][i] = 'N' if j in (2, 4) else 'U'
        for (i, j) in ((0, 0), (w - 1, 0)): g[j][i] = 'O'
    elif f in ('east', 'west'):                                      # the lit slit down the side, ink above and below
        for i in range(1, w - 1):
            g[h // 2 - 1][i] = 'X'; g[h // 2][i] = '%'; g[h // 2 + 1][i] = 'X'
    elif f == 'up': g = [['W'] * w] + [['V'] * w for _ in range(h - 1)]
    elif f == 'down': g = [['X'] * w for _ in range(h)]
    return g


def step_art(f, w, h):
    """A narrower step (crown, lower body, foot): plain bevelled steel, vent slots on the back."""
    g = bevel(w, h, 'U')
    if f == 'south' and w >= 3 and h == 1 and w <= 4:
        for i in range(1, w - 1): g[h // 2][i] = 'X' if i % 2 else 'N'
    if f == 'up': g = [['W'] * w] + [['V'] * w for _ in range(h - 1)]
    if f == 'down': g = [['X'] * w for _ in range(h)]
    return g


def feather_art(f, w, h):
    """One 1 px row of a wing: steel, a violet tip on the outer end (the lit edge sweeping down the wing)."""
    g = [['N'] * w for _ in range(h)]
    if f in ('south', 'north'):
        g[0][0] = 'O'
        g[0][w - 1] = '%'
        if w > 2: g[0][w - 2] = '*'
    elif f == 'up':
        g = [['W'] * w for _ in range(h)]
    elif f == 'down':
        g = [['X'] * w for _ in range(h)]
    else:
        g = [['%' if f == 'east' else 'O'] * w for _ in range(h)] if f == 'east' else [['X'] * w for _ in range(h)]
    return g


# the wing, a triangle of 1 px plates hanging out and down from the lower step: (y bottom, x from, x to), body-side first
WING = ((17.5, 4, 6), (16.5, 5, 7), (15.5, 6, 8), (14.5, 6, 8))


def blade_art(f, w, h):
    """A wing blade: steel, a lit edge down its outer side, ink inside it, violet at the tip."""
    g = [['N'] * w for _ in range(h)]
    for j in range(h): g[j][0] = 'O'; g[j][w - 1] = 'X'
    if f in ('south', 'north'):
        for j in range(1, h - 1): g[j][w - 1] = '%' if j % 2 else 'X'      # dashed: feather lines
    if f == 'up': g = [['W'] * w for _ in range(h)]
    return g


def jetpack():
    """After the Fortnite Alien Jetpack, kept Minecraft-simple: stepped boxes make a gem (a 6 px crown over a 10 px body
    over an 8 px and a 4 px step, 2 px deep), a round violet window in the body (the star spins in front of it) and a
    wing either side, five 1 px plates stepping out and down to a point. Painted at the pixel scale; the shape is texture."""
    P = [part('body', ((-5, 17.5, 3), (5, 24.5, 5)), px(mid_art)),
         part('crown', ((-3, 24.5, 3), (3, 25.5, 5)), px(step_art)),
         part('lower', ((-4, 16.5, 3), (4, 17.5, 5)), px(step_art)),
         part('foot', ((-2, 15.5, 3), (2, 16.5, 5)), px(step_art))]
    # the wing: one broad plate (2 x 8 px) swept out 28 degrees from the lower step, with a short one on its inner edge
    P.append(part('wing', ((4, 9.5, 3), (6, 17.5, 4)), px(blade_art), mirror=True, rot=[0, 0, 28], origin=(4, 17.5, 3.5)))
    P.append(_star_hub())
    return P


def _star_hub():
    """The spin bone's cube: hidden inside the body (the game draws the nether star at the bone's pivot)."""
    h = part('hub', ((-0.5, 21, 3.5), (0.5, 22, 4.5)), hub)
    h['bone'] = 'star_core'
    return h


BACKS = {'A': chain, 'B': jetpack}


def build(design='B', chest_x=6.0):
    """(back parts, open front, armoured front); frame_model.py prefixes them (rb_ / ro_ / ra_)."""
    glyph = sea.element(lens_glyph())
    return BACKS[design](), [glyph_plate(glyph)], [sea.bezel(glyph)]
