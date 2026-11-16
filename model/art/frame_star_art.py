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


BONE_ORIGIN = {'star_core': (0, 21.5, 6.0)}   # raw; the star's spin pivot (the window's middle). The game draws the fuel slot's
                                                # nether star there and turns the bone fast.


# Steel as the firebox's and the tidal engine's housings are drawn (letters of frame_model.PAL: W V U G steel light -> dark,
# O N X gunmetal): a light bevel on top and left, a dark one below and right, ink round every inset, bolts, vent slots; the
# light is only the star's violet (& % * =), as the tidal engine's glass is teal. User, 2026-11-16: "look at the firebox and
# tidal engines ... textures are important and were the real detail lies. Currently your textures are flat and give no
# shape": the boxes stay few and plain, the shape is painted.
# Painted at the frame's own grid (2 texels to the px, K) with its housings' vocabulary (frame_sea_art.tanks_back): ink
# right column X and steel left column O, a lit shoulder (g e) and a ink foot (G X) on every plate, two-row straps (h e),
# features 2 - 3 texels wide. User, 2026-11-16: "use what they use" (the firebox and the tidal engine).
def plate(w, h, base='N'):
    g = [['O'] + [base] * (w - 2) + ['X'] for _ in range(h)]
    g[0], g[1] = ['g'] * w, ['e'] * w                                # the shoulder
    g[-2], g[-1] = ['G'] * w, ['X'] * w
    return g


def top(w, h): return [['g'] * w] + [['h'] * w for _ in range(h - 1)]


def bottom(w, h): return grid(w, h, 'X')


LINE_ROWS = (3, 12)          # the power lines' rows on the floor and the walls (texel rows from the top, 16 tall)


def floor_art(f, w, h):
    """The floor of the cradle (7 x 8 px): a steel plate with a vertical power channel up the middle (where the star hangs
    in front of its node) and lit lines branching out to the walls at LINE_ROWS."""
    if f == 'up': return top(w, h)
    if f == 'down': return bottom(w, h)
    g = plate(w, h)
    if f != 'south': return g
    cx = w // 2
    for j in range(2, h - 2):                                        # the channel: ink, deep violet, a bright core line
        g[j][cx - 2], g[j][cx + 1] = 'X', 'X'
        g[j][cx - 1], g[j][cx] = '=', '='
    for j in range(2, h - 2): g[j][cx - 1] = g[j][cx] = '*' if j % 4 in (0, 1) else '='   # the current: dashes along it
    for j0 in LINE_ROWS:                                             # branch lines: ink, lit, ink, out to each wall
        for i in range(1, w - 1):
            if cx - 2 <= i <= cx + 1: continue
            g[j0 - 1][i], g[j0][i], g[j0 + 1][i] = 'X', '%', 'X'
    for j in range(h // 2 - 3, h // 2 + 3):                          # the node the star hangs in front of
        for i in range(cx - 3, cx + 3):
            g[j][i] = 'X' if j in (h // 2 - 3, h // 2 + 2) or i in (cx - 3, cx + 2) else '&' if j in (h // 2 - 1, h // 2) and i in (cx - 1, cx) else '%' if abs(j - h // 2 + .5) < 1.6 and abs(i - cx + .5) < 1.6 else '*'
    return g


def wall_art(f, w, h):
    """A wall (the wing): the plate's steel, the branch lines running in across its inner face, a lit stripe sweeping its outer."""
    if f == 'up': return top(w, h)
    if f == 'down': return bottom(w, h)
    g = plate(w, h)
    if f == 'west':                                                  # the inner face (a mirrored part's west)
        for j0 in LINE_ROWS:
            for i in range(0, w - 1):
                g[j0 - 1][i], g[j0][i], g[j0 + 1][i] = 'X', '%', 'X'
    elif f == 'east':                                                # the outer face: a violet stripe sweeping back and down
        for i in range(1, w - 1): g[h - 5][i], g[h - 4][i] = 'h', 'e'    # a strap along the foot
        for j in range(2, h - 2): g[j][w - 4], g[j][w - 3] = 'h', 'e'    # and a spar down the trailing edge
        for j in range(h):
            for i in range(w):
                t = abs((j - 4) - (i - 2) * 1.1)
                if 1 < i < w - 2 and 2 < j < h - 2 and t < 1.3: g[j][i] = '%' if t < 0.6 else '*'
    return g


def jetpack():
    """After the Fortnite Alien Jetpack, as simple as it goes (user, 2026-11-16: "narrow the body and let each wing be the
    side of the box ... reduce the stack of boxes ... make the core different from the one in front, it could be power
    lines"): a cradle, three boxes. A floor plate 7 px wide against the back, a wall each side standing 4 px proud and
    reaching back (the wings: nothing spreads sideways over the arms), the star spinning between them in front of a vertical
    power channel, lit lines branching from it across the floor and in along the walls."""
    return [part('floor', ((-3.5, 17.5, 3), (3.5, 25.5, 5)), floor_art),
            part('wall', ((3.5, 17.5, 3), (4.5, 25.5, 8)), wall_art, mirror=True),
            _star_hub()]


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
