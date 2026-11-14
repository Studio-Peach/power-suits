"""The flamethrower for the frame (frame_model.py, TOOL=flame): the fourth power tool brought over from the big suit.

2026-11-14 (user: the flamethrower next, the previous model as the reference). The big suit's (11f1db0,
model/art/flame_drafts_art.py: Fallout's flamer, "the barrel with holes, the tank underneath"): a 5 x 1 x 5 socket
base, a slim 3 x 3 barrel 9 px long in worn steel, perforated (a column of 1 px holes down each face, black inside),
a 3 x 2 red fuel tank behind it (+z: underneath when the arm is raised to fire) with a yellow / black hazard band and a
steel cap, a slate pilot-light rod under the tank reaching to a 1 px blue tip under the muzzle (the reserved pilot
colours: dark when off, lit by the glowmask). Its signatures: the red tank with the hazard band, the perforated barrel,
the blue pilot light.

Built in the tools' slot (power-suits-frame.md, Tools): the body takes the fist's place (5 x 4 x 5, raw y 10-14) and
the tool grows only from its bottom: the barrel 5 px (its end raw y 5, the chaingun's muzzle height), the pilot tip a
px under it. Drafts (FLAME):
- A tank: the body is the fuel tank (red, a steel clamp strap at the arm, the hazard band), the perforated barrel
  under it, the pilot rod down its back;
- B split: the old layout: a steel body (the drill's slate clamp band, a pressure gauge on the outer side), the barrel
  (front) and the red tank (back) side by side under it, daylight between, the pilot rod under the tank;
- C open: A, the barrel's holes cut through (see-through texels) over a black core inside: the big suit's real 3D
  holes, in one box.
Nothing spins: every part is on the still `tool` bone. FLAME_PILOT=dark (the reserved colours, as in game) | lit
(their glow, for review).

Coordinates raw, right arm (+x; the left mirrors), centred on the arm's axis (x c, z 0). Faces as frame_drill_art.py
(north / south as seen from the front / back, east back -> front, west front -> back, up / down rows front -> back).
"""
import frame_drill_art as drill

_c = drill._c
PAL = drill.S | drill.SL | {k: _c(v) for k, v in {
    'x': '1a1d1f', 'n': '4c5559',                                        # dark (bores, seams), slate lit
    'J': 'd9603c', 'H': 'b5412a', 'F': '8e2a1c', 'E': '5e1a14',          # the big suit's tank red: lit .. shade
    'N': 'd9962a', 'K': '1a1d1f',                                        # its hazard band: yellow, black
    'R': 'e8402a', 'G': 'e8e2cf'}.items()} | {'.': '.'}                  # the gauge's needle, its face
PILOT = {'dark': {'u': _c('1b2638'), 'v': _c('22304a')},                 # tools/make-glowmasks.py's pilot colours
         'lit': {'u': _c('2a6cff'), 'v': _c('8ec2ff')}}                  # (their glow)


def _paint(faces, P):
    for f, rows in faces.items(): assert callable(rows) or all(len(r) == len(rows[0]) for r in rows), f
    return lambda f, w, h: [[P[ch] for ch in r] for r in (faces[f](w, h) if callable(faces[f]) else faces[f])]


def one(ch): return lambda w, h: [ch * w] * h


# The fuel tank as the body (A, C), 10 x 8 a side: a steel clamp strap at the arm (lit row, a bolt at each end), the
# red tank (lit top, light from the left: lit first column, shaded last), the hazard band across its middle, a dark
# bottom edge.
TANK_BODY = ['hhhhhhhhhe',
             'pgppppppgs',
             'JJJJJJJJJH',
             'JHHHHHHHHF',
             'NNKKNNKKNN',   # (2-texel diagonal stripes: a 1-texel checker read as a checkerboard)
             'NKKNNKKNNK',
             'HFFFFFFFFE',
             'EEEEEEEEEE']
TANK_DOWN = ['EEEEEEEEEE'] + ['EFFFFFFFFE'] * 8 + ['EEEEEEEEEE']

# The barrel, 3 x 3 px: worn steel (lit left column, shaded right, a glint), a hole (2 x 2 texels: 1 px, as the big
# suit's) twice down each face's middle, a shadow row under the body, the muzzle end sooty (as the big suit's).
BARREL = ['sppppz',
          'hellep',
          'hexxlp',
          'hexxlp',
          'helgep',
          'hellep',
          'hlxxep',
          'hlxxlp',
          'pssssz',
          'szzzsz']
