"""Alternative fireboxes for the frame's engine (frame_model.py, ENGINE=firebox, draft knob FIREBOX).

2026-11-07 (user: "design some alternative firebox designs, go wild"): the back half of the engine redrawn as six
other machines. The core in the chest slot and the copper pipes stay as picked (frame_model.py); each design replaces
the pack and its exhausts, and keeps a box at the abdomen's sides (x +-5, raw y 16-19, z 3-4) where the side pipes
end in copper inlets (add_inlets).

  pistons   the committed one (frame_model.py builds it; listed here for the review only)
  loco      a little locomotive across the back: firebox, a blue boiler drum lying sideways with brass bands, its
            smokebox door on the right end, a diamond stack on the right, steam dome and whistle on the left
  calliope  a steam organ: a windchest with the fire behind brass slats and a pressure gauge, a keyboard on its top,
            six organ pipes fanned out beside the helmet (the tallest outside)
  radial    an aircraft radial engine: seven finned cylinders round a crankcase, the fire in its porthole hub
  furnace   a vanilla furnace strapped on (half scale, lit), a stovepipe with a rain hat. (The draft samples
            vanilla's furnace textures from the Minecraft jar; to ship it, repaint it in that style or have the
            renderer bind vanilla's texture for those faces.)
  hopper    a coal hopper (stepped funnel, the coal heap on top, a shovel in it) over a low firebox, its exhausts
            two jet nozzles out the bottom, angled back (no stacks behind the helmet: the head turns and pitches
            freely)
  diving    a Rapture bathysphere boiler: a riveted copper tank with verdigris, two glowing portholes, a dome with a
            valve wheel, a mushroom vent on the left

Coordinates are raw (frame_model.py adds FY), right side +x, the back is +z. Art at 2 texels per px (K), letters from
frame_model.PAL / the iron ramp plus EXTRA below; RGBA tuples allowed (the furnace). Faces as frame_model.py's:
north / south as seen from the front / back (south column 0 at -x), east back -> front, west front -> back, up rows
front -> back.
"""
import math

K = 2
EXTRA = {'E': (0xd6, 0xbe, 0x7e),   # bright brass
         'P': (0x2a, 0x24, 0x20),   # soot
         'S': (0x8e, 0x2f, 0x25),   # red enamel
         'a': (0x2f, 0x5a, 0x96),   # blue enamel (the old suit's blue)
         'b': (0x21, 0x3f, 0x6b),   # blue enamel, shaded
         'c': (0x16, 0x16, 0x18),   # coal
         'o': (0x4a, 0x4a, 0x54),   # coal glint
         'q': (0xe6, 0xdc, 0xc0),   # gauge face / ivory keys
         'r': (0xc4, 0x2a, 0x1e),   # needle red
         't': (0x4e, 0x9a, 0x84),   # verdigris
         'f': (0x26, 0x2c, 0x34)}   # dark glass
FACES = ('north', 'east', 'south', 'west', 'up', 'down')
OPTIONS = ('pistons', 'loco', 'calliope', 'radial', 'furnace', 'hopper', 'diving')


# ---------------------------------------------------------------- helpers
def T(v): 
    n = round(v * K)
    assert abs(n - v * K) < 1e-6, v
    return n


def dims(box):
    (x0, y0, z0), (x1, y1, z1) = box
    W, H, D = T(x1 - x0), T(y1 - y0), T(z1 - z0)
    return {'north': (W, H), 'south': (W, H), 'east': (D, H), 'west': (D, H), 'up': (W, D), 'down': (W, D)}


def grid(w, h, c): return [[c] * w for _ in range(h)]


def put(g, x, y, rows):
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != ' ' and 0 <= y + j < len(g) and 0 <= x + i < len(g[0]): g[y + j][x + i] = c


