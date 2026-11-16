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


# Round 4 (user: "I like A the best, but iterate on top of that concept further; I also don't like the steel cap on
# top"): the cell housing without its finned cap, up to the helmet's bottom (raw y 25.5), three ways to take it on:
#   A plain    the housing, a big framed window of three cells, vent slits below, bolts, side vent slits: nothing else;
#   B framed   the window raised on its own 0.5 px frame (a second box) so the glass sits proud of the housing, a row of
#              three status lamps over it, two latches down the sides, vents below;
#   C meter    the window as four charge bars (columns of glass of rising height) with a row of lamps below it, the
#              housing's side vents deeper.
def lamps(g, row, cols, c='&'):
    for i in cols:
        g[row][i] = c
        g[row][i + 1] = '%'


def cell_back(design):
    P = []
    W, H = 18, 19                                                             # the housing: 9 x 9.5 x 2.5 (back face)
    def box(f, w, h):
        g = housing(f, w, h)
        if f == 'south':
            if design == 'A':
                win = glass(12, 9)
                for j in range(9):
                    for i in range(12): g[3 + j][3 + i] = win[j][i]
                for i in range(2, 16): g[2][i] = g[12][i] = 'X'
                for j in range(2, 13): g[j][2] = g[j][15] = 'X'
                for i in (6, 11):
                    for j in range(3, 12): g[j][i] = '='
                vents(g, 14, 18, 2, 16)
            elif design == 'B':
                for j in range(2, 4): g[j] = ['N'] * w                         # the lamps' row
                lamps(g, 3, (5, 8, 11))
                vents(g, 15, 18, 2, 16)
                for i in range(2, 16): g[5][i] = 'X'                           # a recess the frame sits in
            else:
                win = grid(12, 9, '=')
                for k, hgt in enumerate((3, 5, 7, 9)):                         # four bars, rising
                    for j in range(9):
                        for i in range(3 * k, 3 * k + 3):
                            if i % 3 == 2 and k < 3: win[j][i] = 'X'
                            elif 9 - j <= hgt: win[j][i] = '&' if 9 - j == hgt else '%' if 9 - j > hgt - 3 else '*'
                for j in range(9):
                    for i in range(12): g[3 + j][3 + i] = win[j][i]
                for i in range(2, 16): g[2][i] = g[12][i] = 'X'
                for j in range(2, 13): g[j][2] = g[j][15] = 'X'
                lamps(g, 14, (4, 7, 10, 13))
                vents(g, 16, 19, 2, 16)
            bolts(g, ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)))
        if f in ('east', 'west'):                                              # side vents (C: deeper) and, B, a latch
            vents(g, 6, 13 if design != 'C' else 15, 1, w - 1)
            if design == 'B':
                for j in range(h - 8, h - 3):
                    for i in (2, 3): g[j][i] = 'h' if i == 2 else 'e'
        return g
    P.append(part('box', ((-4.5, 16, 3), (4.5, 25.5, 5.5)), box))
    if design == 'B':
        def frame(f, w, h):                                                    # 7 x 5.5 x 0.5: the glass in a proud frame
            g = [['O'] * w for _ in range(h)]
            if f == 'south':
                win = glass(w - 4, h - 4)
                for j in range(h - 4):
                    for i in range(w - 4): g[2 + j][2 + i] = win[j][i]
                for i in range(w - 4):
                    if i in ((w - 4) // 3, 2 * (w - 4) // 3): 
                        for j in range(1, h - 5): g[2 + j][2 + i] = '='
                for i in range(1, w - 1): g[1][i] = g[h - 2][i] = 'X'
                for j in range(1, h - 1): g[j][1] = g[j][w - 2] = 'X'
            return g
        P.append(part('window', ((-3.5, 18.5, 5.5), (3.5, 24, 6)), frame))
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


BACKS = {k: (lambda k=k: cell_back(k)) for k in 'ABC'}


def build(design, chest_x=6.0):
    """(back parts, open front, armoured front); frame_model.py prefixes them (rb_ / ro_ / ra_)."""
    glyph = sea.element(lens_glyph())
    return BACKS[design](), [glyph_plate(glyph)], [sea.bezel(glyph)]
