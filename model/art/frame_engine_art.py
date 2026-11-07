"""The engine's paint for the frame (frame_model.py, draft knob ENGINE): every part's faces as letter grids.

The firebox engine (2026-11-05, user: the engines were backpacks; with the redesign, the furnace and exhausts stay on
the back and a core goes in front, pipes running through the sides; the armour is fitted to it later): the core's
porthole, the copper pipes, the pack drawn as a twin-cylinder steam engine (frame_model.py has the shapes and picks;
the exhausts are the old suit's, picked down there).

Letters are frame_model.py's PAL (uppercase: gunmetal N O X, copper Q R, brass Y Z, steel W V U G) and the iron
armour's (lowercase steel ramp, frame_iron_art.py), plus the fire, painted LIT here (F yellow-white, I orange,
J red: the old firebox's glow colours) so the review shows a burning engine; in game they'd be the reserved dark
colours and the glowmask (tools/make-glowmasks.py).
Faces as frame_model.py's: north / south as seen from the front / back, east back -> front, west front -> back; up
rows front -> back.
"""


def _box(front, back, side, up, down, side_w=None):
    return {'north': front, 'south': back, 'east': side, 'west': side_w or side, 'up': up, 'down': down}


def porthole(W=8, H=8, corner='l'):
    """The core's face (2 texels per px over its 4 x 4): a round porthole, a brass ring, the fire behind glass, the
    corners in the housing's colour (corner)."""
    front = ['ccYYYYcc',
             'cYXJJXYc',
             'YXJIIJXY',
             'YJIFFIJY',
             'YJIFFIJY',
             'YXIFFIXY',
             'cZXXXXZc',
             'ccZZZZcc']
    front = [r.replace('c', corner) for r in front]
    rim = {'.': 'Z', 'Q': 'R'}.get(corner, corner)   # its sides (copper: the pipes' shaded side)
    return _box(front, ['X' * W] * H, [rim] * H, [rim * W], [rim * W])


def pipe_box(W, H, D):
    """A copper pipe box W x H x D texels (2 per px), running any way: a face longer than tall lit along its top
    row, a taller one along its left column."""
    face = lambda w, h: [('Q' if j == 0 else 'R') * w for j in range(h)] if h <= w else ['Q' + 'R' * (w - 1)] * h
    return _box(face(W, H), face(W, H), face(D, H), ['Q' * W] * D, ['R' * W] * D)


# ---------------------------------------------------------------- the pack, drawn as an engine
# (2026-11-05, user: the back should look like an engine; frame_model.py has the picks.) The pack is 10 x 11 x 5 px,
# painted at 2 texels per px: back 20 x 22, sides 10 x 22, top / bottom 20 x 10. Letters: frame_model.PAL (gunmetal
# N O X, steel W V U G, copper Q R, brass Y Z, fire F I J) and the iron ramp (lowercase, frame_iron_art.PAL).
# The exhausts leave the top over x +-(2.75..4.75), z 6..8: the holes at columns 1-4 / 15-18, rows 6-9.
PW, PH, PDP = 20, 22, 10


def _grid(w, h, c): return [[c] * w for _ in range(h)]


def _put(g, x, y, rows):
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != ' ' and 0 <= y + j < len(g) and 0 <= x + i < len(g[0]): g[y + j][x + i] = c


def _fire(w, rows=('J', 'I', 'F'), bars=None):
    """Coal rows (red on top, yellow-white at the bottom) w texels wide behind symmetric grate bars."""
    bars = bars if bars is not None else {i for i in range(w) if i % 4 == 2} | {w - 1 - i for i in range(w) if i % 4 == 2}
    return [''.join('X' if i in bars else c for i in range(w)) for c in rows]


def _top(rim='O', plate='N', hole='X', extra=None):
    g = _grid(PW, PDP, plate)
    g[0] = ['O'] * PW
    for c0 in (1, 15):
        for j in range(5, 11):
            for i in range(c0 - 1, c0 + 5):
                if 0 <= i < PW and 0 <= j < PDP:
                    g[j][i] = hole if (c0 <= i < c0 + 4 and 6 <= j < 10) else rim
    if extra: extra(g)
    return [''.join(r) for r in g]


def _faces(back, side, top):
    return {'north': ['X' * PW] * PH, 'south': [''.join(r) for r in back], 'east': side, 'west': [r[::-1] for r in side],
            'up': top, 'down': ['X' * PW] * PDP}


def back_pistons():
    """A twin-cylinder steam engine: two upright cylinders on the back corners (brass heads, the stacks leave their
    tops), their piston rods down into a crankcase, the firebox door between them over an ash slit."""
    g = _grid(PW, PH, 'N')
    cyl = ['YYYYY', 'ZZZZZ'] + ['UVWVN'] * 4 + ['XXXXX'] + ['UVWVN'] * 4 + ['ZZZZZ']
    rod = ['XXWXX'] * 4
    for x0 in (1, 14):
        _put(g, x0, 1, cyl + rod)
    _put(g, 0, 0, ['O' * PW])
    door = ['GWWWWWWG'] + ['G' + r + 'G' for r in _fire(6, rows=('J', 'J', 'I', 'I', 'I', 'F', 'F', 'F'), bars={1, 4})] + \
        ['GUUUUUUG', 'XXXXXXXX', 'NKKKKKKN', 'NNNNNNNN', 'NKKKKKKN']
    _put(g, 6, 2, door)
    _put(g, 0, 17, ['O' * PW, 'N' + 'X' * 18 + 'N', 'NOOOONNNNNNNNNNOOOON', 'NNNNNNNNNNNNNNNNNNNN', 'X' * PW])
    _put(g, 0, 21, ['X' * PW])
    side = ['O' * PDP] + ['NUVWVNNUVN'] * 15 + ['O' * PDP] + ['N' * PDP] * 4 + ['X' * PDP]
    def caps(t):
        for c0 in (1, 15):
            for j in range(5, 11):
                for i in range(c0 - 1, c0 + 5):
                    if 0 <= i < PW and 0 <= j < PDP and t[j][i] != 'X': t[j][i] = 'Y'
    return _faces(g, side, _top(extra=caps))