MUZZLE = ['zssssz', 'sppppz', 'spxxpz', 'spxxpz', 'sppppz', 'zzzzzz']   # its end: a rim round the bore

# The pilot-light rod (1 x 1 px): slate, lit on its left, its bottom px the tip in the pilot colours.
def rod(w, h): return ['mk'] * (h - 2) + ['vu', 'uu']


# B's steel body: the drill's slate clamp band (lit row, bolts), a dark seam, worn steel under it; a pressure gauge
# (a pale dial, a red needle, a dark rim) on the outer side.
SPLIT_BODY = ['nnnnnnnnnm',
              'mmmmmmmmmk',
              'mhmmmmmmhk',
              'xxxxxxxxxx',
              'hellllllep',
              'hellllllep',
              'hellllllep',
              'ssssssssss']
GAUGE = {4: 'helxGGxlep', 5: 'helGRGGlep', 6: 'helxGGxlep'}   # rows 4-6 of the outer side
SPLIT_OUTER = [GAUGE.get(j, r) for j, r in enumerate(SPLIT_BODY)]
SPLIT_DOWN = ['ssssssssss'] + ['sppppppppz'] * 8 + ['zzzzzzzzzz']
# B's tank (3 x 4 px, 1.5 deep), the old one's paint: lit top, the hazard band, a shaded bottom
TANK = ['JJJJJH', 'HHHHHF', 'NNKKNN', 'NKKNNK', 'HFFFFE', 'FFFFFE', 'FFFFFE', 'EEEEEE']
TANK_SIDE = [r[:3] for r in TANK]


def build(c, top, kind='A', pilot='dark'):
    """The flamethrower's parts on an arm centred at x c (right side) whose socket is at y top (bone 'tool': all still)."""
    P = PAL | PILOT[pilot]
    part = lambda name, box, faces: dict(drill.part(name, box, _paint(faces, P)), bone='tool')
    none = one('.')                                         # a face in another part's plane: not drawn
    t, L = top - 4, 5                                       # the body's bottom; the barrel's length
    side = lambda rows: {'north': rows, 'south': rows, 'east': rows, 'west': rows}
    if kind in ('A', 'C'):
        parts = [part('body', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), side(TANK_BODY) | {'up': one('E'), 'down': TANK_DOWN})]
        # the barrel 0.5 px in from the body's front, the rod flush with its back, 0.5 px of daylight between them
        bz0, bz1 = -2, 1
        rbox = ((c - 0.5, t - L - 1, 1.5), (c + 0.5, t, 2.5))
    else:
        parts = [part('body', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)),
                      {'north': SPLIT_BODY, 'south': SPLIT_BODY, 'east': SPLIT_OUTER, 'west': SPLIT_BODY,
                       'up': one('k'), 'down': SPLIT_DOWN})]
        bz0, bz1 = -2.5, 0.5                                # the barrel at the front, the tank behind (0.5 px apart)
        parts.append(part('tank', ((c - 1.5, t - 4, 1), (c + 1.5, t, 2.5)),
                          {'north': TANK, 'south': TANK, 'east': TANK_SIDE, 'west': TANK_SIDE, 'up': none,
                           'down': one('E')}))
        rbox = ((c - 0.5, t - L - 1, 1.25), (c + 0.5, t - 4, 2.25))   # under the tank, down to a px under the muzzle
    holes = BARREL if kind != 'C' else [r.replace('x', '.') for r in BARREL]
    parts.append(part('barrel', ((c - 1.5, t - L, bz0), (c + 1.5, t, bz1)), side(holes) | {'up': none, 'down': MUZZLE}))
    if kind == 'C':   # the core the holes show: black, 2 px inside the 3 px barrel (0.5 behind each hole: a 1 px core let
        # the eye onto the walls' insides, steel), its ends short of the body and the muzzle
        zc = (bz0 + bz1) / 2
        parts.append(part('core', ((c - 1, t - L + 0.5, zc - 1), (c + 1, t - 0.5, zc + 1)),
                          side(one('x')) | {'up': one('x'), 'down': one('x')}))
    parts.append(part('pilot', rbox, side(rod) | {'up': none, 'down': one('v')}))
    for p in parts: p['rot'] = 0
    return parts
