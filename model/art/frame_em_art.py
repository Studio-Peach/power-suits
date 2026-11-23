"""The EM projector for the frame (frame_model.py, TOOL=em): the seventh power tool brought over from the big suit.

2026-11-22 2D-layer rework (user picked B: '2d_gravity_gun'): rebuilt in the approved 2D-texture + 0.5 px cutout
outer-layer design system (7 cubes, 7.5 px overall, 64x64 standalone texture via tools/export-tools.py):
- 6x3.5x6 dark magnetized slate cuff (`cuff_outer` cutout shell over `cuff_inner` 5x3.5x5): upper 0.5 px recessed
  wound copper stator coil bay + lower 0.5 px recessed glowing redstone capacitor window (`em_core`);
- spinning 4x1.5x4 chiseled dark-lodestone bezel + faceted glowing redstone emitter lens (`em_core`, bone 'bit');
- 4 unified single-cube cardinal prongs (2.0 x 4.0 x 1.0 at r=2.0..3.0, flush with cuff, bone 'bit' /
  em_projector_poles): bolted magnetic root, wound copper coil wraps, riveted iron jaw spine, and tall inner-facing
  glowing redstone arc electrode rails & tips (`em_arc`) facing across the emitter core.

Other 2026-11-22 2D-layer drafts kept as knobs:
- 2d_shroud_claw   : (A, 4 cubes, 7.5 px) iron/copper cuff + single cutout L-corner claw crown over spinning core;
- 2d_tesla_cage    : (C, 4 cubes, 7.5 px) iron/copper cuff + spinning coil rod inside a 2D cutout twin-ring cage;
- 2d_lodestone_dish: (D, 7 cubes, 7.0 px) burnished copper/lodestone cuff + 3x1.5x3 dish + 4 compact corner claws.

Earlier 3D rounds kept as knobs: claw_b2 (2026-11-20), claw_b1, claw, splay, corner, step, legacy (2026-11-15).

EM_GLOW: 'dark' (default, reserved dark redstone colours for export-tools.py em_core / em_arc glowmasks) | 'idle'
(powered idle breathing core preview) | 'lit' (active holding preview for review sheets).

Coordinates raw, right arm (+x; the left mirrors), centred on the arm's axis (x c, z 0). Faces as frame_drill_art.py.
"""
import frame_drill_art as drill

_c = drill._c
# Reserved dark redstone colours (lens/vents R0-R3 -> em_core, tips T1-T2 -> em_arc) and their lit preview colours
RES_DARK = dict(R0='3a0e0c', R1='4b1310', R2='5c1813', R3='701f17', T1='4e1411', T2='621a14')
RES_LIT = dict(R0='7a0600', R1='b81206', R2='f0200c', R3='ff6a4a', T1='c01206', T2='ff2a14')
RES = RES_DARK  # kept for external references
BASE_PAL = {k: _c(v) for k, v in dict(
    A='9fa4a9', B='757c85', C='58606a', D='3c424c', E='22262e', g='cdcfcf',
    f='e09868', Q='c07440', R='804426', d='25292c', k='2f3437', m='3b4246',
).items()} | {'.': '.'}
P = BASE_PAL | {k: _c(v) for k, v in RES_DARK.items()}


def _pal(glow='dark'):
    res = RES_LIT if glow == 'lit' else RES_DARK
    return BASE_PAL | {k: _c(v) for k, v in res.items()}


def _paint(faces, pal):
    return lambda f, w, h: [[pal[ch] for ch in r] for r in (faces[f](w, h) if callable(faces[f]) else faces[f])]


def solid(ch):
    return lambda w, h: [[ch] * w for _ in range(h)]


def pole(seg):
    """Side face of a prong segment: wound copper coil, shaded steel shaft, or glowing redstone tip."""
    def f(w, h):
        if seg == 'wind':
            # Alternating lit copper turns with a dark groove between them so it reads as wound wire
            rows = []
            for j in range(h):
                if j % 2 == 1 and j < h - 1:
                    rows.append(['R'] * w)
                else:
                    rows.append(['f'] * max(1, w - 1) + (['Q'] if w > 1 else []))
            if h >= 4:
                rows[-1] = ['R'] * w
            return rows
        if seg == 'steel':
            if h == 1:
                return [['A'] * max(1, w - 1) + (['B'] if w > 1 else [])]
            top_r = ['A'] * max(1, w - 1) + (['B'] if w > 1 else [])
            mid_r = (['B'] + ['C'] * (w - 2) + ['D']) if w > 2 else (['B', 'C'][:w])
            return [top_r] + [mid_r] * (h - 1)
        # Redstone tip: darker collar row into bright sparking tip
        if h == 1:
            return [['T2'] * w]
        return [['T1'] * w] + [['T2'] * w] * (h - 1)
    return f


