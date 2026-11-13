"""The drill for the frame (frame_model.py, TOOL=drill): the first power tool brought over from the big suit, sized
down to the frame's arm and redrawn.

2026-11-13 (user: bring the power tools over from the old suit, scaled down and redesigned; the drill first). It
hangs in the left arm's socket (frame_model.SOCKET, the big suit's playbook: the tool arm has no hand), on its own
bone (`tool`, its pivot on the arm's axis at the socket: the bit spins about y in game). Tools may be models of
several parts (user, 2026-11-13: the exception to the simple boxes).
The big suit's drill (mining_tools_art.py): a 7 x 1 x 7 socket base, a 6 x 2 x 6 motor hub, steel cone steps and a
diamond point, 11 px. The frame's, 7 px under the socket (its point 8 px over the ground with the arm hanging):
- the body: one 6 x 4 x 6 block (base + motor, see BODY below; the user's, 2026-11-13: a 3D guard cuff with a lamp
  and a separate base, 4dad9e4, didn't feel right);
- the cone (picked from drafts A cone, B crossed planes, C auger, commit 0988ca2): the big suit's stepped cone sized
  down, steel step 4 px with diamond studs, diamond steps 3 and 1, 2 px tall but the point (1), turned +-22.5 / 45
  deg in turn (a twisted auger).

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


# The status lamp's colours (red idle, green spinning: LAMP): highlight, lit, rim.
LAMPS = {'red': ('ffb0a0', 'e8402a', '9a2418'), 'green': ('c8ffc0', '4fe05a', '2a8a34')}
# copper (frame_heart_art.EXTRA, frame_model.PAL Q / R): lit, mid, shade
CU = {'f': _c('e09868'), 'Q': _c('c07440'), 'C': _c('804426')}


def _rows(rows, pal):
    for r in rows: assert len(r) == len(rows[0]), rows
    return [[pal[ch] for ch in r] for r in rows]


# BODY (2026-11-13, user: the drill's 3D housing and guard didn't feel right; like the shoulder plates, the heart
# engine and the helmet it reads better as a simple block with the elements painted on, so they replaced it with one
# block, then: fit it to the shoulder plate above it, just bigger than the arm). One 6 x 4 x 6 block, 0.5 px past the
# arm on every side (as the plate is past its top), its top 2 px round the arm's end (the base: it clamps on the
# socket), the bottom 2 px under it (the motor), the bit under that. 2 texels per px: sides 12 x 8, top / bottom 12 x 12.
# The base: a slate clamp band (lit top row, two bolts a face, the status lamp at the front's outer end), a dark seam;
# the motor under it in steel, its middle rows the draft's element (DRILL_ART): A vent slots | B a copper winding
# window | C cooling fins.
BASE = ['nnnnnnnnnnnm', 'mmmmmmmmmmmk', 'mmhmmmmmmhmk', 'xxxxxxxxxxxx']
LAMP_AT = {1: 'mWLmmmmmmmmk', 2: 'mLrmmmmmmhmk'}   # the front's base rows 1-2 (its outer end first)
MOTOR = {'A': ['hhhhhhhhhhhe', 'elzlzllzlzlp', 'elzlzllzlzlp', 'ssssssssssss'],
         'B': ['hhhhhhhhhhhe', 'elzffffffzlp', 'elzQCQCQCzlp', 'ssssssssssss'],
         'C': ['hhhhhhhhhhhe', 'zzzzzzzzzzzz', 'hhhhhhhhhhhe', 'zzzzzzzzzzzz']}
# underneath (rows front -> back): the motor's steel round a dark chuck hole the bit hangs from, a bolt in each corner;
# on top only its 1-texel rim shows round the arm: the base's lit slate
DOWN = ['pppppppppppp', 'phllllllllhp'] + ['plxxxxxxxxlp'] * 8 + ['phllllllllhp', 'pppppppppppp']
UP = ['nnnnnnnnnnnn'] + ['nkkkkkkkkkkn'] * 10 + ['nnnnnnnnnnnn']


# The base open behind and inside (DRILL_BASE=open, 2026-11-13, user, picking B: the inner and back sides without the
# dark band, see-through, for an asymmetric look): the clamp wraps only the front and outer side, a plate 0.5 px off
# the arm like the shoulder plate's decal, and the arm's end shows behind and inside. 'wrap' keeps the closed band.
# So the block is two boxes, base over motor, the same outside: open, one box let the eye down the 0.5 px gap into
# its inside (the bit's top and the block's bottom, back to back there, flickered); the motor's own top closes it,
# its 1-texel rim round the arm a lit ledge.
OPEN = ('south', 'west')   # the back, and the inner side (the right arm's west; the left mirrors it)
LEDGE = ['eeeeeeeeeeee'] + ['ellllllllllp'] * 10 + ['pppppppppppp']


def _pal(lamp):
    W_, L_, r_ = LAMPS[lamp]
    return S | SL | {'x': _c('1a1d1f'), 'n': _c('4c5559')} | CU | {'W': _c(W_), 'L': _c(L_), 'r': _c(r_), '.': '.'}


def base(lamp, mode='open'):
    faces = {'north': [LAMP_AT.get(j, r) for j, r in enumerate(BASE)], 'up': UP, 'down': ['.' * 12] * 12}
    if mode == 'open':
        for f in OPEN: faces[f] = ['.' * 12] * len(BASE)
        # the top's rim along the open sides goes too (rows front -> back, columns inner -> outer on the right arm)
        faces['up'] = ['.' + r[1:] for r in UP[:-1]] + ['.' * 12]
    return lambda f, w, h: _rows(faces.get(f, BASE), _pal(lamp))


def motor(art, lamp):
    faces = {'up': LEDGE, 'down': DOWN}
    return lambda f, w, h: _rows(faces.get(f, MOTOR[art]), _pal(lamp))


def build(c, top, lamp='red', art='B', mode='open'):
    """The drill's parts on an arm centred at x c (right side) whose end (the socket) is at y top: name, box (raw),
    faces, rot (deg about the arm's axis, y), bone ('tool': still; 'bit': spins). The body (base, motor) is still,
    the steps under it spin."""
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    t = top
    parts = [part('base', sq(6, t, t + 2), base(lamp, mode)), part('motor', sq(6, t - 2, t), motor(art, lamp))]
    bit = [part('s2', sq(4, t - 4, t - 2), studded, -22.5),
           part('s3', sq(3, t - 6, t - 4), lambda f, w, h: step(f, w, h, 'diamond'), 22.5),
           part('tip', sq(1, t - 7, t - 6), lambda f, w, h: step(f, w, h, 'diamond'), 45)]
    for p in parts: p['bone'] = 'tool'
    for p in bit: p['bone'] = 'bit'
    return parts + bit
