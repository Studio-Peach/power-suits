"""The chainsaw for the frame (frame_model.py, TOOL=saw): the second power tool brought over from the big suit.

2026-11-13 (user: next after the drill). Built as the drill settled the tools' slot (power-suits-frame.md, Tools): the
body takes the fist's place (the drill's 5 x 4 x 5 body and paint: frame_drill_art.fist, the slate base band with its
bolts and lamp, the copper motor), and the tool grows only from its bottom: here the guide bar, straight down, in the
arm's y-z plane (edge forward, as the big suit's: seen from the side it shows its face, from behind its back edge).
The big suit's (mining_tools_art.py, chainsaw_redesign_apply.js): a 2 x 9 x 5 steel bar with rivets and a slate band
under the base, a 1 px cyan diamond chain round its front, bottom and back (alternating cyans, no black), bar clamps.
The frame's bar is 6 px long (its end raw y 4, a px over the drill's point).

Drafts (SAW):
- A thin: one 1 x 6 x 4 box, the chain painted round its edge (the ring of its side faces, its front, back and bottom);
- B chain: a steel 1 x 6 x 4 bar and the chain its own box round it (0.5 thick, 0.5 past it front, back and bottom; the
  big suit's build: on its own bone, so it can run, a 1 px bob, as chainsaw_run did);
- C thick: as A, 2 px thick (the big suit's bar thickness).

Coordinates raw, right arm (+x; the left mirrors), centred on the arm's axis (x c, z 0). Faces as frame_drill_art.py.
"""
from frame_radial_art import dims, FACES
import frame_drill_art as drill

D, S, SL, _c = drill.D, drill.S, drill.SL, drill._c
PAL = S | SL | {'0': D['0'], '1': D['1'], '2': D['2'], '3': D['3'], '.': '.'}
BRASS = {'b': _c('d9c17a'), 'Y': _c('a89160'), 'Z': _c('6a5838')}   # lit, mid (frame_model.PAL Y), shade (Z)
# The cowl's metal (SAW_COWL, 2026-11-13, user: copper, not brass: copper is in the game): the cowl's letters b / Y / Z
# painted in the heart engine's copper (frame_heart_art.EXTRA f, frame_model.PAL Q / R: lit, mid, shade).
COPPER = {'b': _c('e09868'), 'Y': _c('c07440'), 'Z': _c('804426')}
# SAW_COWL=slate + SAW_BARREL=copper (2026-11-13, user: the drill and chainsaw more alike; draft): the drill's scheme,
# the cowl in its base band's slate (lit, mid, shade) and the barrel between the fins copper, as the drill's window.
SLATE_COWL = {'b': _c('4c5559'), 'Y': SL['m'], 'Z': SL['k']}
BARREL_CU = 'zCQQfffQCz'   # the barrel row of SAW_FINS=A in copper (ink at its sides, lit in the middle)


# The body's paint (SAW_ART; 2026-11-13, user: the body's shape shared by the tools, its paint each tool's own). The
# chainsaw's motor is a two-stroke's finned cylinder (the drill's is the copper winding). Rows of a 10 x 8 face (the
# 5 x 4 body at 2 texels per px), top -> bottom; the status lamp (2 x 1, the drill's) at the front's outer top end.
# - A fins: a steel cowl over cooling fins all round, the muffler (a slate block, its dark port) at the back's outer end;
# - B brass: a brass cowl with two bolts a face over a dark seam, the fins under it;
# - C starter: B, plus the muffler and the pull-start's grip on the outer side (a dark T on the cowl).
FINS = ['hhhhhhhhhe', 'zzzzzzzzzz', 'hhhhhhhhhe', 'zzzzzzzzzz']
MUFFLER = ['hhhhhhkkke', 'zzzzzzkxkz', 'hhhhhhkxke', 'zzzzzzkkkz']   # the back's fins with it (its outer end last)
SAW_BODY = {
    'A': dict(side=['hhhhhhhhhe', 'ellllllllp', 'ellllllllp', 'pppppppppp'] + FINS, back_low=MUFFLER),
    'B': dict(side=['bbbbbbbbbY', 'YYYYYYYYYZ', 'YYhYYYYhYZ', 'xxxxxxxxxx'] + FINS),
    'C': dict(side=['bbbbbbbbbY', 'YYYYYYYYYZ', 'YYhYYYYhYZ', 'xxxxxxxxxx'] + FINS, back_low=MUFFLER,
              outer_top=['bbbbbbbbbY', 'YYYkkkkYYZ', 'YYhYxxYhYZ']),   # the grip across, its cord into the cowl
}
# B picked (2026-11-13, user: C's muffler and grip too small to recognise). Its bottom half, the fins (SAW_FINS; user:
# make it more interesting; A picked):
# - A barrel: the cylinder seen between the fins, round (dark at its sides, lit in the middle);
# - B strap: a brass strap down the middle of each face over the fins, a bolt on it;
# - C heat: the fins heat-tinted, the upper one straw, the lower bronze running to blue at its far end.
FIN_DRAFTS = {'A': ['hhhhhhhhhe', 'zspplllpsz', 'hhhhhhhhhe', 'zspplllpsz'],
              'B': ['hhhhbYhhhe', 'zzzzYZzzzz', 'hhhhhYhhhe', 'zzzzYZzzzz'],
              'C': ['4444444445', 'zzzzzzzzzz', '5555555556', 'zzzzzzzzzz']}
HEAT = {'4': _c('c9a45c'), '5': _c('8a6038'), '6': _c('6a4a8a')}   # straw, bronze, blue (C)
# Underneath (rows front -> back, columns inner -> outer on the right arm), the face that holds the bar (user: geared
# towards the blade, not a square hole): a steel mounting plate along the bar (3 px wide, lit / shaded edges), the
# slot the bar and chain run through down its middle, the length of the chain, two bolts each side of it.
def BAR_MOUNT():
    rows = []
    for j in range(10):
        bolt = j in (1, 8)
        rows.append('kk' + 'e' + ('g' if bolt else 'l') + 'xx' + ('g' if bolt else 'l') + 's' + 'kk')   # (slate round it: the plate stands out)
    return rows


