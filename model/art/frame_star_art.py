"""The star reactor for the frame (frame_model.py, draft knob STAR=A|B|C), 2026-11-16, after the tidal engine's diver
(frame_sea_art.py): the user's rule for the engines, "the light and particles are good but they shouldn't follow the
firebox's shape": a 3D component on the back and flat painted decals on the front.

Round 1 (A crystal in a cage / B halo ring / C pylon) was too much: "a bit simpler, more minimal ... an arc reactor
vibe, the power of the sun in the palm of my hand". Round 2 (a stepped disc: A arc / B sun / C palm, commit "Star reactor
drafts round 2") the user liked the front of C (the lens, no lines) but: "these backs are too far out there. Make them
look more grounded in technology, and don't do wheels anymore". Round 3 (this): the front is C's lens glyph on the
chest (open: on the chest; under the breastplate: in a steel ring), no lines; the back is a plain piece of equipment in
gunmetal and steel (the firebox's and the blower's materials) with the reactor's violet glass as its only light:
  A cell     one housing: a rectangular window over the lit cells, vent slits below, a finned cap on top.
  B module   two stepped blocks: vents and bolts below, a smaller core module over it with a long glass window.
  C fins     a radiator: a lit core bar between five vertical steel fins, a base and a cap.
Light: the glass is the letters & % * = (lit: EXTRA; in the texture dark reserved colours, STAR_DARK, lit by a glowmask
as the sea engine's); STAR_GLOW=lit paints it lit for a review. $ 8 9 (obsidian) are no longer used.

Coordinates raw (frame_model.py adds FY), right side +x, front -z, back +z; 2 texels per px. Faces as frame_sea_art.py.
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


def cell_back():
    P = []
    def box(f, w, h):                                                         # 9 x 8 x 2.5: 18 x 16 texels on the back
        g = housing(f, w, h)
        if f == 'south':
            win = glass(12, 7)
            for j in range(7):
                for i in range(12): g[3 + j][3 + i] = win[j][i]
            for i in range(2, 16): g[2][i] = g[10][i] = 'X'                  # the frame
            for j in range(2, 11): g[j][2] = g[j][15] = 'X'
            for i in (6, 11):                                                # cell dividers
                for j in range(3, 10): g[j][i] = '='
            vents(g, 12, 15, 2, 16)
            bolts(g, ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)))
        return g
    P.append(part('box', ((-4.5, 16, 3), (4.5, 24, 5.5)), box))
    def fins(f, w, h):                                                        # the cap: finned
        if f in ('up', 'down'): return grid(w, h, 'g' if f == 'up' else 'X')
        g = [['h' if i % 2 == 0 else 'p' for i in range(w)] for _ in range(h)]
        for i in range(w): g[0][i] = 'g' if i % 2 == 0 else 'e'
        return g
    P.append(part('fins', ((-3.5, 24, 3.5), (3.5, 25.5, 5)), fins))
    return P


def module_back():
    P = []
    def lower(f, w, h):                                                       # 9 x 5 x 2.5
        g = housing(f, w, h)
        if f == 'south':
            vents(g, 3, 9, 2, 16)
            bolts(g, ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)))
        return g
    P.append(part('base', ((-4.5, 16, 3), (4.5, 21, 5.5)), lower))
    def core(f, w, h):                                                        # 6 x 4 x 2: 12 x 8 on the back
        g = housing(f, w, h, base='O', top='W', bottom='X')
        if f == 'south':
            win = glass(10, 4)
            for j in range(4):
                for i in range(10): g[2 + j][1 + i] = win[j][i]
            for i in range(0, w): g[1][i] = 'X'
            for i in range(0, w): g[h - 2][i] = 'X'
        return g
    P.append(part('core', ((-3, 21, 3), (3, 25, 5)), core))
    def band(f, w, h):                                                        # a steel clamp band round the base, 0.5 proud
        return [['h'] * w] + [['e'] * w for _ in range(h - 1)] if f in ('south', 'north') else grid(w, h, 'e')
    P.append(part('band', ((-4.5, 17.5, 5.5), (4.5, 18.5, 6)), band))
    return P


def fin_back():
    P = []
    def plate(f, w, h):
        return housing(f, w, h)
    P.append(part('base', ((-4.5, 16, 3), (4.5, 18, 5.5)), plate))
    P.append(part('cap', ((-4.5, 24, 3), (4.5, 25.5, 5.5)), plate))
    def core(f, w, h):                                                        # the lit bar the fins stand on: 8 x 6 x 1.5
        g = [['X'] * w for _ in range(h)]
        if f == 'south':
            for j in range(1, h - 1):
                for i in range(w):
                    g[j][i] = '*' if j in (1, h - 2) else '%' if j in (2, h - 3) else '&'
        return g
    P.append(part('core', ((-4, 18, 3), (4, 24, 4.5)), core))
    def fin(f, w, h):
        if f == 'up': return grid(w, h, 'g')
        if f == 'down': return grid(w, h, 'X')
        g = [['h'] * w for _ in range(h)]
        for j in range(h): g[j][0] = 'w' if f in ('north', 'south') else 'g'
        g[0] = ['g'] * w
        return g
    for k, x in enumerate((0.25, 1.75, 3.25)):                               # five fins: the middle, two pairs
        P.append(part(f'fin{k}', ((x - 0.5, 18, 4.5), (x, 24, 6.5)), fin, mirror=k > 0))
    return P


BACKS = {'A': cell_back, 'B': module_back, 'C': fin_back}


def disc_back(design, st):
    return BACKS[design](), 4.5, 21.5, 18.5, 25.5


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


def build(design, chest_x=6.0):
    """(back parts, open front, armoured front); frame_model.py prefixes them (rb_ / ro_ / ra_)."""
    glyph = sea.element(lens_glyph())
    return BACKS[design](), [glyph_plate(glyph)], [sea.bezel(glyph)]
