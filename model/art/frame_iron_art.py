"""The iron armour's paint for the frame (frame_model.py, ARMOR=iron): every piece's faces as letter grids.

Letters: the polished steel ramp of the big suit (model/art/steel_art.py, deep shadow .. glint), its plates' only
colours so paint can swap them later, and the dark slate of the under-armour (the old suit's undersuit greys):
    steel  z 22262e  s 3c424c  p 58606a  l 757c85  e 8a9097  h 9fa4a9  g cdcfcf  w fbf8f0
    slate  x 1a1d1f  d 25292c  k 2f3437  m 3b4246  n 4c5559
The recipe is the big suit's breastplate (Art direction, sm_chest_art.py): flat armour colour, structure in
horizontal plate bands (a lit rim on a plate's top, a shadow row where it tucks under the part above, a rolled rim
over its bottom edge's shadow), soft edge columns (light from the viewer's upper left: the left column lit, the right
one shaded), sparse 1 px wear marks (the grain: no noise, no tube shading). Undersides in the armour's colour (dark
ones read as a hollow bracket). Mirrored parts are mirrored by the model (painted() reverses their u), not here.

Faces as frame_model.py's: north / south as seen from the front / back (a limb's north outer column first, its south
inner first), east back -> front, west front -> back (as seen from that side); up rows front -> back, columns
x- -> x+. Limbs list the cage's rows top -> bottom (the fist's / sole's art goes below them).

Plated (2026-11-05, user): one plate per face over dark slate where the frame bends: the waist, knees, upper arms (the
strip between the pauldron and the chest reads as a dark joint) and the legs' inner sides, like the old suit. Picked
over B, lamellar (all steel but the knees, the chest, pauldrons, thighs and waist in overlapping lames like the
T-45's): on pieces 5-6 px tall every lame adds a lit row and a shadow row, and it read as stripes.
"""
import random

RAMP = 'zsplehgw'
SLATE = 'xdkmn'
PAL = {'z': '22262e', 's': '3c424c', 'p': '58606a', 'l': '757c85', 'e': '8a9097', 'h': '9fa4a9', 'g': 'cdcfcf',
       'w': 'fbf8f0', 'x': '1a1d1f', 'd': '25292c', 'k': '2f3437', 'm': '3b4246', 'n': '4c5559'}


def step(c, k):
    """c moved k steps up (lighter) its ramp, clamped."""
    r = RAMP if c in RAMP else SLATE
    return r[max(0, min(len(r) - 1, r.index(c) + k))]


