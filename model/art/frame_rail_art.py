"""The rail cannon for the frame (frame_model.py, TOOL=rail): the fifth power tool brought over from the big suit.

2026-11-15 (user: the old rail cannon is the reference). The big suit's, as picked in 2026-10-26 (T2 prongs, see-through
core; .scratch/rail/charge_seethrough_frames.jpg, inspired by DOOM 2016's gauss cannon, .scratch/rail/doom_gauss_ref.png):
a steel receiver with a copper band under it, two tapering steel prongs with three black vents down each outer side, and
between them a gap where the core glows blue while it charges.
On the frame it takes the tools' slot (frame_gun_art.py): the receiver 5 x 4 x 5 in the fist's place, the prongs
growing from its bottom straight down the arm. Flat and painted, no flanges. The prongs are on the `bit` bone (the
renderer shakes them while charging, as the big suit's forks).

Drafts (RAIL):
- A gap: two prongs left / right, a 1 px gap between them (see-through, as the big suit's); the prongs' inner faces
  carry the core's light, so the blue shows on the gap's walls;
- B core: the same, a 1 x 3 px core box standing in the gap, painted core glass (dark when idle);
- C split: the prongs front / back instead, so the gap's glow is seen from the arm's outer side (the third-person
  view's) rather than from the front.
RAIL_CORE: dark (the reserved glass colours, as in game: a glowmask lights them while charging) | lit (review).
RAIL_L: the prongs' length in px (default 6: the tips 10 px under the socket, 1 px under the chaingun's muzzle).

Coordinates raw, right arm (+x; the left mirrors), centred on the arm's axis (x c, z 0). Faces as frame_drill_art.py.
"""
import frame_drill_art as drill

_c = drill._c
# steel (frame_iron_art.PAL's ramp), copper (frame_heart_art), the core's reserved glass colours (the big suit's E / F /
# H: dark idle, lit for review; export-frame.py's TOOL_GLOW lights the dark ones), a vent's black
P_BASE = {k: _c(v) for k, v in {'A': '9fa4a9', 'B': '757c85', 'C': '58606a', 'D': '3c424c', 'E': '22262e', 'g': 'cdcfcf',
                                'f': 'e09868', 'Q': 'c07440', 'R': '804426', 'x': '0b0c0d'}.items()} | {'.': '.'}
# The core's light comes in three bands along the prongs (ToolLight RAIL_FLOW_0..2: the energy runs along it toward the
# tips, as on the big suit's rings), each its own pair of reserved colours a shade apart (K: the body, L: the hot row), so
# the exporter's masks (TOOL_GLOW rail_flow_0..2) can tell them. Dark idle (nearly the same blue); lit for review.
BODY_DARK, HOT_DARK = ('1d3f5e', '1d3f6f', '1d3f7f'), ('254e73', '254e74', '254e75')   # (tools/export-frame.py TOOL_GLOW)
CORE = {'dark': {f'{k}{n}': v[n] for n in range(3) for k, v in (('K', BODY_DARK), ('L', HOT_DARK))},
        'lit': {f'{k}{n}': v for n in range(3) for k, v in (('K', '2f9cff'), ('L', 'a8f0ff'))}}


def pal(core): return P_BASE | {k: _c(v) for k, v in CORE[core].items()}


def _paint(faces, P):
    for f, rows in faces.items(): assert callable(rows) or all(len(r) == len(rows[0]) for r in rows), f
    return lambda f, w, h: [[P[ch] for ch in r] for r in (faces[f](w, h) if callable(faces[f]) else faces[f])]   # (a row may be a list of keys)


# The receiver, 10 x 8 texels a side: a lit top edge, two bolts, a groove, the copper band under it (lit top row), a
# shade row. Its top (in the fist) and bottom (the prongs' ground) plain.
SIDE = ['DBBBBBBBBD', 'BgCCCCCCgD', 'DCCCCCCCCE', 'CCCCCCCCCD', 'EDDDDDDDDE', 'ffffffffQQ'[:10], 'QQQQQQQQRR', 'ERRRRRRRRE']
SIDE[5] = 'ffffffffQD'
RECEIVER = dict(north=SIDE, south=SIDE, east=SIDE, west=SIDE, up=['D' * 10] * 10, down=['E' * 10] * 10)


def vents(w, h):
    """A prong's outer side (w texels deep x h tall): a lit edge column, three black vents (2 rows tall, 2 rows apart)."""
    rows = []
    for j in range(h):
        if j in (1, 2, 4, 5, 7, 8) and j < h - 1: rows.append('A' + 'x' * (w - 2) + 'D')
        else: rows.append('B' + 'C' * (w - 2) + 'D')
    rows[0] = 'A' * (w - 1) + 'B'
    rows[-1] = 'D' * w
    return rows


