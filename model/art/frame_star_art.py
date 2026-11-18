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
import math, os
from frame_radial_art import part, grid, disc, K
import frame_sea_art as sea
from frame_motor_art import chrome

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


BONE_ORIGIN = {'star_core': (0, 21.5, 7.0)}   # raw; the star's spin pivot (the window's middle). The game draws the fuel slot's
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


def fin_art(f, w, h, lines=True):
    """A wing plate, as round 14's (the shape the user liked): steel, a lit stripe sweeping down its outer face; on its inner
    face the power lines run in from the floor (rows from the top, as the wings' tops sit level with the floor's)."""
    if f == 'up': return top(w, h)
    if f == 'down': return bottom(w, h)
    g = plate(w, h)
    if f == 'west' and lines:                                        # the inner face (a mirrored part's west)
        for j0 in LINE_ROWS:
            if j0 + 1 < h - 2:
                for i in range(0, w - 1): g[j0 - 1][i], g[j0][i], g[j0 + 1][i] = 'X', '%', 'X'
    elif f == 'east':
        for j in range(h):
            for i in range(w):
                t = abs((j - (h - 3)) + (i - 2) * 1.6)
                if 1 < i < w - 1 and 1 < j < h - 2 and t < 1.1: g[j][i] = '%' if t < 0.5 else '*'   # the diagonal violet stripe
    return g


def jetpack():
    """After the Fortnite Alien Jetpack (user, 2026-11-16: "narrow the body and let each wing be the side of the box ...
    reduce the stack of boxes ... make the core different from the one in front, it could be power lines"; and, when the
    wings had become plain walls, "you destroyed the whole shape of the wings": round 14's fins are the shape): a floor plate
    7 px wide against the back, a wing standing on each edge of it, reaching back in two steps with the tip rising level
    with the top (nothing spreads sideways over the arms, nothing at the foot), the star spinning between them in front of
    a vertical power channel, lit lines branching from it across the floor and in along the wings."""
    return [part('floor', ((-3, 17.5, 3), (3, 25.5, 6)), floor_art),
            part('fin', ((3, 19.5, 3), (4, 25.5, 8)), fin_art, mirror=True),
            part('fin2', ((3, 22.5, 8), (4, 25.5, 10)), fin_art, mirror=True),
            _star_hub()]


def _star_hub():
    """The spin bone's cube: hidden inside the body (the game draws the nether star at the bone's pivot)."""
    h = part('hub', ((-0.5, 21, 3.5), (0.5, 22, 4.5)), hub)
    h['bone'] = 'star_core'
    return h


# ---------------------------------------------------------------- round 20: a fresh start, built as the other engines are
# User, 2026-11-16: "I don't like what we have currently. Let's start from scratch, do something more similar to the
# firebox and tidal engines." So the reactor is built the way they are: the chest's element (the lens, picked in round 3)
# with four glass lines out of it, two over the shoulders and two round the waist (the heart's harness routing, drawn
# by frame_sea_art's code in violet), into a steel back body painted in their housings' vocabulary (a lit shoulder,
# ink foot, steel left column, ink right column, straps, bolts), the light only the star's violet.
# Three backs (knob STAR): C a core block (the firebox's blower: one flat block, the star in a porthole), D a containment
# column (the tidal engine turned inside out: one tall cell in the middle, two charge cells beside it), E a beacon case
# (an obsidian base, a steel case round a pane of beacon glass, the beam up it).
STYLE20 = dict(HR=0.75, tube=('%', '*', '='), band=('g', 'e'), bubbles=True, spark='&')


def housing(f, w, h):
    """Any face of a steel housing: the side faces as the tidal tanks', the top lit at its front, the bottom ink."""
    if f == 'up': return top(w, h)
    if f == 'down': return bottom(w, h)
    return plate(w, h)


def star4(g, cx, cy, r):
    """The nether star as it reads at this size: a bright centre, four arms (lit, then mid), the diagonals mid."""
    for j in range(len(g)):
        for i in range(len(g[0])):
            dx, dy = abs(i + 0.5 - cx), abs(j + 0.5 - cy)
            if dx < 1 and dy < 1: g[j][i] = '&'
            elif (dx < 1 and dy < r) or (dy < 1 and dx < r): g[j][i] = '%' if max(dx, dy) < r - 1 else '*'
            elif dx < 2 and dy < 2: g[j][i] = '*'