def disc(g, cx, cy, r, c, ring=None, rw=1.0):
    """A disc of colour c centred on texel coordinates (cx, cy) (centres between texels allowed), radius r; a ring
    rw wide round its edge in `ring`."""
    for j in range(len(g)):
        for i in range(len(g[0])):
            d = math.hypot(i + 0.5 - cx, j + 0.5 - cy)
            if d <= r: g[j][i] = ring if ring and d > r - rw else c


def hsh(i, j, n, seed=0): return ((i * 73856093) ^ (j * 19349663) ^ (seed * 83492791)) % n


def plate(w, h, base='U', top='W', bottom='G', rivets='O', inset=1):
    g = grid(w, h, base)
    if top: g[0] = [top] * w
    if bottom and h > 1: g[-1] = [bottom] * w
    if rivets and w > 4 and h > 4:
        for i, j in ((inset, inset + 1), (w - 1 - inset, inset + 1), (inset, h - 2 - inset), (w - 1 - inset, h - 2 - inset)):
            g[j][i] = rivets
    return g


def fire(w, h, bars=None):
    """Coals, red on top to yellow-white at the bottom, behind grate bars every few columns."""
    rows = ['J', 'J', 'I', 'I', 'F', 'F'] if h >= 6 else ['J', 'I', 'F', 'F'][-h:]
    while len(rows) < h: rows.insert(1, 'I')
    rows = rows[:h]
    bars = bars if bars is not None else {i for i in range(w) if i % 3 == 2}
    return [['X' if i in bars else c for i in range(w)] for c in rows]


def part(name, box, paint, mirror=False, rot=None, origin=None, shell=None):
    """paint(face, w, h) -> grid. rot: [x, y, z] degrees about origin (raw), as Blockbench's."""
    d = dims(box)
    faces = {f: paint(f, *d[f]) for f in FACES} if paint else None
    for f, g in (faces or {}).items():
        assert len(g) == d[f][1] and all(len(r) == d[f][0] for r in g), (name, f, d[f], len(g), len(g[0]))
    return dict(name=name, box=box, faces=faces, mirror=mirror, rot=rot, origin=origin, shell=shell)


def add_inlets(parts, TX=5, TZ=3):
    """Copper inlets where the side pipes (raw y 16-17, 18-19, at x +-TX, z TZ..TZ+1) meet a part's side."""
    for p in parts:
        if p['faces'] is None or p['rot']: continue
        (x0, y0, z0), (x1, y1, z1) = p['box']
        for f, at in (('east', x1), ('west', -x0)):
            if f == 'west' and p['mirror']: continue      # a mirrored part's west is its inner side
            if abs(at - TX) > 1e-6 or z0 > TZ + 1e-6 or z1 < TZ + 1 - 1e-6: continue
            g = p['faces'][f]
            for y in (16, 18):
                if y < y0 - 1e-6 or y + 1 > y1 + 1e-6: continue
                cols = range(T(z1 - TZ - 1), T(z1 - TZ)) if f == 'east' else range(T(TZ - z0), T(TZ + 1 - z0))
                for j in range(T(y1 - y - 1), T(y1 - y)):
                    for i in cols: g[j][i] = 'Q' if j == T(y1 - y - 1) else 'R'
    return parts


