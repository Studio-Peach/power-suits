"""The tidal (sea) engine for the frame (frame_model.py, knob SEA, on by default): its own back and front, not the
heart's. 2026-11-16, user: the tidal engine's and the star reactor's light and particles are good, but they shouldn't
follow the firebox's shape. The frame can have both a 3D component on the back and a 2D one on the front and sides.
Sea first; three directions were drafted (A diver, B conduit housing with thin circuit traces and gill slits, C
horizontal drum with a window of moving water) and the user
picked A ("it looks great"); B and C were not kept:
  back   two dark iron diving tanks with steel straps and teal level windows, a manifold between them with the Heart
         of the Sea in a porthole, link pipes, a valve on each tank (the bubbles come out of them);
  front  a dive gauge in the chest slot (open: on the chest; under the breastplate: in a steel ring, as the heart's
         core), glass water lines with bubbles and steel bands over the shoulders and down the waist into the tanks.
The lines end in the same places as the heart's harness (frame_heart_art.py), so the code is its own with another paint.

Light: the glass (letters T S y q) is the tidal glow. In the texture it holds dark reserved colours (SEA_DARK in
frame_model.py, as the fire's coals); tools/export-frame.py writes a glowmask that lights them in the teal (SEA_LIT
here), by SuitLights.getTidalGlow. SEA_GLOW=lit paints them lit for a review.

Coordinates raw (frame_model.py adds FY), right side +x, front -z, back +z; 2 texels per px (K). Faces as
frame_heart_art.py's: north / south as seen from the front / back, east back -> front, west front -> back, up rows
front -> back. Letters: frame_model.PAL, the iron ramp (lowercase) and EXTRA here (free letters only: S T j q y).
"""
import math
from frame_radial_art import part, grid, disc, K
from frame_heart_art import _seg
from frame_motor_art import chrome

EXTRA = {'T': (0xd8, 0xf6, 0xf2),   # foam / the brightest light
         'S': (0x4f, 0xe0, 0xd0),   # glass, lit
         'y': (0x1f, 0x9c, 0x98),   # glass, mid
         'q': (0x14, 0x60, 0x5f),   # glass, deep
         'j': (0x0c, 0x3a, 0x3c)}   # the water's dark / empty glass (never lit)
# The glass lit (review, SEA_GLOW=lit) is EXTRA's; in the texture its letters hold these dark reserved colours (the
# glowmask's keys, tools/export-frame.py SEA_GLOW): lit when the engine runs. Not used anywhere else in the texture.
SEA_DARK = {'T': (0x24, 0x58, 0x5e), 'S': (0x1b, 0x48, 0x4e), 'y': (0x14, 0x3a, 0x40), 'q': (0x10, 0x30, 0x36)}
TZ = 3
TOP_Y, BACK_Z = 26.5, 3.5            # the shoulder strip's face and the back plate's face (frame_heart_art)


def side(cx):                        # the waist strip's face and thickness (frame_heart_art.side)
    return (5.5, 0.5) if cx - 5 >= 1 else ((5 + cx) / 2, 0)


# ---------------------------------------------------------------- the water lines 
STYLE = dict(HR=0.75, tube=('S', 'y', 'q'), band=('g', 'e'), bubbles=True)   # 1.5 px glass lines, steel bands
OUT = 0.5


def tube_rows(st):
    """A tube's rows across it, ink to ink (a box 2 * (HR + OUT) wide)."""
    hi, mid, lo = st['tube']
    n = round(st['HR'] * 2 * K)                          # texels across the glass
    mids = [mid] * max(0, n - 2) if n >= 2 else []
    return ['X', hi] + mids + [lo, 'X']


def lit_tube(st, x, y, side_, along):
    """The tube's letter at a glass point: its lit / mid / shade by the side, bubbles and foam over the mid."""
    hi, mid, lo = st['tube']
    HR = st['HR']
    c = hi if side_ < -HR / 3 else lo if side_ > HR / 3 else mid
    if c == mid:
        h = (int(along * K) * 7 + int(y * K) * 13 + int(x * K) * 5) % 11
        if st.get('bubbles') and h == 0: return st.get('spark', 'T')
        if st.get('foam') and h == 1: return st.get('spark', 'T')
    return c