def bolts(g, inset=1, c='h'):
    w, h = len(g[0]), len(g)
    for i, j in ((inset, inset + 1), (w - 1 - inset, inset + 1), (inset, h - 2 - inset), (w - 1 - inset, h - 2 - inset)):
        g[j][i] = c


def cells(g, i0, i1, j0, n, step=2):
    """A charge bar: n cells from j0 down (a lit row over a mid row each), ink between them and round them."""
    for k in range(n):
        j = j0 + k * (step + 1)
        for i in range(i0, i1):
            g[j][i] = '%'
            for jj in range(j + 1, j + step): g[jj][i] = '*'
            g[j + step][i] = 'X'
        if k == 0:
            for i in range(i0, i1): g[j - 1][i] = 'X'
    for j in range(j0 - 1, j0 + n * (step + 1)):
        if i0 - 1 >= 0: g[j][i0 - 1] = 'X'
        if i1 < len(g[0]): g[j][i1] = 'X'


def core_block(st):
    """C: the blower's block (10 x 8 x 2.5, flat on the back), its back the star in a porthole between two charge bars,
    an emitter bar on its top (vent slots: the motes rise out of it), the lines into its sides as the hoses go into the
    blower's."""
    X, Y0, Y1, Z1 = (2.5 if PYLONS else 5), 16, 24, 5.5
    W, H, D = round(2 * X * K), 16, 5

    def block(f, w, h):
        g = housing(f, w, h)
        if f != 'south': return g
        if PYLONS:                                                   # the porthole fills the narrow block
            disc(g, w / 2, 8, 5, 'X')
            disc(g, w / 2, 8, 4.6, '=', ring='h', rw=1)
            disc(g, w / 2, 8, 3.6, '=', ring='*', rw=0.8)
            star4(g, w / 2, 8, 3)
            return g
        disc(g, 10, 8, 6, 'X')
        disc(g, 10, 8, 5.4, '=', ring='h', rw=1)                     # the porthole: a steel ring, deep glass
        disc(g, 10, 8, 4.4, '=', ring='*', rw=0.8)
        star4(g, 10, 8, 3.5)
        cells(g, 1, 3, 4, 3)
        cells(g, w - 3, w - 1, 4, 3)
        return g
    b = part('block', ((-X, Y0, TZ0), (X, Y1, Z1)), block)
    if PYLONS:
        return [b, part('emitter', ((-2, Y1, 3.5), (2, Y1 + 1.5, Z1)), emitter_art)] + pylons(st, 17, 25), 5.5, 22.25, 18.75, 25
    sea.inlets(st, b['faces'], D, H, Y1, (22, 18.25))
    return [b, part('emitter', ((-3, Y1, 3.5), (3, Y1 + 1.5, Z1)), emitter_art)], X, 22, 18.25, Y1


