"""The star reactor for the frame (frame_model.py, draft knob STAR=A|B|C), 2026-11-16, after the tidal engine's diver
(frame_sea_art.py): the user's rule for the engines, "the light and particles are good but they shouldn't follow the
firebox's shape": a 3D component on the back and flat painted decals on the front.

Round 1 (commit "Star reactor drafts", A crystal in a cage / B halo ring / C pylon with three cells) was too much:
"a bit simpler, more minimal ... maybe an arc reactor vibe. After all, it is a star ... the power of the sun in the
palm of my hand". Round 2, all of them a single round plate on the back (a stepped disc, boxes at one depth) with its
light painted, a glyph of the same on the chest, and as few lines as possible:
  A arc    the arc reactor: a stepped disc with a lit ring, a dark coil band and a glass lens standing out of its middle;
           on the chest the same as a ring glyph; one thin line pair over the shoulders joins them (nothing at the waist).
  B sun    a smaller disc, a white core and eight rays painted out of it; a four-pointed glyph on the chest; no lines.
  C palm   the least: a small disc with only a lens and one ring; the chest glyph the same; no lines.
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


# ---------------------------------------------------------------- the back: a stepped disc
# Boxes at one depth (z 3 .. 4.5) whose back faces paint one picture by world coordinates (so the steps read as a
# disc); the middle is raised by a lens or a core. Centre (0, 20.5).
CY = 20.5


def disc_paint(design):
    def at(x, y):
        d = math.hypot(x, y - CY)
        a = math.atan2(y - CY, x)
        if design == 'A':
            if d < 2.0: return '$'                                              # under the lens
            if d < 3.0: return '9' if int((a + math.pi) / (math.pi / 5)) % 2 else '$'   # the coils
            if d < 3.4: return '$'
            if d < 4.4: return '%' if d < 4.0 else '*'                          # the lit ring
            return '9' if d < 4.9 else '8'
        if design == 'B':
            if d < 1.3: return '&'
            if d < 2.0: return '%'
            ray = abs(math.sin(4 * a)) > 0.93 and d < 4.2
            if ray: return '%' if d < 3.0 else '*'
            return '9' if d >= 4.3 else '$'
        if d < 1.4: return '&'
        if d < 2.0: return '*'
        return '9' if d >= 2.3 else '$'
    return at


def disc_back(design, st):
    at = disc_paint(design)
    # (half width, y0, y1) of each box: the steps of the disc
    steps = {'A': [(5, 18, 23), (4, 17, 24), (2.5, 16, 25)],
             'B': [(4, 18, 23), (3, 17, 24), (2, 16.5, 24.5)],
             'C': [(2.5, 18, 23), (2, 17.5, 23.5)]}[design]
    P = []
    for k, (hx, y0, y1) in enumerate(steps):
        def paint(f, w, h, hx=hx, y0=y0, y1=y1):
            if f == 'south': return [[at(-hx + (i + 0.5) / K, y1 - (j + 0.5) / K) for i in range(w)] for j in range(h)]
            g = [['8'] * w for _ in range(h)]
            g[0] = ['9'] * w
            return g
        p = part(f'disc{k}', ((-hx, y0, 3), (hx, y1, 4.5)), paint)
        P.append(p)
    if design == 'A':                                                           # the wide box takes the line in
        sea.inlets(st, P[0]['faces'], 3, 10, 23, (21.5,))
    def lens(f, w, h):
        if f == 'south':
            g = grid(w, h, '*')
            disc(g, w / 2, h / 2, w / 2, '&', ring='%', rw=1)
            return g
        return grid(w, h, '*' if f != 'up' else '%')
    if design == 'A': P.append(part('lens', ((-1.5, CY - 1.5, 4.5), (1.5, CY + 1.5, 5)), lens))
    if design == 'B': P.append(part('core', ((-1, CY - 1, 4.5), (1, CY + 1, 5)), lens))
    if design == 'C': P.append(part('lens', ((-1.5, CY - 1.5, 4.5), (1.5, CY + 1.5, 5.5)), lens))
    return P, {'A': 5, 'B': 4, 'C': 2.5}[design], 21.5, 18.5, 25.5


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
    st = STYLE
    back, pack_x, up_c, low_c, pack_top = disc_back(design, st)
    cx = min(6, chest_x)
    glyph = sea.element(GLYPHS[design]())
    if design == 'A':   # one thin pair over the shoulders into the disc; under the breastplate only the glyph
        open_ = [sea.harness(st, cx, glyph, 2.0, 2.5, low_c, lows=False), sea.strip_top(st, cx),
                 sea.harness_back(st, cx, pack_x, up_c, low_c, pack_top, lows=False)]
    else:
        open_ = [glyph_plate(glyph)]
    armoured = [sea.bezel(glyph)]
    return back, open_, armoured