def lines_at(st, paths, bands=lambda x, y: False):
    HR = st['HR']
    def at(x, y):
        x = abs(x)
        ink = False
        for path in paths:
            d, s = min((_seg((x, y), path[k], path[k + 1]) for k in range(len(path) - 1)), key=lambda d: d[0])
            if d <= HR:
                if bands(x, y): return st['band'][0] if s < 0 else st['band'][1]
                return lit_tube(st, x, y, s, x + y)
            if d <= HR + OUT: ink = True
        return 'X' if ink else '.'
    return at


# ---------------------------------------------------------------- front elements (centred on x 0, y 23)
def element(g):
    """A texel grid (centred on x 0, y 23) as f(x, y) -> letter or None (outside it); x mirrored."""
    h, w = len(g), len(g[0])
    def at(x, y):
        i, j = int(math.floor(x * K + w / 2)), int(math.floor((23 - y) * K + h / 2))
        if 0 <= i < w and 0 <= j < h and g[j][i] != '.': return g[j][i]
        return None
    return at


def gauge():
    """A: a dive gauge, 4 x 4 px: a steel ring, a dark face, ticks, the needle (lit) sweeping up to the right."""
    g = grid(8, 8, '.')
    disc(g, 4, 4, 4, 'h', ring='e', rw=1)
    disc(g, 4, 4, 3, 'j', ring='q', rw=0.9)
    for i, j in ((1, 3), (2, 1), (4, 1), (6, 2)): g[j][i] = 'y'                # ticks
    for i, j in ((5, 3), (6, 2)): g[j][i] = 'S'                                  # the needle
    g[4][4] = g[4][3] = 'T'
    g[3][4] = 'S'
    return g


# ---------------------------------------------------------------- the 2D harness (heart's, with its own look)
def paths(st, cx, start_hw, up_c, low_c, sx):
    HR = st['HR']
    top = [(start_hw - 0.25, 23.5), (cx - HR, 25.0), (cx - HR, 27)]
    low = [(start_hw - 0.25, 22.0), (4.5, low_c), (sx, low_c)]
    return top, low


def harness(st, cx, el, hw, ring, low_c):
    HR = st['HR']
    x0, x1, y0, y1 = -cx, cx, low_c - HR - OUT, TOP_Y
    sx = side(cx)[0]
    top, low = paths(st, cx, hw, 0, low_c, sx)
    at = lines_at(st, [top, low], bands=lambda x, y: hw <= x <= hw + 0.5 and 20 < y < 25 or y >= 26 and x > cx - 2 * HR)

    def front(x, y):
        ax = abs(x)
        e = el(x, y)
        if e: return e
        if ax > sx and y < 20: return '.'
        c = at(x, y)
        if max(ax, abs(y - 23)) < ring and c in '.X': return 'X'
        return c

    def paint(f, w, h):
        if f == 'north': return [[front(x1 - (i + 0.5) / K, y1 - (j + 0.5) / K) for i in range(w)] for j in range(h)]
        return grid(w, h, '.')
    return part('harness', ((x0, y0, -3 - 0.5), (x1, y1, -3)), paint)


def strip_top(st, cx):
    HR = st['HR']
    hi, mid, lo = st['tube']
    def paint(f, w, h):
        if f == 'up': return [['X', hi] + [mid] * (w - 3) + [lo] for _ in range(h)]
        return grid(w, h, '.')
    return part('strip_top', ((cx - 2 * HR - 0.5, TOP_Y - 0.5, -3.5), (cx, TOP_Y, BACK_Z)), paint, mirror=True)


def strip_side(st, cx, low_c):
    HR = st['HR']
    rows = tube_rows(st)
    def paint(f, w, h):
        if f == 'east': return [[c] * w for c in rows]
        return grid(w, h, '.')
    sx, t = side(cx)
    return part('strip_side', ((sx - t, low_c - HR - OUT, -3.5), (sx, low_c + HR + OUT, BACK_Z)), paint, mirror=True)


