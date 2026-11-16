"""The star reactor for the frame (frame_model.py, draft knob STAR=A|B|C), 2026-11-16, after the tidal engine's diver
(frame_sea_art.py): the user's rule for the engines, "the light and particles are good but they shouldn't follow the
firebox's shape": a 3D component on the back and flat painted decals on the front.

Round 1 (A crystal in a cage / B halo ring / C pylon) was too much: "a bit simpler, more minimal ... an arc reactor
vibe, the power of the sun in the palm of my hand". Round 2 (a stepped disc: A arc / B sun / C palm, commit "Star reactor
drafts round 2") the user liked the front of C (the lens, no lines) but: "these backs are too far out there. Make them
look more grounded in technology, and don't do wheels anymore". Round 3 (this): the front is C's lens glyph on the
chest (open: on the chest; under the breastplate: in a steel ring), no lines; the back is a plain piece of equipment in
gunmetal and steel (the firebox's and the blower's materials) with the reactor's violet glass as its only light:
  (the three of round 3: A cell housing with a finned cap, B two stepped blocks, C a radiator of fins; A picked.)
Round 4 (user: "I like A the best, but iterate on top of that concept further; I also don't like the steel cap on top"):
the cell housing without its cap, up to the helmet's bottom: A plain, B the window on a proud frame with status lamps,
C four charge bars (see cell_back).
Light: the glass is the letters & % * = (lit: EXTRA; in the texture dark reserved colours, STAR_DARK, lit by a glowmask
as the sea engine's); STAR_GLOW=lit paints it lit for a review. $ 8 9 (obsidian) are no longer used.

Coordinates raw (frame_model.py adds FY), right side +x, front -z, back +z; 2 texels per px. Faces as frame_sea_art.py.

Round 5 (user: "a star accelerator sort of box where we could interpret the star spinning ... this will be the endgame
engine, so it has to look cool as heck"): the cell housing becomes a containment box with an open window onto a star
that spins (a bone turned by code, like the chaingun's barrels: ToolRotors; bones star_core / star_orbit, pivots
BONE_ORIGIN), in a hollow shell (back plate, four bars; the inner walls and the plate behind painted as the
accelerator's coils and a target):
  A gyro     two gems (cubes turned 45 deg about y and x) as one star, spinning about the vertical axis;
  B orbit    a small steady core and two beads that orbit it (a particle in the accelerator);
  C column   a narrow tall window and a stack of three small spinning gems.

Round 6 (user: "lean into the exoskeleton vibe for the back ... do you know what a Sandevistan is?" The Cyberpunk 2077 /
Edgerunners spinal implant: chrome vertebrae down the back, a lit seam between them, afterimages when it runs; "yes, do
it"): the accelerator box is dropped for a spine, vertebrae (boxes, the lit rod showing in the gaps between them) from
under the helmet to the waist, in the iron's chrome:
  A bare     five vertebrae, each with a spinous process pointing back, the rod glowing in the gaps;
  B plated   the spine under a slim plated housing: a ridge of segments over a base plate, the seams glowing as slits;
  C braced   A's spine with exoskeleton bracing: ribs out of every vertebra and two struts up to the shoulders.
Round 7 (user: "make them look more mechanical and less boney, this isn't a horror mod"): no spinous processes, no
white chrome, no ribs. Machined parts in gunmetal and steel, bolts, clamps, hydraulics, the light in slits and a rod:
  A stack    five machined modules, each a bezel round a lit slit, a lit rod in the gaps, two steel guide rods either side
             through collars;
  B rail     a base plate with a raised rail down it, a continuous lit channel in the rail and steel clamps across it;
  C rams     A's stack with two hydraulic rams either side (barrel, lit strip, rod) and brackets, the exoskeleton.
Round 8 (user: "drop the white tones and make it more slick black and purple", with a photo of the prop,
blasters4masters.com sandevistan-cyberpunk-2077.jpg, .scratch/sand/ref.jpg: a chain of black wedge modules, each with
a small lit screen on its face and thin lit connectors between, round black button pods either side of every module,
a bigger boxy unit at the neck end and a rounded one at the hip end; its light green, ours violet): glossy black
(obsidian $ 8 9, violet-tinged), the light only violet, no steel:
  A chain    the prop: four wedge modules (a wide slab and a narrow ridge with its screen), a pod on a stalk either side
             of each, a head unit with a wide screen at the neck and a base unit at the hip, the lit rod joining them;
  B sleeve   the same under one slim black sleeve: a column of four screens and thin lit lines down its sides;
  C rams     A with two black hydraulic rams outside the pods (lit strip) for the exoskeleton.
The glass letters & % * = are the star's light (see above).
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


def fac(w, h, c): return grid(w, h, c)


# ---------------------------------------------------------------- front glyphs (8 x 8 texels, centred on x 0, y 23)
def arc_glyph():
    g = grid(8, 8, '.')
    disc(g, 4, 4, 4, '9', ring='$', rw=1)
    disc(g, 4, 4, 3, '%', ring='*', rw=0.8)
    disc(g, 4, 4, 2.0, '$')
    disc(g, 4, 4, 1.2, '&')
    return g


def star_glyph():
    g = grid(8, 8, '.')
    for j in range(8):
        for i in range(8):
            dx, dy = abs(i + 0.5 - 4), abs(j + 0.5 - 4)
            if dx * dy <= 1.3:
                d = dx + dy
                g[j][i] = '&' if d <= 1.5 else '%' if d <= 3 else '*'
    return g


def lens_glyph():
    g = grid(8, 8, '.')
    disc(g, 4, 4, 4, '$', ring='9', rw=1)
    disc(g, 4, 4, 3, '*')
    disc(g, 4, 4, 2, '%')
    disc(g, 4, 4, 1, '&')
    return g


GLYPHS = {'A': arc_glyph, 'B': star_glyph, 'C': lens_glyph}


# ---------------------------------------------------------------- the back: equipment
def glass(w, h, lit=True):
    """A window's glass (w x h texels): a deep edge, the cells' glow brightest along the middle row, a hot core line."""
    g = grid(w, h, '*')
    for i in range(w): g[0][i] = '='; g[h - 1][i] = '='
    mid = h // 2
    for i in range(w):
        g[mid][i] = '%'
        if h > 4: g[mid - 1][i] = '%'
    for i in range(1, w - 1): g[mid][i] = '&'
    return g


def housing(f, w, h, base='N', top='O', bottom='X'):
    g = [[base] * w for _ in range(h)]
    g[0] = [top] * w
    g[-1] = [bottom] * w
    for j in range(h): g[j][0], g[j][-1] = top if f != 'south' else 'O', 'X'
    return g


def bolts(g, pts, c='h'):
    for i, j in pts:
        if 0 <= j < len(g) and 0 <= i < len(g[0]): g[j][i] = c


def vents(g, j0, j1, i0, i1):
    for j in range(j0, j1, 2):
        for i in range(i0, i1): g[j][i] = 'X'


# Round 6, see the docstring. Raw coords: the spine runs y 16 .. 25.5 (under the helmet), five vertebrae 1.5 px tall with
# 0.5 px gaps (the lit rod shows in them), on the back from z 3.
BONE_ORIGIN = {}
VERT = [(16, 2.0), (18, 2.0), (20, 1.5), (22, 1.5), (24, 2.0)]        # (bottom y, half width): the lumbar wider, the neck narrow


def blk(f, w, h):
    """Glossy black: a violet-tinged edge light along the top and left, the base dark."""
    g = [['8'] * w for _ in range(h)]
    g[0] = ['9'] * w
    g[-1] = ['$'] * w
    for j in range(h): g[j][0] = '9' if f in ('south', 'north', 'up') else g[j][0]
    return g


def screen(w, h, wide=False):
    """A small lit screen: a row of light over a dim row, a black bezel round it."""
    def paint(f, w_, h_):
        g = blk(f, w_, h_)
        if f == 'south' and w_ >= 3 and h_ >= 2:
            for i in range(1, w_ - 1):
                g[h_ // 2 - 1][i] = '&' if i % 2 else '%'
                if h_ >= 3: g[h_ // 2][i] = '*'
        return g
    return paint


def pod(f, w, h):
    """A round button pod (a box): black with a dark slot across its face and a thin violet rim."""
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


MODS = (18, 19.5, 21, 22.5)                                              # four wedge modules, 1 px tall, 0.5 gaps


def chain():
    P = [part('rod', ((-0.5, 16, 3), (0.5, 25.5, 4.5)), rodfill)]
    def base(f, w, h):                                                   # the hip unit: rounded look, one lit bit
        g = blk(f, w, h)
        if f == 'south':
            for i in range(2, w - 2): g[h // 2][i] = '%'
        return g
    P.append(part('base', ((-2, 16, 3), (2, 17.5, 5)), base))
    def head(f, w, h):                                                   # the neck unit: a wide screen
        g = blk(f, w, h)
        if f == 'south':
            for i in range(2, w - 2):
                g[h // 2 - 1][i] = '&' if i % 2 else '%'
                g[h // 2][i] = '*'
        return g
    P.append(part('head', ((-2.5, 24, 3), (2.5, 25.5, 5.5)), head))
    for k, y in enumerate(MODS):
        P.append(part(f'slab{k}', ((-1.5, y, 3), (1.5, y + 1, 4)), blk))
        P.append(part(f'ridge{k}', ((-0.75, y, 4), (0.75, y + 1, 5)), screen(3, 2)))
        P.append(part(f'stalk{k}', ((1.5, y + 0.25, 3), (2, y + 0.75, 3.5)), blk, mirror=True))
        P.append(part(f'pod{k}', ((2, y, 3), (3.5, y + 1, 4)), pod, mirror=True))
    return P


def spine_a():
    return chain()


def spine_b():
    P = []
    def sleeve(f, w, h):
        g = blk(f, w, h)
        if f == 'south':
            for j in range(h): g[j][1] = g[j][w - 2] = '='                 # thin lit lines down its sides
            for j in range(h):
                g[j][0] = '9'
        return g
    P.append(part('sleeve', ((-2.5, 16, 3), (2.5, 25.5, 4.5)), sleeve))
    def col(f, w, h):
        g = blk(f, w, h)
        if f == 'south':
            for k in range(5):                                             # five screens down it, a dark gap between
                j = k * 4
                for jj in (j + 1, j + 2):
                    if jj < h:
                        for i in range(1, w - 1): g[jj][i] = ('&' if i % 2 else '%') if jj == j + 1 else '*'
        return g
    P.append(part('column', ((-1.5, 16, 4.5), (1.5, 25.5, 5.5)), col))
    return P


def spine_c():
    P = chain()
    def barrel(f, w, h):
        g = blk(f, w, h)
        if f in ('south', 'east'):
            for j in range(2, h - 2): g[j][w // 2] = '*'; g[j][w // 2 - 1 if w > 2 else 0] = '%'
        return g
    P.append(part('barrel', ((4, 16, 3.5), (5.5, 21, 5)), barrel, mirror=True))
    P.append(part('ram', ((4.5, 21, 4), (5, 25.5, 4.5)), blk, mirror=True))
    for k, y in enumerate((16.5, 24.5)):
        P.append(part(f'bracket{k}', ((3.5, y, 3), (5.5, y + 1, 3.5)), blk, mirror=True))
    return P


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


BACKS = {'A': spine_a, 'B': spine_b, 'C': spine_c}


def build(design, chest_x=6.0):
    """(back parts, open front, armoured front); frame_model.py prefixes them (rb_ / ro_ / ra_)."""
    glyph = sea.element(lens_glyph())
    return BACKS[design](), [glyph_plate(glyph)], [sea.bezel(glyph)]
