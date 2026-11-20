"""Copper armour for the frame (model/art/frame_model.py, ARMOR=copper).

Early-game tier below iron: pieces only (torso, arm, leg — no copper helmet), lighter silhouette (no pauldrons,
no knee pads), and its own warm copper palette (fixed RGBA tuples, never swapped by dye paint).

Round 1 (2026-11-20): Style A (clean copper plates, no pauldrons) picked over B (riveted) and C (harness).
Round 2 (2026-11-20): User asked to remove the knee pads and give the chest/abdomen a different silhouette from iron.
Round 3 (2026-11-20): User picked cropped's slim pinched abdomen + small vertical abdomen plate, with the normal full-height
chest (not cropped).
Knob COPPER_TORSO:
  slim    — (picked direction) full-height chest (y 20..26) over the slim tucked abdomen (9 x 5 x 5, flush with
            the legs in depth and pinched in at the sides) with the small 5 x 3 copper abdomen plate
  cropped — high cropped chest (y 21..26, 5 px tall) over a tall, slim tucked waist (9 x 6 x 5)
  belted  — chest (y 20..26) -> pinched dark-slate midriff (y 17..20, 9 x 3 x 5) -> copper utility belt (10 x 2 x 6)
  long    — extended copper cuirass (y 18..26, 8 px tall) over a short tucked dark-slate waist (y 15..18, 9 x 3 x 5)
"""
import random

RAMP = 'zsplehgw'
SLATE = 'xdkmn'

HEX = {
    # 8-step copper ramp (deep shadow .. specular glint), matching the frame's copper hoses (f/Q/R)
    'z': '3b1a0e',  # deep seam / bolt
    's': '5e2c18',  # dark shadow / underside tuck
    'p': '804026',  # shaded copper
    'l': 'a85836',  # main plate copper
    'e': 'c46f44',  # mid-lit copper
    'h': 'de8c5d',  # lit copper
    'g': 'f2b083',  # rolled rim / top edge highlight
    'w': 'fde0c8',  # specular glint
    # Dark slate under-armour (matches frame_iron_art)
    'x': '1a1d1f', 'd': '25292c', 'k': '2f3437', 'm': '3b4246', 'n': '4c5559',
}


def _rgba(c):
    if c == '.':
        return '.'
    h = HEX[c]
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def resolve(faces):
    """Convert letter grids into RGBA tuples (leaving '.' see-through) so copper never collides with PAL or steel paint."""
    return {f: [[_rgba(c) for c in r] for r in rows] for f, rows in faces.items()}


def step(c, k):
    r = RAMP if c in RAMP else SLATE
    return r[max(0, min(len(r) - 1, r.index(c) + k))]