# The bottom half, again (SAW_LOW; 2026-11-13, user: with Y the copper part couldn't be recognised: it was the
# engine's cylinder between its cooling fins, at 4 rows only stripes). Drafts of things a chainsaw shows:
# - shield: the muffler's heat shield, a copper plate punched with a staggered grid of holes, all round;
# - sprocket: the clutch cover on both sides (the bar's plane: the side views): a copper sprocket, 6 x 6 texels, its
#   four teeth out of a ring round a dark hub, over the band and the motor; the shield on the front and back;
# - cover: the sprocket alone, the rest of the motor plain steel.
# 'fins' is Y (the barrel between the fins).
SHIELD = ['fffffffffQ', 'QxQxQxQxQC', 'QQxQxQxQxC', 'CCCCCCCCCC']
PLAIN = ['hhhhhhhhhe', 'ellllllllp', 'ellllllllp', 'ssssssssss']
SPROCKET = ['..fQ..', '.fQQC.', 'fQxxQC', 'QQxxCC', '.QCCC.', '..CC..']   # rows 2-7, columns 2-7 ('.': what's under)


def _stamp(rows, art, at=(2, 2)):
    rows = list(rows)
    for j, r in enumerate(art):
        y = at[1] + j
        rows[y] = ''.join(ch if ch != '.' else rows[y][at[0] + i] for i, ch in enumerate(r)).join(
            (rows[y][:at[0]], rows[y][at[0] + len(r):]))
    return rows


def saw_body(art, lamp, fins='A', cowl='copper', barrel='steel', low='fins'):
    W_, L_, r_ = drill.LAMPS[lamp]
    pal = PAL | {'copper': COPPER, 'brass': BRASS, 'slate': SLATE_COWL}[cowl] | HEAT | drill.CU | {'x': _c('1a1d1f'), 'n': _c('4c5559'), 'W': _c(W_), 'L': _c(L_), 'r': _c(r_)}
    d = dict(SAW_BODY[art])
    if art == 'B':
        rows = FIN_DRAFTS[fins]
        if fins == 'A' and barrel == 'copper': rows = [rows[0], BARREL_CU, rows[2], BARREL_CU]
        d['side'] = d['side'][:4] + rows
    side = d['side']
    front = [side[0], side[1][0] + 'WL' + side[1][3:]] + side[2:]
    back = side[:4] + d.get('back_low', side[4:])
    outer = d.get('outer_top', side[:3]) + side[3:]
    if low != 'fins':
        rest = side[:4] + (PLAIN if low == 'cover' else SHIELD)
        front, back = front[:4] + rest[4:], rest
        side = outer = rest if low == 'shield' else _stamp(side[:4] + PLAIN, SPROCKET)
    faces = {'north': front, 'south': back, 'east': outer, 'west': side,   # (the right arm's east is its outer side)
             'up': ['k' * 10] * 10, 'down': BAR_MOUNT()}
    return lambda f, w, h: [[pal[ch] for ch in r] for r in faces[f]]


def _paint(faces):
    return lambda f, w, h: [[PAL[ch] for ch in r] for r in faces[f](w, h)]


def tooth(i, phase=0): return '2' if (i + phase) % 2 == 0 else '0'   # the chain along an edge: alternating cyans


