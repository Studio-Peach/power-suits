"""The drill for the frame (frame_model.py, TOOL=drill): the first power tool brought over from the big suit, sized
down to the frame's arm and redrawn in its flat style.

2026-11-13 (user: bring the power tools over from the old suit, scaled down and redesigned; the drill first, as it
settles how every tool mounts). The mount, shared by every draft: the tool REPLACES the fist on the tool arm (the left,
as on the big suit, whose tool forearm had no fist): the arm box's bottom 4 px are the drill's motor housing, painted
(frame_model.HOUSING, the fist's place in the arm's art), and only the bit is 3D, hanging from the housing's
underside on its own bone (`tool`, its pivot on the arm's axis: the bit spins about y in game).
The big suit's drill (mining_tools_art.py): a 7 x 1 x 7 socket base, a 6 x 2 x 6 motor hub, then steel cone steps 6, 5
and diamond steps 4, 2, 1, each turned 22.5 deg from the last (a twisted auger), 11 px long. Sized to the frame's 5 px
arm (about 0.7) it is 7 px long, so it ends 5 px over the ground with the arm hanging.

Drafts (DRILL):
- A cone: the old stepped cone sized down: steel 4 and 3, diamond 2 and 1, turned +-22.5 / 45 deg in turn.
- B cross: the drill drawn flat on two crossed planes turned 45 deg (as vanilla draws a sapling or a flower): a cone
  in steel steps with diagonal flutes and a diamond point; spun in game it reads round.
- C auger: a straight 3 x 4 x 3 steel column with helical flutes painted round it (they run on across the corners)
  over a 3 px diamond point (2 x 2 x 2 turned 45 deg, then 1 x 1 x 1).

Coordinates are raw (frame_model.py adds FY), the right arm's (+x; the left mirrors), the bit's top at the arm box's
bottom (raw y 10), centred on the arm's axis (x c, z 0). Art at 2 texels per px, RGBA tuples ('.' see-through).
Faces as frame_model.py's: north / south as seen from the front / back, east back -> front, west front -> back, up
rows front -> back.
"""
from frame_radial_art import dims, FACES

_c = lambda h: tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
# the iron armour's steel ramp (frame_iron_art.PAL) and the big suit's diamond (mining_tools_art.py: vanilla's)
S = {k: _c(v) for k, v in {'z': '22262e', 's': '3c424c', 'p': '58606a', 'l': '757c85', 'e': '8a9097', 'h': '9fa4a9',
                           'g': 'cdcfcf', 'w': 'fbf8f0'}.items()}
D = {k: _c(v) for k, v in {'0': '0e7b7a', '1': '12a1a0', '2': '2ce3d9', '3': 'a1fbe8', '4': 'e4fffa'}.items()}
TOP = 10   # the bit's top: the arm box's bottom (raw)


def grid(w, h, c='.'): return [[c] * w for _ in range(h)]


def step(f, w, h, metal):
    """A cone step's face: a lit rim, the body (lit column left, shaded right: light from the upper left), a shadow
    row under it; metal 'steel' or 'diamond'. Top and bottom: the body colour, a darker ring."""
    if f in ('up', 'down'):
        g = grid(w, h, S['p'] if metal == 'steel' else D['1'])
        for j in range(h):
            for i in range(w):
                if 0 < i < w - 1 and 0 < j < h - 1: g[j][i] = S['l'] if metal == 'steel' else D['2']
        return g
    lit, body, side, shade = (S['h'], S['e'], S['l'], S['p']) if metal == 'steel' else (D['4'], D['2'], D['1'], D['0'])
    g = grid(w, h, body)
    for j in range(h):
        g[j][0], g[j][-1] = lit if j < h - 1 else body, side
    g[0] = [S['g'] if metal == 'steel' and i % 2 == 0 else lit for i in range(w)]
    g[-1] = [shade] * w
    return g


