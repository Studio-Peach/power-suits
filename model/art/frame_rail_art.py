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
# steel (frame_iron_art.PAL's ramp), slate (dark gunmetal chassis), copper (frame_heart_art), the core's reserved glass
# colours (dark idle, lit for review; export-frame.py's TOOL_GLOW lights the dark ones), vent black
P_BASE = {k: _c(v) for k, v in {'A': '9fa4a9', 'B': '757c85', 'C': '58606a', 'D': '3c424c', 'E': '22262e', 'g': 'cdcfcf',
                                'n': '4c5559', 'm': '3b4246', 'k': '2f3437', 'd': '1f2226',
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


# ---------------- 2026-11-21 rework drafts for the 6x6 sleeved footprint ----------------
# All three keep the see-through glowing gap and 3-band flowing charge light (K0..2 / L0..2 -> RAIL_FLOW_0..2) plus
# the moving fork bones ('bit' = rail_fork_out, 'fork_in' = rail_fork_in) so the forks spread and shake while charging.
def _solid(ch):
    return lambda w, h: [[ch] * w for _ in range(h)]


def _bevel_up(w, h, rim='B', mid='m', core='k'):
    """Top face of a 6x6 sleeved receiver: lit bevel catching light round the 5x5 arm."""
    return [[rim if i in (0, w - 1) or j in (0, h - 1) else mid if i in (1, w - 2) or j in (1, h - 2) else core
             for i in range(w)] for j in range(h)]


def _bevel_down(w, h, rim='D', mid='k', core='d'):
    return [[rim if i in (0, w - 1) or j in (0, h - 1) else mid if i in (1, w - 2) or j in (1, h - 2) else core
             for i in range(w)] for j in range(h)]


def _plate_box(lit='A', hi='B', body='C', sh='D', dk='E'):
    """Clean shaded armor plate face of any size."""
    def f(w, h):
        if h == 1:
            return [[lit] * max(1, w - 1) + ([hi] if w > 1 else [])]
        if h == 2:
            return [[lit] * max(1, w - 1) + ([hi] if w > 1 else []),
                    [body] * max(1, w - 1) + ([sh] if w > 1 else [])]
        rows = [[lit] * (w - 1) + [hi]]
        for _ in range(h - 2):
            rows.append([hi] + [body] * max(0, w - 2) + ([sh] if w > 1 else []))
        rows.append([sh] * max(1, w - 1) + ([dk] if w > 1 else []))
        return rows
    return f


def _coil_face(w, h):
    """Wound copper induction coil: alternating bright/mid/dark horizontal turns with dark outer framing."""
    rows = []
    for j in range(h):
        if h >= 3 and j == h - 1:
            rows.append(['R'] * w)
        elif j % 2 == 0:
            rows.append(['f'] * max(1, w - 1) + (['Q'] if w > 1 else []))
        else:
            rows.append(['Q'] * max(1, w - 1) + (['R'] if w > 1 else []))
    return rows


def _breech_bore(w, h):
    """Glowing blue circular/octagonal accelerator breech facing straight down the rail gap."""
    g = [['d'] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            d = min(i, j, w - 1 - i, h - 1 - j)
            if d == 0:
                g[j][i] = 'D' if (i in (0, w - 1) and j in (0, h - 1)) else 'm'
            elif d == 1 and w >= 5:
                g[j][i] = 'K0'
            else:
                g[j][i] = 'L0' if (w <= 4 or d >= 2) else 'K0'
    return g


def _inner_band(y0, y1, rail_top, rail_bot):
    """Inner rail face glowing in 3 bands (K0/L0 -> K1/L1 -> K2/L2) mapped by world y along the rail length."""
    span = rail_top - rail_bot
    def f(w, h):
        rows = []
        for j in range(h):
            # row 0 is at y1 (top of this box), row h-1 is at y0 (bottom)
            frac = ((rail_top - y1) + (j + 0.5) / 2.0) / span
            n = min(2, max(0, int(frac * 3)))
            # thin hot leading crest at top of each band, bright core down the middle columns
            band_pos = (frac * 3) - n
            hot = band_pos < 0.28
            row = []
            for i in range(w):
                edge = (w >= 4 and i in (0, w - 1))
                if edge:
                    row.append('d')
                else:
                    row.append(('L' if (hot or (w >= 5 and 2 <= i < w - 2 and band_pos < 0.55)) else 'K') + str(n))
            rows.append(row)
        return rows
    return f


def _build_gauss(c, top, P, length=6.0):
    """Draft A (DOOM 2016 Gauss Cannon): two-tone dark-slate chassis + bright-steel armor shrouds, glowing blue
    capacitor core windows on front/back, recessed copper induction pockets on the sides, a central glowing breech
    nozzle at the root of the gap, and 3-step sculpted twin rails with vents visible in cockpit AND third-person."""
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    t = top - 4.0
    parts = []

    # 1. 6x4x6 armored receiver (12 x 8 texels per side)
    # Front (north, cockpit top!) & back (south, third-person!): dark slate frame, bolted steel cheeks flanking a
    # recessed glowing blue capacitor window (K0/L0), dark groove, copper power bus at the lower corners.
    fb = [
        list('nBBBBBBBBBBn'),
        list('BgCCdkkdCCgD'),
        list('BCCCd') + ['L0', 'L0'] + list('dCCCD'),
        list('BCCCd') + ['K0', 'K0'] + list('dCCCD'),
        list('dDDDdkkdDDDd'),
        list('dffQdkkdQffd'),
        list('dQQRmmmmRQQd'),
        list('dEEdkkkkdEEd'),
    ]
    # Outer/inner sides (east/west): dark slate top collar, bright steel panel with recessed horizontal copper
    # induction cylinder pocket in the middle, dark vent slit below.
    sd = [
        list('nBBBBBBBBBBn'),
        list('BgCCCCCCCCgD'),
        list('BCddffffddCD'),
        list('BCdQffffQdCD'),
        list('BCdRRRRRRdCD'),
        list('dDDDDDDDDDDd'),
        list('dkxxkxxkxxkd'),
        list('dEEEEEEEEEE' + 'd'),
    ]
    parts.append(part('body', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
        'north': fb, 'south': fb, 'east': sd, 'west': sd,
        'up': _bevel_up, 'down': _bevel_down,
    }))

    # 2. Central accelerator breech nozzle tucked between the fork roots (1.5 x 1.5 x 2.5): glowing blue bore facing
    #    straight down the open channel (like the Gauss Cannon's circular plasma emitter).
    parts.append(part('breech', ((c - 0.75, t - 1.5, -1.25), (c + 0.75, t, 1.25)), {
        'north': _plate_box('m', 'k', 'k', 'd', 'd'),
        'south': _plate_box('m', 'k', 'k', 'd', 'd'),
        'east': _solid('d'), 'west': _solid('d'),
        'up': _solid('.'), 'down': _breech_bore,
    }))

    # 3. Twin 3-step sculpted forks (1.5 px glowing gap x = c +- 0.75, total length 6.0 px -> y_tip = t - 6.0)
    y_tip = t - length
    y_a = t - 1.5         # step 0: heavy breech clamp + copper induction collar (1.5 px tall)
    y_b = t - 4.5         # step 1: vented armored magnetic rail body (3.0 px tall)
    # step 2: y_tip..y_b  # tapered muzzle accelerator tip (1.5 px tall)

    def rail_fb_vented(w, h):
        """Front/back face of the mid rail (visible in cockpit & third-person!): bright steel outer rail, dark inner
        lip beside the beam, two crisp dark cooling slots."""
        rows = [['A'] * (w - 1) + ['B']]
        for j in range(1, h - 1):
            if j in (1, 2, 4) and w >= 4:
                rows.append(['B'] + ['x'] * (w - 2) + ['D'])
            else:
                rows.append(['B'] + ['C'] * (w - 2) + ['D'])
        rows.append(['D'] * (w - 1) + ['E'])
        return rows

    def rail_outer_mid(w, h):
        """Outer side of mid rail: steel frame with glowing blue accelerator window (K1/L1) between dark vents."""
        rows = [['A'] * (w - 1) + ['B']]
        for j in range(1, h - 1):
            if j == 1:
                rows.append(['B', 'd'] + ['x'] * (w - 4) + ['d', 'D'])
            elif j == 2:
                rows.append(['B', 'd'] + ['L1'] * (w - 4) + ['d', 'D'])
            elif j == 3:
                rows.append(['B', 'd'] + ['K1'] * (w - 4) + ['d', 'D'])
            elif j == 4:
                rows.append(['B', 'd'] + ['x'] * (w - 4) + ['d', 'D'])
            else:
                rows.append(['B'] + ['C'] * (w - 2) + ['D'])
        rows.append(['D'] * (w - 1) + ['E'])
        return rows

    def rail_tip_outer(w, h):
        """Dark gunmetal accelerator muzzle tip with bright chamfer and glowing tip notch (K2)."""
        rows = [['n'] * (w - 1) + ['m']]
        for j in range(1, h - 1):
            rows.append(['m', 'k'] + ['K2'] * max(1, w - 4) + ['k', 'd'] if w >= 5 else ['m'] + ['k'] * (w - 2) + ['d'])
        rows.append(['d'] * w)
        return rows

    for s, name in ((1, 'out'), (-1, 'in')):
        bone = 'bit' if s > 0 else 'fork_in'
        outer_f, inner_f = ('east', 'west') if s > 0 else ('west', 'east')

        def bx(y0, y1, x_in, x_out, hd):
            xa, xb = sorted((c + s * x_in, c + s * x_out))
            return ((xa, y0, -hd), (xb, y1, hd))

        # Step 0: heavy copper-wound breech clamp (x +-0.75..2.75 = 2.0 wide, z +-2.5 = 5.0 deep)
        parts.append(part(f'prong_{name}_0', bx(y_a, t, 0.75, 2.75, 2.5), {
            'north': _coil_face, 'south': _coil_face,
            outer_f: _coil_face, inner_f: _inner_band(y_a, t, t, y_tip),
            'up': _solid('.'), 'down': _solid('d'),
        }, bone))
        # Step 1: vented armored magnetic rail (x +-0.75..2.75 = 2.0 wide, z +-2.0 = 4.0 deep)
        parts.append(part(f'prong_{name}_1', bx(y_b, y_a, 0.75, 2.75, 2.0), {
            'north': rail_fb_vented, 'south': rail_fb_vented,
            outer_f: rail_outer_mid, inner_f: _inner_band(y_b, y_a, t, y_tip),
            'up': _solid('.'), 'down': _solid('D'),
        }, bone))
        # Step 2: tapered dark-gunmetal accelerator tip (x +-0.75..2.25 = 1.5 wide, z +-1.5 = 3.0 deep)
        parts.append(part(f'prong_{name}_2', bx(y_tip, y_b, 0.75, 2.25, 1.5), {
            'north': _plate_box('n', 'm', 'k', 'd', 'E'), 'south': _plate_box('n', 'm', 'k', 'd', 'E'),
            outer_f: rail_tip_outer, inner_f: _inner_band(y_tip, y_b, t, y_tip),
            'up': _solid('.'), 'down': _solid('d'),
        }, bone))
    return parts


def _build_coil(c, top, P, length=6.0):
    """Draft B (Industrial Ribbed Coil-Railgun): stepped dark-slate capacitor housing with 3-tier vertical charge
    gauge cells (K0->K1->K2), a recessed copper busbar neck, and twin rails hugged by three proud 3D induction coil
    ribs along their length for an unmistakable ribbed silhouette from every angle."""
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    t = top - 4.0
    parts = []

    # 1. Upper 6x3x6 dark-slate armored capacitor sleeve (top-3..top, 12 x 6 texels)
    #    Vertical 3-stage charge cells down the center of front/back/outer so energy climbs even on the housing!
    cap_fb = [
        list('nBBBBBBBBBBn'),
        list('Bmkkd') + ['L0', 'L0'] + list('dkkmD'),
        list('Bmkkd') + ['K1', 'K1'] + list('dkkmD'),
        list('Bmkkd') + ['L2', 'L2'] + list('dkkmD'),
        list('dmmmddddddmm'[:-1] + 'd'),
        list('dEEEEEEEEEE' + 'd'),
    ]
    cap_fb[4] = list('dmmmddddmmmd')
    cap_sd = [
        list('nBBBBBBBBBBn'),
        list('BgCCdkkdCCgD'),
        list('BCCCdkkdCCCD'),
        list('BCCkd') + ['K0', 'K1'] + list('dkCCD'),
        list('dDDDdkkdDDDd'),
        list('dEEEEEEEEEE' + 'd'),
    ]
    parts.append(part('body', ((c - 3.0, top - 3.0, -3.0), (c + 3.0, top, 3.0)), {
        'north': cap_fb, 'south': cap_fb, 'east': cap_sd, 'west': cap_sd,
        'up': _bevel_up, 'down': _bevel_down,
    }))
    # Recessed 5x1x5 copper busbar neck under the capacitor sleeve (top-4..top-3) — gives real waist silhouette!
    parts.append(part('neck', ((c - 2.5, t, -2.5), (c + 2.5, top - 3.0, 2.5)), {
        'north': _coil_face, 'south': _coil_face, 'east': _coil_face, 'west': _coil_face,
        'up': _solid('.'), 'down': _solid('d'),
    }))
    # Central glowing emitter stud between the rail roots
    parts.append(part('breech', ((c - 0.75, t - 1.0, -1.0), (c + 0.75, t, 1.0)), {
        'north': _solid('k'), 'south': _solid('k'), 'east': _solid('d'), 'west': _solid('d'),
        'up': _solid('.'), 'down': _breech_bore,
    }))

    # 2. Twin slim steel rails (x +-0.75..2.25, z +-1.5 = 3.0 deep, length 6.0) + 3 proud 3D induction coil ribs!
    y_tip = t - length
    for s, name in ((1, 'out'), (-1, 'in')):
        bone = 'bit' if s > 0 else 'fork_in'
        outer_f, inner_f = ('east', 'west') if s > 0 else ('west', 'east')

        def bx(y0, y1, x_in, x_out, hd):
            xa, xb = sorted((c + s * x_in, c + s * x_out))
            return ((xa, y0, -hd), (xb, y1, hd))

        # Main rail core bar
        parts.append(part(f'prong_{name}_bar', bx(y_tip, t, 0.75, 2.25, 1.5), {
            'north': _plate_box('A', 'B', 'C', 'D', 'E'), 'south': _plate_box('A', 'B', 'C', 'D', 'E'),
            outer_f: _plate_box('n', 'm', 'k', 'd', 'E'), inner_f: _inner_band(y_tip, t, t, y_tip),
            'up': _solid('.'), 'down': _solid('d'),
        }, bone))
        # 3 proud 3D induction coil collars stepping down in size toward the tip (tapered ribbed silhouette!)
        ribs = (
            (0, t - 1.5, t - 0.5, 3.0, 2.25, _coil_face),                            # heavy copper coil 1
            (1, t - 3.5, t - 2.5, 2.5, 2.0,  _coil_face),                            # copper coil 2
            (2, t - 5.5, t - 4.5, 2.5, 1.75, _plate_box('n', 'm', 'k', 'd', 'E')),   # dark gunmetal muzzle clamp
        )
        for idx, ry0, ry1, xo, hd, face_fn in ribs:
            # Wraps outer, front and back of the rail (stops at x_in = 1.0 so it never blocks the glowing inner track!)
            parts.append(part(f'prong_{name}_rib{idx}', bx(ry0, ry1, 1.0, xo, hd), {
                'north': face_fn, 'south': face_fn, outer_f: face_fn, inner_f: _solid('.'),
                'up': _solid('A' if idx < 2 else 'n'), 'down': _solid('D'),
            }, bone))
    return parts


def _build_quad(c, top, P, length=6.0):
    """Draft C (Split-Shroud Four-Bar Accelerator): armored dark/light two-tone receiver with glowing center breech,
    and each fork split into front + back magnetic bars joined at the root and muzzle tip — opening a side window
    along the rails so the flowing 3-band blue beam channel is visible from ALL FOUR SIDES (including side profile!)."""
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    t = top - 4.0
    parts = []

    # 1. 6x4x6 sleek dark-slate + light-steel armored receiver (12 x 8)
    fb = [
        list('nBBBBBBBBBBn'),
        list('BgCCCCCCCCgD'),
        list('dDDDDDDDDDDd'),
        list('dkmCC') + ['L0', 'L0'] + list('CCmkd'),
        list('dkmCC') + ['K0', 'K0'] + list('CCmkd'),
        list('dmmddkkkkddm'[:-1] + 'd'),
        list('dQQfdkkkkdfQ'[:-1] + 'd'),
        list('dRRRdEEEEddR'[:-1] + 'd'),
    ]
    fb[5] = list('dmmddkkkkddm'[:11] + 'd')
    fb[6] = list('dQQfdkkkdfQd')
    fb[7] = list('dRRRdEEEddRd')
    sd = [
        list('nBBBBBBBBBBn'),
        list('BgCCCCCCCCgD'),
        list('dDDDDDDDDDDd'),
        list('dkfQQ') + ['K0', 'K0'] + list('QQfkd'),
        list('dkQRR') + ['L0', 'L0'] + list('RRQkd'),
        list('dDDDDDDDDDDd'),
        list('dmmkxxkkxxmd'),
        list('dEEEEEEEEEE' + 'd'),
    ]
    parts.append(part('body', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
        'north': fb, 'south': fb, 'east': sd, 'west': sd,
        'up': _bevel_up, 'down': _bevel_down,
    }))

    #2. Central glowing breech emitter (2.0 x 1.5 x 2.0) visible between the 4 bars from all sides
    parts.append(part('breech', ((c - 1.0, t - 1.5, -1.0), (c + 1.0, t, 1.0)), {
        'north': _solid('K0'), 'south': _solid('K0'), 'east': _solid('K0'), 'west': _solid('K0'),
        'up': _solid('.'), 'down': _breech_bore,
    }))

    # 3. Split-shroud forks: each fork has a solid copper-banded root yoke (1.5 px), TWO separated front/back rail
    #    bars (z = -2.25..-0.75 and +0.75..+2.25) with a 1.5 px open side window showing a glowing inner energy rail,
    #    and a tapered dark-slate muzzle bridge at the tip!
    y_tip = t - length
    y_root = t - 1.5
    y_muzz = y_tip + 1.5

    for s, name in ((1, 'out'), (-1, 'in')):
        bone = 'bit' if s > 0 else 'fork_in'
        outer_f, inner_f = ('east', 'west') if s > 0 else ('west', 'east')

        def bx(y0, y1, x_in, x_out, z0, z1):
            xa, xb = sorted((c + s * x_in, c + s * x_out))
            return ((xa, y0, z0), (xb, y1, z1))

        # Root yoke (x +-1.0..3.0, z +-2.25): heavy copper-banded shoulder clamping the two bars
        parts.append(part(f'prong_{name}_root', bx(y_root, t, 1.0, 3.0, -2.25, 2.25), {
            'north': _coil_face, 'south': _coil_face,
            outer_f: _coil_face, inner_f: _inner_band(y_root, t, t, y_tip),
            'up': _solid('.'), 'down': _solid('d'),
        }, bone))
        # Front & back rail bars (x +-0.75..2.75, z = -2.25..-0.75 and +0.75..+2.25) — 1.5 px side slot between them!
        for zname, z0, z1 in (('f', -2.25, -0.75), ('b', 0.75, 2.25)):
            bar_in_z, bar_out_z = ('south', 'north') if z0 < 0 else ('north', 'south')
            parts.append(part(f'prong_{name}_{zname}', bx(y_muzz, y_root, 0.75, 2.75, z0, z1), {
                bar_out_z: _plate_box('A', 'B', 'C', 'D', 'E'),
                bar_in_z: _plate_box('n', 'm', 'k', 'd', 'E'),
                outer_f: _plate_box('A', 'B', 'C', 'D', 'E'),
                inner_f: _inner_band(y_muzz, y_root, t, y_tip),
                'up': _solid('.'), 'down': _solid('.'),
            }, bone))
        # Thin glowing accelerator rail strip recessed inside the side slot (x +-0.75..1.25 = 0.5 wide) so the
        # flowing blue energy wave shines through BOTH the front/back gap AND the left/right side windows!
        parts.append(part(f'prong_{name}_glow', bx(y_muzz, y_root, 0.75, 1.25, -0.75, 0.75), {
            'north': _solid('.'), 'south': _solid('.'),
            outer_f: _inner_band(y_muzz, y_root, t, y_tip),
            inner_f: _inner_band(y_muzz, y_root, t, y_tip),
            'up': _solid('.'), 'down': _solid('.'),
        }, bone))
        # Tapered dark-gunmetal muzzle clamp tying the front and back bars at the tip (x +-0.75..2.25, z +-1.75)
        parts.append(part(f'prong_{name}_tip', bx(y_tip, y_muzz, 0.75, 2.25, -1.75, 1.75), {
            'north': _plate_box('n', 'm', 'k', 'd', 'E'), 'south': _plate_box('n', 'm', 'k', 'd', 'E'),
            outer_f: _plate_box('n', 'm', 'k', 'd', 'E'), inner_f: _inner_band(y_tip, y_muzz, t, y_tip),
            'up': _solid('m'), 'down': _solid('d'),
        }, bone))
    return parts


def _coil_receiver(c, top, P, part):
    """Shared cohesive 6x4x6 dark-slate capacitor housing with 3-tier vertical blue charge cells (L0 -> K1 -> L2) and
    an integrated copper busbar foot (no pinched neck, so the head flows directly from the 6x6 base)."""
    t = top - 4.0
    fb = [
        list('nBBBBBBBBBBn'),
        list('Bmkkd') + ['L0', 'L0'] + list('dkkmD'),
        list('Bmkkd') + ['K1', 'K1'] + list('dkkmD'),
        list('Bmkkd') + ['L2', 'L2'] + list('dkkmD'),
        list('dmmmddddmmmd'),
        list('dffffffffffd'),
        list('dQQQQQQQQQQd'),
        list('dRRRRRRRRRRd'),
    ]
    sd = [
        list('nBBBBBBBBBBn'),
        list('BgCCdkkdCCgD'),
        list('BCCCdkkdCCCD'),
        list('BCCkd') + ['K0', 'K1'] + list('dkCCD'),
        list('dDDDdkkdDDDd'),
        list('dffffffffffd'),
        list('dQQQQQQQQQQd'),
        list('dRRRRRRRRRRd'),
    ]
    return [
        part('body', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': fb, 'south': fb, 'east': sd, 'west': sd,
            'up': _bevel_up, 'down': _bevel_down,
        }),
        part('breech', ((c - 0.75, t - 1.0, -1.25), (c + 0.75, t, 1.25)), {
            'north': _solid('k'), 'south': _solid('k'), 'east': _solid('d'), 'west': _solid('d'),
            'up': _solid('.'), 'down': _breech_bore,
        }),
    ]


