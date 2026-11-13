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


def build(c, top, lamp='red', kind='A', art='B'):
    """The chainsaw's parts on an arm centred at x c (right side) whose socket is at y top: the body (the drill's)
    and the bar under it; bone 'tool' still, 'bit' the chain (it runs)."""
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    t = top - 4                                         # the body's bottom: the bar hangs from it
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces) if isinstance(faces, dict) else faces), bone=bone)
    parts = [part('body', sq(5, t, top), drill.fist(art, lamp))]
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