def emitter_art(f, w, h):
    if True:
        if f == 'up':
            g = grid(w, h, 'N'); g[0] = ['O'] * w
            for i in range(2, w - 2, 3): g[h // 2][i] = g[h // 2][i + 1] = '='   # the vent slots on top
            return g
        if f == 'down': return bottom(w, h)
        g = [['g'] * w] + [['N'] * w for _ in range(h - 2)] + [['X'] * w]
        if f == 'south':
            for i in range(2, w - 2, 3): g[1][i] = g[1][i + 1] = '*'
        return g


def column(st):
    """D: one tall containment cell in the middle (4 x 9 x 3, steel straps, a window of violet light with the star near
    its top, an emitter valve on its top), a charge cell either side (2.5 x 8 x 2.5, a bar of four cells), glass links
    between them; the lines into the charge cells' sides, as the tidal engine's into its tanks."""
    P = []
    def cell(f, w, h):
        g = housing(f, w, h)
        if f in ('north', 'south', 'east', 'west'):
            for j0 in (3, h - 5): g[j0], g[j0 + 1] = ['h'] * w, ['e'] * w      # two steel straps
        if f == 'south':
            for j in range(6, h - 6):
                for i in range(2, w - 2):
                    t = (j - 6) / max(1, h - 13)
                    g[j][i] = '%' if t < 0.3 else '*' if t < 0.7 else '='
                g[j][1], g[j][w - 2] = 'X', 'X'
            g[5] = ['O'] + ['X'] * (w - 2) + ['X']; g[h - 6] = ['O'] + ['X'] * (w - 2) + ['X']
            star4(g, w / 2, 9, 2.5)
        return g
    P.append(part('cell', ((-2, 16, TZ0), (2, 25, 6)), cell))
    def valve(f, w, h):
        if f == 'up':
            g = grid(w, h, 'X'); g[h // 2][w // 2 - 1] = g[h // 2][w // 2] = '&'; return g
        return chrome(w, h)
    P.append(part('valve', ((-0.5, 25, 4.5), (0.5, 26.5, 5.5)), valve))
    def charge(f, w, h):
        g = housing(f, w, h)
        if f == 'south': cells(g, 1, w - 1, 3, 4)
        return g
    c = part('charge', ((3, 17, TZ0), (5.5, 25, 5.5)), charge, mirror=True)
    sea.inlets(st, c['faces'], 5, 16, 25, (22.25, 18.75))
    P.append(c)
    for k, y in enumerate((18.5, 22)):
        P.append(part(f'link{k}', ((2, y, 3.5), (3, y + 1, 4.5)),
                      lambda f, w, h: [['%'] * w for _ in range(h)] if f in ('north', 'south') else [['*'] * w for _ in range(h)], mirror=True))
    return P, 5.5, 22.25, 18.75, 25


def beacon(st):
    """E: Minecraft's beacon on a back: an obsidian base slab, a steel case (8 x 6.5 x 3) round a pane of beacon glass,
    the beam a lit column up its middle through the star, an obsidian rim on top with the beam's hole (the motes)."""
    P = []
    def base(f, w, h):
        g = [['8'] * w for _ in range(h)]
        if f != 'down': g[0] = ['9'] * w
        if f in ('north', 'south', 'east', 'west'): g[-1] = ['$'] * w
        return g
    CX = 2.5 if PYLONS else 4
    # round 22 (user): no obsidian base under the pylons' version ("remove the bottom bar")
    if not PYLONS: P.append(part('base', ((-4, 16, TZ0), (4, 17.5, 6)), base))
    b = 1 if PYLONS else 2                                                 # the steel round the pane
    def case(f, w, h):
        g = housing(f, w, h)
        if f != 'south': return g
        for j in range(2, h - 2):
            for i in range(b, w - b):
                g[j][i] = 'X' if i in (b, w - 1 - b) or j in (2, h - 3) else '='
        for j in range(3, h - 3):
            for i in range(b + 1, w - b - 1):
                if (i + j) % 5 == 0: g[j][i] = '*'                         # the glass's glints
            g[j][w // 2 - 1] = g[j][w // 2] = '%'                            # the beam
        star4(g, w / 2, h / 2 - 0.5, 3)
        if not PYLONS: bolts(g, 0, 'h')
        return g
    c = part('case', ((-CX, 17.5, TZ0), (CX, 24, 6)), case)
    sea.inlets(st, c['faces'], 6, 13, 24, (22.25, 18.75) if PYLONS else (22, 18.75))
    P.append(c)
    def rim(f, w, h):
        g = [['8'] * w for _ in range(h)]
        if f == 'up':
            g[0] = ['9'] * w
            for j in range(h // 2 - 1, h // 2 + 1): g[j][w // 2 - 1] = g[j][w // 2] = '&'
        elif f != 'down': g[0] = ['9'] * w; g[-1] = ['$'] * w
        return g
    P.append(part('rim', ((-(CX - 0.5), 24, 3.5), (CX - 0.5, 25, 5.5)), rim))
    # round 22 (user: "make the pylons more forward and painted on the back and outer side as well"): the pylons 1 px
    # deeper (z 3 .. 6.5, 0.5 px proud of the case's back), their cells on the outer side too
    # round 23 (user: "you extend the pylons instead of detaching them from the back"): back to 2.5 px deep, moved 1 px
    # off the back instead (z 4 .. 6.5), on the links; the lines on the back run on under them to their inlets (no clip)
    # round 24 (user: "the cables should connect to the body and not the pylons, and currently they don't connect to
    # anything"): the lines run on the back under the pylons and across the gap into the case's sides (inlets in its
    # front 1 px, as the blower's); the pylons' outer sides carry their full bar of cells
    if PYLONS: return P + pylons(st, 17.5, 25.5, z0=4, z1=6.5, side_cells=True, inlets=False), 2.5, 22.25, 18.75, 24
    return P, 4, 22, 18.75, 24


# Round 21 (user, 2026-11-16: "discard D, but try giving its pylons to C and E"): knob STAR_PYLONS=1 stands D's charge
# cells (the pylons: 2.5 px wide, a bar of four lit cells, glass links in to the middle) either side of C's block and E's
# case, which narrow to 5 px (x +-2.5) to make room inside the chest's width; the lines go into the pylons' sides as
# they went into D's.
PYLONS = os.environ.get('STAR_PYLONS') == '1'


def pylons(st, y0, y1, links=(18.5, 22), centres=(22.25, 18.75), inner=3, z1=5.5, side_cells=False, z0=None, inlets=True):
    """side_cells: the bar of cells painted on the outer side too (round 22, user), behind the lines' inlets.
    inlets: the lines go into the pylons' sides (D's way); False: into the middle body's (round 24).
    z0: the pylon's front; past the back's plane (TZ0) it stands off the back, held by the glass links (round 23)."""
    z0 = TZ0 if z0 is None else z0
    D = round((z1 - z0) * K)
    def charge(f, w, h):
        g = housing(f, w, h)
        if f == 'south': cells(g, 1, w - 1, 3, 4)
        if f == 'east' and side_cells:                                  # east columns back -> front: the cells at the back
            cells(g, 1, D - 2 if inlets else D - 1, 3, 4)
        return g
    c = part('pylon', ((inner, y0, z0), (inner + 2.5, y1, z1)), charge, mirror=True)
    if inlets: sea.inlets(st, c['faces'], D, round((y1 - y0) * K), y1, centres)
    # the 0.5 px gap between the pylon and the middle: a dark web at its back, so the frame's teal doesn't show through
    # (with inlets=False the lines cross the gap into the middle body: the web is painted into the back's line decal
    # instead, under them; see webbed())
    P = [c] + ([part('web', ((2.5, y0, TZ0), (inner, y1 - 1, 3.5)), lambda f, w, h: grid(w, h, 'X'), mirror=True)] if inlets else [])
    for k, y in enumerate(links):
        lz = max(3.5, z0 + 0.5)
        P.append(part(f'link{k}', ((2.5, y, lz), (inner, y + 1, lz + 1)),
                      lambda f, w, h: [['%'] * w for _ in range(h)] if f in ('north', 'south') else [['*'] * w for _ in range(h)], mirror=True))
    return P


TZ0 = 3
BACKS20 = {'C': core_block, 'D': column, 'E': beacon}


def webbed(p, x0=2.5, x1=3, y0=17.5, y1=24.5):
    """The pylons' gap web painted dark into a back line decal (harness_back) wherever no line crosses it."""
    (bx0, _, _), (_, by1, _) = p['box']
    g = p['faces']['south']
    for j, row in enumerate(g):
        for i, c in enumerate(row):
            x, y = abs(bx0 + (i + 0.5) / K), by1 - (j + 0.5) / K
            if c == '.' and x0 <= x < x1 and y0 <= y < y1: row[i] = 'X'
    return p


def build20(design, chest_x=6.0):
    st = STYLE20
    back, pack_x, up_c, low_c, pack_top = BACKS20[design](st)
    cx = min(6, chest_x)
    sx = sea.side(cx)[0]
    lens = sea.element(lens_glyph())
    open_ = [sea.harness(st, cx, lens, 2.0, 2.5, low_c), sea.strip_top(st, cx), sea.strip_side(st, cx, low_c),
             sea.harness_back(st, cx, pack_x, up_c, low_c, pack_top)]
    armoured = [sea.bezel(lens), sea.harness_low(st, low_c, sx), sea.strip_side(st, cx, low_c),
                sea.harness_back(st, cx, pack_x, up_c, low_c, pack_top, low_only=True)]
    if PYLONS and design == 'E':
        for p in open_ + armoured:
            if p['name'] == 'harness_back': webbed(p)
    return back, open_, armoured


BACKS = {'A': chain, 'B': jetpack}


def build(design='B', chest_x=6.0):
    """(back parts, open front, armoured front); frame_model.py prefixes them (rb_ / ro_ / ra_)."""
    if design in BACKS20: return build20(design, chest_x)
    glyph = sea.element(lens_glyph())
    return BACKS[design](), [glyph_plate(glyph)], [sea.bezel(glyph)]