def _build_coil_flush(c, top, P, length=6.0):
    """Coil R2-A (Flush): full 6x4x6 capacitor receiver (no neck pinch), wider 2x4 steel rail bars and three tight
    induction coil bands aligned flush with the 6x6 silhouette."""
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    t = top - 4.0
    parts = _coil_receiver(c, top, P, part)
    y_tip = t - length
    for s, name in ((1, 'out'), (-1, 'in')):
        bone = 'bit' if s > 0 else 'fork_in'
        outer_f, inner_f = ('east', 'west') if s > 0 else ('west', 'east')

        def bx(y0, y1, x_in, x_out, hd):
            xa, xb = sorted((c + s * x_in, c + s * x_out))
            return ((xa, y0, -hd), (xb, y1, hd))

        parts.append(part(f'prong_{name}_bar', bx(y_tip, t, 0.75, 2.75, 2.0), {
            'north': _plate_box('A', 'B', 'C', 'D', 'E'), 'south': _plate_box('A', 'B', 'C', 'D', 'E'),
            outer_f: _plate_box('n', 'm', 'k', 'd', 'E'), inner_f: _inner_band(y_tip, t, t, y_tip),
            'up': _solid('.'), 'down': _solid('d'),
        }, bone))
        ribs = (
            (0, t - 1.5, t - 0.5, 3.0, 2.5, _coil_face),
            (1, t - 3.5, t - 2.5, 3.0, 2.5, _coil_face),
            (2, t - 5.5, t - 4.5, 3.0, 2.5, _plate_box('n', 'm', 'k', 'd', 'E')),
        )
        for idx, ry0, ry1, xo, hd, face_fn in ribs:
            parts.append(part(f'prong_{name}_rib{idx}', bx(ry0, ry1, 1.0, xo, hd), {
                'north': face_fn, 'south': face_fn, outer_f: face_fn, inner_f: _solid('.'),
                'up': _solid('f' if idx < 2 else 'n'), 'down': _solid('R' if idx < 2 else 'd'),
            }, bone))
    return parts


