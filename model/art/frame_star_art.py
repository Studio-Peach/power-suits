"""The star reactor for the frame (frame_model.py, draft knob STAR=A|B|C), 2026-11-16, after the tidal engine's diver
(frame_sea_art.py): the user's rule for the engines, "the light and particles are good but they shouldn't follow the
firebox's shape": a 3D component on the back and flat painted decals on the front and sides. It reuses the sea
engine's harness (over the shoulders, down the waist, into the back body's sides) with its own paint: thin violet energy
lines with sparks, and a glyph on the chest instead of the gauge.

The big suit's reactor was a netherite housing between two upright energy canisters (twin tanks: the sea engine has
those now), the glass lit violet-white, ender particles drawn into it. Three new directions, none of them twin tanks:
  A crystal   an end-crystal-like gem (a cube turned 45 deg) floating in an obsidian cage: plinth, cap, two posts;
              front: a four-pointed star (the nether star) on the chest.
  B halo      a square obsidian ring standing off the back, a disc of violet light in it (the event horizon), concentric
              rings turning in it; front: the same rings as a glyph.
  C pylon     a tall obsidian spine with three stacked glass cells (charge) between two swept wings carrying the lines,
              a short spire on top; front: a three-cell meter.
Light: the glass is the letters & % * = (lit: EXTRA; in the texture dark reserved colours, STAR_DARK, lit by a glowmask
as the sea engine's); static obsidian is $ 8 9. STAR_GLOW=lit paints it lit for a review.

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
def star_glyph():
    g = grid(8, 8, '.')
    for j in range(8):
        for i in range(8):
            dx, dy = abs(i + 0.5 - 4), abs(j + 0.5 - 4)
            if dx * dy <= 1.3:
                d = dx + dy
                g[j][i] = '&' if d <= 1.5 else '%' if d <= 3 else '*'
    return g


def rings_glyph():
    g = grid(8, 8, '.')
    disc(g, 4, 4, 4, '$', ring='9', rw=1)
    disc(g, 4, 4, 3, '=', ring='*', rw=0.8)
    disc(g, 4, 4, 1.8, '%')
    disc(g, 4, 4, 0.9, '&')
    return g


def meter_glyph():
    g = grid(8, 8, '9')
    for i in range(8): g[0][i] = g[7][i] = '$'
    for j in range(8): g[j][0] = g[j][7] = '$'
    for j, c in ((1, '&'), (2, '&'), (4, '%'), (5, '%')):
        for i in range(1, 7): g[j][i] = c
    for i in range(1, 7): g[3][i] = g[6][i] = '$'
    return g


GLYPHS = {'A': star_glyph, 'B': rings_glyph, 'C': meter_glyph}


# ---------------------------------------------------------------- A: crystal in a cage
def crystal_back(st):
    P = []
    def plate(f, w, h):
        g = [['8'] * w for _ in range(h)]
        g[0] = ['9'] * w
        g[-1] = ['$'] * w
        if f in ('south', 'north'):
            for i in range(2, w - 2, 4): g[h // 2][i] = '*'
        return g
    P.append(part('plinth', ((-4.5, 16, 3), (4.5, 17.5, 5.5)), plate))
    P.append(part('cap', ((-4.5, 24, 3), (4.5, 25.5, 5.5)), plate))

    def post(f, w, h):
        g = [['9'] + ['8'] * (w - 2) + ['$'] for _ in range(h)]
        if f in ('south', 'east') and w >= 3:
            for j in range(1, h - 1): g[j][w // 2] = '='                    # an energy vein down it
        return g
    p = part('post', ((3.5, 17.5, 3), (4.5, 24, 4.5)), post, mirror=True)
    sea.inlets(st, p['faces'], 3, 13, 24, (21.5, 18.5))
    P.append(p)

    def gem(f, w, h):                                                         # 7 x 7 texels a face: a glowing facet
        g = grid(w, h, '*')
        for j in range(h):
            for i in range(w):
                d = max(abs(i + 0.5 - w / 2), abs(j + 0.5 - h / 2))
                g[j][i] = '&' if d < 1 else '%' if d < 2 else '*' if d < 3 else '='
        if f == 'up': return grid(w, h, '*')
        if f == 'down': return grid(w, h, '=')
        return g
    P.append(part('gem', ((-1.75, 19.5, 4), (1.75, 23, 7.5)), gem, rot=[0, 45, 0], origin=(0, 21.25, 5.75)))
    return P, 4.5, 21.5, 18.5, 25.5


# ---------------------------------------------------------------- B: halo ring
def halo_back(st):
    P = []
    def bar(f, w, h):
        g = [['8'] * w for _ in range(h)]
        g[0] = ['9'] * w
        g[-1] = ['$'] * w
        for j in range(h): g[j][0] = '9'
        return g
    P.append(part('ring_bottom', ((-4, 16, 4.5), (4, 17.5, 5.5)), bar))
    P.append(part('ring_top', ((-4, 23, 4.5), (4, 24.5, 5.5)), bar))
    s = part('ring_side', ((2.5, 17.5, 4.5), (4, 23, 5.5)), bar, mirror=True)
    sea.inlets(st, s['faces'], 2, 11, 23, (21.5, 18.5))
    P.append(s)

    def disc_(f, w, h):                                                       # the event horizon: rings turning
        if f != 'south': return grid(w, h, '=') if f != 'up' else grid(w, h, '*')
        g = grid(w, h, '=')
        for j in range(h):
            for i in range(w):
                d = math.hypot(i + 0.5 - w / 2, j + 0.5 - h / 2)
                g[j][i] = '&' if d < 1.2 else '%' if d < 2.0 else '*' if d < 3.0 else '=' if d < 3.6 else '*' if d < 4.4 else '='
        for i, j in ((1, 1), (w - 2, 2), (2, h - 2), (w - 2, h - 3)): g[j][i] = '&'          # sparks
        return g
    P.append(part('horizon', ((-2.5, 18, 3), (2.5, 23, 4)), disc_))
    return P, 4, 21.5, 18.5, 24.5


# ---------------------------------------------------------------- C: pylon with wings
def pylon_back(st):
    P = []
    def spine(f, w, h):
        g = [['8'] * w for _ in range(h)]
        g[0] = ['9'] * w
        if f == 'south':
            for c in range(3):                                                # three cells, charge rising up the middle
                j0 = 1 + c * 6
                for j in range(j0, j0 + 5):
                    for i in range(1, w - 1):
                        g[j][i] = ('&' if j == j0 else '%' if j == j0 + 1 else '*' if j < j0 + 4 else '=')
                if j0 + 5 < h: g[j0 + 5] = ['$'] * w
        elif f in ('east', 'west'):
            for j in range(1, h - 1): g[j][w // 2] = '='
        return g
    P.append(part('spine', ((-2, 16, 3), (2, 25.5, 5)), spine))

    def wing(f, w, h):
        g = [['8'] * w for _ in range(h)]
        g[0], g[-1] = ['9'] * w, ['$'] * w
        if f in ('south', 'north'):
            for i in range(1, w - 1):                                         # a swept vein, inner top to outer bottom
                j = 1 + (i - 1) * (h - 4) // max(1, w - 3)
                g[j][i] = '%'
                g[j + 1][i] = '*'
        return g
    w = part('wing', ((2, 17.5, 3), (5, 24, 4)), wing, mirror=True)
    sea.inlets(st, w['faces'], 2, 13, 24, (21.5, 18.5))
    P.append(w)

    def spire(f, w, h):
        if f == 'up': return grid(w, h, '&')
        return [['%'] * w for _ in range(h)]
    P.append(part('spire', ((-0.5, 25.5, 4.5), (0.5, 28, 5.5)), spire))
    return P, 5, 21.5, 18.5, 25.5


BACKS = {'A': crystal_back, 'B': halo_back, 'C': pylon_back}


def build(design, chest_x=6.0):
    """(back parts, open front, armoured front); frame_model.py prefixes them (rb_ / ro_ / ra_)."""
    st = STYLE
    back, pack_x, up_c, low_c, pack_top = BACKS[design](st)
    cx = min(6, chest_x)
    sx = sea.side(cx)[0]
    glyph = sea.element(GLYPHS[design]())
    open_ = [sea.harness(st, cx, glyph, 2.0, 2.5, low_c), sea.strip_top(st, cx), sea.strip_side(st, cx, low_c),
             sea.harness_back(st, cx, pack_x, up_c, low_c, pack_top)]
    armoured = [sea.bezel(glyph), sea.harness_low(st, low_c, sx), sea.strip_side(st, cx, low_c),
                sea.harness_back(st, cx, pack_x, up_c, low_c, pack_top, low_only=True)]
    return back, open_, armoured
