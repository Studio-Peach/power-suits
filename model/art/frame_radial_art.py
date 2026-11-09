"""The radial firebox: the back half of the frame's engine (frame_model.py, ENGINE=firebox), drawn as an aircraft
radial engine: seven finned cylinders with brass heads round a crankcase, the fire behind the porthole in its hub,
two copper exhaust stubs out the bottom, all on a gunmetal mounting plate the side pipes end on (copper inlets).

2026-11-07 (user: "design some alternative firebox designs, go wild"; picked radial). It replaced the twin-cylinder
pack with the old suit's exhausts (frame_engine_art.back_pistons until then). Not picked, drafted in commit 7a24d3f
(frame_firebox_drafts.py): a locomotive across the back, a steam calliope with organ pipes, a vanilla furnace
strapped on, a coal hopper with jet nozzles, a copper bathysphere boiler. Nothing rises behind the helmet but the top
cylinder (to raw 25.5), so the head turns and pitches with less to hit than the stacks had (engine_sweep.py).

Coordinates are raw (frame_model.py adds FY), right side +x, the back is +z. Art at 2 texels per px (K), letters from
frame_model.PAL / the iron ramp plus EXTRA below. Faces as frame_model.py's: north / south as seen from the front /
back (south column 0 at -x), east back -> front, west front -> back, up rows front -> back.
"""
import math

K = 2
EXTRA = {'E': (0xd6, 0xbe, 0x7e),   # bright brass
         'P': (0x2a, 0x24, 0x20)}   # soot
FACES = ('north', 'east', 'south', 'west', 'up', 'down')


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


def disc(g, cx, cy, r, c, ring=None, rw=1.0):
    """A disc of colour c centred on texel coordinates (cx, cy) (centres between texels allowed), radius r; a ring
    rw wide round its edge in `ring`."""
    for j in range(len(g)):
        for i in range(len(g[0])):
            d = math.hypot(i + 0.5 - cx, j + 0.5 - cy)
            if d <= r: g[j][i] = ring if ring and d > r - rw else c


def plate(w, h, base='U', top='W', bottom='G', rivets='O', inset=1):
    g = grid(w, h, base)
    if top: g[0] = [top] * w
    if bottom and h > 1: g[-1] = [bottom] * w
    if rivets and w > 4 and h > 4:
        for i, j in ((inset, inset + 1), (w - 1 - inset, inset + 1), (inset, h - 2 - inset), (w - 1 - inset, h - 2 - inset)):
            g[j][i] = rivets
    return g


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
    # seven cylinders (odd, as real radials), one straight up, all sharing cyl0's paint
    n = 7
    for k in range(n):
        a = k * 360 / n
        P.append(part(f'cyl{k}', ((-1, CY + 2.5, 4.5), (1, CY + 5, 6.5)), cyl if k == 0 else None,
                      rot=[0, 0, round(a, 3)], origin=(0, CY, 5.5), shell='cyl0'))
    # two short exhaust stubs out of the mount's bottom corners, angled down and out, sooty (a leg swung back
    # 40 deg or more meets them: engine_sweep.py)
    def stub(f, w, h):
        if f == 'down': return [['X'] * w, ['X', 'P', 'X'], ['X'] * w][:h]
        g = grid(w, h, 'R')
        for j in range(h): g[j][0] = 'Q'
        g[-1] = ['P'] * w
        return g
    P.append(part('stub', ((3.25, 13.5, 3.75), (4.75, 15, 5.25)), stub, mirror=True, rot=[0, 0, 20], origin=(4, 15, 4.5)))
    return P


def build():
    return add_inlets(radial())
