"""The drill for the frame (frame_model.py, TOOL=drill): the first power tool brought over from the big suit, sized
down to the frame's arm and redrawn.

2026-11-13 (user: bring the power tools over from the old suit, scaled down and redesigned; the drill first). It
hangs in the left arm's socket (frame_model.SOCKET, the big suit's playbook: the tool arm has no hand), on its own
bone (`tool`, its pivot on the arm's axis at the socket: the bit spins about y in game). Tools may be models of
several parts (user, 2026-11-13: the exception to the simple boxes).
The big suit's drill (mining_tools_art.py): a 7 x 1 x 7 socket base, a 6 x 2 x 6 motor hub, steel cone steps and a
diamond point, 11 px. The frame's, 7 px (its point 8 px over the ground with the arm hanging), straight under the
socket (its base is painted on the arm's end, frame_model.SOCKET: a 1 px base cube read as a step; user, 2026-11-13):
- the cone (picked from drafts A cone, B crossed planes, C auger, commit 0988ca2): the big suit's stepped cone sized
  down, steel steps 4 and 3 px (the second with diamond studs), diamond steps 2 and 1, each 2 px tall but the point
  (1), turned +-22.5 / 45 deg in turn (a twisted auger).

Coordinates are raw (frame_model.py adds FY), the right arm's (+x; the left mirrors), centred on the arm's axis (x c,
z 0) under the socket (y top). Art at 2 texels per px, RGBA tuples ('.' see-through). Faces as frame_model.py's: north
/ south as seen from the front / back, east back -> front, west front -> back, up rows front -> back.
"""
from frame_radial_art import dims, FACES

_c = lambda h: tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
# the iron armour's steel ramp (frame_iron_art.PAL) and the big suit's diamond (mining_tools_art.py: vanilla's)
S = {k: _c(v) for k, v in {'z': '22262e', 's': '3c424c', 'p': '58606a', 'l': '757c85', 'e': '8a9097', 'h': '9fa4a9',
                           'g': 'cdcfcf', 'w': 'fbf8f0'}.items()}
SL = {k: _c(v) for k, v in {'d': '25292c', 'k': '2f3437', 'm': '3b4246'}.items()}   # slate
D = {k: _c(v) for k, v in {'0': '0e7b7a', '1': '12a1a0', '2': '2ce3d9', '3': 'a1fbe8', '4': 'e4fffa'}.items()}


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


def part(name, box, paint, rot=0):
    d = dims(box)
    return dict(name=name, box=box, faces={f: paint(f, *d[f]) for f in FACES}, rot=rot)


def studded(f, w, h):
    """The second steel step: diamond studs in its shadow row (the old cone_2's)."""
    g = step(f, w, h, 'steel')
    if f not in ('up', 'down'):
        for i in range(1, w, 3): g[-1][i] = D['2']
    else:
        for j, i in ((0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)): g[j][i] = D['2']
    return g


# The guard's lamp: its colours per state.
LAMPS = {'red': ('ffb0a0', 'e8402a', '9a2418'), 'green': ('c8ffc0', '4fe05a', '2a8a34')}   # highlight, lit, rim


def _rows(rows, pal):
    for r in rows: assert len(r) == len(rows[0]), rows
    return [[pal[ch] for ch in r] for r in rows]


def panel(lamp):
    """The guard's two painted views, 2 texels per px, 4 rows (its 2 px): the front (12 columns: outer corner ->
    inner end) and the outer side (12 columns: back -> front corner). Plain steel (a lit top row and corner, a shadow
    row), the status lamp (red idle, green spinning) in a dark bezel at the front's outer end; two bolts on the side.
    (Drafted first 4 px tall with gauges, a bar-meter screen, vents or hazard stripes: too busy, user, 2026-11-13.)"""
    W_, R_, r_ = LAMPS[lamp]
    pal = {k: v for k, v in S.items()} | {k: v for k, v in SL.items()} | {'W': _c(W_), 'R': _c(R_), 'r': _c(r_)}
    front = ['hghghghghghp', 'hdWRdeeeeelp', 'hdRrdeeeeelp', 'pppppppppppp']
    side = ['ghghghghghgh', 'lemeeeeeemeh', 'leeeeeeeeeeh', 'pppppppppppp']
    return _rows(front, pal), _rows(side, pal)


def cuff(c, top, lamp, T=1, H=2):
    """The guard: an L-shaped cuff T px thick round the arm's front and outer side, its last H px over the
    socket (x c +-2.5 the arm), flush with the arm's inner side and back (the tools grow outward and forward: user,
    2026-11-13); two boxes, the front one over the corner."""
    front, side = panel(lamp)
    fbox = ((c - 2.5, top, -2.5 - T), (c + 2.5 + T, top + H, -2.5))
    obox = ((c + 2.5, top, -2.5), (c + 2.5 + T, top + H, 2.5))
    k = round(T * 2)
    lid = lambda w, h: [[S['h'] if j == 0 else S['l'] for i in range(w)] for j in range(h)]
    def fpaint(f, w, h):
        if f == 'north': return front
        if f == 'east': return [r[-k:] for r in side]                 # the corner's side: the outer view's front end
        if f == 'up': return lid(w, h)
        if f == 'west': return [[S['l']] * w for _ in range(h)]
        return grid(w, h, S['p'])
    def opaint(f, w, h):
        if f == 'east': return [r[:-k] for r in side]
        if f == 'up': return lid(w, h)
        if f == 'south': return [[S['l']] * w for _ in range(h)]
        return grid(w, h, S['p'])
    return [part('panel_front', fbox, fpaint), part('panel_side', obox, opaint)]


def build(c, top, lamp='red'):
    """The drill's parts on an arm centred at x c (right side) whose end (the socket) is at y top: name, box (raw),
    faces, rot (deg about the arm's axis, y), bone ('tool': still; 'bit': spins). The first step is the bit's fixed
    base (2026-11-13, user): square under the arm, not turned, on the still bone; the steps under it spin."""
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    t = top
    parts = cuff(c, top, lamp) + [part('base', sq(5, t - 2, t), lambda f, w, h: step(f, w, h, 'steel'))]
    bit = [part('s2', sq(4, t - 4, t - 2), studded, -22.5),
           part('s3', sq(3, t - 6, t - 4), lambda f, w, h: step(f, w, h, 'diamond'), 22.5),
           part('tip', sq(1, t - 7, t - 6), lambda f, w, h: step(f, w, h, 'diamond'), 45)]
    for p in parts: p['bone'] = 'tool'
    for p in bit: p['bone'] = 'bit'
    return parts + bit
