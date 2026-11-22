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


# ---------------- 2026-11-22 2D-texture + 0.5 px outer-cutout-layer rework drafts ----------------
# Matches the rail cannon's approved 2-layer language (2d_hybrid_closed): pure iron-armor steel outer coverings
# (z s p l e h g w) with alpha-0 cutout windows/perforations revealing recessed dark-slate, warm copper fuel lines,
# red hazard canisters, and a cleanly integrated muzzle pilot flame (ToolLight.PILOT) 0.5 px deeper.

def _cuff_ring(w, h):
    """1-texel lit steel bevel ring around the 5x5 arm opening; inner 10x10 transparent."""
    g = [['.'] * w for _ in range(h)]
    for i in range(w):
        g[0][i] = 'g' if i < w - 1 else 'h'
        g[h - 1][i] = 'e' if i == 0 else 's'
    for j in range(1, h - 1):
        g[j][0] = 'h'
        g[j][w - 1] = 'p'
    return g


def _build_2d_shroud(c, top, P, mode='shroud'):
    """4-cube stepped arm-cannon flamer (6x4x6 iron cuff -> 5x5x5 perforated iron heat shroud -> 4x4 sooty nozzle,
    9 px total matching MUZZLE_DROP=9).
    - mode='shroud'     : iron cuff w/ front pressure gauge window, side recessed copper pump+valve windows, and back
                          recessed red hazard fuel cell; barrel has twin 2x2 cutout cooling holes over copper burner.
    - mode='caged_tank' : red hazard fuel canister wraps all 4 sides of the recessed 5x4x5 inner cuff behind bold
                          6x4 iron armor cage windows (unmistakable red/hazard read from every angle) + perforated barrel."""
    part = lambda name, box, faces: dict(drill.part(name, box, _paint(faces, P)), bone='tool', rot=0)
    none = one('.')
    t = top - 4.0
    y_bot = top - 9.0

    # 1. Cuff inner (5x4x5 -> 10x8 sides, 10x10 down)
    if mode == 'caged_tank':
        # Pressurized red fuel canister with yellow/black hazard band recessed inside the iron cage on all 4 sides
        tank_side = [
            'dkkkkkkkkd',
            'dJJJJJJJHd',
            'dJHHHHHHFd',
            'dNNKKNNKKd',
            'dNKKNNKKNd',
            'dHFFFFFFEd',
            'dEEEEEEEEd',
            'dddddddddd',
        ]
        # Front has a crisp copper feed manifold + gauge detail centered over the canister
        cuff_in_n = [
            'dkkkkkkkkd',
            'dJJJffJJHd',
            'dJHHQQHHFd',
            'dNNKffKKNd',
            'dNKKQQKNNd',
            'dHFFCCFFEd',
            'dEEEEEEEEd',
            'dddddddddd',
        ]
        cuff_in_s = tank_side
        cuff_in_e = tank_side
        cuff_in_w = tank_side
        # Outer 6x4x6 pure iron-armor cage with bold 6x4 cutout windows on all 4 sides
        cage_face = [
            'ghhhhhhhhhhe',
            'ezllllllllzp',
            'elX......Xlp',
            'elX......Xlp',
            'elX......Xlp',
            'elX......Xlp',
            'sssssssssssz',
            'XXXXXXXXXXXX',
        ]
        cage_fb = [
            'ghhhhhhhhhhe',
            'ezllllllllzp',
            'elX..XX..Xlp',
            'elX..XX..Xlp',
            'elX..XX..Xlp',
            'elX..XX..Xlp',
            'sssssssssssz',
            'XXXXXXXXXXXX',
        ]
        cuff_out = {'north': cage_fb, 'south': cage_face, 'east': cage_face, 'west': cage_face}
    else:
        # 'shroud': slate inner base with front pressure gauge, side copper pump + red valve wheel, back red hazard tank
        cuff_in_n = [
            'dkkkkkkkkd',
            'dmmmmmmmmd',
            'dkkXGGXkkd',
            'dmmGGRGmmd',
            'dkkGxGGkkd',
            'dmmXGGXmmd',
            'dkkkkkkkkd',
            'dddddddddd',
        ]
        cuff_in_e = [
            'dkkkkkkkkd',
            'dmmmmmmmmd',
            'dXCCrRrCCd',
            'dfffRxRffd',
            'dQQQrRrQQd',
            'dXCCCCCCXd',
            'dkkkkkkkkd',
            'dddddddddd',
        ]
        cuff_in_w = [
            'dkkkkkkkkd',
            'dmmmmmmmmd',
            'dXCCCCCCXd',
            'dffffffffd',
            'dQQQQQQQQd',
            'dXCCCCCCXd',
            'dkkkkkkkkd',
            'dddddddddd',
        ]
        cuff_in_s = [
            'dkkkkkkkkd',
            'dJJJJJJJHd',
            'dJHHHHHHFd',
            'dNNKKNNKKd',
            'dNKKNNKKNd',
            'dHFFFFFFEd',
            'dEEEEEEEEd',
            'dddddddddd',
        ]
        cuff_out = {
            'north': [
                'ghhhhhhhhhhe',
                'ezllllllllzp',
                'ellXX..XXllp',
                'ellX....Xllp',
                'ellX....Xllp',
                'hhhXX..XXhhp',
                'ssssXXXXsssz',
                'XXXXXXXXXXXX',
            ],
            'east': [
                'ghhhhhhhhhhe',
                'ezllllllllzp',
                'ellllllllllp',
                'elX......Xlp',
                'elX......Xlp',
                'hhhhhhhhhhhp',
                'sssssssssssz',
                'XXXXXXXXXXXX',
            ],
            'west': [
                'ghhhhhhhhhhe',
                'ezllllllllzp',
                'ellllllllllp',
                'elX......Xlp',
                'elX......Xlp',
                'hhhhhhhhhhhp',
                'sssssssssssz',
                'XXXXXXXXXXXX',
            ],
            'south': [
                'ghhhhhhhhhhe',
                'ezllllllllzp',
                'elX......Xlp',
                'elX......Xlp',
                'elX......Xlp',
                'elX......Xlp',
                'sssssssssssz',
                'XXXXXXXXXXXX',
            ],
        }

    cuff_dn = ['dddddddddd'] + ['dkkkkkkkkd'] * 8 + ['dddddddddd']
    parts = [
        part('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in_n, 'south': cuff_in_s, 'east': cuff_in_e, 'west': cuff_in_w,
            'up': none, 'down': cuff_dn,
        }),
        part('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), cuff_out | {
            'up': _cuff_ring, 'down': none,
        }),
    ]

    # 2. Recessed 4x5x4 inner burner tube (8x10 sides, 8x8 down): dark slate + warm copper fuel burner pipe,
    # heat-darkened/sooty muzzle tip at row 9 with the glowing blue pilot flame (u/v) tucked cleanly on the front rim!
    bar_in_plain = [
        'dkkkkkkd',
        'dXCCCCXd',
        'dXfQQfXd',
        'dXQCCQXd',
        'dXCCCCXd',
        'dXfQQfXd',
        'dXQCCQXd',
        'dXzzzzXd',
        'dzzzzzzd',
        'zssssssz',
    ]
    bar_in_north = bar_in_plain[:-2] + [
        'dzzuuzzd',
        'zssvvssz',
    ]
    # Muzzle bore (8x8 down, rows back -> front): sooty ring, black flame bore, glowing blue pilot flame at front edge
    bar_dn = [
        'zssssssz',
        'szzzzzzs',
        'szxxxxzs',
        'szxxxxzs',
        'szxxxxzs',
        'szxxxxzs',
        'szzuuzzs',
        'zssvvssz',
    ]
    parts.append(part('barrel_inner', ((c - 2.0, y_bot, -2.0), (c + 2.0, t, 2.0)), {
        'north': bar_in_north, 'south': bar_in_plain, 'east': bar_in_plain, 'west': bar_in_plain,
        'up': none, 'down': bar_dn,
    }))

    # 3. Arm-flush 5x5x5 perforated iron-armor heat shield (10x10 sides, 0.5 px proud of barrel_inner):
    # Real cutout cooling holes (2x2 twin perforations per row) darkening to heat-charred steel near the muzzle,
    # stopping 0.5 px short of barrel_inner so the sooty inner nozzle + blue pilot flame steps out cleanly!
    shroud = [
        'ghhhhhhhhe',
        'ezllllllzp',
        'elX..X..Xp',
        'elX..X..Xp',
        'ellllllllp',
        'elX..X..Xp',
        'elX..X..Xp',
        'sssssssssz',
        'zzzzzzzzzz',
        '..........',
    ]
    # Symmetric twin 2x2 holes centered on 10 texels: cols 2..3 and 6..7 -> 'eX..XX..Xp' (10 chars, exact mirror!)
    shroud_sym = [
        'ghhhhhhhhe',
        'ezllllllzp',
        'eX..XX..Xp',
        'eX..XX..Xp',
        'ehhhhhhhhp',
        'eX..XX..Xp',
        'eX..XX..Xp',
        'sssssssssz',
        'zzzzzzzzzz',
        '..........',
    ]
    parts.append(part('barrel_outer', ((c - 2.5, y_bot, -2.5), (c + 2.5, t, 2.5)), {
        'north': shroud_sym, 'south': shroud_sym, 'east': shroud_sym, 'west': shroud_sym,
        'up': none, 'down': none,
    }))
    return parts


