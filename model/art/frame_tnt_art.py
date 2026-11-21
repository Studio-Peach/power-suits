"""The TNT launcher for the frame (frame_model.py, TOOL=tnt): the sixth power tool brought over from the big suit.

The big suit's (picked 2026-10-25, round 5 of .scratch/tnt/): a revolver drum after Team Fortress 2's grenade launcher:
a dark gunmetal-slate octagonal drum with vertical flutes on the sides and four red TNT chamber ends painted on its
muzzle (down) face at 90 deg steps round the drum axis (so a quarter turn per shot lands on the same picture;
ToolRotors: bone tnt_launcher_drum, about y), a bright light-steel fat barrel tucked against the front (-z) chamber,
a dark slate muzzle ring flush with the drum's front, and a two-prong fork sight on the barrel's front (top when
aiming).

2026-11-20 rework (knob TNT; picked 'wide' with ch_out=2.5 so no red chamber peeks past the barrel's top):
- wide   : (default) 6 x 3 x 6 octagonal drum (0.5 px proud of the 5 x 5 arm, matching the old launcher's
           wider-than-socket silhouette; clears Steve by 0.5 px and Alex flush), 4 red TNT chamber ends recessed inside
           a 1-texel dark slate rim (ch_in=1.0, ch_out=2.5, ch_span=1.0: top chamber stays completely hidden behind the
           barrel), 3.5 x 4 x 3.5 light-steel barrel, 4 x 1 x 4 dark-slate muzzle ring flush with the drum front,
           two-prong 0.5 px fork sight (1 px gap); 9 px overall;
- flush  : 5 x 3 x 5 octagonal drum (flush with the 5 x 5 arm), 3 x 4 x 3 steel barrel, 3.5 x 1 x 3.5 muzzle ring,
           fork sight; 9 px overall;
- chunky : 6 x 3 x 6 octagonal drum with the big suit's full 4 x 4 fat steel barrel, 4.5 x 1 x 4.5 muzzle ring and
           1 px fork prongs; 9 px overall;
- legacy : the 2026-11-15 frame version.

Coordinates raw, right arm (+x; the left mirrors), centred on the arm's axis (x c, z 0). Faces as frame_drill_art.py
(north / south as seen from front / back, east back -> front, west front -> back, up rows front -> back, down rows
back -> front).
"""
import frame_drill_art as drill

_c = drill._c
# Legacy palette (chaingun warm black + TNT)
P_LEGACY = {k: _c(v) for k, v in dict(
    A='6a7077', B='454a50', C='2e3237', D='202327', E='131517', g='9fa4a9',
    i='6e1e14', j='a3301e', l='d2442a', m='e6e2d6', n='3a2f2a', s='a69c8c', x='5a5248',
).items()} | {'.': '.'}

# Rework palette: big suit's gunmetal slate (S/I/U/M/D/V), frame iron steel for the barrel (h/e/l/p/s/z),
# big suit's TNT reds (R lit, r mid, k shade), deep bore black (x).
P = {k: _c(v) for k, v in dict(
    S='747d82', I='5d666b', U='434b4f', M='333a3e', D='25292c', V='16191c',
    h='9fa4a9', e='8a9097', l='757c85', p='58606a', s='3c424c', z='22262e',
    R='d2442a', r='a3301e', k='6e1e14', x='0b0c0d',
).items()} | {'.': '.'}


def _paint(faces, pal=P):
    return lambda f, w, h: [[pal[ch] for ch in row] for row in (faces[f](w, h) if callable(faces[f]) else faces[f])]


def solid(ch):
    return lambda w, h: [ch * w] * h