def _build_coil_taper(c, top, P, length=6.0):
    """Coil R2-B (Flush Taper): full 6x4x6 capacitor receiver flowing smoothly into 3-step tapered rail bars wrapped by
    tightly-hugging copper coils & muzzle clamp (one continuous 6.0 -> 5.5 -> 5.0 envelope)."""
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    t = top - 4.0
    parts = _coil_receiver(c, top, P, part)
    y_tip = t - length
    for s, name in ((1, 'out'), (-1, 'in')):
        bone = 'bit' if s > 0 else 'fork_in'
        outer_f, inner_f = ('east', 'west') if s > 0 else ('west', 'east')

        def bx(y0, y1, x_in, x_out, hd):
            xa, xb = sorted((c + s * x_in, c + s * x_out))
            return ((xa, y0, -hd), (xb, y1, hd))

        segs = (
            (0, t - 2.0, t,       2.75, 2.5),
            (1, t - 4.0, t - 2.0, 2.25, 2.0),
            (2, y_tip,   t - 4.0, 2.25, 1.5),
        )
        for idx, y0, y1, xo, hd in segs:
            parts.append(part(f'prong_{name}_s{idx}', bx(y0, y1, 0.75, xo, hd), {
                'north': _plate_box('A', 'B', 'C', 'D', 'E'), 'south': _plate_box('A', 'B', 'C', 'D', 'E'),
                outer_f: _plate_box('n', 'm', 'k', 'd', 'E'), inner_f: _inner_band(y0, y1, t, y_tip),
                'up': _solid('.'), 'down': _solid('d'),
            }, bone))
        ribs = (
            (0, t - 1.5, t - 0.5, 3.0, 2.75, _coil_face),
            (1, t - 3.5, t - 2.5, 2.5, 2.25, _coil_face),
            (2, t - 5.5, t - 4.5, 2.5, 2.0,  _plate_box('n', 'm', 'k', 'd', 'E')),
        )
        for idx, ry0, ry1, xo, hd, face_fn in ribs:
            parts.append(part(f'prong_{name}_rib{idx}', bx(ry0, ry1, 1.0, xo, hd), {
                'north': face_fn, 'south': face_fn, outer_f: face_fn, inner_f: _solid('.'),
                'up': _solid('f' if idx < 2 else 'n'), 'down': _solid('R' if idx < 2 else 'd'),
            }, bone))
    return parts