def _build_2d_tank_split(c, top, P):
    """5-cube classic Fallout flamer silhouette modernized in 2 layers (9 px total):
    - 6x3x6 pure iron cutout cuff over 5x3x5 slate/copper pump+valve inner base (encloses Steve's hand y 14..17);
    - front 4x6x4 perforated iron heat shroud (real 2x2 cutout holes) over 3x6x3 slate/copper burner + muzzle pilot;
    - underslung 4x4.5x1.5 red hazard fuel tank tucked cleanly behind the barrel (0.5 px daylight, zero floating stick)."""
    part = lambda name, box, faces: dict(drill.part(name, box, _paint(faces, P)), bone='tool', rot=0)
    none = one('.')
    t = top - 3.0
    y_bot = top - 9.0

    # 1. Cuff (5x3x5 inner + 6x3x6 outer -> 10x6 and 12x6 sides)
    cuff_in_fb = [
        'dkkkkkkkkd',
        'dXCCCCCCXd',
        'dffffffffd',
        'dQQQQQQQQd',
        'dXCCCCCCXd',
        'dddddddddd',
    ]
    cuff_in_e = [
        'dkkkkkkkkd',
        'dXCCrRrCCd',
        'dfffRxRffd',
        'dQQQrRrQQd',
        'dXCCCCCCXd',
        'dddddddddd',
    ]
    cuff_out_fb = [
        'ghhhhhhhhhhe',
        'ezllllllllzp',
        'elllllllllp'[:10] + 'lp',
        'hhhhhhhhhhhp',
        'sssssssssssz',
        'XXXXXXXXXXXX',
    ]
    cuff_out_sd = [
        'ghhhhhhhhhhe',
        'ezllllllllzp',
        'elX......Xlp',
        'elX......Xlp',
        'sssssssssssz',
        'XXXXXXXXXXXX',
    ]
    cuff_dn = ['dddddddddd'] + ['dkkkkkkkkd'] * 8 + ['dddddddddd']
    parts = [
        part('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in_fb, 'south': cuff_in_fb, 'east': cuff_in_e, 'west': cuff_in_fb,
            'up': none, 'down': cuff_dn,
        }),
        part('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': cuff_out_fb, 'south': cuff_out_fb, 'east': cuff_out_sd, 'west': cuff_out_sd,
            'up': _cuff_ring, 'down': none,
        }),
    ]

    # 2. Front perforated 2-layer barrel: inner 3x6x3 (z -2.5..+0.5) + outer 4x6x4 (z -3.0..+1.0)
    bar_in = [
        'dkkkkd',
        'dXCCXd',
        'dXffXd',
        'dXQQXd',
        'dXCCXd',
        'dXffXd',
        'dXQQXd',
        'dXCCXd',
        'dXffXd',
        'dXQQXd',
        'dzzzzd',
        'zssssz',
    ]
    bar_in_south = bar_in[:-2] + ['dzuuzd', 'zsvvsz']  # pilot igniter tucked at back/underside edge of nozzle
    bar_dn = [
        'zsvvsz',
        'szuuzs',
        'szxxzs',
        'szxxzs',
        'szzzzs',
        'zssssz',
    ]
    parts.append(part('barrel_inner', ((c - 1.5, y_bot, -2.5), (c + 1.5, t, 0.5)), {
        'north': bar_in, 'south': bar_in_south, 'east': bar_in, 'west': bar_in,
        'up': none, 'down': bar_dn,
    }))

    bar_out = [
        'ghhhhhhe',
        'ezllllzp',
        'elX..Xlp',
        'elX..Xlp',
        'ehhhhhhp',
        'elX..Xlp',
        'elX..Xlp',
        'ehhhhhhp',
        'elX..Xlp',
        'elX..Xlp',
        'zzzzzzzz',
        '........',
    ]
    parts.append(part('barrel_outer', ((c - 2.0, y_bot, -3.0), (c + 2.0, t, 1.0)), {
        'north': bar_out, 'south': bar_out, 'east': bar_out, 'west': bar_out,
        'up': none, 'down': none,
    }))

    # 3. Underslung red hazard fuel tank (4x4.5x1.5 at z +1.5..+3.0, 0.5 px daylight from barrel, iron end-caps)
    tk_fb = [
        'ghhhhhhe',
        'JJJJJJJH',
        'JHHHHHHF',
        'NNKKNNKK',
        'NKKNNKKN',
        'HFFFFFFE',
        'FFFFFFFE',
        'ssssssss',
        'XXXXXXXX',
    ]
    tk_sd = [r[:3] for r in tk_fb]
    parts.append(part('tank', ((c - 2.0, t - 4.5, 1.5), (c + 2.0, t, 3.0)), {
        'north': tk_fb, 'south': tk_fb, 'east': tk_sd, 'west': tk_sd,
        'up': none, 'down': one('s'),
    }))
    return parts