# ---------------- legacy (2026-11-15) ----------------
def _legacy_build(c, top):
    plate = lambda w, h: ['A' * (w - 1) + 'B'] + ['B' + 'C' * (w - 2) + 'D'] * (h - 2) + ['D' * w]
    slab_side = lambda w, h: ['B' * w] + ['C' * w] * (h - 2) + ['D' * w]

    def round_end(w, h):
        g = [['D'] * w for _ in range(h)]
        for j in range(1, h - 1):
            for i in range(1, w - 1):
                g[j][i] = 'j'
        for i in range(1, w - 1):
            g[1][i] = 'l'
            g[h // 2][i] = 'm'
            g[h // 2 - 1][i] = 'm'
        g[h // 2 - 1][w // 2 - 1] = 'x'
        return [''.join(r) for r in g]

    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P_LEGACY)), bone=bone)
    housing = {f: plate for f in ('north', 'south', 'east', 'west')} | {'up': solid('D'), 'down': solid('E')}
    parts = [part('housing', ((c - 2.5, top - 1, -2.5), (c + 2.5, top, 2.5)), housing)]
    y0, y1 = top - 4, top - 1
    ends = lambda: {'up': solid('D'), 'down': solid('E')}
    parts.append(part('drum_x', ((c - 2.5, y0, -1.5), (c + 2.5, y1, 1.5)),
                      {'north': slab_side, 'south': slab_side, 'east': round_end, 'west': round_end} | ends(), 'bit'))
    parts.append(part('drum_z', ((c - 1.5, y0, -2.5), (c + 1.5, y1, 2.5)),
                      {'east': slab_side, 'west': slab_side, 'north': round_end, 'south': round_end} | ends(), 'bit'))
    parts.append(part('barrel', ((c - 1.5, y0 - 4, -2.5), (c + 1.5, y0, 0.5)),
                      {f: plate for f in ('north', 'south', 'east', 'west')} | {'up': solid('D'), 'down': solid('E')}))
    ring = lambda w, h: ['A' * (w - 1) + 'B'] + ['B' * (w - 1) + 'C'] * (h - 1)
    bore = lambda w, h: [''.join('B' if i in (0, w - 1) or j in (0, h - 1) else 'E' for i in range(w)) for j in range(h)]
    parts.append(part('muzzle', ((c - 2, y0 - 5, -3), (c + 2, y0 - 4, 1)),
                      {f: ring for f in ('north', 'south', 'east', 'west')} | {'up': solid('C'), 'down': bore}))
    return parts


# ---------------- rework painters (after the big suit's round 5 launcher) ----------------
def slate_side(w, h):
    """Gunmetal slate side face: lit top edge, lit left column, shaded right column and bottom row."""
    if h == 1:
        return ['I' + 'U' * max(0, w - 2) + ('D' if w > 1 else '')]
    if h == 2:
        return ['S' * max(1, w - 1) + ('I' if w > 1 else ''),
                'I' + 'U' * max(0, w - 2) + ('D' if w > 1 else '')]
    rows = ['S' * (w - 1) + 'I']
    for _ in range(h - 2):
        rows.append(('I' + 'U' * (w - 2) + 'D') if w > 2 else ('I' + 'D')[:w])
    rows.append('D' * w)
    return rows


def drum_cardinal(w, h):
    """A cardinal side of the octagonal drum: solid dark gunmetal slate with a 2-texel dark vertical flute down its
    middle (like the big suit's fluted slate drum, without extra striping)."""
    rows = [list(r) for r in slate_side(w, h)]
    m0, m1 = w // 2 - 1, w // 2
    for j in range(h):
        rows[j][m0] = 'V'
        rows[j][m1] = 'V'
    return [''.join(r) for r in rows]


def drum_step(w, h):
    """The narrow stepped corner face of the octagonal drum (2 texels wide, or outer margins of drum_x)."""
    rows = [list(r) for r in slate_side(w, h)]
    for j in range(1, h - 1):
        for i in range(w):
            rows[j][i] = 'U' if i == 0 else ('D' if i == w - 1 else 'M')
    return [''.join(r) for r in rows]


def barrel_side(w, h):
    """Light-steel barrel face (the big suit's bright steel contrast against the dark slate drum & muzzle):
    shadow row under the drum, bright steel body (lit left, shaded right), shadow row above the muzzle ring."""
    rows = ['p' * (w - 1) + 's']
    for j in range(1, h - 1):
        if w <= 2:
            rows.append('e' + 'p')
        else:
            body = 'e' if j <= 2 else 'l'
            rows.append('h' + 'e' + body * (w - 4) + 'l' + 'p' if w >= 5 else 'h' + body * (w - 2) + 'p')
    rows.append('s' * (w - 1) + 'z')
    return rows


def muzzle_ring(w, h):
    """Dark slate muzzle ring side (2 texels tall): bright top bevel catching light under the steel barrel, dark base."""
    return ['S' * (w - 1) + 'I', 'U' + 'M' * (w - 2) + 'D']