def bar_side(w, h, chain=True):
    """A bar's side face, w (front -> back or back -> front) x h: a slate row under the body, steel (lit near column,
    shaded far one), three rivets down its middle; with chain, the ring round the front, bottom and back edges teeth."""
    g = [['l'] * w for _ in range(h)]
    for j in range(h):
        g[j][0], g[j][-1] = 'e', 'p'
    g[0] = ['k'] * w
    g[-1] = ['p'] * w
    for j in (3, 6, 9):
        if j < h - 1: g[j][w // 2 - 1] = 'g'
    if chain:
        for j in range(1, h):
            g[j][0], g[j][-1] = tooth(j), tooth(j, 1)
        g[-1] = [tooth(i, h) for i in range(w)]
    return [''.join(r) for r in g]


def edge(w, h, chain=True):   # the bar's front / back edge, w (its thickness) x h
    return ['k' * w] + [(tooth(j) if chain else 'p') * w for j in range(1, h)]


def ring(w, h):
    """The chain box's side face (B): only its ring outside the bar is seen, 1 texel (0.5 px) along the front, bottom
    and back; inside see-through (the bar's face covers it). Its top row is inside the body."""
    g = [['.'] * w for _ in range(h)]
    for j in range(h):
        g[j][0], g[j][-1] = tooth(j), tooth(j, 1)
    g[-1] = [tooth(i, h) for i in range(w)]
    return [''.join(r) for r in g]


# The bar's shape (SAW_BAR; 2026-11-13, user: with Y's paint, still couldn't tell it's a chainsaw). The 6 x 4 bar read
# as a paddle, its 0.5 px chain as a dashed outline. Drafts, as seen from the side (the bar in the arm's y-z plane):
# - box: the bar so far (6 long x 4 deep, square, 0.5 px chain);
# - slim: 7 long x 2.5 deep, square end, the same chain (proportion alone);
# - tooth: 6.5 long x 2 deep, a round nose, the chain a 1 px band round it: an inner row of links and teeth standing
#   out of it every other texel (the side's outline saw-toothed);
# - long: tooth, 8 long.
BARS = {'box': None, 'slim': (2.5, 7, 0.5, False), 'tooth': (2, 6.5, 1, True), 'long': (2, 8, 1, True)}


def bar_grid(depth, length, cw, nose):
    """The bar and its chain as seen from the side, texels, column 0 the front (z-), row 0 the top (the body's bottom):
    {(i, j): letter} for the bar ('B' edge, 'b' inside) and the chain (its colours). The chain box's grid is W x H,
    the bar inside it from column cw2 (cw2 = the chain's width in texels)."""
    cw2, D, L = round(cw * 2), round(depth * 2), round(length * 2)
    W, H = D + 2 * cw2, L + cw2
    R, cx, cy = D / 2, cw2 + D / 2, L - D / 2
    def in_bar(i, j):
        if not (cw2 <= i < cw2 + D and 0 <= j < L): return False
        return not nose or j + 0.5 <= cy or (i + 0.5 - cx) ** 2 + (j + 0.5 - cy) ** 2 <= R * R + 0.3
    bar = {(i, j) for i in range(W) for j in range(H) if in_bar(i, j)}
    g = {}
    for (i, j) in bar:
        edge = any((i + di, j + dj) not in bar for di, dj in ((1, 0), (-1, 0), (0, 1)))
        g[i, j] = 'B' if edge else 'b'
    for i in range(W):
        for j in range(H):
            if (i, j) in bar: continue
            d = min(((i - a) ** 2 + (j - b) ** 2) ** 0.5 for a, b in bar)
            if cw2 == 1:
                if d <= 1.5: g[i, j] = tooth(i + j)
            elif d <= 1.5: g[i, j] = '1'                                       # the links
            elif d <= 2.9 and (i + j) % 2 == 0: g[i, j] = '3'                  # a tooth every other texel
    return g, W, H, cw2, D, L


def toothed_parts(c, t, shape, part):
    depth, length, cw, nose = shape
    g, W, H, cw2, D, L = bar_grid(depth, length, cw, nose)
    bar_px = lambda i, j: {'B': 'p', 'b': 'l'}.get(g.get((i, j)), '.')
    def side(cols, rows, fn, rev):   # a side face: east runs back -> front (rev), west front -> back
        out = []
        for j in rows:
            r = [fn(i, j) for i in cols]
            out.append(''.join(r[::-1] if rev else r))
        return out
    bcols, brows = range(cw2, cw2 + D), range(L)
    def bar_side_face(rev):
        rows = side(bcols, brows, bar_px, rev)
        rows[0] = ''.join('k' if ch != '.' else '.' for ch in rows[0])    # the slate row under the body
        mid = D // 2 - 1
        for j in (3, 6, 9, 12):                                            # rivets down its middle
            if j < L - D: rows[j] = rows[j][:mid] + 'g' + rows[j][mid + 1:]
        if nose: rows[round(L - D / 2) - 1] = rows[round(L - D / 2) - 1][:mid] + 'g' + rows[round(L - D / 2) - 1][mid + 1:]   # the nose sprocket
        return rows
    edge_rows = lambda i: (lambda w, h: ['k' * w] + [(('p' if (i, j) in g else '.') * w) for j in range(1, L)])
    parts = [part('bar', ((c - 0.5, t - length, -depth / 2), (c + 0.5, t, depth / 2)),
                  {'east': lambda w, h: bar_side_face(True), 'west': lambda w, h: bar_side_face(False),
                   'north': edge_rows(cw2), 'south': edge_rows(cw2 + D - 1), 'up': lambda w, h: ['k' * w] * h,
                   'down': lambda w, h: [('p' if (cw2 + k, L - 1) in g else '.') * w for k in range(D)]})]
    ch = lambda i, j: g.get((i, j), '.') if g.get((i, j), 'B') not in 'Bb' else '.'
    cols, rows = range(W), range(H)
    out = lambda i: (lambda w, h: [ch(i, j) * w for j in rows])          # the front (i 0) / back (W - 1) edge
    parts.append(part('chain', ((c - 0.25, t - length - cw, -depth / 2 - cw), (c + 0.25, t, depth / 2 + cw)),
                      {'east': lambda w, h: side(cols, rows, ch, True), 'west': lambda w, h: side(cols, rows, ch, False),
                       'north': out(0), 'south': out(W - 1), 'up': lambda w, h: ['.' * w] * h,
                       'down': lambda w, h: [ch(k, H - 1) * w for k in range(W)]}, bone='bit'))
    return parts


# A new body (SAW_LOOK; 2026-11-14, user: still not a chainsaw; a reference, a Husqvarna 455 Rancher; anything goes
# but the body's size, 5 x 4 x 5). Its parts mapped onto the block with the bar down: the saw's front (where the bar
# leaves it) at the body's bottom, its rear up at the arm, its top (the handles) facing back (when the arm swings up
# the bar points forward, its cutting underside down, as a saw is held), its clutch side (the bar nuts) outward:
# - the wrap-around front handle, the reference's grey tube: a 1 px band round the whole body (rows 2-3);
# - the rear handle on the back's top, a loop (a dark gap in it); the chain brake's hand guard, a grey frame, standing
#   on the back's bottom (rows 5-7, 1 px round onto the sides): the reference turned bar-down has the guard there;
# - the clutch cover (outer side): the muffler (silver, a hole) next to the guard, two black bar nuts; the starter
#   cover (inner): vent slits; underneath, the muffler's face between the bar slot and the guard;
# - the felling dogs (the spikes beside the bar) along the front's bottom; the status lamp stays (front, outer top).
# Drafts: rancher (the reference's orange and grey) | copper (the game's copper and slate) | hoop (rancher, the wrap
# handle a real hoop 0.5 px proud round a 4 x 4 x 4 core: its outline the envelope); 'old' the body so far.
# rancher picked (2026-11-14, user: "looks great, zero notes"; the default): the orange is what makes it read as a
# chainsaw, and the only body that stands out from the grey armour in third person. copper / hoop / old stay knobs.
LOOKS = {'rancher': dict(O='f28a3a', o='e0621f', u='a9461a', v='6b2a10', G='7d8389', H='5a5f65', J='3b3f44'),
         'copper': dict(O='e09868', o='c07440', u='804426', v='5a2e18', G='4c5559', H='3b4246', J='2a2e31')}
LOOKS['hoop'] = LOOKS['rancher']


def rancher_faces(w, band=True):
    """Rows of the body's faces, w texels wide (10: the 5 px block; 8: the hoop's 4 px core), 8 tall; band False
    leaves the handle band's rows in the housing's shade (under the hoop)."""
    m, n = w // 2, w - 10                                   # n: columns more than the 10 the art is drawn for
    G, H = ('G' * (w - 1) + 'H', 'H' * (w - 1) + 'J') if band else ('u' * w, 'v' * w)
    back = ['O' * (m - 2) + 'GGGG' + 'O' * (w - m - 3) + 'o',            # the rear handle's top
            'o' * (m - 2) + 'HxxJ' + 'o' * (w - m - 3) + 'u',            # its loop, the gap dark
            G, H, 'u' * (w - 1) + 'v',                                   # the wrap handle, its shadow
            'G' * (w - 1) + 'H', 'HH' + 'x' * (w - 4) + 'HJ', 'J' * (w - 1) + 'z']   # the hand guard, a frame
    nuts = 'O' + 'o' * (w - 6) + 'u'
    outer = ['G' + 'O' * (w - 1), 'J' + 'o' * (w - 2) + 'u', G, H,                   # (back -> front)
             'GH' + 'u' * (w - 3) + 'v',                                             # the guard's side
             'HJghh' + nuts[:w - 5],
             'HJhxh' + ''.join('x' if i in (1, 3) else ch for i, ch in enumerate(nuts[1:w - 4])),   # muffler, bar nuts
             'JJppp' + 'u' * (w - 6) + 'v']
    vents = 'o' + ''.join('x' if i % 2 else 'o' for i in range(w - 3)) + 'oJ'
    inner = ['O' * (w - 1) + 'G', vents, G, H, 'v' + 'u' * (w - 3) + 'HG',          # (front -> back)
             'o' * (w - 2) + 'JH', 'o' * (w - 2) + 'JH', 'u' * (w - 2) + 'JJ']
    dogs = ''.join('l' if i % 2 else 'z' for i in range(w))
    front = ['O' * (w - 1) + 'o', 'oWL' + 'o' * (w - 4) + 'u', G, H, 'u' * (w - 1) + 'v',
             'o' * (w - 1) + 'u', 'o' * (w - 1) + 'u', dogs]
    slot = lambda a, b: a * (m - 2) + 'JxxJ' + b * (w - m - 2)
    holes = lambda: 'h' * (m - 2) + 'JxxJ' + 'h' * (w - m - 2)
    down = [dogs] + [slot("o", "o")] * (w - 5) + [slot('g', 'g'), ''.join('x' if i % 2 and r == 'h' else r for i, r in enumerate(holes())),
                                                   'G' * (w - 1) + 'H', 'J' * w]
    for f in (back, outer, inner, front, down): assert all(len(r) == w for r in f) and len(f) == (w if f is down else 8), f
    up = (['O' * (w - 1) + 'o'] + ['O' + 'J' * (w - 2) + 'o'] * (w - 2) + ['o' * w]) if w > 10 else ['J' * w] * w
    return {'south': back, 'east': outer, 'west': inner, 'north': front, 'up': up, 'down': down}


def look_pal(look, lamp):
    W_, L_, r_ = drill.LAMPS[lamp]
    return PAL | {k: _c(v) for k, v in LOOKS[look].items()} | {'x': _c('1a1d1f'), 'W': _c(W_), 'L': _c(L_), '.': '.'}


def rancher_parts(c, t, look, lamp, part, sleeve=False):
    pal = look_pal(look, lamp)
    paint = lambda faces: (lambda f, w, h: [[pal[ch] for ch in r] for r in faces[f]])
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    bw = 6 if sleeve else 5
    if look != 'hoop': return [part('body', sq(bw, t, t + 4), paint(rancher_faces(bw * 2)))]
    parts = [part('body', sq(4, t, t + 4), paint(rancher_faces(8, band=False)))]
    y0, y1 = t + 4 - 2, t + 4 - 1                        # the band's rows 2-3
    def band(f, w, h):
        if f == 'up': return [[pal['G']] * w for _ in range(h)]
        if f == 'down': return [[pal['J']] * w for _ in range(h)]
        return [[pal['G' if j == 0 and i < w - 1 else 'H' if j == 0 or i < w - 1 else 'J'] for i in range(w)] for j in range(h)]
    for k, box in (('hoop_f', ((c - 2.5, y0, -2.5), (c + 2.5, y1, -2))), ('hoop_b', ((c - 2.5, y0, 2), (c + 2.5, y1, 2.5))),
                   ('hoop_o', ((c + 2, y0, -2), (c + 2.5, y1, 2))), ('hoop_i', ((c - 2.5, y0, -2), (c - 2, y1, 2)))):
        parts.append(part(k, box, band))
    return parts


def _blade_pal():
    """Clean 2-layer palette for the 2D-texture + 0.5 px cutout chainsaw blades (2026-11-22):
    - Brushed steel outer plates: w g h e l p s z (no bluish/slate mixing)
    - Neutral dark gunmetal recessed core & chain links: n m k d x
    - Husqvarna orange accents: O o u v (exact match to LOOKS['rancher'])
    - Machined copper inner core / tensioner / sprocket: F f Q C q
    - Diamond-cyan tooth accents: 3 2 1 0
    """
    return {
        '.': '.',
        # Brushed steel ramp
        'w': _c('eef2f5'), 'g': _c('cfd5db'), 'h': _c('aeb6be'), 'e': _c('919aa3'),
        'l': _c('767f89'), 'p': _c('5a626c'), 's': _c('404750'), 'z': _c('292e35'),
        # Neutral dark gunmetal slate (recessed inner bar + oiled chain links)
        'n': _c('5a5e63'), 'm': _c('44484d'), 'k': _c('2e3136'), 'd': _c('1d2024'), 'x': _c('121417'),
        # Husqvarna Rancher orange accents (matches LOOKS['rancher'])
        'O': _c('f28a3a'), 'o': _c('e0621f'), 'u': _c('a9461a'), 'v': _c('6b2a10'),
        # Recessed copper tensioner / oil-feed / sprocket internals
        'F': _c('f2b47e'), 'f': _c('e09868'), 'Q': _c('c07440'), 'C': _c('804426'), 'q': _c('522814'),
        # Diamond-cyan tooth ramp (matches Power Suits diamond D)
        '3': D['3'], '2': D['2'], '1': D['1'], '0': D['0'],
    }


def _paint_blade(faces, P):
    return lambda f, w, h: [
        [P[ch] for ch in r]
        for r in (faces[f](w, h) if callable(faces[f]) else faces[f])
    ]


def _make_blade_box(name, box, side, P, bone='tool', north=None, south=None, down=None, up=None,
                    edge_n='k', edge_s='d', edge_d='k'):
    """Builds one blade cube from its canonical side grid (col 0 = front/-z, col W-1 = back/+z;
    row 0 = root/+y, row H-1 = tip/-y). Automatically mirrors east, derives watertight edge faces
    (painting only where the side silhouette reaches that cube boundary so zero slivers float),
    and leaves buried up faces transparent."""
    (x0, y0, z0), (x1, y1, z1) = box
    wx, wy, wz = round((x1 - x0) * 2), round((y1 - y0) * 2), round((z1 - z0) * 2)
    assert len(side) == wy and all(len(r) == wz for r in side), (name, len(side), wy, len(side[0]), wz)
    west = list(side)
    east = [r[::-1] for r in side]
    def _fill(ch, n):
        return ch if len(ch) == n else ch * n
    def _derive_edge(col_idx, default_ch):
        out = []
        for j in range(wy):
            c = side[j][col_idx]
            if c == '.':
                out.append('.' * wx)
            else:
                out.append(_fill(c if default_ch is None else default_ch, wx))
        return out
    n_face = north if north is not None else _derive_edge(0, edge_n)
    s_face = south if south is not None else _derive_edge(-1, edge_s)
    if down is not None:
        d_face = down
    else:
        d_face = []
        for k in range(wz):
            c = side[-1][k]
            d_face.append('.' * wx if c == '.' else _fill(c if edge_d is None else edge_d, wx))
    u_face = up if up is not None else ['.' * wx] * wz
    for fn, rows, ew, eh in (('north', n_face, wx, wy), ('south', s_face, wx, wy),
                             ('east', east, wz, wy), ('west', west, wz, wy),
                             ('up', u_face, wx, wz), ('down', d_face, wx, wz)):
        assert len(rows) == eh and all(len(r) == ew for r in rows), (name, fn, len(rows), eh, len(rows[0]), ew)
    faces = {'north': n_face, 'south': s_face, 'east': east, 'west': west, 'up': u_face, 'down': d_face}
    return dict(drill.part(name, box, _paint_blade(faces, P)), bone=bone, rot=0)


def _blade_rancher_2d(c, t, P, include_phase_b=False):
    """Option A (`rancher_2d`): Classic Husqvarna laminated guide bar in 2D-layer style (3 blade cubes).
    - Sleek 3.0 x 7.5 px recessed gunmetal bar_inner with rounded nose + nose sprocket rivets;
    - 0.5 px proud brushed-steel bar_outer cheek plates (2.0 x 7.0 x 2.0) with Husqvarna orange collar stripe,
      cutout central fuller slot, and circular nose-sprocket cutout;
    - 0.5 px thick jagged razor-steel sawtooth chain (5.0 x 8.5) with dark oiled drive links + bright teeth."""
    # bar_inner: 1.0 x 7.5 x 3.0 (wx=2, wy=15, wz=6)
    bi_side = [
        'dkmmkd',  # 0 root
        'dknmkd',  # 1
        'dkmmkd',  # 2
        'dkmmkd',  # 3
        'dkmkkd',  # 4
        'dmnnmd',  # 5 behind fuller: recessed dark slate + machined steel spline
        'dmkkmd',  # 6
        'dmnnmd',  # 7
        'dmkkmd',  # 8
        'dmnnmd',  # 9
        'dkmmkd',  # 10
        'dmffmd',  # 11 behind sprocket cutout: recessed copper/steel bearing hub
        'dmCQmd',  # 12
        'kmmmmk',  # 13 nose shoulder
        '.kmmk.',  # 14 rounded nose tip
    ]
    # bar_outer: 2.0 x 7.0 x 2.0 (wx=4, wy=14, wz=4), 0.5 px proud on cheeks, inset 0.5 px from bar_inner edges
    bo_side = [
        'zssz',  # 0 root clamp
        'shhs',  # 1 clamp bolts
        'zssz',  # 2 clamp lower rim
        'Ooou',  # 3 Husqvarna orange accent band
        'hell',  # 4 brushed steel laminated bar
        'h..p',  # 5 cutout fuller slot (reveals recessed bar_inner)
        'e..p',  # 6
        'e..p',  # 7
        'e..p',  # 8
        'e..p',  # 9
        'ellp',  # 10 bridge above nose sprocket
        'e..p',  # 11 cutout nose sprocket window
        'l..p',  # 12
        '.lp.',  # 13 rounded outer cheek tip
    ]
    bo_n = ['zssz', 'sllp', 'zssz', 'Oooo', 'hlll', 'hlll', 'elll', 'elll', 'elll', 'elll', 'elll', 'elll', 'llll', '....']
    bo_s = ['zzzz', 'spps', 'zzzz', 'uuvv', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', '....']
    bo_d = ['....', 'pllp', 'pllp', '....']
    # chain: 0.5 x 8.5 x 5.0 (wx=1, wy=17, wz=10), 2-texel toothed rim around rounded bar_inner
    # bar_inner occupies cols 2..7, rows 0..14 (hidden inside bar_inner -> '.')
    ch_side = [
        'gk......kh',  # 0
        '.d......d.',  # 1
        'wk......kw',  # 2
        '.k......k.',  # 3
        'gk......kh',  # 4
        '.d......d.',  # 5
        'wk......kw',  # 6
        '.k......k.',  # 7
        'gk......kh',  # 8
        '.d......d.',  # 9
        'wk......kw',  # 10
        '.k......k.',  # 11
        'gk......kh',  # 12
        '.d......d.',  # 13
        'wkd....dkw',  # 14 curves round nose shoulder
        '.hkdkkdkh.',  # 15 lower drive links + diagonal corner teeth
        '..w.g.w...',  # 16 nose tip cutter teeth (Wait: symmetric! '..w.gw.w..' -> 10 chars!)
    ]
    ch_side[16] = '..g.ww.g..'
    ch_side_b = [
        '.k......k.',  # 0 phase B: teeth shifted 1 texel along the perimeter (zero gap!)
        'wk......kw',  # 1
        '.d......d.',  # 2
        'gk......kh',  # 3
        '.k......k.',  # 4
        'wk......kw',  # 5
        '.d......d.',  # 6
        'gk......kh',  # 7
        '.k......k.',  # 8
        'wk......kw',  # 9
        '.d......d.',  # 10
        'gk......kh',  # 11
        '.k......k.',  # 12
        'wk......kw',  # 13
        '.kd....dk.',  # 14
        'gkkdkkdkkh',  # 15
        '.w.g..g.w.',  # 16
    ]
    ch_box = ((c - 0.25, t - 8.5, -2.5), (c + 0.25, t, 2.5))
    out = [
        _make_blade_box('bar_inner', ((c - 0.5, t - 7.5, -1.5), (c + 0.5, t, 1.5)), bi_side, P,
                        edge_n='km', edge_s='dk', edge_d='km'),
        _make_blade_box('bar_outer', ((c - 1.0, t - 7.0, -1.0), (c + 1.0, t, 1.0)), bo_side, P,
                        north=bo_n, south=bo_s, down=bo_d),
        _make_blade_box('chain', ch_box, ch_side, P, bone='bit', edge_n=None, edge_s=None, edge_d=None),
    ]
    if include_phase_b:
        out.append(_make_blade_box('chain_b', ch_box, ch_side_b, P, bone='bit_b',
                                   edge_n=None, edge_s=None, edge_d=None))
    return out


def _blade_diamond_truss(c, t, P, include_phase_b=False):
    """Option B (`diamond_truss`): Heavy industrial diamond trench-saw (3 blade cubes).
    - Muscular 4.0 x 7.0 px bar_inner with recessed copper tensioner rod + copper nose sprocket;
    - 0.5 px proud steel/slate bar_outer (2.0 x 6.5 x 3.0) with 3 staggered cutout truss windows + orange collar;
    - 0.5 px thick 6.0 x 8.0 px jagged diamond-cyan chain (dark oiled drive links + bright cyan teeth)."""
    # bar_inner: 1.0 x 7.0 x 4.0 (wx=2, wy=14, wz=8)
    bi_side = [
        'ddkkkkdd',  # 0
        'dkmQQmkd',  # 1
        'dkmfQmkd',  # 2
        'dkmCQmkd',  # 3 recessed copper oil/tensioner spine visible through cutouts
        'dkmfFmkd',  # 4
        'dkmQQmkd',  # 5
        'dkmCQmkd',  # 6
        'dkmfFmkd',  # 7
        'dkmQQmkd',  # 8
        'dkmCQmkd',  # 9
        'dkfFFfkd',  # 10 copper nose sprocket wheel
        'dkQCCQkd',  # 11
        '.kmmmmk.',  # 12 rounded nose shoulder
        '..kmmk..',  # 13 rounded nose tip
    ]
    # bar_outer: 2.0 x 6.5 x 3.0 (wx=4, wy=13, wz=6), 0.5 px proud each cheek, inset 0.5 px inside bar_inner
    bo_side = [
        'zssssz',  # 0 heavy dark-iron root clamp
        'shllhs',  # 1 twin bolts
        'OOoouu',  # 2 Husqvarna orange collar stripe
        'helllp',  # 3 upper steel bridge
        'he..lp',  # 4 truss cutout 1 (shows copper spine)
        'he..lp',  # 5
        'hllllp',  # 6 riveted cross-rib
        'el..lp',  # 7 truss cutout 2 (shows copper spine)
        'el..lp',  # 8
        'ellllp',  # 9 lower cross-rib
        'el..pp',  # 10 nose sprocket cutout window
        'll..pp',  # 11
        '.ellp.',  # 12 rounded cheek nose
    ]
    bo_n = ['zssz', 'sllp', 'Oooo', 'hlll', 'hlll', 'hlll', 'hlll', 'elll', 'elll', 'elll', 'elll', 'llll', '....']
    bo_s = ['zzzz', 'spps', 'uuvv', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', '....']
    bo_d = ['....', 'pllp', 'pllp', 'pllp', 'pllp', '....']
    # chain: 0.5 x 8.0 x 6.0 (wx=1, wy=16, wz=12), flush with 6x6 base!
    # bar_inner occupies cols 2..9, rows 0..13 (row 12 cols 3..8, row 13 cols 4..7)
    ch_side = [
        '2k........k2',  # 0
        '.d........d.',  # 1
        '3k........k3',  # 2
        '.k........k.',  # 3
        '2k........k2',  # 4
        '.d........d.',  # 5
        '3k........k3',  # 6
        '.k........k.',  # 7
        '2k........k2',  # 8
        '.d........d.',  # 9
        '3k........k3',  # 10
        '.k........k.',  # 11
        '2kd......dk2',  # 12 hugs rounded nose shoulder
        '.3kd....dk3.',  # 13
        '..2kdkkdk2..',  # 14 lower drive links + corner diamond teeth
        '...3.22.3...',  # 15 nose tip diamond teeth
    ]
    ch_side_b = [
        '.k........k.',  # 0 phase B: diamond teeth shifted 1 texel along the perimeter
        '3k........k3',  # 1
        '.d........d.',  # 2
        '2k........k2',  # 3
        '.k........k.',  # 4
        '3k........k3',  # 5
        '.d........d.',  # 6
        '2k........k2',  # 7
        '.k........k.',  # 8
        '3k........k3',  # 9
        '.d........d.',  # 10
        '2k........k2',  # 11
        '.kd......dk.',  # 12
        '3kkd....dkk3',  # 13
        '.2kdkddkdk2.',  # 14
        '..3..22..3..',  # 15
    ]
    ch_box = ((c - 0.25, t - 8.0, -3.0), (c + 0.25, t, 3.0))
    out = [
        _make_blade_box('bar_inner', ((c - 0.5, t - 7.0, -2.0), (c + 0.5, t, 2.0)), bi_side, P,
                        edge_n='km', edge_s='dk', edge_d='km'),
        _make_blade_box('bar_outer', ((c - 1.0, t - 6.5, -1.5), (c + 1.0, t, 1.5)), bo_side, P,
                        north=bo_n, south=bo_s, down=bo_d),
        _make_blade_box('chain', ch_box, ch_side, P, bone='bit', edge_n=None, edge_s=None, edge_d=None),
    ]
    if include_phase_b:
        out.append(_make_blade_box('chain_b', ch_box, ch_side_b, P, bone='bit_b',
                                   edge_n=None, edge_s=None, edge_d=None))
    return out


def _blade_chainsword(c, t, P, include_phase_b=False):
    """Option C (`chainsword`): Armoured Chainsword / Ripper Blade (3 blade cubes).
    - Asymmetric silhouette: Husqvarna-orange & iron armoured spine shroud wraps OVER the top edge (-z/north,
      the hero first-person cockpit face!) with 3 recessed cutout cooling vents showing a copper inner rail;
    - Clean squared iron nose collar (zero hollow bevel slivers in 3/4 views) + exposed bottom cutting edge
      (+z/south) and chamfered tip with jagged razor-steel & diamond teeth."""
    # bar_inner: 1.0 x 7.5 x 3.5 (wx=2, wy=15, wz=7), z: -2.0..+1.5
    bi_side = [
        'ddkkmmd',  # 0
        'dkfQmmk',  # 1 recessed copper rail under top shroud + steel lower track
        'dkCQmlk',  # 2
        'dkfFmlk',  # 3
        'dkQQmlk',  # 4
        'dkCQmlk',  # 5
        'dkfFmlk',  # 6
        'dkQQmlk',  # 7
        'dkCQmlk',  # 8
        'dkfFmlk',  # 9
        'dkQQmlk',  # 10
        'dkCQmlk',  # 11
        'dkmmllk',  # 12
        'dkmmmmk',  # 13 solid nose shoulder
        '.kmmmm.',  # 14 clean 1-texel chamfered nose (no jagged stair-step!)
    ]
    # bar_outer: 2.0 x 6.5 x 3.0 (wx=4, wy=13, wz=6), z: -2.5..+0.5 (wraps OVER -z top spine!)
    # Ends cleanly in a solid bevel-capped iron nose collar at row 12 (0.5 px above bar_inner's tip -> zero slivers!)
    bo_side = [
        'zsszsz',  # 0 heavy iron root housing
        'sOOoou',  # 1 Husqvarna orange spine casing
        'sO..ou',  # 2 cutout vent 1 (reveals recessed copper spine)
        'sO..ou',  # 3
        'sOOoou',  # 4 solid rib
        'so..ou',  # 5 cutout vent 2
        'so..ou',  # 6
        'sOOoou',  # 7 solid rib
        'so..ou',  # 8 cutout vent 3
        'so..ou',  # 9
        'sOOoou',  # 10 solid lower guard
        'zssllp',  # 11 heavy iron nose collar
        'zzsspp',  # 12 solid lower rim (watertight down cap!)
    ]
    # Hero top spine face (north, wx=4 x wy=13): sleek orange/iron rail with recessed dark vents down the center
    bo_n = [
        'zssz', 'OOOO', 'OxxO', 'OxxO', 'OuuO', 'OxxO', 'OxxO', 'OuuO', 'OxxO', 'OxxO', 'OuuO', 'zssz', 'zzzz',
    ]
    bo_s = ['zzzz'] + ['uuvv'] * 10 + ['ppss', 'zzzz']
    bo_d = ['zzzz', 'ssss', 'ssss', 'ssss', 'ssss', 'zzzz']
    # chain: 0.5 x 8.5 x 4.0 (wx=1, wy=17, wz=8), z: -1.5..+2.5 (buried under shroud on -z, roaring out +z & nose!)
    ch_side = [
        '......kw',  # 0 exposed bottom cutting teeth (cols 6-7)
        '......d.',  # 1
        '......k3',  # 2 alternating razor steel & diamond-tipped fangs
        '......k.',  # 3
        '......kw',  # 4
        '......d.',  # 5
        '......k3',  # 6
        '......k.',  # 7
        '......kw',  # 8
        '......d.',  # 9
        '......k3',  # 10
        '......k.',  # 11
        '......kw',  # 12
        '......d.',  # 13
        '.....dk3',  # 14 wraps nose corner
        '.dkdkdk.',  # 15 drive links hugging bar_inner tip
        '..3.w.3.',  # 16 clean nose cutter teeth
    ]
    ch_side_b = [
        '......k.',  # 0 phase B: fangs shifted 1 texel along the cutting edge & nose
        '......k3',  # 1
        '......d.',  # 2
        '......kw',  # 3
        '......k.',  # 4
        '......k3',  # 5
        '......d.',  # 6
        '......kw',  # 7
        '......k.',  # 8
        '......k3',  # 9
        '......d.',  # 10
        '......kw',  # 11
        '......k.',  # 12
        '......k3',  # 13
        '.....dk.',  # 14
        '.dkdkdkw',  # 15
        '.w.3.w..',  # 16
    ]
    ch_box = ((c - 0.25, t - 8.5, -1.5), (c + 0.25, t, 2.5))
    out = [
        _make_blade_box('bar_inner', ((c - 0.5, t - 7.5, -2.0), (c + 0.5, t, 1.5)), bi_side, P,
                        edge_n='km', edge_s='dk', edge_d='km'),
        _make_blade_box('bar_outer', ((c - 1.0, t - 6.5, -2.5), (c + 1.0, t, 0.5)), bo_side, P,
                        north=bo_n, south=bo_s, down=bo_d),
        _make_blade_box('chain', ch_box, ch_side, P, bone='bit', edge_n=None, edge_s=None, edge_d=None),
    ]
    if include_phase_b:
        out.append(_make_blade_box('chain_b', ch_box, ch_side_b, P, bone='bit_b',
                                   edge_n=None, edge_s=None, edge_d=None))
    return out


def _blade_felling_taper(c, t, P, include_phase_b=False):
    """Option D (`felling_taper`): Heavy Industrial Felling Saw (4 blade cubes, zero shared planes).
    - Wide 5.5 x 2.0 px bar_clamp root collar with twin parallel serrated 2D cutout felling-dog spikes
      biting out front & back where the bar exits the orange housing;
    - Sleek 3.0 x 8.0 px bar_inner + 0.5 px proud 2.0 x 5.5 px brushed-steel bar_outer with recessed copper
      tensioner fuller windows + bold Husqvarna orange tip guard around the exposed nose sprocket;
    - 0.5 px thick 5.0 x 9.0 px razor-steel toothed chain running cleanly out from inside the root clamp."""
    # 1. bar_clamp: 2.0 x 2.0 x 5.5 (wx=4, wy=4, wz=11), z: -2.75..+2.75 (0.25 px wider than chain -> zero coplanar!)
    bc_side = [
        'gzzzzzzzzzg',  # 0 upper felling-dog spike + dark iron clamp
        '.shOOoOOhs.',  # 1 Husqvarna orange bar-clamp stripe + twin steel bolts
        'hsszzzzzssh',  # 2 lower felling-dog spike
        '..zsssssz..',  # 3 bevelled taper step down onto the sleek bar
    ]
    # Twin parallel cheek spikes ('g..g') instead of a solid wide block: reads as real twin chainsaw felling dogs!
    bc_n = ['g..g', '....', 'h..h', '....']
    bc_s = ['g..g', '....', 'h..h', '....']
    bc_d = ['....', '....', 'zzzz', 'ssss', 'ssss', 'ssss', 'ssss', 'ssss', 'zzzz', '....', '....']
    # 2. bar_inner: 1.0 x 8.0 x 3.0 (wx=2, wy=16, wz=6), z: -1.5..+1.5
    bi_side = [
        'dkmmkd',  # 0 inside clamp
        'dkmmkd',  # 1
        'dkmmkd',  # 2
        'dkmmkd',  # 3
        'dkmmkd',  # 4
        'dmfQmd',  # 5 recessed copper tensioner bar visible through outer fuller
        'dmCQmd',  # 6
        'dkmmkd',  # 7 behind mid cross-rib
        'dmfFmd',  # 8 lower copper tensioner window
        'dmQQmd',  # 9
        'dkmmkd',  # 10
        'dkmmkd',  # 11
        'dmffmd',  # 12 copper nose sprocket bearing
        'dmCQmd',  # 13
        'kmmmmk',  # 14 nose shoulder
        '.kmmk.',  # 15 rounded nose tip
    ]
    # 3. bar_outer: 2.0 x 5.5 x 2.0 (wx=4, wy=11, wz=4), y: t-7.5..t-2.0 (starts cleanly below bar_clamp!)
    bo_side = [
        'hell',  # 0 brushed steel cheek
        'h..p',  # 1 upper fuller cutout (reveals recessed copper tensioner)
        'e..p',  # 2
        'ellp',  # 3 solid steel center cross-rib (breaks up the long slot cleanly)
        'e..p',  # 4 lower fuller cutout
        'e..p',  # 5
        'ellp',  # 6 steel bridge
        'Ooou',  # 7 Husqvarna orange tip-guard band
        'O..u',  # 8 nose sprocket cutout framed in orange & steel
        'l..p',  # 9
        '.lp.',  # 10 rounded tip
    ]
    bo_n = ['hlll', 'hlll', 'elll', 'elll', 'elll', 'elll', 'elll', 'Oooo', 'Oooo', 'llll', '....']
    bo_s = ['ppss', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', 'ppss', 'uuvv', 'uuvv', 'ppss', '....']
    bo_d = ['....', 'pllp', 'pllp', '....']
    # 4. chain: 0.5 x 9.0 x 5.0 (wx=1, wy=18, wz=10), y: t-9.0..t (runs up inside bar_clamp so running anim never gaps!)
    ch_side = [
        '.k......k.',  # 0 inside clamp
        '.d......d.',  # 1
        '.k......k.',  # 2
        '.d......d.',  # 3
        'wk......kw',  # 4 emerges cleanly below felling dogs
        '.k......k.',  # 5
        'gk......kh',  # 6
        '.d......d.',  # 7
        'wk......kw',  # 8
        '.k......k.',  # 9
        'gk......kh',  # 10
        '.d......d.',  # 11
        'wk......kw',  # 12
        '.k......k.',  # 13
        'gk......kh',  # 14
        'wkd....dkw',  # 15 curves round nose shoulder
        '.hkdkkdkh.',  # 16 drive links + corner teeth
        '..g.ww.g..',  # 17 nose tip razor teeth
    ]
    ch_side_b = [
        '.d......d.',  # 0 phase B: teeth shifted 1 texel along the perimeter
        '.k......k.',  # 1
        '.d......d.',  # 2
        '.k......k.',  # 3
        '.d......d.',  # 4
        'gk......kh',  # 5
        '.k......k.',  # 6
        'wk......kw',  # 7
        '.d......d.',  # 8
        'gk......kh',  # 9
        '.k......k.',  # 10
        'wk......kw',  # 11
        '.d......d.',  # 12
        'gk......kh',  # 13
        'wk......kw',  # 14
        '.kd....dk.',  # 15
        'gkkdkkdkkh',  # 16
        '.w.g..g.w.',  # 17
    ]
    ch_box = ((c - 0.25, t - 9.0, -2.5), (c + 0.25, t, 2.5))
    out = [
        _make_blade_box('bar_clamp', ((c - 1.0, t - 2.0, -2.75), (c + 1.0, t, 2.75)), bc_side, P,
                        north=bc_n, south=bc_s, down=bc_d),
        _make_blade_box('bar_inner', ((c - 0.5, t - 8.0, -1.5), (c + 0.5, t, 1.5)), bi_side, P,
                        edge_n='km', edge_s='dk', edge_d='km'),
        _make_blade_box('bar_outer', ((c - 1.0, t - 7.5, -1.0), (c + 1.0, t - 2.0, 1.0)), bo_side, P,
                        north=bo_n, south=bo_s, down=bo_d),
        _make_blade_box('chain', ch_box, ch_side, P, bone='bit', edge_n=None, edge_s=None, edge_d=None),
    ]
    if include_phase_b:
        out.append(_make_blade_box('chain_b', ch_box, ch_side_b, P, bone='bit_b',
                                   edge_n=None, edge_s=None, edge_d=None))
    return out


BLADES_2D = {
    'rancher_2d': _blade_rancher_2d,
    'diamond_truss': _blade_diamond_truss,
    'chainsword': _blade_chainsword,
    'felling_taper': _blade_felling_taper,
}


def build(c, top, lamp='red', kind='B', art='B', fins='A', cowl='slate', barrel='copper', bar_shape='box', low='fins', look='rancher', sleeve=False, head_scale=False, blade='felling_taper', include_phase_b=False):
    """The chainsaw's parts on an arm centred at x c (right side) whose socket is at y top: the body (the drill's)
    and the bar under it (SAW, picked: B), its paint SAW_ART; bone 'tool' still, 'bit' the chain (it runs)."""
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    t = top - 4                                         # the body's bottom: the bar hangs from it
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces) if isinstance(faces, dict) else faces), bone=bone)
    parts = ([part('body', sq(5, t, top), saw_body(art, lamp, fins, cowl, barrel, low))] if look == 'old' else
             rancher_parts(c, t, look, lamp, part, sleeve=sleeve))
    if blade in BLADES_2D:
        parts += BLADES_2D[blade](c, t, _blade_pal(), include_phase_b=include_phase_b)
        for p in parts: p.setdefault('rot', 0)
        return parts
    if BARS[bar_shape]:
        parts += toothed_parts(c, t, BARS[bar_shape], part)
        for p in parts: p.setdefault('rot', 0)
        return parts
    T = 2 if kind == 'C' else 1                         # the bar's thickness (x)
    bd = 2.5 if head_scale else 2.0                     # bar half-depth (z): 5 px under 6x6 body (chain 6 px flush)
    bar = ((c - T / 2, t - 6, -bd), (c + T / 2, t, bd))
    lid = lambda w, h: ['k' * w] * h
    if kind in ('A', 'C'):
        parts.append(part('bar', bar, {'north': edge, 'south': edge, 'east': bar_side, 'west': bar_side, 'up': lid,
                                       'down': lambda w, h: [tooth(j) * w for j in range(h)]}))
    else:
        plain = lambda w, h: bar_side(w, h, chain=False)
        parts.append(part('bar', bar, {'north': lambda w, h: edge(w, h, False), 'south': lambda w, h: edge(w, h, False),
                                       'east': plain, 'west': plain, 'up': lid, 'down': lambda w, h: ['p' * w] * h}))
        # the chain: 0.5 thick in the bar's middle, 0.5 past it front, back and bottom, up to the body (not into it:
        # 0.5 past the bar is the body's front and back plane; its top, see-through, isn't drawn)
        teeth = lambda w, h: [tooth(j) * w for j in range(h)]
        cd = bd + 0.5
        ch_box = ((c - 0.25, t - 6.5, -cd), (c + 0.25, t, cd))
        parts.append(part('chain', ch_box,
                          {'north': teeth, 'south': teeth, 'east': ring, 'west': ring, 'up': lambda w, h: ['.' * w] * h,
                           'down': teeth}, bone='bit'))
        if include_phase_b:
            teeth_b = lambda w, h: [tooth(j, 1) * w for j in range(h)]
            def ring_b(w, h):
                g = [['.'] * w for _ in range(h)]
                for j in range(h):
                    g[j][0], g[j][-1] = tooth(j, 1), tooth(j, 0)
                g[-1] = [tooth(i, h + 1) for i in range(w)]
                return [''.join(r) for r in g]
            parts.append(part('chain_b', ch_box,
                              {'north': teeth_b, 'south': teeth_b, 'east': ring_b, 'west': ring_b,
                               'up': lambda w, h: ['.' * w] * h, 'down': teeth_b}, bone='bit_b'))
    for p in parts: p.setdefault('rot', 0)
    return parts