def housing_side(w, h):
    """Housing side (10 or 12 wide x 6 or 7 tall): lit top rim, bolted steel body, dark iron collar with symmetric
    redstone vent slits, dark shadow foot."""
    assert w in (10, 12) and h in (6, 7), (w, h)
    rows = [
        list('A' * (w - 1) + 'B'),
        list('Bg' + 'C' * (w - 4) + 'gD'),
        list('B' + 'C' * (w - 2) + 'D'),
    ]
    if h == 7:
        rows.append(list('D' * (w - 1) + 'E'))
    pad = ['k'] * ((w - 10) // 2)
    rows += [
        list('d' + 'k' * (w - 2) + 'd'),
        ['d', 'k'] + pad + ['R2', 'k', 'R3', 'R3', 'k', 'R2'] + pad + ['k', 'd'],
        list('E' * w),
    ]
    return rows


def housing_up(w, h):
    """Housing top face: lit steel bevel rim round the 5 x 5 arm when sleeved (12 x 12), plain dark at 10 x 10."""
    if w <= 10:
        return [['D'] * w for _ in range(h)]
    return [list('A' * (w - 1) + 'B')] + [list('B' + 'D' * (w - 2) + 'C') for _ in range(h - 2)] + [list('D' * w)]


def housing_down(w, h):
    """Underside of housing: dark steel plate with subtle bezel framing the central emitter."""
    g = [['D'] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            if i in (0, w - 1) or j in (0, h - 1):
                g[j][i] = 'E'
            elif 2 <= i < w - 2 and 2 <= j < h - 2:
                g[j][i] = 'k'
    return g


def lens_down(w, h):
    """Glowing redstone emitter lens centred on a bezel (works for 3x3, 4x4, 6x6, 8x8 texels)."""
    g = [['C'] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            d = min(i, j, w - 1 - i, h - 1 - j)
            if w <= 4:
                # 3x3 or 4x4 lens boss: outer ring R1/R2, bright R3 core
                g[j][i] = 'R3' if d >= 1 else ('R2' if (i + j) % 2 == 0 else 'R1')
            elif w == 6:
                # 6x6 core (outer steel rim removed): 1-texel dark bezel (d=0), 4x4 redstone lens (d>=1), bright core (d>=2)
                if d == 0:
                    g[j][i] = 'E'
                elif d >= 2:
                    g[j][i] = 'R3'
                else:
                    g[j][i] = 'R2' if (i + j) % 2 == 0 else 'R1'
            else:
                # 8x8 emitter hub (dark bezel matching 6x6 claw_b2): dark bezel (d=0), 6x6 redstone lens (d>=1), bright core (d>=2)
                if d == 0:
                    g[j][i] = 'E'
                elif d >= 2:
                    g[j][i] = 'R3'
                else:
                    g[j][i] = 'R2' if (i + j) % 2 == 0 else 'R1'
    return g


def lens_side(w, h):
    """Bezel rim around the protruding lens boss."""
    if h == 1:
        return [['B'] + ['C'] * max(0, w - 2) + (['D'] if w > 1 else [])]
    return [list('dkkkkkkkkd')[:w]] + [['d', 'k', 'R1'] + ['k'] * max(0, w - 6) + ['R1', 'k', 'd'] if w >= 6 else ['d'] * w] * (h - 1)


def _legacy_build(c, top, pal):
    """The 2026-11-15 straight 10 px EM projector (4 px housing + four straight 2 x 2 x 6 corner poles)."""
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, pal), 0), bone=bone)
    t = top - 4

    def side(w, h):
        rows = ['A' * (w - 1) + 'B', 'B' + 'g' + 'C' * (w - 4) + 'g' + 'D'] + ['B' + 'C' * (w - 2) + 'D'] * (h - 5)
        rows = [list(r) for r in rows]
        rows += [['d'] + ['k'] * (w - 2) + ['d']]
        rows += [['d'] + ['R1' if i % 2 == 0 else 'k' for i in range(1, w - 1)] + ['d']]
        rows += [['E'] * w]
        return rows

    def bezel(w, h):
        g = [['C'] * w for _ in range(h)]
        for j in range(h):
            for i in range(w):
                if 2 <= i < w - 2 and 2 <= j < h - 2:
                    g[j][i] = 'E'
                if 3 <= i < w - 3 and 3 <= j < h - 3:
                    g[j][i] = ['R0', 'R1', 'R2', 'R3'][(i + j) % 4]
        return g

    parts = [part('body', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)),
                  {f: side for f in ('north', 'south', 'east', 'west')} | {'up': solid('D'), 'down': bezel})]
    for sx, name_x in ((1, 'a'), (-1, 'b')):
        for sz, name_z in ((1, 'a'), (-1, 'b')):
            xa, xb = sorted((c + sx * 0.5, c + sx * 2.5))
            za, zb = sorted((sz * 0.5, sz * 2.5))
            y = t
            for seg, h in (('wind', 2), ('steel', 3), ('tip', 1)):
                faces = {f: pole(seg) for f in ('north', 'south', 'east', 'west')} | \
                        {'up': solid('D') if seg != 'tip' else solid('R'),
                         'down': solid('E') if seg != 'tip' else pole('tip')}
                parts.append(part(f'pole_{name_x}{name_z}_{seg}', ((xa, y - h, za), (xb, y, zb)), faces, 'bit'))
                y -= h
    return parts


def _part(name, box, faces, pal, bone='tool', rot=0, origin=None):
    p = dict(drill.part(name, box, _paint(faces, pal), rot), bone=bone)
    if origin is not None:
        p['origin'] = origin
    return p


def _prong_faces(seg):
    return {f: pole(seg) for f in ('north', 'south', 'east', 'west')} | {
        'up': solid('Q') if seg == 'wind' else (solid('B') if seg == 'steel' else solid('T1')),
        'down': solid('R') if seg == 'wind' else (solid('D') if seg == 'steel' else pole('tip')),
    }