def _build_2d_flamer(c, top, P, barrel_style='classic', tank_style='flat', fuse_style='cutout'):
    """Distinct 2-layer flamethrower (2026-11-22, user feedback: distinct from the rail cannon; keep the red tank
    underneath with its fuse, outer perforated iron barrel over dark inner metal barrel, copper reserved ONLY for
    the valve on the base cuff). 9 px total (muzzle at top-9, pilot fuse tip at top-10)."""
    part = lambda name, box, faces: dict(drill.part(name, box, _paint(faces, P)), bone='tool', rot=0)
    none = one('.')
    t = top - 3.0
    y_bot = top - 9.0

    # 1. Compact 3 px base cuff: 5x3x5 dark-slate inner base + 6x3x6 pure iron-armor outer covering.
    # Copper is reserved STRICTLY for the recessed 4x3 copper valve wheel on the outer side (east)!
    cuff_in_plain = [
        'dkkkkkkkkd',
        'dmmmmmmmmd',
        'dkkkkkkkkd',
        'dmmmmmmmmd',
        'dkkkkkkkkd',
        'dddddddddd',
    ]
    cuff_in_valve = [
        'dkkkkkkkkd',
        'dkkCffCkkd',
        'dmmfxQfmmd',
        'dkkCQQCkkd',
        'dkkkkkkkkd',
        'dddddddddd',
    ]
    cuff_out_solid = [
        'ghhhhhhhhhhe',
        'ezllllllllzp',
        'ellllllllllp',
        'hhhhhhhhhhhp',
        'sssssssssssz',
        'XXXXXXXXXXXX',
    ]
    cuff_out_valve = [
        'ghhhhhhhhhhe',
        'ezlX....Xlzp',
        'ellX....Xllp',
        'hhhX....Xhhp',
        'sssssssssssz',
        'XXXXXXXXXXXX',
    ]
    cuff_dn = ['dddddddddd'] + ['dkkkkkkkkd'] * 8 + ['dddddddddd']
    parts = [
        part('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in_plain, 'south': cuff_in_plain, 'east': cuff_in_valve, 'west': cuff_in_plain,
            'up': none, 'down': cuff_dn,
        }),
        part('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': cuff_out_solid, 'south': cuff_out_solid, 'east': cuff_out_valve, 'west': cuff_out_solid,
            'up': _cuff_ring, 'down': none,
        }),
    ]

    # 2. Front 2-layer perforated metal barrel: 3x6x3 dark inner metal barrel (ZERO copper!) wrapped in a 4x6x4
    # iron-armor perforated outer heat shield with real alpha-0 cutout cooling holes, stopping 0.5 px short of tip.
    bar_in = [
        'dkkkkd',
        'dmmmmk',
        'dmkkkd',
        'dmmmmk',
        'dmkkkd',
        'dmmmmk',
        'dmkkkd',
        'dmmmmk',
        'dzzzzd',
        'dzzzzd',
        'szzzzs',
        'zssssz',
    ]
    bar_dn = [
        'zssssz',
        'szzzzs',
        'szxxzs',
        'szxxzs',
        'szzzzs',
        'zssssz',
    ]
    parts.append(part('barrel_inner', ((c - 1.5, y_bot, -2.5), (c + 1.5, t, 0.5)), {
        'north': bar_in, 'south': bar_in, 'east': bar_in, 'west': bar_in,
        'up': none, 'down': bar_dn,
    }))

    if barrel_style == 'stagger':
        # Staggered ventilation perforations (classic M2/Fallout flamer heat jacket)
        bar_out = [
            'ghhhhhhe',
            'ezllllzp',
            'eX.XX.Xp',
            'eX.XX.Xp',
            'ehhhhhhp',
            'elX..Xlp',
            'elX..Xlp',
            'ehhhhhhp',
            'eX.XX.Xp',
            'eX.XX.Xp',
            'zzzzzzzz',
            '........',
        ]
    else:
        # Clean 3-hole centered column of 2x2 perforations (direct 2-layer upgrade of the big suit's flamer barrel)
        bar_out = [
            'ghhhhhhe',
            'ezllllzp',
            'elX..Xlp',
            'elX..Xlp',
            'ehhhhhhp',
            'elX..Xlp',
            'elX..Xlp',
            'ehhhhhhp',
            'elX..Xlp',
            'elX..Xlp',
            'zzzzzzzz',
            '........',
        ]
    parts.append(part('barrel_outer', ((c - 2.0, y_bot, -3.0), (c + 2.0, t, 1.0)), {
        'north': bar_out, 'south': bar_out, 'east': bar_out, 'west': bar_out,
        'up': none, 'down': none,
    }))

    # 3. Underslung red fuel tank with yellow/black hazard band (behind barrel, +z, 0.5 px daylight gap)
    if tank_style == 'strapped':
        # 2-layer strapped tank: 3x4.5x1.0 inner red hazard canister + 4x4.5x1.5 outer iron clamp straps
        tk_in_fb = [
            'JJJJJH',
            'JHHHHF',
            'NNKKNN',
            'NKKNNK',
            'HFFFFE',
            'HFFFFE',
            'FFFFFE',
            'FFFFFE',
            'EEEEEE',
        ]
        tk_in_sd = [r[:2] for r in tk_in_fb]
        parts.append(part('tank_inner', ((c - 1.5, t - 4.5, 1.5), (c + 1.5, t, 2.5)), {
            'north': tk_in_fb, 'south': tk_in_fb, 'east': tk_in_sd, 'west': tk_in_sd,
            'up': none, 'down': one('E'),
        }))
        tk_out_s = [
            'ghhhhhhe',
            '........',
            '........',
            '........',
            'ehhhhhhp',
            '........',
            '........',
            'ssssssss',
            'XXXXXXXX',
        ]
        tk_out_sd = [
            'ghh',
            '...',
            '...',
            '...',
            'ehh',
            '...',
            '...',
            'sss',
            'XXX',
        ]
        parts.append(part('tank_outer', ((c - 2.0, t - 4.5, 1.5), (c + 2.0, t, 3.0)), {
            'north': none, 'south': tk_out_s, 'east': tk_out_sd, 'west': [r[::-1] for r in tk_out_sd],
            'up': none, 'down': none,
        }))
    else:
        # Clean 4x4.5x1.5 red hazard tank with crisp iron top/bottom caps
        tk_fb = [
            'ghhhhhhe',
            'JJJJJJJH',
            'JHHHHHHF',
            'NNKKNNKK',
            'NKKNNKKN',
            'HFFFFFFE',
            'FFFFFFFE',
            'ssssssss',
            'XXXXXXXX',
        ]
        tk_sd = [r[:3] for r in tk_fb]
        parts.append(part('tank', ((c - 2.0, t - 4.5, 1.5), (c + 2.0, t, 3.0)), {
            'north': tk_fb, 'south': tk_fb, 'east': tk_sd, 'west': tk_sd,
            'up': none, 'down': one('s'),
        }))

    # 4. Fuse / pilot igniter coming straight down from the red tank underneath and reaching forward to the bore!
    y_fuse = y_bot - 1.0  # 1 px below the barrel muzzle (raw top-10)
    if fuse_style == 'cutout':
        # Single sleek 0.5 px (1-texel) 2D cutout fin from under the tank forward to the bore edge (-1.0..+2.5 -> 7x5)
        # East face runs back (+z=2.5, col 0) -> front (-z=-1.0, col 6); row 0 = top (under tank), row 4 = bottom.
        fuse_e = [
            '.mk....',
            '.mk....',
            '.mk..vu',
            '.mkkkvu',
            '.dddd..',
        ]
        fuse_w = [r[::-1] for r in fuse_e]
        parts.append(part('pilot_fuse', ((c - 0.25, y_fuse, -1.0), (c + 0.25, t - 4.5, 2.5)), {
            'north': ['.', '.', 'v', 'u', '.'],
            'south': ['.', '.', '.', '.', '.'],
            'east': fuse_e, 'west': fuse_w,
            'up': none, 'down': ['.', 'd', 'k', 'k', 'k', 'u', 'v'],
        }))
    else:
        # Classic solid 1x1 matchstick rod under the tank + foot forward to the bore's back edge
        parts.append(part('pilot', ((c - 0.5, y_fuse, 1.5), (c + 0.5, t - 4.5, 2.5)),
                          {'north': one('k'), 'south': one('k'), 'east': one('k'), 'west': lambda w, h: ['mk'] * h,
                           'up': none, 'down': one('k')}))
        head = lambda w, h: ['k' * (w - 2) + 'uv'] * h
        parts.append(part('pilot_foot', ((c - 0.5, y_fuse, -0.5), (c + 0.5, y_fuse + 1.0, 1.5)), {
            'north': one('v'), 'south': none, 'east': head, 'west': lambda w, h: [r[::-1] for r in head(w, h)],
            'up': none, 'down': lambda w, h: ['kk'] * (h - 2) + ['uu', 'vv'],
        }))
    return parts


