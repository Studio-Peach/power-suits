"""The EM projector for the frame (frame_model.py, TOOL=em): the seventh power tool brought over from the big suit.

2026-11-15 (user: use the old designs): 'legacy' — 4 px housing + four straight 2 x 2 x 6 px corner poles (10 px total).
2026-11-20 rework (user: "Currently its too long and too straight, maybe the prongs could be shorted and peek out the
sides a little"): shorter (~7.0-7.5 px overall, shorter than the 9 px guns/drill/TNT), slimmer prongs that peek ~0.5 px
past the 5 x 5 housing sides (staying within +-3.0 px so Steve clears by 0.5 px and Alex sits flush, like TNT wide).

Drafts (EM knob; picked 'claw_b2' on 2026-11-20, spinning via ToolRotors):
- claw_b2: (default) 3 px housing with redstone vents + spinning 3 x 1 x 3 dark-bezel redstone core and 4 cardinal
           (N/S/E/W) copper-wound prongs with aligned glowing redstone tips flush at r=1.5..2.5 (7.0 px overall; core
           and prongs share bone 'bit' / em_projector_poles so the assembly spins cleanly with zero clipping);
- claw_b1: 3 x 1 x 3 core with prongs at r=1.75..2.75 (0.25 px side peek, 7.0 px overall);
- claw   : 4 x 1 x 4 core with steel rim and prongs at r=2.0..3.0 (0.5 px side peek, 7.0 px overall);
- splay  : 4 cardinal prongs angled outward 13 deg from under a 3.5 px housing around a 1.5 x 0.5 x 1.5 lens (7.5 px);
- corner : 4 corner prongs angled diagonally outward 11 deg from under a 3.5 px housing (7.5 px);
- step   : 4 corner boxy stepped claws on a 4 x 1 x 4 hub (7.0 px);
- legacy : the 2026-11-15 straight 10 px version.

EM_GLOW: 'dark' (default, reserved dark redstone colours for export-frame.py em_core / em_arc glowmasks) | 'lit'
(bright glowing redstone preview for review sheets).

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
                # 8x8 emitter hub: steel rim (d=0), dark bezel (d=1), redstone lens (d>=2) with bright core (d>=3)
                if d == 0:
                    g[j][i] = 'C'
                elif d == 1:
                    g[j][i] = 'E'
                elif d >= 3:
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


def _build_claw_variant(c, top, pal, hub_r=2.0, r0=2.0, r1=3.0, hub_bone='tool', sleeve=False):
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
            ('wind',  t - 1.5, t,       r0, r1, 2.0),   # copper coil collar
            ('steel', t - 3.0, t - 1.5, r0, r1, 1.5),   # steel prong body
            ('tip',   t - 4.0, t - 3.0, r0, r1, 1.5),   # glowing redstone tip aligned with prong body
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


def _build_claw_b2(c, top, pal, sleeve=False):
    """B with outer steel rim removed from the center core (3 x 1 x 3) and prongs pulled in 0.5 px (flush with 5x5 arm,
    snug on core). The 3 x 1 x 3 hub sits on 'bit' (em_projector_poles) so core and prongs spin together cleanly with
    zero clipping at any angle (hub corner r 2.12 < 2.5)."""
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


BUILDERS = {
    'legacy': _legacy_build,
    'splay': _build_splay,
    'claw': _build_claw,
    'claw_b1': _build_claw_b1,
    'claw_b2': _build_claw_b2,
    'corner': _build_corner,
    'step': _build_step,
}


def build(c, top, lamp='dark', kind='claw_b2', length=0.0, glow='dark', sleeve=False):
    """The EM projector's parts on an arm centred at x c whose socket is at y top: the housing (bone 'tool') and the
    poles (bone 'bit'). `lamp` and `length` are the tools' common signature."""
    assert kind in BUILDERS, kind
    if kind == 'claw_b2':
        return _build_claw_b2(c, top, _pal(glow), sleeve=sleeve)
    return BUILDERS[kind](c, top, _pal(glow))