def plate(w, h, top='rim', bottom='roll', base='l', edges=True, marks=True, seed=''):
    """One steel plate face, w x h texels. top: 'rim' a lit edge, 'tuck' the shadow under the part above, None.
    bottom: 'roll' a rolled rim (a lit row over its shadow), 'shade' one darker row, None."""
    g = [[base] * w for _ in range(h)]
    if marks and w > 2 and h > 2:   # the grain: a few 1 px marks, a step off the base (never on the edges)
        rng = random.Random(seed)
        for _ in range(max(1, w * h // 12)):
            x, y = rng.randrange(1, w - 1), rng.randrange(1, h - 1)
            g[y][x] = step(base, rng.choice((1, -1)))
    if edges and w > 2:
        for row in g:
            row[0], row[-1] = step(base, 1), step(base, -1)
    if top == 'rim': g[0] = [step(base, 3)] + [step(base, 2)] * (w - 1)
    elif top == 'tuck': g[0] = [step(base, -2)] * w
    if bottom == 'roll' and h >= 3:
        g[-2] = [step(base, 2)] * (w - 1) + [step(base, 1)]
        g[-1] = [step(base, -2)] * w
    elif bottom == 'shade': g[-1] = [step(base, -1)] * w
    return [''.join(r) for r in g]


def ribs(w, h, phase=0):
    """Ribbed slate under-armour: alternating ridge / groove rows."""
    return [('m' if (j + phase) % 2 == 0 else 'k') * w for j in range(h)]


def overlay(face, x0, y0, patch):
    """Paint patch's rows into face at column x0, row y0."""
    face = [list(r) for r in face]
    for j, r in enumerate(patch):
        for i, c in enumerate(r):
            if c != ' ': face[y0 + j][x0 + i] = c
    return [''.join(r) for r in face]


def chest(W, D, hole):
    """The chest box (W x 6 x D). hole: the up face at 2 texels per px, its side columns outside his torso (the top
    is open over it, as the frame's)."""
    front = plate(W, 6, top='rim', bottom='roll', seed='cf')   # the breastplate, its rolled rim over the waist
    back = plate(W, 6, top='rim', bottom='shade', seed='cb')
    side = plate(D, 6, top='rim', bottom='roll', seed='cs')
    U, V = 2 * W, 2 * D
    up = [('g' if j == 0 else 'h' if j < 2 else 'e') * U for j in range(V)]
    up = [r if j < 2 or j >= V - 2 else r[:hole] + '.' * (U - 2 * hole) + r[-hole:] for j, r in enumerate(up)]
    return {'north': front, 'south': back, 'east': side, 'west': side,
            'up': up, 'down': ['p' * W] * D}


def waist(W, D, H=3):
    """Ribbed slate with an abdomen plate in front that tapers on with the steps above it (2026-11-05, user): its top
    row 8 texels wide, the row under it 6 (first 6 over 4: the user had it 1 px wider all round), the bottom row
    ribbed slate (the plate stopped a row short of the waist's bottom, user). Back and sides ribbed, the top row in
    the band's shadow."""
    front = ['d' * W] + ribs(W, H - 1)
    c = W // 2
    front = overlay(front, c - 4, 0, ['g' + 'h' * 6 + 'e'])
    front = overlay(front, c - 3, 1, plate(6, H - 2, top=None, bottom=None, marks=False))
    back = ['d' * W] + ribs(W, H - 1, 1)
    side = ['d' * D] + ribs(D, H - 1, 1)
    return {'north': front, 'south': back, 'east': side, 'west': side, 'up': ['d' * W] * D, 'down': ['p' * W] * D}


def waist_step(W, H, D):
    """A band between the chest and the waist, the breastplate's steel stepping in: its top a lit ledge, its face a
    lit row over its body (one row: just the lit edge), a shaded bottom row."""
    face = lambda w: (['h' * w] if H == 1 else plate(w, H, top='rim', bottom='shade', marks=False))
    return {'north': face(W), 'south': face(W), 'east': face(D), 'west': face(D), 'up': ['h' * W] * D,
            'down': ['p' * W] * D}


def pauldron(W, H, D):
    """The pauldron: lit from the top, darker down to a rolled bottom rim (the old pads' ladder by height)."""
    ladder = ['g', 'h', 'e', 'e', 'l', 'l', 'l', 'h', 's'][:H]
    def face(w, k=0):
        out = []
        for j, c in enumerate(ladder):
            c = step(c, k)
            out.append(step(c, 1 if j < H - 2 else 0) + c * (w - 2) + step(c, -1))
        return out
    up = ['g' * W] + ['h' * (W - 1) + 'g'] * (D - 1)
    return {'north': face(W), 'south': face(W), 'east': face(D), 'west': face(D, -1), 'up': up, 'down': ['p' * W] * D}


def arm(rows=12):
    """The arm piece's cage rows (5 wide), top (the shoulder, under the pauldron) -> bottom (over the fist). The
    pauldron covers the top 8; below it the forearm's vambrace (4 rows)."""
    upper = lambda w: ribs(w, rows - 4)   # slate: its inner strip shows beside the chest, a dark joint
    vam = lambda w, s: plate(w, 4, top='tuck', bottom='roll', seed=s)
    return {f: upper(5) + vam(5, 'a' + f) for f in ('north', 'east', 'south', 'west')} | {'up': ['k' * 5] * 5}


def leg(rows=13):
    """The leg piece's cage rows (5 wide), the waist (y 17) -> the sole's top (y 4): thigh 6, knee 2, shin 5. North
    outer column first, so the knee cap sits in the middle three; the inner side (west) faces the other leg."""
    thigh = lambda w, s: plate(w, 6, top='tuck', bottom='roll', seed=s)
    knee = lambda w: ['k' * w, 'm' * w]
    shin = lambda w, s: plate(w, 5, top='rim', bottom='shade', seed=s)
    inner = ['d' * 5] + ribs(5, rows - 1)
    out = {}
    for f in ('north', 'east', 'south', 'west'):
        if f == 'west' and inner: out[f] = inner; continue
        col = thigh(5, 'lt' + f) + knee(5) + shin(5, 'ls' + f)
        if f == 'north':   # the knee cap
            col = overlay(col, 1, 6, ['ghh', 'ell'])
        out[f] = col
    out['up'] = ['k' * 5] * 5
    return out


def hip(W, D):
    return {f: ['k' * (W if f in ('north', 'south', 'up', 'down') else D)] * (D if f in ('up', 'down') else 1)
            for f in ('north', 'east', 'south', 'west', 'up', 'down')}


# ---------------------------------------------------------------- flat (ARMOR_FORM=flat)
# (2026-11-12, user: "not digging the mix of 3D and 2D armour"; the copper and the core went 2D, so the armour too.)
# The pieces are the frame's boxes, nothing standing proud of them: the step band between chest and waist is painted
# on the waist's top rows, the pauldron is a decal (like the frame's shoulder plate) at 2 texels per px.

def waist_flat(W, D, H=5):
    """The waist box with the step band painted on its top two rows (lit rim, shaded row), the waist under it."""
    band = waist_step(W, 2, D)
    low = waist(W, D, H - 2)
    return {f: band[f] + low[f] for f in ('north', 'east', 'south', 'west')} | {'up': low['up'], 'down': low['down']}


def pauldron_decal(W, H, D, inner_depth=None):
    """The pauldron drawn on (2 texels per px): W texels inner -> outer, H rows, D front -> back. Only the outward faces
    (top, outer side, front, back) are painted, see-through below the plate's edge; the front and back run from the full
    depth at the outer corner up to inner_depth at the chest side (the plate's bottom edge curves up), a rolled rim
    (lit row, shadow, a dark slate edge) along it. Two bolts near the top of each face."""
    inner_depth = inner_depth or H - 4
    def col(depth, k=0):   # one column of the plate, top -> bottom
        c = ['g'] + ['h'] * 4 + ['e'] * (depth - 9) + ['l'] * 1 + ['h', 's', 'x']
        c = [step(x, k) if x not in 'x' else x for x in c][:depth]
        return c + ['.'] * (H - depth)
    def face(w, depths, k=0, bolts=()):
        cols = [col(d, k) for d in depths]
        for i in bolts: cols[i][2] = 'z'
        return [''.join(cols[i][j] for i in range(w)) for j in range(H)]
    curve = [round(inner_depth + (H - inner_depth) * (i / (W - 1)) ** 2) for i in range(W)]   # inner -> outer
    north = face(W, curve[::-1], bolts=(1, W - 2))           # outer column first
    south = face(W, curve, k=-1, bolts=(1, W - 2))           # inner first, in the shade
    east = face(D, [H] * D, bolts=(1, D - 2))
    up = [['h'] * W for _ in range(D)]
    for i in range(W): up[0][i], up[-1][i] = 'g', 's'
    for j in range(1, D - 1): up[j][0], up[j][-1] = 'e', 'g'
    for i, j in ((1, 1), (W - 2, 1), (1, D - 2), (W - 2, D - 2)): up[j][i] = 'z'
    return {'north': north, 'south': south, 'east': east, 'west': ['.' * D] * H,
            'up': [''.join(r) for r in up], 'down': ['.' * W] * D}