def _build_halo_flamer(c, top, P, palette='olive', cuff_metal='olive'):
    """Halo 3 M7057/DP flamethrower head reworked in our 2D-texture + 0.5 px cutout outer-layer language (4 cubes):
    - Compact 3 px base cuff (5x3x5 inner + 6x3x6 cutout outer collar) with recessed side warning badge/mechanics;
    - Heavy dark-gunmetal protruding nozzle barrel (3x7x3, tucked neatly under the overhanging top hood, with side
      muzzle vents + glowing blue pilot igniter at the bore);
    - Angled 2D cutout cheek/hood heat shield (5x6x5 outer layer) carrying the iconic Flying Tigers shark-mouth nose
      art (upright & facing forward when the arm raises to aim!) + overhanging top hood carved cleanly via alpha-0."""
    # Extend palette with Halo military olive-drab ramp + shark-mouth white/crimson/yellow (or suit-steel option)
    Ph = dict(P)
    if palette == 'steel':
        Ph.update({'G': _c('9fa4a9'), 'O': _c('757c85'), 'o': _c('58606a'), 'v': _c('3c424c'), 'b': _c('cdcfcf')})
    else:
        Ph.update({'G': _c('6d7a58'), 'O': _c('4f5a40'), 'o': _c('3a432f'), 'v': _c('252b1e'), 'b': _c('869470')})
    Ph.update({
        'W': _c('edece6'), 'w': _c('c5c4bc'),
        'M': _c('cf2a22'), 'q': _c('8f1915'),
        'Y': _c('e8c438'), 'y': _c('a88620'),
    })
    part = lambda name, box, faces: dict(drill.part(name, box, _paint(faces, Ph)), bone='tool', rot=0)
    none = one('.')
    t = top - 3.0

    # 1. Base cuff (5x3x5 inner + 6x3x6 outer collar, y top-3..top, encloses Steve's hand y 14..17)
    # Recessed dark slate + clear, unmistakable 6x4 red valve wheel with metallic center hub on outer side (east).
    cuff_in_plain = [
        'dkkkkkkkkd',
        'dmmmmmmmmd',
        'dkkkkkkkkd',
        'dmmmmmmmmd',
        'dkkkkkkkkd',
        'dddddddddd',
    ]
    cuff_in_valve = [
        'dkkkkkkkkd',
        'dffrRRrffd',
        'dQQRxxRQQd',
        'dCCrRRrCCd',
        'dkkkkkkkkd',
        'dddddddddd',
    ]
    if cuff_metal == 'iron':
        cl, cm, cs, cd, ct = 'g', 'l', 'h', 's', 'z'
    else:
        cl, cm, cs, cd, ct = 'b', 'O', 'G', 'o', 'v'
    # Crisp military armor cuff: lit bevel rim, recessed corner bolts, subtle center panel seam, rolled lower hem
    cuff_out_fb = [
        cl + cs * 10 + cm,
        cs + ct + cm * 3 + cd + cd + cm * 3 + ct + cd,
        cs + cm * 4 + ct + ct + cm * 4 + cd,
        cs + cm + cs * 3 + cd + cd + cs * 3 + cm + cd,
        cd * 11 + ct,
        'XXXXXXXXXXXX',
    ]
    cuff_out_west = [
        cl + cs * 10 + cm,
        cs + ct + cm * 8 + ct + cd,
        cs + cm * 3 + cs + cm * 2 + cd + cm * 3 + cd,
        cs * 11 + cd,
        cd * 11 + ct,
        'XXXXXXXXXXXX',
    ]
    # Tight 4x3 cutout window (cols 4..7, rows 1..3) snugly framing the 4x3 red valve wheel (rRRr / RxxR / rRRr)
    cuff_out_side = [
        cl + cs * 10 + cm,
        cs + ct + cm + 'X....X' + cm + ct + cd,
        cs + cm + cm + 'X....X' + cm + cm + cd,
        cs + cs + cs + 'X....X' + cs + cs + cd,
        cd * 11 + ct,
        'XXXXXXXXXXXX',
    ]
    def cuff_ring_fn(w, h):
        g = [['.'] * w for _ in range(h)]
        for i in range(w):
            g[0][i] = cl if i < w - 1 else cs
            g[h - 1][i] = cm if i == 0 else cd
        for j in range(1, h - 1):
            g[j][0] = cs
            g[j][w - 1] = cd
        return g

    cuff_dn = ['dddddddddd'] + ['dkkkkkkkkd'] * 8 + ['dddddddddd']
    parts = [
        part('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in_plain, 'south': cuff_in_plain, 'east': cuff_in_valve, 'west': cuff_in_plain,
            'up': none, 'down': cuff_dn,
        }),
        part('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': cuff_out_fb, 'south': cuff_out_fb, 'east': cuff_out_side, 'west': cuff_out_west,
            'up': cuff_ring_fn, 'down': none,
        }),
    ]

    # 2. Heavy dark-gunmetal protruding nozzle barrel (3x7x3, y top-10..top-3, z -1.0..+2.0 -> tucked neatly under
    # the overhanging -z top hood, projecting 1.0 px past the hood tip and 3.0 px past the angled lower cheek cut!).
    # Strictly uniform dark gunmetal slate ramp (x/d/k/m/n — no bluish steel clash or horizontal stripes), symmetric
    # centered side exhaust vent, and 4-way symmetric centered blue pilot accents (cols 2..3 on all 4 sides meeting
    # the down bore face to the exact texel!).
    bar_fb = [
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'dkkkkd',
        'nmmmmn',   # clean machined muzzle collar ring (aligned all 4 sides)
        'mkkkkm',
        'dkkkkd',
        'dkuukd',   # centered blue pilot accent (cols 2..3 -> meets down face!)
        'dkvvkd',
    ]
    bar_side = [
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'mkkkkm',
        'dkkkkd',
        'nmmmmn',   # clean machined muzzle collar ring (aligned all 4 sides)
        'mkxxkm',   # centered symmetric Halo 3 side muzzle exhaust vent
        'dkkkkd',
        'dkuukd',   # centered blue pilot accent (cols 2..3 -> meets down face!)
        'dkvvkd',
    ]
    # 4-way symmetric muzzle face (6x6): every outer edge has vv at cols/rows 2..3 meeting N/S/E/W to the exact texel!
    bar_dn = [
        'dkvvkd',
        'kduudk',
        'vuxxuv',
        'vuxxuv',
        'kduudk',
        'dkvvkd',
    ]
    parts.append(part('barrel_inner', ((c - 1.5, top - 10.0, -1.0), (c + 1.5, t, 2.0)), {
        'north': bar_fb, 'south': bar_fb, 'east': bar_side, 'west': bar_side,
        'up': none, 'down': bar_dn,
    }))

    # 3. Halo 3 angled shark-mouth heat shield (5x6x5 cutout outer layer, y top-9..top-3, z -2.5..+2.5 -> 10x12 sides):
    # Authored upright as aimed forward (12 cols: 0=rear..11=front hood tip; 10 rows: 0=top/-z..9=bottom/+z), then
    # transposed onto east/west so the shark mouth faces forward right-side-up when aiming!
    # User hand-painted shark face (2026-11-22, carried texel-for-texel from Blockbench into both outer & inner sides):
    # sweeping forward-biting shark jaw following the diagonal snout bevel, classic 2-dot eye (Wx) by the top brow.
    shark_upright = [
        'bGGGGGGGGGGb',  # uy=0: lit top bevel of overhanging hood (all 12 solid -> matches sh_north!)
        'GvOOOOOWxGoo',  # uy=1: rear rivet (1) + classic 2-dot shark EYE (Wx at 7..8) by the top brow!
        'GOYOOOOOOOov',  # uy=2: yellow lightning flash (2)
        'GYOOOxxxxxxv',  # uy=3: yellow streak (1) + sweeping black upper jaw line all the way to snout!
        'GOOOOxWWWWWv',  # uy=4: bold sweeping white upper teeth right along the snout!
        'GOOOOOxqqqv.',  # uy=5: dark crimson upper throat
        'GOOOOOOxMMv.',  # uy=6: bright red open lower jaw sweeping down the angled chin
        'GOOOOOOOxv..',  # uy=7: dark jaw corner curving cleanly with the angled bevel
        'GoOOOOOov...',  # uy=8: clean olive cheek & bevel
        'vvvvvvvv....',  # uy=9: bottom rim (cols 0..7 solid -> matches sh_south rows 0..7!)
    ]
    # Transpose upright (uy=0..9 top->bot, ux=0..11 rear->front) to east (row=ux, col=9-uy) & west (row=ux, col=uy)
    sh_east = [''.join(shark_upright[9 - col][row] for col in range(10)) for row in range(12)]
    sh_west = [''.join(shark_upright[col][row] for col in range(10)) for row in range(12)]

    # Top hood face (north, -z, 10x12 — hero view in first-person cockpit!):
    # Beveled olive armor plate with corner rivets, recessed center cooling louvers, and subtle soot at front lip.
    sh_north = [
        'bGGGGGGGGb',
        'GvOOOOOOvo',
        'GOOooooOOo',
        'GOOxxxxOOo',
        'GOOGGGGGOo',
        'GOOooooOOo',
        'GOOxxxxOOo',
        'GOOGGGGGOo',
        'GvOOOOOOvo',
        'Gooooooooo',
        'ovvvvvvvvo',
        'XXXXXXXXXX',
    ]
    # Bottom underside face (south, +z, 10x12 — hero view in third-person back!):
    # Bolted military access hatch ending cleanly at row 7 where the dark-gunmetal barrel emerges underneath.
    sh_south = [
        'bGGGGGGGGb',
        'GvOOOOOOvo',
        'GOoxxxxoOo',
        'GOoOOOOoOo',
        'GOoOGGOoOo',
        'Gvoxxxxovo',
        'oooooooooo',
        'vvvvvvvvvv',
        '..........',
        '..........',
        '..........',
        '..........',
    ]
    parts.append(part('shield_outer', ((c - 2.5, top - 9.0, -2.5), (c + 2.5, t, 2.5)), {
        'north': sh_north, 'south': sh_south, 'east': sh_east, 'west': sh_west,
        'up': none, 'down': none,
    }))
    return parts