def harness_back(st, cx, pack_x, up_c, low_c, pack_top, low_only=False):
    HR = st['HR']
    sx = side(cx)[0]
    x0, x1, y0, y1 = -max(cx, sx), max(cx, sx), low_c - HR - OUT, 20 if low_only else TOP_Y
    ps = [[(max(cx, sx) + 0.5, low_c), (pack_x - 0.5, low_c)]]
    if not low_only: ps.insert(0, [(cx - HR, 27), (cx - HR, up_c), (pack_x - 0.5, up_c)])
    at = lines_at(st, ps)

    def clip(x, y):
        if abs(x) < pack_x and y < pack_top: return '.'
        if abs(x) > sx and y < 20: return '.'
        return at(x, y)

    def paint(f, w, h):
        if f == 'south': return [[clip(x0 + (i + 0.5) / K, y1 - (j + 0.5) / K) for i in range(w)] for j in range(h)]
        return grid(w, h, '.')
    return part('harness_back', ((x0, y0, 3), (x1, y1, BACK_Z)), paint)


def inlets(st, faces, D, H, y1, centres):
    """The glass lines arriving at a back body's sides (east: columns back -> front; west: front -> back), in its front
    1 px (2 columns), centred at the given raw heights."""
    rows = tube_rows(st)
    for yc in centres:
        j0 = round((y1 - (yc + st['HR'] + OUT)) * K)
        for k, c in enumerate(rows):
            j = j0 + k
            if not 0 <= j < H: continue
            if j == 0 and k == 0: c = rows[1]
            for i in range(2):
                faces['east'][j][D - 1 - i] = c
                faces['west'][j][i] = c