def _build_splay(c, top, pal):
    """4 cardinal (N/S/E/W) prongs angled outward 13 deg from under a 3.5 px housing (7.5 px overall, peeking ~0.5 px
    past the housing sides). Sized so the prongs spin 360 deg around the arm axis (ToolRotors: em_projector_poles)
    without clipping the stationary 1.5 x 0.5 x 1.5 central lens (corner r 1.06 < inner r 1.11) or poking out the
    5 x 5 housing at their buried roots (root outer r 2.21 < 2.5)."""
    t = top - 3.5
    parts = [
        _part('body', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)),
              {f: housing_side for f in ('north', 'south', 'east', 'west')} | {'up': solid('D'), 'down': housing_down}, pal),
        _part('lens', ((c - 0.75, t - 0.5, -0.75), (c + 0.75, t, 0.75)),
              {f: lens_side for f in ('north', 'south', 'east', 'west')} | {'up': solid('E'), 'down': lens_down}, pal),
    ]
    tilt = 13.0
    # Cardinal directions: (name, axis, sign)
    # East (+x) / West (-x): radial x in [1.1, 2.1], pivot at r=1.6, rot z = +sign*tilt
    # South (+z) / North (-z): radial z in [1.1, 2.1], pivot at r=1.6, rot x = -sign*tilt
    for name, axis, s in (('e', 'x', 1), ('w', 'x', -1), ('s', 'z', 1), ('n', 'z', -1)):
        piv = (c + s * 1.6, t, 0.0) if axis == 'x' else (c, t, s * 1.6)
        rot = (0.0, 0.0, s * tilt) if axis == 'x' else (-s * tilt, 0.0, 0.0)
        # Stepped wider copper collar (2.0 tangential, seated 0.5 px up into the housing so the tilt leaves no gap)
        # into slimmer 1.5 steel blade and redstone tip
        for seg, y0, y1, tw in (('wind', t - 1.5, t + 0.5, 2.0), ('steel', t - 3.0, t - 1.5, 1.5), ('tip', t - 4.0, t - 3.0, 1.5)):
            if axis == 'x':
                xa, xb = sorted((c + s * 1.1, c + s * 2.1))
                box = ((xa, y0, -tw / 2), (xb, y1, tw / 2))
            else:
                za, zb = sorted((s * 1.1, s * 2.1))
                box = ((c - tw / 2, y0, za), (c + tw / 2, y1, zb))
            parts.append(_part(f'pole_{name}_{seg}', box, _prong_faces(seg), pal, bone='bit', rot=rot, origin=piv))
    return parts


def _build_claw_variant(c, top, pal, hub_r=2.0, r0=2.0, r1=3.0, hub_bone='tool', sleeve=False, w_coil=2.0, w_prong=1.5):
    """4 cardinal (N/S/E/W) side-mounted prongs around a recessed emitter hub under a 3 px housing (7.0 px overall)."""
    t = top - 3.0
    bw = 3.0 if sleeve else 2.5
    parts = [
        _part('body', ((c - bw, t, -bw), (c + bw, top, bw)),
              {f: housing_side for f in ('north', 'south', 'east', 'west')} | {'up': housing_up, 'down': housing_down}, pal),
        _part('hub', ((c - hub_r, t - 1.0, -hub_r), (c + hub_r, t, hub_r)),
              {f: lens_side for f in ('north', 'south', 'east', 'west')} | {'up': solid('E'), 'down': lens_down}, pal,
              bone=hub_bone),
    ]
    for name, axis, s in (('e', 'x', 1), ('w', 'x', -1), ('s', 'z', 1), ('n', 'z', -1)):
        segs = (
            ('wind',  t - 1.5, t,       r0, r1, w_coil),    # copper coil collar
            ('steel', t - 3.0, t - 1.5, r0, r1, w_prong),   # steel prong body
            ('tip',   t - 4.0, t - 3.0, r0, r1, w_prong),   # glowing redstone tip aligned with prong body
        )
        for seg, y0, y1, p0, p1, tw in segs:
            if axis == 'x':
                xa, xb = sorted((c + s * p0, c + s * p1))
                box = ((xa, y0, -tw / 2), (xb, y1, tw / 2))
            else:
                za, zb = sorted((s * p0, s * p1))
                box = ((c - tw / 2, y0, za), (c + tw / 2, y1, zb))
            parts.append(_part(f'pole_{name}_{seg}', box, _prong_faces(seg), pal, bone='bit'))
    return parts


def _build_claw(c, top, pal):
    return _build_claw_variant(c, top, pal, hub_r=2.0, r0=2.0, r1=3.0)


def _build_claw_b1(c, top, pal):
    """B with outer steel rim removed from the center core (3 x 1 x 3) and prongs pulled in 0.25 px (0.25 px side peek)."""
    return _build_claw_variant(c, top, pal, hub_r=1.5, r0=1.75, r1=2.75)


def _build_claw_b2(c, top, pal, sleeve=False, head_scale=False):
    """B2: dark-bezel spinning core + 4 cardinal prongs flush with the housing (3x3 core + r=1.5..2.5 at 5x5; scaled to
    4x4 core + r=2.0..3.0 with 2.5/2.0 prongs flush with the 6x6 sleeve; corner r 2.83 < 3.0, zero clipping)."""
    if head_scale:
        return _build_claw_variant(c, top, pal, hub_r=2.0, r0=2.0, r1=3.0, hub_bone='bit', sleeve=sleeve, w_coil=2.5, w_prong=2.0)
    return _build_claw_variant(c, top, pal, hub_r=1.5, r0=1.5, r1=2.5, hub_bone='bit', sleeve=sleeve)


def _build_corner(c, top, pal):
    """4 corner prongs (keeping the old 4-corner layout), slimmed to 1.5 x 1.5, shortened to 4 px and angled
    diagonally outward 11 deg from under a 3.5 px housing (7.5 px overall, peeking ~0.5 px past the sides)."""
    t = top - 3.5
    parts = [
        _part('body', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)),
              {f: housing_side for f in ('north', 'south', 'east', 'west')} | {'up': solid('D'), 'down': housing_down}, pal),
        _part('lens', ((c - 0.75, t - 0.5, -0.75), (c + 0.75, t, 0.75)),
              {f: lens_side for f in ('north', 'south', 'east', 'west')} | {'up': solid('E'), 'down': lens_down}, pal),
    ]
    tilt = 11.0
    for sx, nx in ((1, 'a'), (-1, 'b')):
        for sz, nz in ((1, 'a'), (-1, 'b')):
            piv = (c + sx * 1.5, t, sz * 1.5)
            rot = (-sz * tilt, 0.0, sx * tilt)
            xa, xb = sorted((c + sx * 0.75, c + sx * 2.25))
            za, zb = sorted((sz * 0.75, sz * 2.25))
            for seg, y0, y1 in (('wind', t - 1.5, t + 0.5), ('steel', t - 3.0, t - 1.5), ('tip', t - 4.0, t - 3.0)):
                parts.append(_part(f'pole_{nx}{nz}_{seg}', ((xa, y0, za), (xb, y1, zb)),
                                   _prong_faces(seg), pal, bone='bit', rot=rot, origin=piv))
    return parts