def muzzle_bore(w, h):
    """Muzzle down face: 1-texel slate lip, 1-texel dark inner bevel, deep black square bore."""
    g = [['x'] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            d = min(i, j, w - 1 - i, h - 1 - j)
            if d == 0:
                g[j][i] = 'I' if (i == 0 or j == 0) and not (i == w - 1 or j == h - 1) else 'U' if i < w - 1 and j < h - 1 else 'D'
            elif d == 1:
                g[j][i] = 'V'
    return [''.join(r) for r in g]


def drum_down_painter(c, x0, z1, R, ch_in, ch_out, ch_span):
    """Paints a drum cube's down face in drum-axis coordinates (dx, dz) so all three flush octagon boxes share one
    seamless 90-degree-symmetric muzzle-end pattern: four red TNT chamber ends recessed inside a dark slate outer rim
    (ch_out <= R - 0.5 keeps the top/front chamber completely behind the barrel so no red peeks above it).
    (down face: col i runs -x -> +x, row j runs back +z -> front -z.)"""
    def f(w, h):
        rows = []
        for j in range(h):
            dz = z1 - (j + 0.5) / 2
            row = []
            for i in range(w):
                dx = (x0 - c) + (i + 0.5) / 2
                # Check the 4 chambers symmetrically at 90 deg around (0, 0):
                # radial coordinate u (ch_in..ch_out outward), tangential coordinate v (-ch_span..+ch_span)
                ch = None
                if -ch_out <= dx <= -ch_in and abs(dz) <= ch_span:
                    ch = (-dx, dz)       # left chamber
                elif ch_in <= dx <= ch_out and abs(dz) <= ch_span:
                    ch = (dx, -dz)       # right chamber
                elif ch_in <= dz <= ch_out and abs(dx) <= ch_span:
                    ch = (dz, dx)        # back chamber
                elif -ch_out <= dz <= -ch_in and abs(dx) <= ch_span:
                    ch = (-dz, -dx)      # front chamber (100% hidden behind the barrel)
                if ch is not None:
                    u, v = ch
                    # Vivid TNT round end: bright lit red on one side (R), vivid red body (r), shade (k) on trailing edge
                    if v > ch_span - 0.55:
                        row.append('k')
                    elif v < -ch_span + 0.55 or (u > ch_out - 0.55 and v < 0):
                        row.append('R')
                    else:
                        row.append('r')
                else:
                    # Dark slate drum face with subtle inner hub ring
                    if abs(dx) < 0.75 and abs(dz) < 0.75:
                        row.append('V')
                    elif abs(dx) > R - 0.55 or abs(dz) > R - 0.55:
                        row.append('D')
                    else:
                        row.append('M')
            rows.append(''.join(row))
        return rows
    return f


def drum_up_painter(c, x0, z0, R):
    """Drum top face (mostly covered by the 5 x 5 socket collar; exposed 0.5 px rim on 6 x 6 drums catches light)."""
    def f(w, h):
        rows = []
        for j in range(h):
            dz = z0 + (j + 0.5) / 2
            row = []
            for i in range(w):
                dx = (x0 - c) + (i + 0.5) / 2
                if abs(dx) > R - 0.55 or abs(dz) > R - 0.55:
                    row.append('I' if dx < 0 or dz < 0 else 'U')
                else:
                    row.append('D')
            rows.append(''.join(row))
        return rows
    return f


SPECS = {
    # (drum_W, drum_N, ch_in, ch_out, ch_span, barrel_W, muzzle_W, sight_W, sight_gap)
    # wide: drum_N=5.0 gives crisp 0.5 px (1-texel) octagonal corner bevels AND 0.5 px clearance around Steve's 4x4 arm
    # inside the lifted sleeve (zero z-fighting).
    'wide':   (6.0, 5.0, 1.0, 2.5, 1.0, 3.5, 4.0, 0.5, 1.0),
    'flush':  (5.0, 3.0, 1.0, 2.0, 1.0, 3.0, 3.5, 0.5, 1.0),
    'chunky': (6.0, 4.0, 1.0, 2.5, 1.0, 4.0, 4.5, 1.0, 1.0),
}


def build(c, top, lamp='dark', kind='wide', length=0.0, collar_w=5.0, sleeve=False):
    """The TNT launcher's parts on an arm centred at x c whose socket is at y top: the collar, barrel, muzzle ring and
    fork sight (bone 'tool'), and the octagonal drum (bone 'bit': turns 90 deg per shot)."""
    if kind == 'legacy':
        return _legacy_build(c, top)
    assert kind in SPECS, kind
    W, N, ch_in, ch_out, ch_span, bW, mW, sW, sGap = SPECS[kind]
    R, r = W / 2, N / 2

    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces)), bone=bone)
    parts = []

    # 1. Socket collar: when sleeved (6x6), an octagonal 6x1x6 collar matches the drum's exact outline (zero square
    #    eaves overhanging the drum's beveled corners); otherwise a flush 5x1x5 collar.
    if sleeve:
        cy0, cy1 = top - 1, top
        parts.append(part('housing_x', ((c - R, cy0, -r), (c + R, cy1, r)), {
            'east': slate_side, 'west': slate_side, 'north': slate_side, 'south': slate_side,
            'up': drum_up_painter(c, c - R, -r, R), 'down': solid('V'),
        }))
        parts.append(part('housing_f', ((c - r, cy0, -R), (c + r, cy1, -r)), {
            'north': slate_side, 'south': solid('.'), 'east': slate_side, 'west': slate_side,
            'up': drum_up_painter(c, c - r, -R, R), 'down': solid('V'),
        }))
        parts.append(part('housing_b', ((c - r, cy0, r), (c + r, cy1, R)), {
            'south': slate_side, 'north': solid('.'), 'east': slate_side, 'west': slate_side,
            'up': drum_up_painter(c, c - r, r, R), 'down': solid('V'),
        }))
    else:
        cw = collar_w / 2
        col_up = (lambda w, h: ['S' * w] + ['I' + 'D' * (w - 2) + 'U'] * (h - 2) + ['U' * w]) if collar_w > 5 else solid('D')
        collar = {f: slate_side for f in ('north', 'south', 'east', 'west')} | {'up': col_up, 'down': solid('V')}
        parts.append(part('housing', ((c - cw, top - 1, -cw), (c + cw, top, cw)), collar))

    # 2. Octagonal revolver drum (3 px tall, 3 flush non-overlapping cubes: drum_x + drum_f + drum_b, zero z-fighting!)
    y0, y1 = top - 4, top - 1
    dx_box = ((c - R, y0, -r), (c + R, y1, r))
    df_box = ((c - r, y0, -R), (c + r, y1, -r))
    db_box = ((c - r, y0, r), (c + r, y1, R))
    parts.append(part('drum_x', dx_box, {
        'east': drum_cardinal, 'west': drum_cardinal,
        'north': drum_step, 'south': drum_step,
        'up': drum_up_painter(c, c - R, -r, R),
        'down': drum_down_painter(c, c - R, r, R, ch_in, ch_out, ch_span),
    }, 'bit'))
    parts.append(part('drum_f', df_box, {
        'north': drum_cardinal, 'south': solid('.'),
        'east': drum_step, 'west': drum_step,
        'up': drum_up_painter(c, c - r, -R, R),
        'down': drum_down_painter(c, c - r, -r, R, ch_in, ch_out, ch_span),
    }, 'bit'))
    parts.append(part('drum_b', db_box, {
        'south': drum_cardinal, 'north': solid('.'),
        'east': drum_step, 'west': drum_step,
        'up': drum_up_painter(c, c - r, r, R),
        'down': drum_down_painter(c, c - r, R, R, ch_in, ch_out, ch_span),
    }, 'bit'))

    # 3. Light-steel fat barrel (4 px exposed between drum and muzzle ring), front recessed 0.25 px behind drum front
    # so the muzzle ring (+0.25 px lip) sits flush with the drum's front face (-R), exactly like round 5.
    bz0 = -R + 0.25
    bz1 = bz0 + bW
    parts.append(part('barrel', ((c - bW / 2, y0 - 4, bz0), (c + bW / 2, y0, bz1)), {
        'north': barrel_side, 'south': barrel_side, 'east': barrel_side, 'west': barrel_side,
        'up': solid('.'), 'down': solid('.'),
    }))

    # 4. Dark slate muzzle ring (1 px tall, 0.25 px wider per side than barrel, front flush at -R; 9 px total from socket)
    mz0 = -R
    mz1 = mz0 + mW
    parts.append(part('muzzle', ((c - mW / 2, y0 - 5, mz0), (c + mW / 2, y0 - 4, mz1)), {
        'north': muzzle_ring, 'south': muzzle_ring, 'east': muzzle_ring, 'west': muzzle_ring,
        'up': solid('I'), 'down': muzzle_bore,
    }))

    # 5. Two-prong fork sight on the barrel's front (-z, facing up when raised to fire), right behind the muzzle ring.
    # Depth 1.0 px (tucked 0.25 px into barrel front, projecting 0.5 px proud of drum/muzzle front — exact old projection).
    sz0, sz1 = -R - 0.5, -R + 0.5
    sy0, sy1 = y0 - 4, y0 - 2
    sight_faces = {
        'north': slate_side, 'south': solid('.'), 'east': slate_side, 'west': slate_side,
        'up': solid('S'), 'down': solid('.'),
    }
    x_in = sGap / 2
    parts.append(part('sight_l', ((c - x_in - sW, sy0, sz0), (c - x_in, sy1, sz1)), sight_faces))
    parts.append(part('sight_r', ((c + x_in, sy0, sz0), (c + x_in + sW, sy1, sz1)), sight_faces))

    return parts
