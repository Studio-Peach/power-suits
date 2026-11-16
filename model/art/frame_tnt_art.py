"""The TNT launcher for the frame (frame_model.py, TOOL=tnt): the sixth power tool brought over from the big suit.

2026-11-15 (user: use the old designs). The big suit's (picked 2026-10-25, round 5 of .scratch/tnt/): a revolver drum
after Team Fortress 2's grenade launcher, all dark iron: four chambers a quarter turn apart round the tool's vertical
axis, a red TNT round showing in each, a square barrel under the one that faces front (-z). The drum turns as the
rounds are loaded (ToolRotors: bone tnt_launcher_drum, about y).
On the frame, in the tools' slot (frame_gun_art.py): a 5 x 1 x 5 housing in the fist's place, the drum under it (a cross
of two 3 px slabs inside the arm's 5 x 5 footprint, the chambers' ends 3 x 3), the barrel 3 x 4 x 3 hanging at the front
under the drum, a muzzle plate 4 x 1 x 4: 9 px under the socket, the chaingun's length. Flat and painted.

Coordinates raw, right arm (+x; the left mirrors), centred on the arm's axis (x c, z 0). Faces as frame_drill_art.py.
"""
import frame_drill_art as drill

_c = drill._c
# the chaingun's warm black ramp (frame_gun_art.METAL), TNT (the big suit's: shade, red, lit, label, letters, tan end)
P = {k: _c(v) for k, v in dict(A='6a7077', B='454a50', C='2e3237', D='202327', E='131517', g='9fa4a9',
                              i='6e1e14', j='a3301e', l='d2442a', m='e6e2d6', n='3a2f2a', s='a69c8c', x='5a5248').items()} | {'.': '.'}


def _paint(faces):
    return lambda f, w, h: [[P[ch] for ch in r] for r in (faces[f](w, h) if callable(faces[f]) else faces[f])]


def plate(w, h):   # the housing's side: a lit top edge over the body, a bolt, the shade at the foot
    return ['A' * (w - 1) + 'B'] + ['B' + 'C' * (w - 2) + 'D'] * (h - 2) + ['D' * w]


def solid(ch): return lambda w, h: [ch * w] * h


def slab_side(w, h):    # a drum slab's long side: lit top, the iron body, a seam row, shade under
    return ['B' * w] + ['C' * w] * (h - 2) + ['D' * w]


def round_end(w, h):
    """A chamber's end (3 x 3 px = 6 x 6 texels): the TNT round seen end on: a dark rim, red, a white label band across
    its middle, the fuse's hole at the centre."""
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


def build(c, top, lamp='dark', kind='A', length=0.0):
    """The TNT launcher's parts on an arm centred at x c whose socket is at y top: the housing and the barrel (bone
    'tool'), the drum (bone 'bit': it turns). `lamp` and `length` are the tools' common signature."""
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces)), bone=bone)
    housing = {f: plate for f in ('north', 'south', 'east', 'west')} | {'up': solid('D'), 'down': solid('E')}
    parts = [part('housing', ((c - 2.5, top - 1, -2.5), (c + 2.5, top, 2.5)), housing)]
    y0, y1 = top - 4, top - 1                                        # the drum's 3 px
    # two slabs crossing: x-long (5 x 3) and z-long (3 x 5), the chambers' ends at the four tips
    ends = lambda: {'up': solid('D'), 'down': solid('E')}
    parts.append(part('drum_x', ((c - 2.5, y0, -1.5), (c + 2.5, y1, 1.5)),
                      {'north': slab_side, 'south': slab_side, 'east': round_end, 'west': round_end} | ends(), 'bit'))
    parts.append(part('drum_z', ((c - 1.5, y0, -2.5), (c + 1.5, y1, 2.5)),
                      {'east': slab_side, 'west': slab_side, 'north': round_end, 'south': round_end} | ends(), 'bit'))
    # the barrel under the front chamber, a square tube with a muzzle plate; the bore dark
    parts.append(part('barrel', ((c - 1.5, y0 - 4, -2.5), (c + 1.5, y0, 0.5)),
                      {f: plate for f in ('north', 'south', 'east', 'west')} | {'up': solid('D'), 'down': solid('E')}))
    ring = lambda w, h: ['A' * (w - 1) + 'B'] + ['B' * (w - 1) + 'C'] * (h - 1)
    bore = lambda w, h: [''.join('B' if i in (0, w - 1) or j in (0, h - 1) else 'E' for i in range(w)) for j in range(h)]
    parts.append(part('muzzle', ((c - 2, y0 - 5, -3), (c + 2, y0 - 4, 1)),
                      {f: ring for f in ('north', 'south', 'east', 'west')} | {'up': solid('C'), 'down': bore}))
    return parts