def _build_step(c, top, pal):
    """4 corner boxy stepped claws mounted on a recessed 4 x 1 x 4 emitter hub under a 3 px housing: 1.5 x 1.5 copper
    shoulders and steel jaws peek 0.5 px past the housing corners, glowing redstone tips hook 0.5 px inward (7.0 px
    overall, zero rotation)."""
    t = top - 3.0
    parts = [
        _part('body', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)),
              {f: housing_side for f in ('north', 'south', 'east', 'west')} | {'up': solid('D'), 'down': housing_down}, pal),
        _part('hub', ((c - 2.0, t - 1.0, -2.0), (c + 2.0, t, 2.0)),
              {f: lens_side for f in ('north', 'south', 'east', 'west')} | {'up': solid('E'), 'down': lens_down}, pal),
    ]
    for sx, nx in ((1, 'a'), (-1, 'b')):
        for sz, nz in ((1, 'a'), (-1, 'b')):
            segs = (
                ('wind',  t - 1.5, t,       1.5, 3.0),   # copper shoulder peeking 0.5 px past the housing corners
                ('steel', t - 3.0, t - 1.5, 1.5, 3.0),   # steel claw arm proud at r=3.0
                ('tip',   t - 4.0, t - 3.0, 1.0, 2.5),   # glowing redstone tip hooked 0.5 px inward
            )
            for seg, y0, y1, r0, r1 in segs:
                xa, xb = sorted((c + sx * r0, c + sx * r1))
                za, zb = sorted((sz * r0, sz * r1))
                parts.append(_part(f'pole_{nx}{nz}_{seg}', ((xa, y0, za), (xb, y1, zb)),
                                   _prong_faces(seg), pal, bone='bit'))
    return parts


# ---------------------------------------------------------------------------
# 2026-11-22: 2D-texture + 0.5 px cutout outer-layer redesign drafts
# ---------------------------------------------------------------------------

def _pal_2d(glow='dark'):
    """Single-char palette strictly separated by material ramp:
    - Iron armour steel: z s p l e h g w (exact frame_iron_art.PAL)
    - Neutral dark slate / lodestone: x d k m n N (exact frame_iron_art.SLATE + chiseled stone edge)
    - Warm wound copper: u q Q f F (deep groove -> bright copper highlight)
    - Reserved redstone em_core: 0 1 2 3 (dark/idle/lit; dark matches export-tools.py GLOW_MAPS['em_core'])
    - Reserved redstone em_arc:  8 9     (dark/idle/lit; dark matches export-tools.py GLOW_MAPS['em_arc'])
    """
    base = {
        # Iron armour steel ramp
        'z': '22262e', 's': '3c424c', 'p': '58606a', 'l': '757c85',
        'e': '8a9097', 'h': '9fa4a9', 'g': 'cdcfcf', 'w': 'fbf8f0',
        # Neutral dark slate / chiseled lodestone ramp
        'x': '1a1d1f', 'd': '25292c', 'k': '2f3437', 'm': '3b4246', 'n': '4c5559', 'N': '656e73',
        # Warm wound copper ramp
        'u': '4e2816', 'q': '804426', 'Q': 'b86a38', 'f': 'dc8f5c', 'F': 'f2b482',
    }
    if glow == 'lit':
        red = {'0': '7a0600', '1': 'b81206', '2': 'f0200c', '3': 'ff6a4a',
               '8': 'c01206', '9': 'ff2a14'}
    elif glow == 'idle':
        # Powered idle preview: core breathes faintly warm, prong arcs stay off
        red = {'0': '4c100b', '1': '72150d', '2': '981a0f', '3': 'be2d1e',
               '8': '4e1411', '9': '621a14'}
    else:
        red = {'0': '3a0e0c', '1': '4b1310', '2': '5c1813', '3': '701f17',
               '8': '4e1411', '9': '621a14'}
    return {k: _c(v) for k, v in (base | red).items()} | {'.': '.'}


def _paint_2d(faces, pal):
    def fn(f, w, h):
        src = faces[f](w, h) if callable(faces[f]) else faces[f]
        assert len(src) == h and all(len(r) == w for r in src), (f, (w, h), (len(src), [len(r) for r in src]))
        return [[pal[ch] for ch in r] for r in src]
    return fn


def _part_2d(name, box, faces, pal, bone='tool'):
    return dict(drill.part(name, box, _paint_2d(faces, pal), 0), bone=bone)


def _none(w, h):
    return ['.' * w] * h


def _ring_up(lit, top_c, side_c, shade):
    """1-texel hollow top bevel ring for a 6x6 outer cuff (inner 10x10 '.' so zero arm overlap)."""
    def fn(w, h):
        g = [['.'] * w for _ in range(h)]
        for i in range(w):
            g[0][i] = lit if i < w - 1 else top_c
            g[h - 1][i] = side_c if i == 0 else shade
        for j in range(1, h - 1):
            g[j][0] = top_c
            g[j][w - 1] = shade
        return [''.join(r) for r in g]
    return fn


def _orient(rows, flip):
    return [r[::-1] for r in rows] if flip else list(rows)