def firebox_door(w, h, frame='Y'):
    """A firebox door: a frame round the lit coals behind bars, a latch."""
    g = grid(w, h, frame)
    put(g, 1, 1, fire(w - 2, h - 2, bars={i for i in range(w - 2) if i % 3 == 1}))
    g[h // 2][w - 1] = 'E'
    return g


# ---------------------------------------------------------------- loco
def loco():
    P = []

    def fb(f, w, h):
        if f == 'south':
            g = plate(w, h, 'N', 'O', 'X')
            put(g, 6, 1, firebox_door(8, 6))
            g[7] = ['X'] * w
            g[8] = ['S'] * w
            g[9] = ['S'] * w
            for x in (1, 2, w - 3, w - 2):              # brass buffers on the red buffer beam
                g[8][x] = 'Y'; g[9][x] = 'Z'
            g[8][5] = g[8][w - 6] = 'O'
            return g
        if f in ('east', 'west'): return plate(w, h, 'N', 'O', 'X')
        if f == 'up': return grid(w, h, 'N')
        return grid(w, h, 'X')
    P.append(part('fb', ((-5, 15, 3), (5, 20, 8)), fb))

    def bands(w, h, base, lit=None, shade=None):
        g = grid(w, h, base)
        if lit: g[0] = [lit] * w
        if shade: g[-1] = [shade] * w
        for b in (2, 9, 16):
            for j in range(h):
                if b < w: g[j][b] = 'Y'
                if b + 1 < w: g[j][b + 1] = 'Z'
        return g

    def drum_a(f, w, h):          # the drum's octagon: the tall box (its flat top, bottom and the end caps)
        if f in ('east', 'west'):
            g = grid(w, h, 'b')
            if f == 'east':        # the smokebox door: a dark round door, hinge straps, a brass number plate
                disc(g, w / 2, h / 2, 4.6, 'N', ring='O')
                for j in (3, 6):
                    for i in range(1, w - 1): g[j][i] = 'O' if g[j][i] == 'N' else g[j][i]
                g[4][3] = g[4][4] = 'Y'; g[5][3] = g[5][4] = 'E'
                g[h // 2][w - 2] = 'W'              # the handle
            else:                  # the backhead: a brass ring
                disc(g, w / 2, h / 2, 4.6, 'b', ring='Y')
                g[h // 2 - 1][w // 2] = 'r'; g[h // 2][w // 2] = 'q'   # a gauge glass
            return g
        if f == 'south':
            g = bands(w, h, 'b', lit='a')
            return g
        if f == 'up': return bands(w, h, 'a', lit='a', shade='b')
        return grid(w, h, 'b')
    P.append(part('drum_a', ((-5, 20, 4), (5, 25, 8)), drum_a))

    def drum_b(f, w, h):          # the deep box: its back is the drum's belly, lit along the middle
        if f == 'south':
            g = grid(w, h, 'a')
            g[0] = ['b'] * w
            g[2] = ['b'] * w
            for b in (2, 8, 16):
                for j in range(h):
                    if b < w: g[j][b] = 'Y'
                    if b + 1 < w: g[j][b + 1] = 'Z'
            for i in range(0, w, 3): g[3][i] = 'Y' if g[3][i] in 'ab' else g[3][i]   # rivet row
            g[3 if h > 3 else 0][w // 2] = g[3 if h > 3 else 0][w // 2]
            return g
        if f in ('east', 'west'): return grid(w, h, 'b')
        if f == 'up':
            g = grid(w, h, 'a'); return g
        return grid(w, h, 'b')
    P.append(part('drum_b', ((-4.75, 21, 3), (4.75, 24, 9)), drum_b))

    def stack(f, w, h):
        if f in ('up', 'down'): return grid(w, h, 'X')
        g = grid(w, h, 'N')
        for j in range(h): g[j][0] = 'O'
        g[3] = ['X'] * w
        g[0] = ['P'] * w
        return g
    def stack_base(f, w, h):
        if f in ('up', 'down'): return grid(w, h, 'O')
        return [['Y'] * w]
    def cap(f, w, h):
        if f == 'up':
            g = grid(w, h, 'O')
            for j in range(1, h - 1):
                for i in range(1, w - 1): g[j][i] = 'X' if hsh(i, j, 3) else 'P'
            return g
        if f == 'down': return grid(w, h, 'N')
        g = grid(w, h, 'N'); g[0] = ['O'] * w; g[-1] = ['X'] * w
        g[1][0] = 'O'
        return g
    P.append(part('stack_base', ((2, 25, 4.5), (5, 25.5, 7.5)), stack_base))
    P.append(part('stack', ((2.75, 25.5, 5.25), (4.25, 29, 6.75)), stack))
    # the diamond stack's flared top: two steps out (a spark arrestor's mesh on top)
    P.append(part('stack_flare', ((2.25, 29, 4.75), (4.75, 30, 7.25)), lambda f, w, h: grid(w, h, 'N') if f in ('up', 'down') else [['O'] * w, ['N'] * w]))
    P.append(part('stack_cap', ((1.75, 30, 4.25), (5.25, 31, 7.75)), cap))

    def dome(f, w, h):
        g = grid(w, h, 'Y')
        if f not in ('up', 'down'): g[-1] = ['Z'] * w; g[0][0] = 'E'
        if f == 'up': g[0] = ['E'] * w
        return g
    P.append(part('dome', ((-4, 25, 4.75), (-1.5, 26.5, 7.25)), dome))
    P.append(part('dome_top', ((-3.25, 26.5, 5.5), (-2.25, 27, 6.5)), lambda f, w, h: grid(w, h, 'E')))

    def whistle(f, w, h):
        if f in ('up', 'down'): return grid(w, h, 'Z')
        return [['E'] * w] + [['Y'] * w for _ in range(h - 2)] + [['Z'] * w]
    P.append(part('whistle', ((-1, 25, 5.75), (-0.5, 27.5, 6.25)), whistle))
    P.append(part('whistle_bell', ((-1.25, 27.5, 5.5), (-0.25, 28.5, 6.5)),
                  lambda f, w, h: grid(w, h, 'X') if f == 'up' else [['E'] * w] + [['Y'] * w for _ in range(h - 1)]))
    return P


# ---------------------------------------------------------------- calliope
def calliope():
    P = []

    def chest(f, w, h):
        if f == 'south':
            g = grid(w, h, 'N')
            for j in range(h): g[j][0] = g[j][w - 1] = 'Y'
            g[0] = ['E'] * w
            g[h - 1] = ['Z'] * w
            disc(g, w / 2, 4.5, 3.6, 'q', ring='Y')       # the pressure gauge
            g[4][w // 2] = 'X'; g[3][w // 2 + 1] = 'r'; g[2][w // 2 + 2] = 'r'
            for i, j in ((w // 2 - 3, 4), (w // 2 + 2, 4), (w // 2 - 1, 2), (w // 2 - 1, 6)): g[j][i] = 'X'   # ticks
            for j in range(9, h - 2):                     # brass slats over the fire
                for i in range(2, w - 2):
                    g[j][i] = ('Y' if i % 2 == 0 else ['J', 'I', 'I', 'F', 'F'][min(4, j - 9)])
            g[8] = ['Y'] + ['Z'] * (w - 2) + ['Y']
            g[h - 2] = ['Y'] + ['Z'] * (w - 2) + ['Y']
            return g
        if f in ('east', 'west'):
            g = plate(w, h, 'N', 'Y', 'Z')
            return g
        if f == 'up':              # a keyboard along the front, pipe feet behind
            g = grid(w, h, 'N')
            g[0] = ['Z'] * w
            for j in (1, 2):
                for i in range(1, w - 1):
                    g[j][i] = 'X' if i % 3 == 0 else 'q'
            for i in range(1, w - 1):
                if i % 3 in (1, 2) and j == 1: pass
            for i in range(2, w - 1, 3):
                if i % 7 not in (0, 4): g[1][i] = 'X'
            g[3] = ['Z'] * w
            return g
        return grid(w, h, 'X')
    P.append(part('windchest', ((-5, 15, 3), (5, 23, 7)), chest))

    def pipe(mat):
        lit, base, shade = ('E', 'Y', 'Z') if mat == 'brass' else ('Q', 'Q', 'R')
        def paint(f, w, h):
            if f == 'up': return [[shade] * w, [shade, 'X', shade], [shade] * w]
            if f == 'down': return grid(w, h, shade)
            g = [[lit, base, shade] for _ in range(h)]
            g[0] = [shade] * w; g[1] = [lit] * w     # the rim
            if f == 'south' or f == 'north':          # the mouth: a lower lip under a dark slot, an arched upper lip
                m = h - 7
                g[m] = [shade, lit, shade]
                g[m + 1] = [base, 'X', base]
                g[m + 2] = [base, 'X', base]
                g[m + 3] = [lit, lit, lit]
            g[-1] = [shade] * w; g[-2] = [shade, base, shade]   # the foot
            return g
        return paint
    # three a side, tallest outside, fanned out (tops lean outwards; Blockbench z: positive turns +x up -> -y... see
    # frame_model.ARM_SPLAY: +z on the right swings a hanging arm out, so an upright pipe leans out with -z)
    for i, (x0, top, lean, mat) in enumerate(((0.25, 27.5, -2, 'brass'), (1.75, 30.5, -4, 'copper'), (3.25, 33.5, -6, 'brass'))):
        box = ((x0, 23, 5), (x0 + 1.5, top, 6.5))
        P.append(part(f'pipe{i}', box, pipe(mat), mirror=True, rot=[0, 0, lean], origin=(x0 + 0.75, 23, 5.75)))
    return P


# ---------------------------------------------------------------- radial
def radial():
    P = []
    CY = 20.5
    def mount(f, w, h):
        g = plate(w, h, 'N', 'O', 'X')
        if f == 'south':
            for i in range(1, w - 1, 3): g[1][i] = g[h - 2][i] = 'O'
            disc(g, w / 2, (26 - CY) * K, 9.6, 'N', ring='X', rw=1.2)   # the shadow ring the cylinders sit in
        return g
    P.append(part('mount', ((-5, 15, 3), (5, 26, 4)), mount))

    def hub(f, w, h):
        if f == 'south':
            g = grid(w, h, 'N')
            disc(g, w / 2, h / 2, 4.0, 'F', ring='Y', rw=1.0)
            disc(g, w / 2, h / 2, 3.0, 'I', ring='J', rw=0.9)
            g[h // 2][w // 2] = g[h // 2 - 1][w // 2 - 1] = 'F'
            g[h // 2 - 1][w // 2] = g[h // 2][w // 2 - 1] = 'F'
            for j in range(1, h - 1):                    # grate bars across the porthole
                g[j][2] = 'X' if g[j][2] in 'FIJ' else g[j][2]
                g[j][5] = 'X' if g[j][5] in 'FIJ' else g[j][5]
            return g
        g = grid(w, h, 'N'); g[0] = ['O'] * w
        return g
    P.append(part('hub', ((-2, CY - 2, 4), (2, CY + 2, 7)), hub))
    def hub45(f, w, h):
        g = grid(w, h, 'O')
        if f == 'south':
            for i, j in ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)): g[j][i] = 'Y'
        return g
    P.append(part('hub45', ((-2, CY - 2, 4), (2, CY + 2, 6)), hub45, rot=[0, 0, 45], origin=(0, CY, 5)))

    def cyl(f, w, h):
        if f == 'up':
            g = grid(w, h, 'Y'); g[0] = ['E'] * w
            g[1][1] = g[2][2] = 'X'                       # the spark plug lead
            return g
        if f == 'down': return grid(w, h, 'X')
        rows = [['Z', 'E', 'E', 'Z'], ['Y'] * 4, ['X'] * 4, ['W', 'V', 'V', 'U'], ['X'] * 4]
        return [r[:w] for r in rows[:h]]
    n = 7
    for k in range(n):
        a = k * 360 / n
        P.append(part(f'cyl{k}', ((-1, CY + 2.5, 4.5), (1, CY + 5, 6.5)), cyl if k == 0 else None,
                      rot=[0, 0, round(a, 3)], origin=(0, CY, 5.5), shell='cyl0'))
    # two short exhaust stubs out of the mount's bottom corners, angled down and out, sooty
    def stub(f, w, h):
        if f == 'down': return [['X'] * w, ['X', 'P', 'X'], ['X'] * w][:h]
        g = grid(w, h, 'R'); 
        for j in range(h): g[j][0] = 'Q'
        g[-1] = ['P'] * w
        return g
    P.append(part('stub', ((3.25, 13.5, 3.75), (4.75, 15, 5.25)), stub, mirror=True, rot=[0, 0, 20], origin=(4, 15, 4.5)))
    return P


# ---------------------------------------------------------------- furnace
def furnace(vanilla):
    """vanilla: {'front_on': rows, 'side': rows, 'top': rows} of RGBA, 16 x 16 each."""
    P = []
    def tray(f, w, h):
        g = grid(w, h, 'U'); g[0] = ['W'] * w
        if f == 'south':
            for i in range(1, w - 1, 3): g[1][i] = 'O'
        if f == 'up': g = grid(w, h, 'U')
        if f == 'down': g = grid(w, h, 'G')
        return g
    P.append(part('tray', ((-5, 15, 3), (5, 17, 10)), tray))
    def rail(f, w, h):
        g = grid(w, h, 'N')
        for j in range(0, h, 5): g[j] = ['O'] * w
        return g
    P.append(part('rail', ((4, 17, 3), (5, 25, 4.5)), rail, mirror=True))
    def block(f, w, h):
        src = vanilla['front_on' if f == 'south' else 'top' if f in ('up', 'down') else 'side']
        if f == 'north': src = vanilla['side']
        # crop 16 to w columns / h rows from the middle
        x0, y0 = (16 - w) // 2, (16 - h) // 2
        return [[src[y0 + j][x0 + i] for i in range(w)] for j in range(h)]
    P.append(part('furnace', ((-4, 17, 3.5), (4, 25, 9.5)), block))
    def strap(f, w, h):
        g = grid(w, h, 'N')
        if f in ('south', 'east', 'west'):
            g[0] = ['O'] * w
            for i in range(1, w, 4): g[0][i] = 'W'
        return g
    P.append(part('strap', ((-4.25, 23.5, 3.5), (4.25, 24, 10)), strap))
    def stovepipe(f, w, h):
        if f in ('up', 'down'): return [['N'] * w, ['N', 'X', 'N'], ['N'] * w]
        g = [['O', 'N', 'X'] for _ in range(h)]
        g[0] = ['P'] * w; g[1] = ['P', 'N', 'P']
        g[6] = ['W', 'O', 'N']
        return g
    P.append(part('stovepipe', ((1.5, 25, 6.5), (3, 31, 8)), stovepipe))
    def hat(f, w, h):
        if f == 'down': return grid(w, h, 'P')
        g = grid(w, h, 'O')
        if f == 'up':
            for j in range(h):
                for i in range(w):
                    if 1 <= i < w - 1 and 1 <= j < h - 1: g[j][i] = 'W' if (i, j) == (2, 2) else 'O'
                    else: g[j][i] = 'N'
        return g
    P.append(part('hat', ((0.75, 31.5, 5.75), (3.75, 32, 8.75)), hat))
    return P


# ---------------------------------------------------------------- hopper
def hopper():
    P = []
    def fb(f, w, h):
        if f == 'south':
            g = plate(w, h, 'N', 'O', 'X')
            put(g, 4, 1, firebox_door(12, 5, frame='O'))
            g[7] = ['X'] * w
            for i in range(2, w - 2, 2): g[8][i] = 'J'     # the ash grate glowing
            return g
        if f in ('east', 'west'): return plate(w, h, 'N', 'O', 'X')
        return grid(w, h, 'N' if f == 'up' else 'X')
    P.append(part('fb', ((-5, 15, 3), (5, 20, 8)), fb))
    def sheet(base='V'):
        def paint(f, w, h):
            g = grid(w, h, base)
            if f not in ('up', 'down'):
                g[0] = ['W'] * w
                g[-1] = ['U'] * w
                for i in range(1, w - 1, 3): g[0][i] = 'O'
            if f == 'down': g = grid(w, h, 'U')
            return g
        return paint
    P.append(part('h1', ((-3, 20, 4), (3, 22, 8)), sheet()))
    P.append(part('h2', ((-4, 22, 4), (4, 24, 9)), sheet()))
    def h3(f, w, h):
        if f == 'up':              # the coal heap inside a rim
            g = grid(w, h, 'O')
            for j in range(1, h - 1):
                for i in range(1, w - 1):
                    v = hsh(i, j, 11, 3)
                    g[j][i] = 'o' if v == 0 else 'P' if v in (1, 2) else 'X' if v in (3, 4) else 'c'
            g[1] = ['G'] + ['G' if hsh(i, 1, 2) else 'c' for i in range(1, w - 1)] + ['G']   # the heap's shadow front edge
            return g
        g = sheet()(f, w, h)
        if f == 'south':           # a sight glass showing the coal level
            for j in range(1, h - 1):
                g[j][w // 2 - 1] = 'G'; g[j][w // 2] = 'f' if j < 3 else 'c'
            g[1][w // 2] = 'W'
            for x in (2, w - 3):   # stencilled lettering: a COAL plate
                g[2][x] = 'Y'; g[3][x] = 'Y'
        return g
    P.append(part('h3', ((-5, 24, 4.5), (5, 27, 9.5)), h3))
    def shovel(f, w, h):
        g = grid(w, h, 'L')
        if h < 3: return grid(w, h, 'H')
        for j in range(h): g[j][0] = 'H'
        g[0] = ['Z'] * w; g[1] = ['H'] * w
        return g
    P.append(part('shovel', ((1.5, 26, 7.5), (2, 30, 8)), shovel, rot=[-15, 0, -22], origin=(1.75, 26.5, 7.75)))
    def blade(f, w, h):
        return grid(w, h, 'U' if f in ('north', 'south') else 'G')
    P.append(part('blade', ((1, 26.5, 7.5), (2.5, 27.5, 8)), blade, rot=[-15, 0, -22], origin=(1.75, 26.5, 7.75)))
    # jet nozzles out the firebox's bottom, angled back (Blockbench x: + leans an upright part back, so a hanging one
    # swings back with -x), a glowing throat
    def nozzle(f, w, h):
        if f == 'down': return [['X', 'X', 'X', 'X'], ['X', 'J', 'J', 'X'], ['X', 'J', 'I', 'X'], ['X', 'X', 'X', 'X']][:h]
        if f == 'up': return grid(w, h, 'N')
        g = grid(w, h, 'N')
        for j in range(h): g[j][0] = 'O'
        g[1] = ['b'] * w; g[2] = ['a'] * w           # heat tint
        g[3] = ['Z'] * w
        return g
    P.append(part('nozzle', ((2, 12.5, 4.5), (4, 15, 6.5)), nozzle, mirror=True, rot=[-55, 0, 0], origin=(3, 15, 5.5)))
    def bell(f, w, h):
        if f == 'down':
            g = grid(w, h, 'X'); disc(g, w / 2, h / 2, 2.2, 'I', ring='J', rw=0.9); return g
        if f == 'up': return grid(w, h, 'N')
        return [['O'] * w, ['P'] * w]
    P.append(part('bell', ((1.5, 11.5, 4), (4.5, 12.5, 7)), bell, mirror=True, rot=[-55, 0, 0], origin=(3, 15, 5.5)))
    return P


# ---------------------------------------------------------------- diving
def diving():
    P = []
    def streaks(g, seed):
        for i in range(len(g[0])):
            if hsh(i, 0, 4, seed) == 0:
                for j in range(len(g) - 1 - hsh(i, 1, 5, seed), len(g)): g[j][i] = 't'
    def seams(g, step=7):
        for j in range(0, len(g), step):
            g[j] = ['R'] * len(g[0])
            for i in range(1, len(g[0]), 2): g[j][i] = 'Y'
    def tank_a(f, w, h):
        g = grid(w, h, 'R' if f == 'south' else 'Q')
        if f in ('up', 'down'): return grid(w, h, 'Q')
        seams(g); streaks(g, 1)
        if f in ('east', 'west'):
            disc(g, w / 2, 10, 2.6, 'q', ring='Y')   # a gauge each side
            g[9][w // 2] = 'r'; g[10][w // 2] = 'X'
        return g
    P.append(part('tank_a', ((-4, 15, 3.5), (4, 26, 9.5)), tank_a))
    def tank_b(f, w, h):
        if f in ('up', 'down'): return grid(w, h, 'Q')
        g = grid(w, h, 'Q')
        for j in range(h): g[j][0] = 'R'; g[j][w - 1] = 'R'
        seams(g); streaks(g, 2)
        if f == 'south':
            for cy in (5.5, 15.5):
                disc(g, w / 2, cy, 4.6, 'Y', ring='Z', rw=1)
                disc(g, w / 2, cy, 3.3, 'F', ring='X', rw=0.8)
                for j in range(len(g)):
                    for i in range(len(g[0])):
                        d = math.hypot(i + 0.5 - w / 2, j + 0.5 - cy)
                        if d < 3.3 and g[j][i] == 'F':   # the coals behind the glass: red on top, white-hot below
                            dy = j + 0.5 - cy
                            g[j][i] = 'J' if dy < -1.2 else 'I' if dy < 0.6 else 'F'
                g[int(cy) - 2][w // 2 - 2] = 'q'          # a glint on the glass
                for a in range(0, 360, 45):              # rivets round the ring
                    i, j = int(w / 2 + 4.1 * math.cos(math.radians(a))), int(cy + 4.1 * math.sin(math.radians(a)))
                    if 0 <= j < h and 0 <= i < w: g[j][i] = 'E'
        return g
    P.append(part('tank_b', ((-3, 15.25, 3), (3, 25.75, 10.5)), tank_b))
    def dome(f, w, h):
        g = grid(w, h, 'Q')
        if f != 'up': g[-1] = ['R'] * w
        else:
            for i in range(0, w, 2): g[0][i] = 'Y'
        return g
    P.append(part('dome1', ((-3, 26, 4.5), (3, 27, 9.5)), dome))
    P.append(part('dome2', ((-2, 27, 5.5), (2, 27.5, 8.5)), dome))
    P.append(part('stem', ((-0.25, 27.5, 6.75), (0.25, 28.5, 7.25)), lambda f, w, h: grid(w, h, 'O')))
    def wheel(f, w, h):
        if f in ('up', 'down'):
            g = grid(w, h, '.')
            for j in range(h):
                for i in range(w):
                    if i in (0, w - 1) or j in (0, h - 1): g[j][i] = 'S'
                    if i == j or i == w - 1 - j: g[j][i] = 'S'
            g[h // 2][w // 2] = 'Y'
            return g
        return grid(w, h, 'S')
    P.append(part('wheel', ((-1.5, 28.5, 5.5), (1.5, 29, 8.5)), wheel))
    def saddle(f, w, h):
        return plate(w, h, 'N', 'O', 'X', rivets=None)
    P.append(part('saddle', ((4, 15, 3), (5, 20, 5)), saddle, mirror=True))
    def vent(f, w, h):
        if f in ('up', 'down'): return grid(w, h, 'R')
        g = [['Q', 'R'] for _ in range(h)]
        g[2] = ['Y', 'Y']
        return g
    P.append(part('vent', ((-3.75, 27, 7.5), (-2.75, 31, 8.5)), vent))
    def mushroom(f, w, h):
        if f == 'down': return [['t' if (i + j) % 2 else 'X' for i in range(w)] for j in range(h)]
        if f == 'up':
            g = grid(w, h, 'Q'); g[0] = ['t'] * w; return g
        return [['Q'] * w, ['t' if i % 2 else 'R' for i in range(w)]]
    P.append(part('mushroom', ((-4.5, 31, 6.75), (-2, 32, 9.25)), mushroom))
    return P


def build(option, vanilla=None):
    parts = {'loco': loco, 'calliope': calliope, 'radial': radial, 'hopper': hopper, 'diving': diving,
             'furnace': lambda: furnace(vanilla)}[option]()
    return add_inlets(parts)
