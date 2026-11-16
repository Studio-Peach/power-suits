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
The glass letters & % * = are the star's light (see above).
"""
import math
from frame_radial_art import part, grid, disc, K
import frame_sea_art as sea

EXTRA = {'&': (0xf4, 0xe6, 0xff),   # the core: white-violet
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


def vertebra(f, w, h):
    """A chrome vertebra: lit top edge, a centre groove down the back, a shaded base."""
    g = [['h'] * w for _ in range(h)]
    g[0] = ['w'] * w
    g[-1] = ['e'] * w
    if f in ('south', 'north'):
        for j in range(1, h - 1):
            g[j][0], g[j][-1] = 'g', 'l'
            if w >= 5: g[j][w // 2] = 'x'
    return g


def rod(f, w, h):
    g = [['*'] * w for _ in range(h)]
    if f in ('south', 'north'):
        for j in range(h):
            g[j][w // 2 - 1], g[j][w // 2] = '%', '%'
            if w >= 4 and w // 2 + 1 < w: g[j][w // 2 - 1] = g[j][w // 2] = '&'
    return g


def spine_a():
    P = [part('rod', ((-1, 16, 3), (1, 25.5, 4.5)), rod)]
    for k, (y, hw) in enumerate(VERT):
        P.append(part(f'v{k}', ((-hw, y, 3), (hw, y + 1.5, 5.5)), vertebra))
        P.append(part(f'p{k}', ((-0.5, y + 0.25, 5.5), (0.5, y + 1.25, 6.5)),
                      lambda f, w, h: [['g'] * w for _ in range(h)] if f != 'up' else grid(w, h, 'w')))
    return P


def spine_b():
    P = []
    def base(f, w, h):
        g = housing(f, w, h)
        if f == 'south':
            for k in range(4):                                              # the seams: lit slits either side of the ridge
                j = round((25.5 - (17.5 + 2 * k + 0.25)) * 2)
                for i in list(range(2, w // 2 - 2)) + list(range(w // 2 + 2, w - 2)): g[j][i] = '%'; g[j + 1][i] = '*' if j + 1 < h else g[j + 1][i]
            for i in (0, w - 1):
                for j in range(h): g[j][i] = 'X'
        return g
    P.append(part('base', ((-2.5, 16, 3), (2.5, 25.5, 4.5)), base))
    def ridge(f, w, h):
        g = [['h'] * w for _ in range(h)]
        if f in ('south', 'east', 'west'):
            for k in range(5):                                              # segments with a lit gap between
                j = round((25.5 - (16 + 2 * k)) * 2)                          # the segment's bottom row (from the top)
                for jj in range(max(0, j - 1), j):                            # (a 1-texel gap above each)
                    pass
            for k in range(4):
                j = round((25.5 - (17.5 + 2 * k)) * 2)
                if 0 <= j - 1 < h:
                    for i in range(w): g[j - 1][i] = '&'
            for j in range(h): g[j][0] = 'g' if f == 'south' else g[j][0]
        g[0] = ['w'] * w
        return g
    P.append(part('ridge', ((-1, 16, 4.5), (1, 25.5, 5.5)), ridge))
    return P


def spine_c():
    P = spine_a()
    def rib(f, w, h):
        g = [['h'] * w for _ in range(h)]
        for j in range(h): g[j][-1] = '%' if f in ('south', 'north', 'up') else g[j][-1]
        g[0] = ['w'] * w
        return g
    for k, y in enumerate((16.5, 18.5, 20.5, 22.5)):                        # a rib off every gap, 0.5 tall, out to x 4.5
        P.append(part(f'rib{k}', ((VERT[k][1] if k < 2 else 1.5, y + 1, 3), (4.5, y + 1.5, 4)), rib, mirror=True))
    def strut(f, w, h):
        g = [['g'] * w for _ in range(h)]
        for j in range(h): g[j][0], g[j][-1] = 'w', 'e'
        if f in ('south', 'north'):
            for j in range(1, h - 1, 3): g[j][w // 2] = '%'
        return g
    P.append(part('strut', ((1.5, 22.5, 4.5), (2.0, 26.5, 5.5)), strut, mirror=True, rot=[0, 0, -35], origin=(1.75, 22.5, 5)))
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