def _lodestone_lens_8():
    """8x8 chiseled dark-lodestone bezel framing a 4x4 faceted glowing redstone emitter lens."""
    return [
        'xNmmmmNx',
        'Ndkkkkdn'.replace('n', 'd'),
        'mk0110km',
        'mk1231km',
        'mk1321km',
        'mk0110km',
        'mdkkkkdm',
        'xNmmmmNx',
    ]


def _lodestone_lens_6():
    """6x6 chiseled dark-lodestone bezel framing a 4x4 glowing redstone emitter core."""
    return [
        'xNmmNx',
        'N0110N',
        'm1231m',
        'm1321m',
        'N0110N',
        'xNmmNx',
    ]


def _build_2d_shroud_claw(c, top, glow='dark'):
    """Option A (4 cubes, 7.5 px): Pure 2D-layer cutout L-corner claw crown cradling a spinning lodestone/redstone
    emitter core under a 2-layer iron-and-copper sleeve cuff.
    - cuff_inner (5x3.5x5, tool): recessed horizontal copper windings flanking a vertical glowing redstone bus;
    - cuff_outer (6x3.5x6, tool): iron-armour collar with bold 6x3 cutout bay windows + dark magnetic rim;
    - emitter_core (4x2.0x4, bit): spinning chiseled lodestone & redstone field core (8x8 faceted emitter down);
    - claw_shroud (5x4.0x5, bit, 0.5 px proud): single cutout outer shell carved into 4 rigid L-shaped corner claws
      (copper-wound roots -> iron jaws -> tapered redstone arc tips 8/9) framing wide open arches into the core."""
    P = _pal_2d(glow)
    t = top - 3.5

    # 1. Cuff (3.5 px tall -> 7 texel rows): recessed copper stator coils + central redstone energy bus
    in_side = [
        'xddddddddx',
        'dQuF12FuQd',
        'dQfF23FfQd',
        'dquu12uuqd',
        'dQuF23FuQd',
        'dQfF12FfQd',
        'xddddddddx',
    ]
    out_side = [
        'ghhhhhhhhhhe',
        'epllllllllps',
        'epk......kps',
        'epk......kps',
        'epk......kps',
        'esddddddddsz',
        'zzzzzzzzzzzz',
    ]
    cuff_dn = [
        'xxxxxxxxxx',
        'xddddddddx',
        'xdmmmmmmmx'.replace('mx', 'dx'),
        'xdmkkkkmdx',
        'xdmkxxkmdx',
        'xdmkxxkmdx',
        'xdmkkkkmdx',
        'xdmmmmmmmx'.replace('mx', 'dx'),
        'xddddddddx',
        'xxxxxxxxxx',
    ]

    # 2. Spinning 4x2.0x4 core (8x4 sides, 8x8 down): chiseled lodestone bezel + glowing redstone flux ring
    core_side = [
        'xNmmmmNx',
        'd012210d',
        'd123321d',
        'xdddddnx'.replace('n', 'd'),
    ]

    # 3. Spinning 5x4.0x5 cutout L-corner claw shroud (10x8 sides):
    #    Every corner wraps identically (cols 0..k mirror cols 9-k..9), forming 4 solid angle-iron jaws with
    #    wide open arches straight into the spinning core and zero floating slivers!
    claw_side = [
        'xNmmmmmmNx',   # row 0: chiseled magnetic mounting collar locking onto cuff
        'fQu....uQf',   # row 1: copper-wound corner coil shoulders (3 texels per face around each corner)
        'FQq....qQF',   # row 2: bright copper coil wrap
        'uqd....dqu',   # row 3: dark coil clamp collar
        'hl......lh',   # row 4: iron-armour jaw arms (stepped to 2 texels per corner, projecting past core)
        'sp......ps',   # row 5: shaded jaw lower plate
        '89......98',   # row 6: glowing redstone arc electrodes (2 texels per corner face)
        '9........9',   # row 7: sharp 1-texel sparking corner claw tips cradling focal zone
    ]

    return [
        _part_2d('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
            'north': in_side, 'south': in_side, 'east': in_side, 'west': in_side,
            'up': _none, 'down': cuff_dn,
        }, P, 'tool'),
        _part_2d('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': out_side, 'south': out_side, 'east': out_side, 'west': out_side,
            'up': _ring_up('g', 'h', 'e', 's'), 'down': _none,
        }, P, 'tool'),
        _part_2d('emitter_core', ((c - 2.0, t - 2.0, -2.0), (c + 2.0, t, 2.0)), {
            'north': core_side, 'south': core_side, 'east': core_side, 'west': core_side,
            'up': _none, 'down': _lodestone_lens_8(),
        }, P, 'bit'),
        _part_2d('claw_shroud', ((c - 2.5, t - 4.0, -2.5), (c + 2.5, t, 2.5)), {
            'north': claw_side, 'south': claw_side, 'east': claw_side, 'west': claw_side,
            'up': _none, 'down': _none,
        }, P, 'bit'),
    ]