def plate(w, h, top='rim', bottom='roll', base='l', edges=True, marks=True, seed=''):
    g = [[base] * w for _ in range(h)]
    if marks and w > 2 and h > 2:
        rng = random.Random(seed)
        for _ in range(max(1, w * h // 12)):
            x, y = rng.randrange(1, w - 1), rng.randrange(1, h - 1)
            g[y][x] = step(base, rng.choice((1, -1)))
    if edges and w > 2:
        for row in g:
            row[0], row[-1] = step(base, 1), step(base, -1)
    if top == 'rim':
        g[0] = [step(base, 3)] + [step(base, 2)] * (w - 1)
    elif top == 'tuck':
        g[0] = [step(base, -2)] * w
    if bottom == 'roll' and h >= 3:
        g[-2] = [step(base, 2)] * (w - 1) + [step(base, 1)]
        g[-1] = [step(base, -2)] * w
    elif bottom == 'shade':
        g[-1] = [step(base, -1)] * w
    return [''.join(r) for r in g]


def ribs(w, h, phase=0):
    return [('m' if (j + phase) % 2 == 0 else 'k') * w for j in range(h)]


def overlay(face, x0, y0, patch):
    face = [list(r) for r in face]
    for j, r in enumerate(patch):
        for i, c in enumerate(r):
            if c != ' ':
                face[y0 + j][x0 + i] = c
    return [''.join(r) for r in face]


def torso_boxes(chest_x, tz, variant='slim'):
    """Return list of (name, box) for copper torso pieces (raw coordinates)."""
    if variant == 'slim':
        return [
            ('chest', ((-chest_x, 20, -tz), (chest_x, 26, tz))),
            ('waist', ((-4.5, 15, -2.5), (4.5, 20, 2.5))),
        ]
    if variant == 'cropped':
        return [
            ('chest', ((-chest_x, 21, -tz), (chest_x, 26, tz))),
            ('waist', ((-4.5, 15, -2.5), (4.5, 21, 2.5))),
        ]
    if variant == 'belted':
        return [
            ('chest', ((-chest_x, 20, -tz), (chest_x, 26, tz))),
            ('waist', ((-4.5, 17, -2.5), (4.5, 20, 2.5))),
            ('belt',  ((-5.0, 15, -tz), (5.0, 17, tz))),
        ]
    if variant == 'long':
        return [
            ('chest', ((-chest_x, 18, -tz), (chest_x, 26, tz))),
            ('waist', ((-4.5, 15, -2.5), (4.5, 18, 2.5))),
        ]
    raise ValueError(variant)


def chest(W, D, hole, H=6, variant='cropped'):
    """Copper chest plate: W x H x D (or at 2 texels/px vertically when H is half-px, passed as int rows)."""
    front = plate(W, H, top='rim', bottom='roll', seed='acf_' + variant)
    back = plate(W, H, top='rim', bottom='shade', seed='acb_' + variant)
    side = plate(D, H, top='rim', bottom='roll', seed='acs_' + variant)
    if variant == 'long':
        # Subtle lower-hem seam 2 rows from the bottom so the extended cuirass has structure without looking busy
        seam_f = ['s' * W, 'h' + 'e' * (W - 2) + 'p']
        seam_s = ['s' * D, 'h' + 'e' * (D - 2) + 'p']
        front = overlay(front, 0, H - 3, [seam_f[0]])
        back = overlay(back, 0, H - 3, [seam_f[0]])
        side = overlay(side, 0, H - 3, [seam_s[0]])
    U, V = 2 * W, 2 * D
    up = [('g' if j == 0 else 'h' if j < 2 else 'e') * U for j in range(V)]
    up = [r if j < 2 or j >= V - 2 else r[:hole] + '.' * (U - 2 * hole) + r[-hole:] for j, r in enumerate(up)]
    return resolve({'north': front, 'south': back, 'east': side, 'west': side,
                    'up': up, 'down': ['p' * W] * D})


def waist(W, D, H, variant='slim'):
    """Slim tucked abdomen (9 px wide x 5 px deep) — cleaner and leaner than iron's stepped slab."""
    if variant in ('slim', 'cropped'):
        # Slim tucked waist: small 5 x 4 copper abdomen plate starting at row 0 so it connects directly to the chest's
        # bottom edge, framed by dark ribbed slate on the sides and along the bottom edge meeting the legs.
        front = ['d' * W] + ribs(W, H - 1)
        c = W // 2
        ab = plate(5, 4, top='tuck', bottom='roll', seed='cw_ab', marks=False)
        front = overlay(front, c - 2, 0 if variant == 'slim' else 1, ab)
        back = ['d' * W] + ribs(W, H - 1, 1)
        side = ['d' * D] + ribs(D, H - 1, 1)
        return resolve({'north': front, 'south': back, 'east': side, 'west': side,
                        'up': ['d' * W] * D, 'down': ['k' * W] * D})
    if variant == 'belted':
        # Pinched dark ribbed slate midriff between broad chest and flared copper belt
        front = ['d' * W] + ribs(W, H - 1)
        back = ['d' * W] + ribs(W, H - 1, 1)
        side = ['d' * D] + ribs(D, H - 1, 1)
        return resolve({'north': front, 'south': back, 'east': side, 'west': side,
                        'up': ['d' * W] * D, 'down': ['k' * W] * D})
    # long: short tucked dark-slate waist with a slim copper buckle tab in front
    front = ['d' * W] + ribs(W, H - 1)
    c = W // 2
    front = overlay(front, c - 2, 1, ['ghhhe', 'slllp'][:H - 1])
    back = ['d' * W] + ribs(W, H - 1, 1)
    side = ['d' * D] + ribs(D, H - 1, 1)
    return resolve({'north': front, 'south': back, 'east': side, 'west': side,
                    'up': ['d' * W] * D, 'down': ['k' * W] * D})


def belt(W, D, H=2):
    """Copper utility belt for variant 'belted' (10 x 2 x 6): copper band stepping out over the hips with a slate buckle."""
    front = ['g' + 'h' * (W - 2) + 'e', 'p' + 'l' * (W - 2) + 's']
    c = W // 2
    front = overlay(front, c - 1, 0, ['nm', 'kd'])  # clean dark slate centre clasp
    back = ['h' + 'e' * (W - 2) + 'l', 'p' + 'l' * (W - 2) + 's']
    side = ['h' + 'e' * (D - 2) + 'l', 'p' + 'l' * (D - 2) + 's']
    return resolve({
        'north': front, 'south': back, 'east': side, 'west': side,
        'up': ['h' * W] * D, 'down': ['p' * W] * D,
    })


def arm(rows=12):
    """Style A clean copper arm without pauldrons: copper shoulder cap, dark slate elbow, copper vambrace."""
    out = {}
    for f in ('north', 'east', 'south', 'west'):
        if f == 'west':
            col = ribs(5, 8) + plate(5, 4, top='tuck', bottom='roll', seed='ca_v' + f)
        else:
            cap = plate(5, 5, top='rim', bottom='roll', seed='ca_u' + f)
            elbow = ['d' * 5, 'm' * 5, 'k' * 5]
            vam = plate(5, 4, top='rim', bottom='roll', seed='ca_v' + f)
            col = cap + elbow + vam
        out[f] = col
    out['up'] = ['ghhhg', 'heeeh', 'ellle', 'ellle', 'sppps']
    return resolve(out)


def leg(rows=13):
    """Style A clean copper leg WITHOUT knee pads: copper thigh, clean dark-slate knee joint, copper shin."""
    inner = ['d' * 5] + ribs(5, rows - 1)
    out = {}
    for f in ('north', 'east', 'south', 'west'):
        if f == 'west':
            out[f] = inner
            continue
        thigh = plate(5, 6, top='tuck', bottom='roll', seed='la_t' + f)
        knee = ['k' * 5, 'm' * 5]
        shin = plate(5, 5, top='rim', bottom='shade', seed='la_s' + f)
        out[f] = thigh + knee + shin
    out['up'] = ['k' * 5] * 5
    return resolve(out)


def hip(W, D):
    return resolve({f: ['k' * (W if f in ('north', 'south', 'up', 'down') else D)] * (D if f in ('up', 'down') else 1)
                    for f in ('north', 'east', 'south', 'west', 'up', 'down')})
