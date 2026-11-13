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


def build(c, top, lamp='red', kind='B', art='B', fins='A', cowl='slate', barrel='copper', bar_shape='box', low='fins'):
    """The chainsaw's parts on an arm centred at x c (right side) whose socket is at y top: the body (the drill's)
    and the bar under it (SAW, picked: B), its paint SAW_ART; bone 'tool' still, 'bit' the chain (it runs)."""
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    t = top - 4                                         # the body's bottom: the bar hangs from it
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces) if isinstance(faces, dict) else faces), bone=bone)
    parts = [part('body', sq(5, t, top), saw_body(art, lamp, fins, cowl, barrel, low))]
    if BARS[bar_shape]:
        parts += toothed_parts(c, t, BARS[bar_shape], part)
        for p in parts: p.setdefault('rot', 0)
        return parts
    T = 2 if kind == 'C' else 1                         # the bar's thickness (x)
    bar = ((c - T / 2, t - 6, -2), (c + T / 2, t, 2))
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
        parts.append(part('chain', ((c - 0.25, t - 6.5, -2.5), (c + 0.25, t, 2.5)),
                          {'north': teeth, 'south': teeth, 'east': ring, 'west': ring, 'up': lambda w, h: ['.' * w] * h,
                           'down': teeth}, bone='bit'))
    for p in parts: p.setdefault('rot', 0)
    return parts