def _build_2d_gravity_gun(c, top, glow='dark'):
    """Option B (7 cubes, 7.5 px): Half-Life 2 Gravity Gun evolution in 2D-layer language.
    - cuff_inner + cuff_outer (6x3.5x6, tool): dark magnetized gunmetal & steel-trimmed housing with recessed copper
      stator windings above and glowing redstone capacitor ports below;
    - emitter_core (4x1.5x4, bit): spinning recessed chiseled lodestone + redstone emitter lens;
    - 4 unified 1-cube cardinal prongs (2.0 x 4.0 x 1.0 at r=2.0..3.0, flush with cuff, bit): copper-wound root,
      riveted iron jaw spine, and tall inner-facing glowing redstone arc electrode rails (8/9) facing the core."""
    P = _pal_2d(glow)
    t = top - 3.5

    # 1. Cuff (3.5 px tall -> 7 rows): upper copper stator bay + lower redstone core port
    in_side = [
        'xddddddddx',
        'duQfFFfQud',
        'dqQffffQqd',
        'xddddddddx',
        'dk012210kd',
        'dk123321kd',
        'xxxxxxxxxx',
    ]
    out_side = [
        'NnnnnnnnnnNd',
        'nmk......kmd',
        'nmk......kmd',
        'nNmmmmmmmmNd',
        'dkd......dkd',
        'dkd......dkd',
        'xxxxxxxxxxxx',
    ]
    cuff_dn = ['x' * 10] + ['x' + 'd' * 8 + 'x'] * 8 + ['x' * 10]

    # 2. Spinning 4x1.5x4 emitter core (8x3 sides, 8x8 down)
    core_side = [
        'xNmmmmNx',
        'd012210d',
        'xdddddnx'.replace('n', 'd'),
    ]

    parts = [
        _part_2d('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
            'north': in_side, 'south': in_side, 'east': in_side, 'west': in_side,
            'up': _none, 'down': cuff_dn,
        }, P, 'tool'),
        _part_2d('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': out_side, 'south': out_side, 'east': out_side, 'west': out_side,
            'up': _ring_up('N', 'n', 'm', 'd'), 'down': _none,
        }, P, 'tool'),
        _part_2d('emitter_core', ((c - 2.0, t - 1.5, -2.0), (c + 2.0, t, 2.0)), {
            'north': core_side, 'south': core_side, 'east': core_side, 'west': core_side,
            'up': _none, 'down': _lodestone_lens_8(),
        }, P, 'bit'),
    ]

    # 3. Four unified single-cube cardinal prongs (tangential 2.0 px = 4 texels, radial 1.0 px = 2 texels, height 4.0 = 8)
    pr_outer = [
        'xNmx'.replace('xNmx', 'dNmd'),   # row 0: dark magnetic mounting clamp
        'qFFq',                           # row 1: wound copper coil turn 1
        'uQQu',                           # row 2: dark coil wire groove
        'qffq',                           # row 3: wound copper coil turn 2
        'glle',                           # row 4: iron jaw shoulder w/ rivet highlight
        'spps',                           # row 5: iron jaw lower bevel
        'd88d',                           # row 6: framed redstone arc tip base
        'x99x',                           # row 7: sparking redstone electrode tip
    ]
    pr_inner = [
        'dddd',
        'qFFq',
        'uQQu',
        'qffq',
        'd88d',                           # rows 4..7: tall inner-facing arc rail aimed across the emitter core!
        'd89d',
        '8998',
        '9999',
    ]
    # Canonical side face (2x8): col 0 = OUTER (away from core), col 1 = INNER (toward core)
    pr_side_oi = [
        'dm',
        'fF',
        'uQ',
        'Qf',
        'e8',
        'p8',
        'd9',
        '89',
    ]
    pr_up = ['dd', 'dd', 'dd', 'dd']  # 2x4 or 4x2 set per axis below

    for name, axis, s in (('e', 'x', 1), ('w', 'x', -1), ('s', 'z', 1), ('n', 'z', -1)):
        if axis == 'x':
            xa, xb = sorted((c + s * 2.0, c + s * 3.0))
            box = ((xa, t - 4.0, -1.0), (xb, t, 1.0))
            # north: col 0=+x, col 1=-x -> outer-first when s=+1, inner-first when s=-1
            # south: col 0=-x, col 1=+x -> outer-first when s=-1, inner-first when s=+1
            dn_row = '98' if s > 0 else '89'   # down col 0=-x (inner if s>0), col 1=+x (outer if s>0)
            faces = {
                'east': pr_outer if s > 0 else pr_inner,
                'west': pr_inner if s > 0 else pr_outer,
                'north': _orient(pr_side_oi, s < 0),
                'south': _orient(pr_side_oi, s > 0),
                'up': ['dd'] * 4,
                'down': ['d' + dn_row[1] if s < 0 else dn_row[0] + 'd', dn_row, dn_row,
                         'd' + dn_row[1] if s < 0 else dn_row[0] + 'd'],
            }
        else:
            za, zb = sorted((s * 2.0, s * 3.0))
            box = ((c - 1.0, t - 4.0, za), (c + 1.0, t, zb))
            # east: col 0=+z, col 1=-z -> outer-first when s=+1, inner-first when s=-1
            # west: col 0=-z, col 1=+z -> outer-first when s=-1, inner-first when s=+1
            # down: row 0=+z, row 1=-z -> inner row is 1 when s>0, 0 when s<0
            dn_inner = 'd99d'
            dn_outer = 'd88d'
            faces = {
                'south': pr_outer if s > 0 else pr_inner,
                'north': pr_inner if s > 0 else pr_outer,
                'east': _orient(pr_side_oi, s < 0),
                'west': _orient(pr_side_oi, s > 0),
                'up': ['dddd'] * 2,
                'down': [dn_outer, dn_inner] if s > 0 else [dn_inner, dn_outer],
            }
        parts.append(_part_2d(f'prong_{name}', box, faces, P, 'bit'))
    return parts