def _build_coil_solid(c, top, P, length=6.0):
    """Coil R2-C (Grooved Armored Coils): full 6x4x6 capacitor receiver seamlessly joined to heavy flush twin rails
    built from alternating armored steel sleeves and recessed copper induction coil channels (zero protruding ears)."""
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    t = top - 4.0
    parts = _coil_receiver(c, top, P, part)
    y_tip = t - length

    def sleeve_outer_glow(w, h):
        rows = [['A'] * (w - 1) + ['B']]
        for j in range(1, h - 1):
            if w >= 6:
                rows.append(['B', 'd'] + ['L1' if j == 1 else 'K1'] * (w - 4) + ['d', 'D'])
            else:
                rows.append(['B'] + ['C'] * (w - 2) + ['D'])
        rows.append(['D'] * (w - 1) + ['E'])
        return rows

    for s, name in ((1, 'out'), (-1, 'in')):
        bone = 'bit' if s > 0 else 'fork_in'
        outer_f, inner_f = ('east', 'west') if s > 0 else ('west', 'east')

        def bx(y0, y1, x_in, x_out, hd):
            xa, xb = sorted((c + s * x_in, c + s * x_out))
            return ((xa, y0, -hd), (xb, y1, hd))

        # 5 stacked non-overlapping segments: recessed copper coil -> flush steel shroud -> copper coil -> steel shroud -> dark tip
        stack = (
            ('c0',  t - 1.0, t,       2.75, 2.5,  _coil_face,                        _coil_face,        'd'),
            ('sh0', t - 2.5, t - 1.0, 2.75, 2.75, _plate_box('A', 'B', 'C', 'D', 'E'), _plate_box('A', 'B', 'C', 'D', 'E'), 'D'),
            ('c1',  t - 3.5, t - 2.5, 2.25, 2.25, _coil_face,                        _coil_face,        'R'),
            ('sh1', t - 5.0, t - 3.5, 2.75, 2.5,  _plate_box('A', 'B', 'C', 'D', 'E'), sleeve_outer_glow, 'D'),
            ('tip', y_tip,   t - 5.0, 2.25, 2.0,  _plate_box('n', 'm', 'k', 'd', 'E'), _plate_box('n', 'm', 'k', 'd', 'E'), 'd'),
        )
        for tag, y0, y1, xo, hd, fb_fn, out_fn, dn_ch in stack:
            parts.append(part(f'prong_{name}_{tag}', bx(y0, y1, 0.75, xo, hd), {
                'north': fb_fn, 'south': fb_fn, outer_f: out_fn,
                inner_f: _inner_band(y0, y1, t, y_tip),
                'up': _solid('B' if tag.startswith('sh') else '.'),
                'down': _solid(dn_ch),
            }, bone))
    return parts


