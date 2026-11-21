"""The flamethrower for the frame (frame_model.py, TOOL=flame): the fourth power tool brought over from the big suit.

PICKED (2026-11-14, after eight rounds; user: "definitely 5 tall"; frame_model's defaults): FLAME=D, FLAME_BODY=pump,
FLAME_BODY_H=2, FLAME_HOLES=even, FLAME_TANK_H=5. Under the socket: a 2 px steel body (a lit strap with two bolts, the
copper fuel line painted round it: up out of the tank on the back, along the outer side through a red valve wheel,
across the front and down into the barrel); under it the perforated 3 x 3 barrel at the front (7 px, three 1 px holes
a face two plain rows apart, the sooty muzzle 9 px under the socket), the red tank behind it (3 x 5 x 1.5, its hazard
band under the lit top, 0.5 px of daylight between), the matchstick: a slate rod down from the tank's bottom and a foot
forward under the barrel, its blue head (the reserved pilot colours) at the bore's back edge. The sections below are
the rounds, oldest first; their knobs rebuild them.

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


# Round 8 (2026-11-14, user: the barrel grew, scale the tank a bit as well): FLAME_TANK_H / FLAME_TANK_W (px) size it;
# tank_rows paints it at any size (lit top, the hazard band under it, red shaded to the right, a dark bottom row).
def tank_rows(n, w):
    def row(a, b): return a * (w - 1) + b
    hazard = [('NNKK' * w)[:w], ('NKKN' * w)[:w]]
    rows = [row('J', 'H'), row('H', 'F')] + hazard + [row('F', 'E')] * (n - 5) + ['E' * w]
    rows[4] = 'H' + rows[4][1:] if n > 5 else rows[4]
    assert len(rows) == n, rows
    return rows


# Round 2 (2026-11-14, user: "none are great honestly. The gas tank should not be the base, but then in B the base is
# basically wasted space"). The body must do a flamethrower's work itself, the tank off it. Drafts:
# - D burner: B's layout (barrel front, tank behind, under the body), the body the burner: the slate clamp band, then
#   two glowing slots a face (the fire's colours, hottest at the bottom, where the fuel lights);
# - E shroud: B's layout, the body the big perforated heat jacket (Fallout's flamer: a staggered grid of holes, a lit
#   collar at the arm), the barrel under it a plain steel nozzle with a sooty tip;
# - F arm tank: the tank strapped to the arm's back above the socket (3 x 3.5 px, 1.5 proud: the face the third-person
#   view sees), the body D's burner, the perforated barrel centred under it, the pilot rod behind (A's).
# FLAME_GLOW=lit (review) | dark (frame_model's reserved coal colours, as the fire glowmask lights them in game).
GLOW = {'lit': {'1': _c('ffdc6e'), '2': _c('ff9632'), '3': _c('d24619')},
        'dark': {'1': _c('3f211b'), '2': _c('371d19'), '3': _c('2f1a17')}}
BURNER = ['nnnnnnnnnm',
          'mhmmmmmmhk',
          'xxxxxxxxxx',
          'hezzllzzep',
          'he33ll33ep',
          'he22ll22ep',
          'he11ll11ep',
          'ssssssssss']
BURNER_DOWN = SPLIT_DOWN
JACKET = ['hhhhhhhhhe',
          'pppppppppz',
          'hxxllxxllp',
          'hxxllxxllp',
          'hellgllllp',
          'hllxxllxxp',
          'hllxxllxxp',
          'ssssssssss']
NOZZLE = ['sppppz', 'hellep', 'hellep', 'hglllp', 'hellep', 'zzzzzz', 'hellep', 'hellep', 'pssssz', 'szzzsz']
# the arm's tank (F), 6 x 7 a side (3.5 px: the iron pauldron comes down to raw 18 behind the arm): a steel strap at
# each end, the red body, the hazard band
ARM_TANK = ['hhhhhe', 'JJJJJH', 'NNKKNN', 'NKKNNK', 'HFFFFE', 'EEEEEE', 'hhhhhe']
ARM_TANK_SIDE = [r[:3] for r in ARM_TANK]


# Round 3 (2026-11-14, user: D, but change the base, and make the matchstick (the pilot rod) meet the fire hole). The
# pilot: the rod down from the tank's bottom, then a foot forward under the barrel, its blue head against the muzzle's
# bore (it lights the fuel as it leaves). The body (FLAME_BODY; 'burner' D's):
# - jacket: E's perforated jacket, its holes glowing in the fire's colours (the burner seen through it);
# - porthole: worn steel, a round brass-rimmed window on each side, the fire in it (the engine core's porthole);
# - grille: the iron armour's hot radiator (GUARD=hot): three slats across a dark slate surround, hottest in the middle.
BRASS = {'b': _c('d9c17a'), 'Y': _c('a89160'), 'Z': _c('6a5838')}
BODIES = {
    'burner': BURNER,
    'jacket': ['hhhhhhhhhe',
               'pppppppppz',
               'h33ll33llp',
               'h22ll22llp',
               'hellgllllp',
               'hll22ll22p',
               'hll11ll11p',
               'ssssssssss'],
    'porthole': ['hhhhhhhhhe',
                 'helbbYYlep',
                 'heb3333Zep',
                 'heb2222Zep',
                 'heY2211Zep',
                 'heY1111Zep',
                 'helZZZZlep',
                 'ssssssssss'],
    'grille': ['nnnnnnnnnm',
               'mxxxxxxxxk',
               'mx222222xk',
               'mxxxxxxxxk',
               'mx111111xk',
               'mxxxxxxxxk',
               'mx222222xk',
               'kkkkkkkkkk']}


# Round 4 (2026-11-14, user: the base more solid; seeing through to the fire doesn't make sense for a flamethrower).
# Closed steel bodies, the fire only implied (FLAME_BODY):
# - pump: the fuel line painted on: copper, up out of the tank on the back, along the outer side through a red valve
#   wheel, across the front and down into the barrel (tank -> body -> barrel: the body is where the fuel goes);
# - heat: the steel heat-tinted towards the barrel (straw, bronze, blue: steel that has been hot), a sooty bottom edge;
# - warning: a hazard band under the strap, a flame sign (an orange flame on a dark plate) on the outer side and front.
BODY4 = {'4': _c('c9a45c'), '5': _c('8a6038'), '6': _c('6a4a8a'), '7': _c('4a3460'),   # heat tints (straw .. blue)
         'f': drill.CU['f'], 'Q': drill.CU['Q'], 'C': drill.CU['C'], 'r': _c('9a2418')}  # copper, the wheel's shade
TOP2 = ['hhhhhhhhhe', 'pgppppppgz']
PLAIN = TOP2 + ['hellllllep'] * 5 + ['ssssssssss']
BODY_FACES = {   # (north, east, south, west) a body: north column 0 is the outer side, south the last
    # (round 4's pump, the line low; pump_faces() below draws it centred, at any height)
    'pump4': (TOP2 + ['hellllllep', 'hellllllep', 'fffffellep', 'QQQQfQllep', 'CCCCfQllep', 'sssCfQssss'],
             TOP2 + ['hellllllep', 'hellrRrlep', 'ffffRxRfff', 'QQQQrRrQQQ', 'CCCCCrCCCC', 'ssssssssss'],
             TOP2 + ['hellllllep', 'hellllllep', 'hellffffff', 'hellfQQQQQ', 'hellfQCCCC', 'sssCfQssss'],
             PLAIN),
    'heat': (TOP2 + ['hellllllep', 'hellllllep', '4444444445', '5555555556', '6666666667', 'zzzzzzzzzz'],) * 4,
    'warning': (TOP2 + ['NNKKNNKKNN', 'NKKNNKKNNK', 'hellxNxlep', 'hellNJxlep', 'helNJJNlep', 'sssxJJxsss'],
                TOP2 + ['NNKKNNKKNN', 'NKKNNKKNNK', 'helxNxxlep', 'helxNJxlep', 'helNJJNlep', 'sssxJJxsss'],
                TOP2 + ['NNKKNNKKNN', 'NKKNNKKNNK'] + ['hellllllep'] * 3 + ['ssssssssss'],
                TOP2 + ['NNKKNNKKNN', 'NKKNNKKNNK'] + ['hellllllep'] * 3 + ['ssssssssss'])}


# Round 5 (2026-11-14, user: the pump picked; the pump more in the middle; and the body's height should be each tool's
# own, not every tool gains from the same 4 px). FLAME_BODY_H (px, halves allowed: 2 texels a px) sets the body's
# height (its top stays at the socket, the barrel, tank and pilot hang from its bottom); the pump's paint is drawn for
# any height: the strap's two rows on top (one under 2.5 px), the bottom's shadow row (none under 3 px), the copper
# line (lit, mid, shade rows) centred between them, the valve wheel (4 x 3) centred on the outer side over it.
def pump_faces(n, w=10):
    """The pump body's (north, east, south, west) for a face n texels tall and w texels wide (10 or 12)."""
    top2 = ['h' * (w - 1) + 'e', 'pg' + 'p' * (w - 4) + 'gz']
    top = top2 if n >= 5 else top2[:1]
    bot = 's' * w
    bottom = [bot] if n >= 6 else []
    free = n - len(top) - len(bottom)
    assert free >= 3, n
    a = len(top) + (free - 3) // 2                          # the line's lit row
    plain = 'he' + 'l' * (w - 4) + 'ep'
    m = w // 2
    def face(line, below, last):
        rows = top + [plain] * free + bottom
        for k in range(3): rows[a + k] = line[k]
        for j in range(a + 3, n): rows[j] = last if j == n - 1 and bottom else below
        return rows
    n_below = 'he' + 'l' * (m - 3) + 'fQ' + 'l' * (w - m - 3) + 'ep'
    n_last = 's' * (m - 2) + 'CfQ' + 's' * (w - m - 1)
    north = face(['f' * m + 'e' + 'l' * (w - m - 3) + 'ep',
                  'Q' * (m - 1) + 'fQ' + 'l' * (w - m - 3) + 'ep',
                  'C' * (m - 1) + 'fQ' + 'l' * (w - m - 3) + 'ep'], n_below, n_last)
    south = face(['he' + 'l' * (m - 3) + 'f' * (w - m + 1),
                  'he' + 'l' * (m - 3) + 'f' + 'Q' * (w - m),
                  'he' + 'l' * (m - 3) + 'fQ' + 'C' * (w - m - 1)], n_below, n_last)
    east = face(['f' * w, 'Q' * w, 'C' * w], plain, bot)
    vx = m - 2
    for k, vw in enumerate(('rRRr', 'RxxR', 'rRRr')): east[a + k] = east[a + k][:vx] + vw + east[a + k][vx + 4:]
    return north, east, south, top + [plain] * free + bottom


