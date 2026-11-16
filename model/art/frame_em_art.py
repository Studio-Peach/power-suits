"""The EM projector for the frame (frame_model.py, TOOL=em): the seventh power tool brought over from the big suit.

2026-11-15 (user: use the old designs). The big suit's (em_redstone_art.py, 2026-10-13): a redstone electromagnet: a
housing with a dark iron collar and redstone vent slits, a steel bezel round a redstone lens on its face, four short
steel pole pieces straight out of the housing, copper windings round each, redstone tips that spark while the beam runs.
On the frame, in the tools' slot (frame_gun_art.py): a 5 x 4 x 5 housing in the fist's place (the vents a dark collar
row on each side, red), under it the bezel and lens, and the four poles at the footprint's corners, 2 x 2 px: copper
winding 2 px at the top, 3 px of steel, a 1 px redstone tip: 10 px under the socket. Flat and painted.

The lens, the vents and the tips are painted in reserved dark reds (the big suit's, em_redstone_art.py GLOW), lit by
glowmasks (tools/export-frame.py TOOL_GLOW em_core / em_arc: ToolLight.EM_CORE / EM_ARC).

Coordinates raw, right arm (+x; the left mirrors), centred on the arm's axis (x c, z 0). Faces as frame_drill_art.py.
"""
import frame_drill_art as drill

_c = drill._c
# steel (frame_iron_art.PAL's ramp), copper, slate, the reserved reds: lens / vents R0-R3, tips T1-T2 (dark: dead redstone)
RES = dict(R0='3a0e0c', R1='4b1310', R2='5c1813', R3='701f17', T1='4e1411', T2='621a14')
P = {k: _c(v) for k, v in dict(A='9fa4a9', B='757c85', C='58606a', D='3c424c', E='22262e', g='cdcfcf',
                              f='e09868', Q='c07440', R='804426', d='25292c', k='2f3437', m='3b4246').items()} | \
    {k: _c(v) for k, v in RES.items()} | {'.': '.'}


def _paint(faces):
    return lambda f, w, h: [[P[ch] for ch in r] for r in (faces[f](w, h) if callable(faces[f]) else faces[f])]


def solid(ch): return lambda w, h: [ch * w] * h


def pole(seg):
    def f(w, h):
        if seg == 'wind': return ['f' * w] + ['Q' * (w - 1) + 'R'] * (h - 2) + ['R' * w]       # copper, a coil's rows
        if seg == 'steel': return ['A' * (w - 1) + 'B'] + ['B' * (w - 1) + 'C'] * (h - 1)
        return [['T1'] * w] + [['T2'] * w] * (h - 1)                                            # the redstone tip
    return f


def build(c, top, lamp='dark', kind='A', length=0.0):
    """The EM projector's parts on an arm centred at x c whose socket is at y top: the housing (bone 'tool'), the poles
    (bone 'bit', which does nothing). `lamp`, `kind` and `length` are the tools' common signature."""
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces), 0), bone=bone)
    t = top - 4

    def side(w, h):
        """The housing's side, 10 x 8 texels: a lit top edge with two bolts, plain steel, then the collar: a dark iron row
        over a row of redstone vent slits (R1, every other texel), a shade foot."""
        rows = ['A' * (w - 1) + 'B', 'B' + 'g' + 'C' * (w - 4) + 'g' + 'D'] + ['B' + 'C' * (w - 2) + 'D'] * (h - 5)
        rows = [list(r) for r in rows]
        rows += [['d'] + ['k'] * (w - 2) + ['d']]
        rows += [['d'] + ['R1' if i % 2 == 0 else 'k' for i in range(1, w - 1)] + ['d']]
        rows += [['E'] * w]
        return rows

    parts = [part('body', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)),
                  {f: side for f in ('north', 'south', 'east', 'west')} | {'up': solid('D'), 'down': solid('E')})]
    # under the housing: the bezel (steel) round the lens (the reserved reds: dark idle), the poles round it
    def bezel(w, h):   # 10 x 10: a steel rim, a dark ring, the lens 4 x 4 in the middle
        g = [['C'] * w for _ in range(h)]
        for j in range(h):
            for i in range(w):
                if 2 <= i < w - 2 and 2 <= j < h - 2: g[j][i] = 'E'
                if 3 <= i < w - 3 and 3 <= j < h - 3: g[j][i] = ['R0', 'R1', 'R2', 'R3'][(i + j) % 4]
        return g
    parts[0]['faces']['down'] = _paint({'down': bezel})('down', 10, 10)
    for sx, name_x in ((1, 'a'), (-1, 'b')):
        for sz, name_z in ((1, 'a'), (-1, 'b')):
            xa, xb = sorted((c + sx * 0.5, c + sx * 2.5))
            za, zb = sorted((sz * 0.5, sz * 2.5))
            y = t
            for seg, h in (('wind', 2), ('steel', 3), ('tip', 1)):
                faces = {f: pole(seg) for f in ('north', 'south', 'east', 'west')} | \
                        {'up': solid('D') if seg != 'tip' else solid('R'), 'down': solid('E') if seg != 'tip' else solid('T2')}
                if seg == 'tip': faces['down'] = pole('tip')
                parts.append(part(f'pole_{name_x}{name_z}_{seg}', ((xa, y - h, za), (xb, y, zb)), faces, 'bit'))
                y -= h
    return parts