def _ori_receiver(c, top, P, part, style='steel'):
    """Clean, uncluttered 6x4x6 Oritech-inspired receiver: big calm color planes, subtle corner bolts, and a single
    clean glowing charge bar (no busy black grids or choppy stripes)."""
    t = top - 4.0
    if style == 'copper':
        # Oritech's iconic 2-material split: warm copper body with clean dark-slate top/bottom trim & cyan charge bar
        fb = [
            list('nmmmmmmmmmmn'),
            list('kffffffffffk'),
            list('kQfgQQQQgfQk'),
            list('kQQQQ') + ['L0', 'L0'] + list('QQQQk'),
            list('kQQQQ') + ['K0', 'K0'] + list('QQQQk'),
            list('kQQQQQQQQQQk'),
            list('kRRRRRRRRRRk'),
            list('dkkkkkkkkkkd'),
        ]
        sd = [
            list('nmmmmmmmmmmn'),
            list('kffffffffffk'),
            list('kQQQQQQQQQQk'),
            list('kQgQQ') + ['L0', 'K0'] + list('QQgQk'),
            list('kQQQQQQQQQQk'),
            list('kRRRRRRRRRRk'),
            list('kRRRRRRRRRRk'),
            list('dkkkkkkkkkkd'),
        ]
        up = _bevel_up(12, 12, rim='n', mid='m', core='k')
    elif style == 'flush_clean':
        # Seamless steel receiver flowing straight into the flush steel cheek plates (no copper divider)
        fb = [
            list('nBBBBBBBBBBn'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCD') + ['L0', 'L0'] + list('DCCCD'),
            list('BCCCD') + ['K0', 'K0'] + list('DCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('DDDDDDDDDDDE'),
        ]
        sd = [
            list('nBBBBBBBBBBn'),
            list('BgCCCCCCCCgD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('DDDDDDDDDDDE'),
        ]
        up = _bevel_up(12, 12, rim='B', mid='C', core='k')
    elif style == 'flush_seam':
        # Seamless steel receiver with a taller glowing cyan channel slit feeding straight into the rail gap
        fb = [
            list('nBBBBBBBBBBn'),
            list('BCCCCCCCCCCD'),
            list('BCCCD') + ['L0', 'L0'] + list('DCCCD'),
            list('BCCCD') + ['K0', 'K0'] + list('DCCCD'),
            list('BCCCD') + ['K0', 'K0'] + list('DCCCD'),
            list('BCCCD') + ['K0', 'K0'] + list('DCCCD'),
            list('BCCCD') + ['d', 'd'] + list('DCCCD'),
            list('DDDDDDDDDDDE'),
        ]
        sd = [
            list('nBBBBBBBBBBn'),
            list('BgCCCCCCCCgD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('DDDDDDDDDDDE'),
        ]
        up = _bevel_up(12, 12, rim='B', mid='C', core='k')
    elif style == 'flush_dark':
        # Unified dark-slate gunmetal receiver matching the dark rails + crisp light-steel side cheeks flowing straight down
        fb = [
            list('nmmmmmmmmmmn'),
            list('mkkkkkkkkkkd'),
            list('mkkkd') + ['L0', 'L0'] + list('dkkkd'),
            list('mkkkd') + ['K0', 'K0'] + list('dkkkd'),
            list('mkkkd') + ['K0', 'K0'] + list('dkkkd'),
            list('mkkkkkkkkkkd'),
            list('mkkkkkkkkkkd'),
            list('dddddddddddE'),
        ]
        sd = [
            list('nBBBBBBBBBBn'),
            list('BgCCCCCCCCgD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('DDDDDDDDDDDE'),
        ]
        up = _bevel_up(12, 12, rim='n', mid='m', core='k')
    else:
        # Calm Power Suits steel/slate housing with one clean copper accent collar at the top & single cyan charge bar
        fb = [
            list('nBBBBBBBBBBn'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCD') + ['L0', 'L0'] + list('DCCC' + 'D'),
            list('BCCCD') + ['K0', 'K0'] + list('DCCC' + 'D'),
            list('BCCCCCCCCCCD'),
            list('DffffffffffQ'),
            list('dQQQQQQQQQQd'),
        ]
        sd = [
            list('nBBBBBBBBBBn'),
            list('BgCCCCCCCCgD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('BCCCCCCCCCCD'),
            list('DDDDDDDDDDDE'),
            list('DffffffffffQ'),
            list('dQQQQQQQQQQd'),
        ]
        up = _bevel_up(12, 12, rim='B', mid='C', core='k')
    return [
        part('body', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': fb, 'south': fb, 'east': sd, 'west': sd,
            'up': up, 'down': _bevel_down,
        }),
    ]


def _smooth_rail(lit='n', body='k', sh='d', dk='E'):
    """Clean, unbroken rail face: subtle top bevel + smooth solid body + clean shaded edge (zero visual noise)."""
    def f(w, h):
        rows = [[lit] * max(1, w - 1) + ([body] if w > 1 else [])]
        for _ in range(max(0, h - 2)):
            rows.append([body] * max(1, w - 1) + ([sh] if w > 1 else []))
        if h > 1:
            rows.append([sh] * max(1, w - 1) + ([dk] if w > 1 else []))
        return rows
    return f


def _glow_rod(y0, y1, rail_top, rail_bot):
    """Protruding glowing cyan accelerator bar (Oritech's inner glowing rail): smooth 3-band charge wave K0->K1->K2
    with bright hot tip at the muzzle end."""
    span = rail_top - rail_bot
    def f(w, h):
        rows = []
        for j in range(h):
            frac = ((rail_top - y1) + (j + 0.5) / 2.0) / span
            n = min(2, max(0, int(frac * 3)))
            tip = (j >= h - 2)
            crest = ((frac * 3) - n) < 0.25
            ch = ('L' if (tip or crest) else 'K') + str(n)
            rows.append([ch] * w)
        return rows
    return f


def _build_oritech(c, top, P, length=6.0, style='steel'):
    """Oritech-inspired clean twin-rail cannon:
    - style='steel'  : calm steel/slate receiver with slim copper collar + sleek dark-slate rails + protruding cyan rods
    - style='copper' : Oritech's 2-material split (clean copper receiver + unbroken dark-slate rails + protruding cyan rods)
    - style='flush'  : full-width flush monolithic dark-slate rails hugging the 6x6 base + bold protruding cyan rods"""
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    t = top - 4.0
    rec_style = style if style in ('copper', 'flush_clean', 'flush_seam', 'flush_dark') else 'steel'
    parts = _ori_receiver(c, top, P, part, style=rec_style)

    y_rod_tip = t - length              # glowing inner cyan rods extend full 6.0 px (0.5 px past outer rails!)
    y_rail_tip = y_rod_tip + 0.5        # outer dark-slate rails stop 0.5 px shy so glowing cyan tips protrude cleanly
    flush = style.startswith('flush')

    # Outer rail geometry: clean, unbroken monolithic blocks (all exact 0.5 px multiples, zero overlap)
    x_rod_in, x_rod_out = (0.5, 1.0)                   # 0.5 px wide glowing inner accelerator rod (1.0 px open center gap)
    x_rail_in, x_rail_out = (1.0, 2.5)                 # 1.5 px wide unbroken dark-slate rail
    rail_hd = 2.5 if flush else 2.0                    # 5.0 deep (flush) or 4.0 deep (sleek)
    rod_hd = 1.0 if flush else 0.75                    # glowing cyan bar depth in Z (2.0 or 1.5 deep)

    for s, name in ((1, 'out'), (-1, 'in')):
        bone = 'bit' if s > 0 else 'fork_in'
        outer_f, inner_f = ('east', 'west') if s > 0 else ('west', 'east')

        def bx(y0, y1, xa_, xb_, hd):
            xa, xb = sorted((c + s * xa_, c + s * xb_))
            return ((xa, y0, -hd), (xb, y1, hd))

        # 1. Clean, unbroken dark-slate outer rail (smooth, calm, zero noisy stripes)
        rail_fb = _smooth_rail('n', 'm', 'k', 'd')
        rail_out = _smooth_rail('B', 'C', 'D', 'E') if style == 'steel' else _smooth_rail('n', 'm', 'k', 'd')
        parts.append(part(f'prong_{name}_rail', bx(y_rail_tip, t, x_rail_in, x_rail_out, rail_hd), {
            'north': rail_fb, 'south': rail_fb, outer_f: rail_out,
            inner_f: _smooth_rail('k', 'd', 'd', 'E'),
            'up': _solid('.'), 'down': _solid('d'),
        }, bone))

        # 2. Glowing cyan inner accelerator rod protruding 0.5 px past the outer rail tip (Oritech's signature!)
        rod_fn = _glow_rod(y_rod_tip, t, t, y_rod_tip)
        parts.append(part(f'prong_{name}_rod', bx(y_rod_tip, t, x_rod_in, x_rod_out, rod_hd), {
            'north': rod_fn, 'south': rod_fn,
            outer_f: rod_fn, inner_f: rod_fn,
            'up': _solid('.'), 'down': _solid('L2'),
        }, bone))

        # 3. Subtle dark-slate capacitor lugs / flush upper cheek sitting flush with the 6x6 receiver (+-3.0)
        if not flush:
            for idx, ly in enumerate((t - 1.5, t - 3.5)):
                parts.append(part(f'prong_{name}_lug{idx}', bx(ly - 0.5, ly + 0.5, 2.5, 3.0, 1.5), {
                    'north': _solid('d'), 'south': _solid('d'),
                    outer_f: _smooth_rail('m', 'k', 'd', 'E'), inner_f: _solid('.'),
                    'up': _solid('n'), 'down': _solid('E'),
                }, bone))
        else:
            # Flush style: clean outer cheek plate on the upper half of the rail for a cohesive 6x6 flush transition
            parts.append(part(f'prong_{name}_cheek', bx(t - 3.0, t, 2.5, 3.0, 2.5), {
                'north': _smooth_rail('n', 'k', 'd', 'E'), 'south': _smooth_rail('n', 'k', 'd', 'E'),
                outer_f: _smooth_rail('A', 'B', 'C', 'D'), inner_f: _solid('.'),
                'up': _solid('.'), 'down': _solid('d'),
            }, bone))
    return parts


def _build_oritech_concave(c, top, P, length=6.0, mode='side'):
    """Concave rail variations built on ori_flush_seam (seamless steel receiver + tall glowing cyan channel slit,
    no copper divider):
    - mode='side'    : concave carved side waist (z 5.0 -> 3.5 -> 5.0) with flared dark muzzle lip
    - mode='both'    : concave hourglass waist in BOTH width and depth (6.0 -> 5.0 -> 6.0 wide, 5.0 -> 4.0 -> 5.0 deep)
    - mode='channel' : concave C-channel rails (flush front/back rail flanges with a recessed outer trough cradling the bar)"""
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    t = top - 4.0
    parts = _ori_receiver(c, top, P, part, style='flush_seam')

    y_rod_tip = t - length              # 6.0 px glowing cyan rods (0.5 px past outer rail tips)
    y_rail_tip = y_rod_tip + 0.5        # 5.5 px outer rails
    y_sh = t - 1.5                      # upper flush shoulder bottom
    y_mz = y_rail_tip + 1.0             # muzzle flare top

    rail_fb = _smooth_rail('n', 'm', 'k', 'd')
    steel_side = _smooth_rail('A', 'B', 'C', 'D')
    dark_side = _smooth_rail('n', 'm', 'k', 'd')

    for s, name in ((1, 'out'), (-1, 'in')):
        bone = 'bit' if s > 0 else 'fork_in'
        outer_f, inner_f = ('east', 'west') if s > 0 else ('west', 'east')

        def bx(y0, y1, xa_, xb_, z0, z1):
            xa, xb = sorted((c + s * xa_, c + s * xb_))
            return ((xa, y0, z0), (xb, y1, z1))

        # Glowing cyan inner accelerator rod (protrudes 0.5 px past the rail tip)
        rod_fn = _glow_rod(y_rod_tip, t, t, y_rod_tip)
        parts.append(part(f'prong_{name}_rod', bx(y_rod_tip, t, 0.5, 1.0, -1.0, 1.0), {
            'north': rod_fn, 'south': rod_fn, outer_f: rod_fn, inner_f: rod_fn,
            'up': _solid('.'), 'down': _solid('L2'),
        }, bone))

        # Upper flush steel shoulder seamlessly continuing the 6x6 receiver
        parts.append(part(f'prong_{name}_root', bx(y_sh, t, 1.0, 3.0, -2.5, 2.5), {
            'north': steel_side, 'south': steel_side, outer_f: steel_side,
            inner_f: _smooth_rail('k', 'd', 'd', 'E'), 'up': _solid('.'), 'down': _solid('d'),
        }, bone))

        if mode in ('side', 'both'):
            mid_hd = 1.75 if mode == 'side' else 2.0
            mz_xo = 2.5 if mode == 'side' else 3.0
            # Concave carved middle waist
            parts.append(part(f'prong_{name}_mid', bx(y_mz, y_sh, 1.0, 2.5, -mid_hd, mid_hd), {
                'north': rail_fb, 'south': rail_fb, outer_f: dark_side,
                inner_f: _smooth_rail('k', 'd', 'd', 'E'), 'up': _solid('.'), 'down': _solid('.'),
            }, bone))
            # Flared muzzle end-cap completing the concave profile
            parts.append(part(f'prong_{name}_tip', bx(y_rail_tip, y_mz, 1.0, mz_xo, -2.5, 2.5), {
                'north': steel_side if mode == 'both' else rail_fb,
                'south': steel_side if mode == 'both' else rail_fb,
                outer_f: steel_side if mode == 'both' else dark_side,
                inner_f: _smooth_rail('k', 'd', 'd', 'E'),
                'up': _solid('B' if mode == 'both' else 'n'), 'down': _solid('d'),
            }, bone))
        else:
            # C-channel concave rails: front & back outer rail flanges framing a recessed dark outer trough
            for tag, z0, z1 in (('fl_f', -2.5, -1.5), ('fl_b', 1.5, 2.5)):
                z_out, z_in = ('north', 'south') if z0 < 0 else ('south', 'north')
                parts.append(part(f'prong_{name}_{tag}', bx(y_rail_tip, y_sh, 1.0, 2.5, z0, z1), {
                    z_out: rail_fb, z_in: _smooth_rail('k', 'd', 'd', 'E'),
                    outer_f: steel_side, inner_f: _smooth_rail('k', 'd', 'd', 'E'),
                    'up': _solid('.'), 'down': _solid('d'),
                }, bone))
            # Recessed dark-slate trough web connecting the front & back flanges (0.5 px recessed from outer face)
            parts.append(part(f'prong_{name}_web', bx(y_rail_tip, y_sh, 1.0, 2.0, -1.5, 1.5), {
                'north': _solid('.'), 'south': _solid('.'),
                outer_f: _smooth_rail('k', 'd', 'd', 'E'),
                inner_f: _smooth_rail('k', 'd', 'd', 'E'),
                'up': _solid('.'), 'down': _solid('E'),
            }, bone))
    return parts


def build(c, top, lamp='dark', kind='ori_concave_channel', core='dark', length=6.0, sleeve=False, head_scale=False):
    """The rail cannon's parts on an arm centred at x c whose socket is at y top: the receiver (bone 'tool') and the
    prongs / core under it (bone 'bit'). `lamp` is unused (the tools' common signature)."""
    P = pal(core)
    if kind == 'gauss':
        return _build_gauss(c, top, P, length)
    if kind == 'coil':
        return _build_coil(c, top, P, length)
    if kind == 'coil_flush':
        return _build_coil_flush(c, top, P, length)
    if kind == 'coil_taper':
        return _build_coil_taper(c, top, P, length)
    if kind == 'coil_solid':
        return _build_coil_solid(c, top, P, length)
    if kind == 'ori_steel':
        return _build_oritech(c, top, P, length, style='steel')
    if kind == 'ori_copper':
        return _build_oritech(c, top, P, length, style='copper')
    if kind == 'ori_flush':
        return _build_oritech(c, top, P, length, style='flush')
    if kind == 'ori_flush_clean':
        return _build_oritech(c, top, P, length, style='flush_clean')
    if kind == 'ori_flush_seam':
        return _build_oritech(c, top, P, length, style='flush_seam')
    if kind == 'ori_flush_dark':
        return _build_oritech(c, top, P, length, style='flush_dark')
    if kind == 'ori_concave_side':
        return _build_oritech_concave(c, top, P, length, mode='side')
    if kind == 'ori_concave_both':
        return _build_oritech_concave(c, top, P, length, mode='both')
    if kind == 'ori_concave_channel':
        return _build_oritech_concave(c, top, P, length, mode='channel')
    if kind == 'quad':
        return _build_quad(c, top, P, length)
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