def studded(f, w, h):
    """The second steel step: diamond studs in its shadow row (the old cone_2's)."""
    g = step(f, w, h, 'steel')
    if f not in ('up', 'down'):
        for i in range(1, w, 3): g[-1][i] = D['2']
    else:
        for j, i in ((0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)): g[j][i] = D['2']
    return g


def part(name, box, paint, rot=0):
    d = dims(box)
    return dict(name=name, box=box, faces={f: paint(f, *d[f]) for f in FACES}, rot=rot)


def cone(c):
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    return [part('s1', sq(4, 8, 10), lambda f, w, h: step(f, w, h, 'steel'), 22.5),
            part('s2', sq(3, 6, 8), studded, -22.5),
            part('s3', sq(2, 4, 6), lambda f, w, h: step(f, w, h, 'diamond'), 22.5),
            part('tip', sq(1, 3, 4), lambda f, w, h: step(f, w, h, 'diamond'), 45)]


def sprite():
    """The drill as seen from the side, 10 x 14 texels (5 x 7 px): steel steps 8, 6 texels wide with diagonal flutes,
    diamond steps 4, 2 to the point; each step's top row lit, its left column lit, its right column shaded."""
    W, H = 10, 14
    widths = [8] * 4 + [6] * 4 + [4] * 3 + [2] * 3
    g = grid(W, H)
    for j, w in enumerate(widths):
        a = (W - w) // 2
        diamond = j >= 8
        first = j == 0 or widths[j - 1] != w
        for i in range(a, a + w):
            k = i - a
            if diamond:
                c = D['4'] if first or k == 0 else D['0'] if k == w - 1 else D['3'] if (i + j) % 4 == 0 else D['2']
            else:
                f = (i + j) % 6   # the flutes: diagonal grooves (a dark row under a lit ridge), as the auger's
                c = S['g'] if first and k % 2 == 0 else S['h'] if first or k == 0 else S['p'] if k == w - 1 else \
                    S['s'] if f == 0 else S['p'] if f == 1 else S['h'] if f == 5 else S['e']
            g[j][i] = c
    return g


def cross(c):
    """Two planes through the axis, turned +-45 deg, the sprite on one face of each (the other see-through: a face
    and its back in one plane would flicker); the renderer draws the backs (entityCutoutNoCull)."""
    box = ((c - 2.5, TOP - 7, 0), (c + 2.5, TOP, 0))
    def paint(f, w, h):
        if f == 'north': return [list(r) for r in sprite()]
        return grid(w, h)
    return [part('p1', box, paint, 45), part('p2', box, paint, -45)]


def helix(f, w, h, period=12):
    """The column's faces: helical flutes round it, continuous across the corners (positions round the
    column: north x+ -> x-, west front -> back, south x- -> x+, east back -> front, as each face's columns run), a
    lit row over each flute; top steel, bottom a diamond-rimmed end."""
    if f in ('up', 'down'):
        g = grid(w, h, S['l'])
        if f == 'down':
            for j in range(h):
                for i in range(w):
                    if i in (0, w - 1) or j in (0, h - 1): g[j][i] = D['1']
        return g
    start = {'north': 0, 'west': w, 'south': 2 * w, 'east': 3 * w}[f]
    g = grid(w, h, S['e'])
    for j in range(h):
        for i in range(w):
            p = (start + i + j) % (period // 2)
            g[j][i] = S['s'] if p == 0 else S['p'] if p == 1 else S['h'] if p == 5 else S['e']
    g[0] = [S['g'] if i % 2 == 0 else S['h'] for i in range(w)]
    return g


def auger(c):
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    return [part('col', sq(3, 6, 10), helix),
            part('s3', sq(2, 4, 6), lambda f, w, h: step(f, w, h, 'diamond'), 45),
            part('tip', sq(1, 3, 4), lambda f, w, h: step(f, w, h, 'diamond'))]


def build(style, c):
    """The bit's parts for draft `style` on an arm centred at x c (right side): name, box (raw), faces, rot (deg
    about the arm's axis, y)."""
    return {'A': cone, 'B': cross, 'C': auger}[style](c)