def build(c, top, kind='halo_olive', pilot='dark', glow='lit', body_art='burner', body_h=4, holes='keep', tank_h=4, tank_w=3, sleeve=False, head_scale=False):
    """The flamethrower's parts on an arm centred at x c (right side) whose socket is at y top (bone 'tool': all still)."""
    P = PAL | PILOT[pilot] | GLOW[glow] | BRASS | BODY4 | {'X': _c('1a1d1f')}
    if kind == 'halo_olive':
        return _build_halo_flamer(c, top, P, palette='olive', cuff_metal='olive')
    if kind == 'halo_iron_cuff':
        return _build_halo_flamer(c, top, P, palette='olive', cuff_metal='iron')
    if kind == 'halo_steel':
        return _build_halo_flamer(c, top, P, palette='steel', cuff_metal='iron')
    if kind == '2d_shroud':
        return _build_2d_shroud(c, top, P, mode='shroud')
    if kind == '2d_caged_tank':
        return _build_2d_shroud(c, top, P, mode='caged_tank')
    if kind == '2d_tank_split':
        return _build_2d_tank_split(c, top, P)
    if kind == '2d_flame_A':
        return _build_2d_flamer(c, top, P, barrel_style='classic', tank_style='flat', fuse_style='cutout')
    if kind == '2d_flame_B':
        return _build_2d_flamer(c, top, P, barrel_style='stagger', tank_style='strapped', fuse_style='cutout')
    if kind == '2d_flame_C':
        return _build_2d_flamer(c, top, P, barrel_style='classic', tank_style='flat', fuse_style='solid')
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
