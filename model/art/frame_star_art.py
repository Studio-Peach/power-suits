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


# Round 5, see the docstring. The housing is a shell: z 3 .. 7 (4 px out of the back), the window x +-3 (C: +-2).
BONE_ORIGIN = {'star_core': (0, 21, 5.25), 'star_orbit': (0, 21, 5.25)}   # raw; the spin pivots (the window's middle)


def inner(w, h, vertical=False):
    """A window wall: the accelerator's coil, a violet line every third texel across a dark liner."""
    g = grid(w, h, 'X')
    for j in range(h):
        for i in range(w):
            k = j if vertical else i
            if k % 3 == 1: g[j][i] = '*'
            if k % 3 == 2: g[j][i] = '='
    return g


def target(w, h):
    """The plate behind the star: concentric squares of dim light round a cross, seen through the window."""
    g = grid(w, h, 'X')
    for j in range(h):
        for i in range(w):
            r = min(i, j, w - 1 - i, h - 1 - j)
            if r % 3 == 1: g[j][i] = '='
            if abs(i - (w - 1) / 2) < 0.6 or abs(j - (h - 1) / 2) < 0.6: g[j][i] = '*'
    return g


def shell(wx, y0, y1):
    """The housing round a window x +-wx, raw y y0 .. y1 (its sides mirrored): back plate, top, bottom, sides."""
    P = []
    def plate(f, w, h):
        if f == 'south': return target(w, h)
        g = grid(w, h, 'X'); return g
    P.append(part('plate', ((-4.5, 16, 3), (4.5, 25.5, 3.5)), plate))
    def bar(role):
        def paint(f, w, h):
            g = housing(f, w, h)
            if f == 'south':
                bolts(g, ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)))
                if role == 'bottom': vents(g, 2, h - 2, 3, w - 3)
            if f == 'down' and role == 'top': return inner(w, h, vertical=True)
            if f == 'up' and role == 'bottom': return inner(w, h, vertical=True)
            return g
        return paint
    P.append(part('top', ((-4.5, y1, 3.5), (4.5, 25.5, 7)), bar('top')))
    P.append(part('bottom', ((-4.5, 16, 3.5), (4.5, y0, 7)), bar('bottom')))
    def side(f, w, h):
        if f == 'west': return inner(w, h)                                     # the wall facing the window (a mirrored part's inner)
        return housing(f, w, h)
    P.append(part('side', ((wx, y0, 3.5), (4.5, y1, 7)), side, mirror=True))
    return P


def gem(size, spin_x=False):
    def paint(f, w, h):
        g = grid(w, h, '*')
        for j in range(h):
            for i in range(w):
                d = max(abs(i + 0.5 - w / 2), abs(j + 0.5 - h / 2))
                g[j][i] = '&' if d < 1 else '%' if d < 1.8 else '*' if d < 2.8 else '='
        if f == 'up': return grid(w, h, '%')
        if f == 'down': return grid(w, h, '=')
        return g
    return paint


def accelerator(design):
    P = []
    cx, cy, cz = BONE_ORIGIN['star_core']
    if design in ('A', 'B'):
        P += shell(3, 18.5, 23.5)
    else:
        P += shell(2, 17.5, 24.5)
    def bone(p, name):
        p['bone'] = name
        return p
    if design == 'A':
        for rot in ([0, 45, 0], [45, 0, 0]):
            P.append(bone(part(f'gem{rot[0] and 1 or 0}', ((-1.25, cy - 1.25, cz - 1.25), (1.25, cy + 1.25, cz + 1.25)), gem(2.5),
                               rot=rot, origin=(cx, cy, cz)), 'star_core'))
    elif design == 'B':
        P.append(bone(part('heart', ((-0.75, cy - 0.75, cz - 0.75), (0.75, cy + 0.75, cz + 0.75)), gem(1.5), rot=[0, 45, 0],
                           origin=(cx, cy, cz)), 'star_core'))
        P.append(bone(part('bead', ((1.5, cy - 0.5, cz - 0.5), (2.5, cy + 0.5, cz + 0.5)), gem(1), mirror=True), 'star_orbit'))
    else:
        for k, y in enumerate((18.75, 21, 23.25)):
            P.append(bone(part(f'gem{k}', ((-1, y - 1, cz - 1), (1, y + 1, cz + 1)), gem(2), rot=[0, 45, 0], origin=(0, y, cz)),
                          'star_core'))
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


BACKS = {k: (lambda k=k: accelerator(k)) for k in 'ABC'}


def build(design, chest_x=6.0):
    """(back parts, open front, armoured front); frame_model.py prefixes them (rb_ / ro_ / ra_)."""
    glyph = sea.element(lens_glyph())
    return BACKS[design](), [glyph_plate(glyph)], [sea.bezel(glyph)]