def _build_2d_tesla_cage(c, top, glow='dark'):
    """Option C (4 cubes, 7.5 px): Industrial Electromagnet / Tesla Field Projector.
    - cuff_inner + cuff_outer (6x3.5x6, tool): iron-armour sleeve with vertical cutout bays exposing vertical copper
      busbars flanking a glowing redstone power slot;
    - coil_core (3.0 x 3.5 x 3.0, bit): central spinning copper-wound electromagnet rod with glowing redstone flux
      rings and a 6x6 faceted redstone emitter dish on down;
    - ring_cage (5.0 x 4.0 x 5.0, bit): single 2D cutout outer focusing cage (upper steel/slate clamp ring + wide
      open see-through middle bay + front steel/copper accelerator ring + 4 projecting redstone arc tips 8/9)."""
    P = _pal_2d(glow)
    t = top - 3.5

    # 1. Cuff (3.5 px tall -> 7 rows): vertical copper busbars flanking central redstone pulse slot
    in_side = [
        'xddddddddx',
        'dqFf12fFqd',
        'dqFQ23QFqd',
        'dqFf23fFqd',
        'dqFQ12QFqd',
        'dqFf12fFqd',
        'xddddddddx',
    ]
    out_side = [
        'ghhhhhhhhhhe',
        'epd......dpe',
        'epd......dpe',
        'epd..xx..dpe',   # twin vertical side bays? No, clean centered brace dividing upper & lower core read
        'epd......dpe',
        'esddddddddsz',
        'zzzzzzzzzzzz',
    ]
    # Make cuff_outer super clean: one crisp iron collar w/ flanking copper-busbar + center redstone cutout
    out_side = [
        'ghhhhhhhhhhe',
        'epllllllllps',
        'epd......dpe',
        'epd......dpe',
        'epd......dpe',
        'eslhhhhhhlzs'.replace('zs', 'sz'),
        'zzzzzzzzzzzz',
    ]
    cuff_dn = ['x' * 10] + ['x' + 'd' * 8 + 'x'] * 8 + ['x' * 10]

    # 2. Central spinning electromagnet coil column (3.0 x 3.5 x 3.0 -> 6x7 sides, 6x6 down)
    core_side = [
        'qFffFq',   # row 0: upper copper coil
        'uQQQQu',   # row 1: dark coil groove
        '012210',   # row 2: glowing redstone flux band
        'qFffFq',   # row 3: mid copper coil
        'uQQQQu',   # row 4: dark coil groove
        '123321',   # row 5: intense lower redstone flux band
        'xNmmNx',   # row 6: lodestone dish rim
    ]

    # 3. Single 5.0 x 4.0 x 5.0 2D cutout outer accelerator cage (10x8 sides, 1.0 px open air gap around core!)
    cage_side = [
        'dm......md',   # row 0: 4 corner struts hanging from cuff
        'ghhhhhhhhe',   # row 1: upper steel focusing ring (continuous all 4 sides)
        'spppppppps',   # row 2: dark steel ring underside
        'dk......kd',   # row 3: wide open see-through bay exposing spinning copper/redstone core!
        'dk......kd',   # row 4: wide open bay
        'qFllllllFq',   # row 5: front copper-cornered steel accelerator crown ring
        '89spppps98',   # row 6: corner redstone arc emitters integrated into front ring
        '9........9',   # row 7: 4 corner redstone arc tips extending 0.5 px past central dish
    ]

    return [
        _part_2d('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
            'north': in_side, 'south': in_side, 'east': in_side, 'west': in_side,
            'up': _none, 'down': cuff_dn,
        }, P, 'tool'),
        _part_2d('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': out_side, 'south': out_side, 'east': out_side, 'west': out_side,
            'up': _ring_up('g', 'h', 'e', 's'), 'down': _none,
        }, P, 'tool'),
        _part_2d('coil_core', ((c - 1.5, t - 3.5, -1.5), (c + 1.5, t, 1.5)), {
            'north': core_side, 'south': core_side, 'east': core_side, 'west': core_side,
            'up': _none, 'down': _lodestone_lens_6(),
        }, P, 'bit'),
        _part_2d('ring_cage', ((c - 2.5, t - 4.0, -2.5), (c + 2.5, t, 2.5)), {
            'north': cage_side, 'south': cage_side, 'east': cage_side, 'west': cage_side,
            'up': _none, 'down': _none,
        }, P, 'bit'),
    ]


