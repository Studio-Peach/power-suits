"""The engine's paint for the frame (frame_model.py, draft knob ENGINE): every part's faces as letter grids.

The firebox engine (2026-11-05, user: the engines were backpacks; with the redesign, the furnace and exhausts stay on
the back and a core goes in front, pipes running through the sides; the armour is fitted to it later): the core's
porthole, the copper pipes (frame_model.py has the shapes and picks). The back is the radial firebox,
frame_radial_art.py (2026-11-07; the twin-cylinder pack painted here before it is in git history, commit 7a24d3f).

Letters are frame_model.py's PAL (uppercase: gunmetal N O X, copper Q R, brass Y Z, steel W V U G) and the iron
armour's (lowercase steel ramp, frame_iron_art.py), plus the fire, painted LIT here (F yellow-white, I orange,
J red: the old firebox's glow colours) so the review shows a burning engine; in game they'd be the reserved dark
colours and the glowmask (tools/make-glowmasks.py).
Faces as frame_model.py's: north / south as seen from the front / back, east back -> front, west front -> back; up
rows front -> back.
"""


def _box(front, back, side, up, down, side_w=None):
    return {'north': front, 'south': back, 'east': side, 'west': side_w or side, 'up': up, 'down': down}


def porthole(W=8, H=8, corner='l'):
    """The core's face (2 texels per px over its 4 x 4): a round porthole, a brass ring, the fire behind glass, the
    corners in the housing's colour (corner)."""
    front = ['ccYYYYcc',
             'cYXJJXYc',
             'YXJIIJXY',
             'YJIFFIJY',
             'YJIFFIJY',
             'YXIFFIXY',
             'cZXXXXZc',
             'ccZZZZcc']
    front = [r.replace('c', corner) for r in front]
    rim = {'.': 'Z', 'Q': 'R'}.get(corner, corner)   # its sides (copper: the pipes' shaded side)
    return _box(front, ['X' * W] * H, [rim] * H, [rim * W], [rim * W])


def pipe_box(W, H, D):
    """A copper pipe box W x H x D texels (2 per px), running any way: a face longer than tall lit along its top
    row, a taller one along its left column."""
    face = lambda w, h: [('Q' if j == 0 else 'R') * w for j in range(h)] if h <= w else ['Q' + 'R' * (w - 1)] * h
    return _box(face(W, H), face(W, H), face(D, H), ['Q' * W] * D, ['R' * W] * D)