def plain(w, h):   # a prong's front / back: lit left column, shaded right, a lit top row
    return ['A' * (w - 1) + 'B'] + ['B' + 'C' * (w - 2) + 'D'] * (h - 2) + ['D' * w]


def inner(seg, h_total):
    """A prong's inner face, towards the gap, the core's light on it: the prong's rows split into three bands of a third
    of its length each (seg 0 the upper half, 1 the lower), the first row of each hot (L), the rest body (K)."""
    def f(w, h):
        rows = []
        for j in range(h):
            r = j + seg * h_total // 2                     # the row down the whole prong
            n = min(2, r * 3 // h_total)
            first = r == (n * h_total + 2) // 3
            rows.append(('L' if first else 'K') + str(n))
        return [[k for _ in range(w)] for k in rows]
    return f


def tip(w, h): return ['E' * w] * h
def cap(w, h): return ['D' * w] * h


def _receiver(w=10):
    if w == 10: return RECEIVER
    s = ['D' + 'B' * (w - 2) + 'D', 'Bg' + 'C' * (w - 4) + 'gD', 'D' + 'C' * (w - 2) + 'E',
         'C' * (w - 1) + 'D', 'E' + 'D' * (w - 2) + 'E', 'f' * (w - 2) + 'QD',
         'Q' * (w - 2) + 'RR', 'E' + 'R' * (w - 2) + 'E']
    up = ['B' * w] + ['B' + 'D' * (w - 2) + 'B'] * (w - 2) + ['B' * w]
    dn = ['D' * w] + ['D' + 'E' * (w - 2) + 'D'] * (w - 2) + ['D' * w]
    return dict(north=s, south=s, east=s, west=s, up=up, down=dn)


def build(c, top, lamp='dark', kind='A', core='dark', length=6.0, sleeve=False, head_scale=False):
    """The rail cannon's parts on an arm centred at x c whose socket is at y top: the receiver (bone 'tool') and the
    prongs / core under it (bone 'bit'). `lamp` is unused (the tools' common signature)."""
    P = pal(core)
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    t = top - 4                                          # the receiver's bottom
    bw = 3.0 if sleeve else 2.5
    parts = [part('body', ((c - bw, t, -bw), (c + bw, top, bw)), _receiver(round(bw * 4)))]
    y_tip = t - length
    nrows = round(length * 2)                            # the prongs' rows (texels)
    split = (t - y_tip) * 0.5                            # the prong narrows halfway down its outer edge (the forks' taper)
    pd = 2.0 if head_scale else 1.5                      # prong half-depth (z): 4 px under 6x6 receiver
    xo_top, xo_bot = (3.0, 2.5) if head_scale else (2.5, 2.0)
    if kind in ('A', 'B'):    # prongs left / right of the arm's axis (x)
        for s, name in ((1, 'out'), (-1, 'in')):
            def box(y0, y1, x_in, x_out):
                xa, xb = sorted((c + s * x_in, c + s * x_out))
                return ((xa, y0, -pd), (xb, y1, pd))
            outer_f, inner_f = ('east', 'west') if s > 0 else ('west', 'east')
            for seg, (y0, y1, xo) in enumerate(((t - split, t, xo_top), (y_tip, t - split, xo_bot))):
                faces = {'north': plain, 'south': plain, 'up': cap, 'down': tip if seg == 1 else cap,
                         outer_f: vents if seg == 0 else plain, inner_f: inner(seg, nrows)}
                parts.append(part(f'prong_{name}_{seg}', box(y0, y1, 0.5, xo), faces, 'bit' if s > 0 else 'fork_in'))
        if kind == 'B':
            glass = lambda w, h: [['K1'] * w for _ in range(h)]
            parts.append(part('core', ((c - 0.5, y_tip, -1.5), (c + 0.5, t, 1.5)),
                              {'north': glass, 'south': glass, 'east': glass, 'west': glass, 'up': cap, 'down': glass}, 'bit'))
    else:                    # C: prongs front / back (z), 3 wide (x): the gap's light seen from the arm's side
        for s, name in ((-1, 'front'), (1, 'back')):
            def box(y0, y1, z_in, z_out):
                za, zb = sorted((s * z_in, s * z_out))
                return ((c - 1.5, y0, za), (c + 1.5, y1, zb))
            outer_f, inner_f = ('south', 'north') if s > 0 else ('north', 'south')
            for seg, (y0, y1, zo) in enumerate(((t - split, t, 2.5), (y_tip, t - split, 2.0))):
                faces = {'east': plain, 'west': plain, 'up': cap, 'down': tip if seg == 1 else cap,
                         outer_f: vents if seg == 0 else plain, inner_f: inner(seg, nrows)}
                parts.append(part(f'prong_{name}_{seg}', box(y0, y1, 0.5, zo), faces, 'bit' if s > 0 else 'fork_in'))
    return parts