# Round 6 (2026-11-14, user: 3 px picked; give the px the body lost to the barrel): the muzzle stays where it was (9 px
# under the socket, the chaingun's), the barrel takes what the body leaves: 6 px under the 3 px body. Its paint for
# any length (barrel_rows): the shadow row, the 1 px holes down the middle, the sooty end. FLAME_HOLES: 'keep' the
# 5 px barrel's rhythm (a hole, two plain rows, a hole; the rest plain over the soot) | 'even' as many holes as fit
# one plain row apart (three on 6 px).
MUZZLE_DROP = 9   # px from the socket to the muzzle


def barrel_rows(n, holes='keep', w=6):
    pad = (w - 6) // 2
    pl = 'he' + 'l' * (w - 4) + 'ep'
    gl = 'he' + 'l' * (pad + 1) + 'g' + 'l' * pad + 'ep'
    h0 = 'he' + 'l' * pad + 'xx' + 'l' * (pad + 1) + 'p'
    h1a = 'hl' + 'l' * pad + 'xx' + 'l' * pad + 'ep'
    h1b = 'hl' + 'l' * pad + 'xx' + 'l' * (pad + 1) + 'p'
    holes_ = ([h0, h0], [h1a, h1b])  # (the barrel's holes, lit a little differently)
    mid = n - 3                                             # between the shadow row and the two soot rows
    if holes == 'even':
        # (round 7, user: three holes a row apart looked smushed; the body down to 2 px for room) as many holes as fit
        # the 5 px barrel's rhythm (a plain row first, two between holes), the spare plain rows spread between them
        k = max(1, (mid + 1) // 4)
        spare = mid - 2 * k - 1 - 2 * (k - 1)
        rows = [pl] + holes_[0]
        for i in range(1, k):
            gap = 2 + spare // (k - 1) + (1 if i <= spare % (k - 1) else 0)
            rows += ([gl] + [pl] * (gap - 1)) + holes_[i % 2]
    else:
        rows = [pl] + holes_[0] + [gl, pl] + holes_[1]
    rows += [pl] * (mid - len(rows))
    assert len(rows) == mid, (n, rows)
    return ['s' + 'p' * (w - 2) + 'z'] + rows + ['p' + 's' * (w - 2) + 'z', 's' + 'z' * (w - 3) + 'sz']


def muzzle_face(w):
    if w == 6: return MUZZLE
    pad = (w - 4) // 2
    return (['z' + 's' * (w - 2) + 'z'] +
            ['s' + 'p' * (w - 2) + 'z'] * pad +
            ['s' + 'p' * pad + 'xx' + 'p' * pad + 'z'] * 2 +
            ['s' + 'p' * (w - 2) + 'z'] * pad +
            ['z' * w])


def build(c, top, kind='A', pilot='dark', glow='lit', body_art='burner', body_h=4, holes='keep', tank_h=4, tank_w=3, sleeve=False, head_scale=False):
    """The flamethrower's parts on an arm centred at x c (right side) whose socket is at y top (bone 'tool': all still)."""
    P = PAL | PILOT[pilot] | GLOW[glow] | BRASS | BODY4
    part = lambda name, box, faces: dict(drill.part(name, box, _paint(faces, P)), bone='tool')
    none = one('.')                                         # a face in another part's plane: not drawn
    t = top - body_h                                        # the body's bottom
    L = MUZZLE_DROP - body_h                                # the barrel's length: down to the muzzle
    side = lambda rows: {'north': rows, 'south': rows, 'east': rows, 'west': rows}
    bw = 3.0 if (sleeve and body_art == 'pump' and kind == 'D') else 2.5
    body = ((c - bw, t, -bw), (c + bw, top, bw))
    split = kind in ('B', 'D', 'E')                         # barrel at the front, the tank behind it
    if kind in ('A', 'C'):
        parts = [part('body', body, side(TANK_BODY) | {'up': one('E'), 'down': TANK_DOWN})]
    elif kind == 'B':
        parts = [part('body', body, {'north': SPLIT_BODY, 'south': SPLIT_BODY, 'east': SPLIT_OUTER, 'west': SPLIT_BODY,
                                     'up': one('k'), 'down': SPLIT_DOWN})]
    elif kind == 'E':
        parts = [part('body', body, side(JACKET) | {'up': one('k'), 'down': SPLIT_DOWN})]
    else:
        assert body_h == 4 or body_art == 'pump', 'only the pump is drawn for other heights'
        tw = round(bw * 4)
        faces = (side(BODIES[body_art]) if body_art in BODIES else dict(zip(
            ('north', 'east', 'south', 'west'), pump_faces(round(body_h * 2), tw) if body_art == 'pump' else BODY_FACES[body_art])))
        up_f = (['h' * (tw - 1) + 'e'] + ['h' + 'k' * (tw - 2) + 'p'] * (tw - 2) + ['p' * (tw - 1) + 'z']) if tw > 10 else one('k')
        dn_f = (['s' * tw] + ['s' + 'p' * (tw - 2) + 'z'] * (tw - 2) + ['z' * tw]) if tw > 10 else BURNER_DOWN
        parts = [part('body', body, faces | {'up': up_f, 'down': dn_f})]
    bar_w = 4.0 if (head_scale and split) else 3.0
    tw_ = 4.0 if (head_scale and split) else tank_w
    if split:
        bz0, bz1 = (-3.0, 1.0) if head_scale else (-2.5, 0.5)   # (0.5 px of daylight to the tank)
        tz0, tz1 = (1.5, 3.0) if head_scale else (1.0, 2.5)
        tf = tank_rows(round(tank_h * 2), round(tw_ * 2))
        ts = [r[-3:] for r in tf]
        parts.append(part('tank', ((c - tw_ / 2, t - tank_h, tz0), (c + tw_ / 2, t, tz1)),
                          {'north': tf, 'south': tf, 'east': ts, 'west': ts, 'up': none, 'down': one('E')}))
        rbox = ((c - 0.5, t - L - 1, tz0 + 0.25), (c + 0.5, t - tank_h, tz0 + 1.25))   # under the tank
    else:
        # the barrel 0.5 px in from the body's front, the rod flush with its back, 0.5 px of daylight between them
        bz0, bz1 = -2, 1
        tz0 = 1.0
        rbox = ((c - 0.5, t - L - 1, 1.5), (c + 0.5, t, 2.5))
    art = barrel_rows(round(L * 2), holes, round(bar_w * 2))
    holes = NOZZLE if kind == 'E' else art if kind != 'C' else [r.replace('x', '.') for r in art]
    parts.append(part('barrel', ((c - bar_w / 2, t - L, bz0), (c + bar_w / 2, t, bz1)),
                      side(holes) | {'up': none, 'down': muzzle_face(round(bar_w * 2))}))
    if kind == 'C':   # the core the holes show: black, 2 px inside the 3 px barrel (0.5 behind each hole: a 1 px core let
        # the eye onto the walls' insides, steel), its ends short of the body and the muzzle
        zc = (bz0 + bz1) / 2
        parts.append(part('core', ((c - 1, t - L + 0.5, zc - 1), (c + 1, t - 0.5, zc + 1)),
                          side(one('x')) | {'up': one('x'), 'down': one('x')}))
    if kind == 'F':   # on the arm's back (z 2.5), its front against it (not drawn), its bottom at the socket
        parts.append(part('tank', ((c - 1.5, top, 2.5), (c + 1.5, top + 3.5, 4)),
                          {'north': none, 'south': ARM_TANK, 'east': ARM_TANK_SIDE, 'west': ARM_TANK_SIDE,
                           'up': one('h'), 'down': one('p')}))
    if kind == 'D':   # (round 3) the matchstick: the rod 1 px under the tank, the foot forward to the bore's back edge
        y0 = t - L - 1                                      # the foot's bottom, a px under the muzzle
        assert t - tank_h > y0 + 1, 'the tank reaches the matchstick'
        pz0, pz1 = (1.5, 2.5) if head_scale else (1.0, 2.0)
        parts.append(part('pilot', ((c - 0.5, y0, pz0), (c + 0.5, t - tank_h, pz1)),
                          side(one('k')) | {'west': lambda w, h: ['mk'] * h, 'up': none, 'down': one('k')}))
        # the foot: from the bore's back edge (-0.5) to the rod, its front 2 texels the blue head
        head = lambda w, h: ['k' * (w - 2) + 'uv'] * h      # east: back -> front
        parts.append(part('pilot_foot', ((c - 0.5, y0, -0.5), (c + 0.5, y0 + 1, pz0)),
                          {'north': one('v'), 'south': none, 'east': head, 'west': lambda w, h: [r[::-1] for r in head(w, h)],
                           # (a down face's rows run back -> front, checked from straight below: written front -> back
                           # the blue went to the back, the slate under the head)
                           'up': none, 'down': lambda w, h: ['kk'] * (h - 2) + ['uu', 'vv']}))
    else:
        parts.append(part('pilot', rbox, side(rod) | {'up': none, 'down': one('v')}))
    for p in parts: p['rot'] = 0
    return parts