def _build_2d_lodestone_dish(c, top, glow='dark'):
    """Option D (7 cubes, 7.0 px): Signature Copper + Chiseled Lodestone Projector with 4 Corner Claws.
    Leans directly into the crafting recipe (Lodestone + Copper + Redstone + Iron) for an unmistakable warm-copper &
    chiseled-slate palette distinct from every other tool; corner claws leave wide 3 px cardinal sightlines straight
    into the spinning glowing redstone dish!
    - cuff_inner + cuff_outer (6x3.5x6, tool): burnished copper rimmed + chiseled dark lodestone cuff with geometric
      cutout apertures showing glowing redstone circuit traces (clears Steve's hand at raw y=14 by 0.5 px);
    - dish_core (3.0 x 1.5 x 3.0, bit): spinning chiseled lodestone emitter dish (6x6 faceted redstone lens);
    - 4 compact corner claws (1.5 x 3.5 x 1.5 at |x|,|z| in [1.5, 3.0], zero overlap w/ dish_core, bit): copper coil
      root -> chiseled lodestone jaw -> inner-corner glowing redstone arc electrodes (8/9)."""
    P = _pal_2d(glow)
    t = top - 3.5

    # 1. Compact 3.5 px cuff (7 rows): glowing redstone lodestone circuit inside + copper/lodestone outer armor
    in_side = [
        'xddddddddx',
        'dk012210kd',
        'dk123321kd',
        'dk123321kd',
        'dk012210kd',
        'xddddddddx',
        'xxxxxxxxxx',
    ]
    out_side = [
        'FffffffffffQ',         # row 0: burnished copper top rim (12 chars)
        'qQNNNNNNNNQq',         # row 1: chiseled lodestone upper frame
        'qNm......mNq',         # row 2: wide geometric lodestone aperture exposing redstone core
        'qNm......mNq',         # row 3: aperture
        'qQmmmmmmmmQq',         # row 4: chiseled lower bevel
        'qQffffffffQq',         # row 5: burnished copper lower collar band
        'uqqqqqqqqqqu',         # row 6: dark copper lower lip
    ]
    cuff_dn = ['x' * 10] + ['x' + 'd' * 8 + 'x'] * 8 + ['x' * 10]

    # 2. Spinning 3.0 x 1.5 x 3.0 lodestone dish core (6x3 sides, 6x6 down)
    dish_side = [
        'xNmmNx',
        'd1221d',
        'xddddx',
    ]

    parts = [
        _part_2d('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
            'north': in_side, 'south': in_side, 'east': in_side, 'west': in_side,
            'up': _none, 'down': cuff_dn,
        }, P, 'tool'),
        _part_2d('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': out_side, 'south': out_side, 'east': out_side, 'west': out_side,
            'up': _ring_up('F', 'f', 'Q', 'q'), 'down': _none,
        }, P, 'tool'),
        _part_2d('dish_core', ((c - 1.5, t - 1.5, -1.5), (c + 1.5, t, 1.5)), {
            'north': dish_side, 'south': dish_side, 'east': dish_side, 'west': dish_side,
            'up': _none, 'down': _lodestone_lens_6(),
        }, P, 'bit'),
    ]

    # 3. Four 1.5 x 3.5 x 1.5 corner claws (3x7 sides, 3x3 up/down).
    # Canonical face (3x7): col 0 = OUTER edge, col 2 = INNER edge (toward the core axis)!
    claw_outer_oi = [
        'qFf',   # row 0: copper coil shoulder
        'uQQ',   # row 1: dark coil groove
        'qFf',   # row 2: copper coil turn 2
        'Nmm',   # row 3: chiseled lodestone jaw top
        'mkk',   # row 4: lodestone jaw lower
        'd88',   # row 5: redstone electrode collar (biased toward inner corner)
        'x89',   # row 6: sparking redstone tip on inner corner
    ]
    claw_inner_oi = [
        'qFf',
        'uQQ',
        'qFf',
        'dmk',
        'd88',   # rows 4..6: inner-facing redstone arc electrode strip facing the dish!
        '899',
        '899',
    ]

    for sx, nx in ((1, 'a'), (-1, 'b')):
        for sz, nz in ((1, 'a'), (-1, 'b')):
            xa, xb = sorted((c + sx * 1.5, c + sx * 3.0))
            za, zb = sorted((sz * 1.5, sz * 3.0))
            box = ((xa, t - 3.5, za), (xb, t, zb))
            # Outer vs inner faces per corner (sx, sz):
            # - X faces: east is outer if sx>0 else inner; west is inner if sx>0 else outer
            # - Z faces: south is outer if sz>0 else inner; north is inner if sz>0 else outer
            # Inner-edge direction per face (canonical has inner at col 2 = right):
            # - north (col0=+x, col2=-x): inner is -x when sx>0 (col 2 -> flip=False), +x when sx<0 (col 0 -> flip=True)
            # - south (col0=-x, col2=+x): inner is -x when sx>0 (col 0 -> flip=True),  +x when sx<0 (col 2 -> flip=False)
            # - east  (col0=+z, col2=-z): inner is -z when sz>0 (col 2 -> flip=False), +z when sz<0 (col 0 -> flip=True)
            # - west  (col0=-z, col2=+z): inner is -z when sz>0 (col 0 -> flip=True),  +z when sz<0 (col 2 -> flip=False)
            f_north = _orient(claw_outer_oi if sz < 0 else claw_inner_oi, sx < 0)
            f_south = _orient(claw_outer_oi if sz > 0 else claw_inner_oi, sx > 0)
            f_east  = _orient(claw_outer_oi if sx > 0 else claw_inner_oi, sz < 0)
            f_west  = _orient(claw_outer_oi if sx < 0 else claw_inner_oi, sz > 0)
            # Down face (3x3, col 0=-x..col 2=+x, row 0=+z..row 2=-z):
            # Put hot '9' at the inner corner (towards x=c, z=0), '8' flanking it, 'd' on outer corner!
            dn = [['d'] * 3 for _ in range(3)]
            ix = 0 if sx > 0 else 2
            iz = 2 if sz > 0 else 0
            for j in range(3):
                for i in range(3):
                    dist = abs(i - ix) + abs(j - iz)
                    dn[j][i] = '9' if dist <= 1 else ('8' if dist == 2 else 'd')
            parts.append(_part_2d(f'claw_{nx}{nz}', box, {
                'north': f_north, 'south': f_south, 'east': f_east, 'west': f_west,
                'up': ['ddd'] * 3, 'down': [''.join(r) for r in dn],
            }, P, 'bit'))
    return parts


BUILDERS = {
    'legacy': _legacy_build,
    'splay': _build_splay,
    'claw': _build_claw,
    'claw_b1': _build_claw_b1,
    'claw_b2': _build_claw_b2,
    'corner': _build_corner,
    'step': _build_step,
}

BUILDERS_2D = {
    '2d_shroud_claw': _build_2d_shroud_claw,
    '2d_gravity_gun': _build_2d_gravity_gun,
    '2d_tesla_cage': _build_2d_tesla_cage,
    '2d_lodestone_dish': _build_2d_lodestone_dish,
}


def build(c, top, lamp='dark', kind='2d_gravity_gun', length=0.0, glow='dark', sleeve=False, head_scale=False):
    """The EM projector's parts on an arm centred at x c whose socket is at y top: the housing (bone 'tool') and the
    poles (bone 'bit'). `lamp` and `length` are the tools' common signature."""
    if kind in BUILDERS_2D:
        return BUILDERS_2D[kind](c, top, glow=glow)
    assert kind in BUILDERS, kind
    if kind == 'claw_b2':
        return _build_claw_b2(c, top, _pal(glow), sleeve=sleeve, head_scale=head_scale)
    return BUILDERS[kind](c, top, _pal(glow))