# ---------------------------------------------------------------- A: tanks + manifold
def tanks_back(st):
    P = []
    X0, X1, Y0, Y1, Z1 = 3.0, 5.5, 16, 25, 6          # a tank: 2.5 x 9 x 3
    W, H, D = 5, 18, 6

    def tank(f, w, h):
        if f == 'up': return [['g'] * w] + [['h'] * w for _ in range(h - 1)]
        if f == 'down': return grid(w, h, 'X')
        g = [['O'] + ['N'] * (w - 2) + ['X'] for _ in range(h)]
        g[0], g[1] = ['g'] * w, ['e'] * w                                   # the shoulder
        g[-2], g[-1] = ['G'] * w, ['X'] * w
        for j0 in (4, 13):                                                   # two steel straps
            g[j0], g[j0 + 1] = ['h'] * w, ['e'] * w
        if f in ('south', 'east'):                                           # the level window: air over water
            for j in range(6, 12):
                for i in range(1, w - 1):
                    g[j][i] = 'j' if j < 8 else ('y' if j < 11 else 'S')
            g[8] = ['O'] + ['T'] * (w - 2) + ['X']                           # the water line
            for i in range(1, w - 1): g[8][i] = 'T' if i % 2 else 'S'
        return g
    t = part('tank', ((X0, Y0, TZ), (X1, Y1, Z1)), tank, mirror=True)
    inlets(st, t['faces'], D, H, Y1, (22.25, 18.75))
    P.append(t)

    def valve(f, w, h):
        if f == 'up':
            g = grid(w, h, 'X')
            g[h // 2][w // 2 - 1] = g[h // 2][w // 2] = 'S'                  # the bubbles' outlet
            return g
        return chrome(w, h)
    P.append(part('valve', ((3.75, 25, 4.5), (4.75, 26.5, 5.5)), valve, mirror=True))

    def man(f, w, h):                                                         # the manifold: 5 x 7 x 2
        if f == 'south':
            g = grid(w, h, 'N')
            g[0], g[1] = ['g'] * w, ['e'] * w
            for i in range(w): g[2][i] = 'X'
            heart = grid(10, 10, '.')                                         # the Heart of the Sea in its porthole
            disc(heart, 5, 5, 5, 'g', ring='e', rw=1)
            disc(heart, 5, 5, 3.9, 'q', ring='y', rw=0.9)
            disc(heart, 5, 5, 2.6, 'S')
            disc(heart, 5, 5, 1.4, 'T')
            for j in range(10):
                for i in range(10):
                    if heart[j][i] != '.': g[3 + j][i] = heart[j][i]
            for j in (11, 12): g[j] = ['X' if i % 2 else 'N' for i in range(w)]   # grille
            g[-1] = ['X'] * w
            return g
        if f in ('up', 'down'): return grid(w, h, 'h' if f == 'up' else 'X')
        return [['g'] * w, ['e'] * w] + [['N'] * w for _ in range(h - 3)] + [['X'] * w]
    P.append(part('manifold', ((-2.5, 17, TZ), (2.5, 24, 5)), man))
    for k, y in enumerate((18.5, 22)):                                        # link pipes between the manifold and the tanks
        def link(f, w, h):
            return [['S'] * w for _ in range(h)] if f in ('north', 'south') else \
                [['y'] * w for _ in range(h)]
        P.append(part(f'link{k}', ((2.5, y, 3.5), (3.0, y + 1, 4.5)), link, mirror=True))
    return P, 5.5, 22.25, 18.75, 25






# ---------------------------------------------------------------- under the breastplate (the heart's armoured front)
# The breastplate covers the chest's lines (the shoulder strips, the front plate's and the back's upper ones); the
# gauge shows in a steel ring 0.5 px proud of it, and the lower pair comes out from under its bottom edge (raw y 20),
# round the waist (the strip) and in on the back to the tanks: frame_heart_art.build(armored=True, flat=True).
def bezel(el=None):
    """The gauge (x +-2, raw y 21-25) in a 0.5 px steel ring: lit top and left, shaded bottom and right, a dark bolt in
    each corner."""
    g = el or element(gauge())
    hx, y0, y1 = 2.5, 20.5, 25.5
    def front(x, y):
        e = g(x, y)
        if e: return e
        ax, cy = abs(x), y - 23
        if ax >= hx - 0.5 and abs(cy) >= (y1 - y0) / 2 - 0.5: return 'z'
        return 'h' if cy >= (y1 - y0) / 2 - 0.5 or x >= hx - 0.5 else 's'
    def paint(f, w, h):
        if f == 'north': return [[front(hx - (i + 0.5) / K, y1 - (j + 0.5) / K) for i in range(w)] for j in range(h)]
        return grid(w, h, '.')
    return part('bezel', ((-hx, y0, -3.5), (hx, y1, -3)), paint)


def harness_low(st, low_c, sx, z=-3.5):
    """The lower pair below the breastplate (raw y < 20), from under its edge to the waist strip."""
    HR = st['HR']
    start = 1.75
    at = lines_at(st, [[(start, 22.0), (4.5, low_c), (sx, low_c)]])
    hx = math.floor(sx * 4) / 4
    def front(x, y): return '.' if abs(x) > sx else at(x, y)
    def paint(f, w, h):
        if f == 'north': return [[front(hx - (i + 0.5) / K, 20 - (j + 0.5) / K) for i in range(w)] for j in range(h)]
        return grid(w, h, '.')
    return part('harness_low', ((-hx, low_c - HR - OUT, z), (hx, 20, z)), paint)


def build(chest_x=6.0):
    """(back parts, open front, armoured front): the back body's parts, the front's decals on a bare chest, and under the
    breastplate. Names: frame_model.py prefixes them (sb_ / so_ / sa_)."""
    st = STYLE
    back, pack_x, up_c, low_c, pack_top = tanks_back(st)
    cx = min(6, chest_x)
    sx = side(cx)[0]
    open_ = [harness(st, cx, element(gauge()), 2.0, 2.5, low_c), strip_top(st, cx), strip_side(st, cx, low_c),
             harness_back(st, cx, pack_x, up_c, low_c, pack_top)]
    armoured = [bezel(), harness_low(st, low_c, sx), strip_side(st, cx, low_c),
                harness_back(st, cx, pack_x, up_c, low_c, pack_top, low_only=True)]
    return back, open_, armoured
