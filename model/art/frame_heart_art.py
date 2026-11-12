"""The heart engine's front: the frame's engine (frame_model.py, ENGINE=heart) after Shiro Tomoe's in Tailenders
(2026-11-11, user: his heart replaced by an engine, "exhaust in the back and an iron ball of sorts in the front").
Its back is the twin-cylinder pack with the old suit's exhausts (frame_engine_art.back_pistons_sized,
frame_model.py).

Picks so far (2026-11-11, user): copper hoses over the shoulders and a second pair under the chest piece; then "too
3D, they stand out in a bad way" (rotated hoses, collars and fittings 1-2.5 px proud round an iron ball, all in commit
f688cc9 and its follow-ups), so it is flat now, as the frame (simple boxes, detail in the texture); then the ball back
into the firebox's core (no white bolt; the octagon ball is in git history):
- 2D the whole way (2026-11-11, user: the pipes flat all round, the core too): thin plates (0.5 px) with the hoses
  and the core painted on, see-through but for them (cutout texels), a dark outline round everything (the show's
  heavy ink): the front harness (the core's porthole in the chest slot, x +-2, raw y 21-25; the four hoses out of its
  corners), a strip over each shoulder, one along each side of the waist (the 1 px gap under the arm) and the back
  harness, down to the pack's copper inlets;
- the core's fire (and the pack's fire door) light up and die with the engine: painted in the reserved coal colours
  of tools/make-glowmasks.py (dead coals in the texture, the fire mask lit by SuitGlowLayer by the burn state), so
  the frame's renderer, when it is in game, drives them as the suit's firebox (frame_model.py FIRE=lit shows them
  burning for the review, FIRE=dark as an engine that is off).
No face of a plate lies in another's plane where they overlap (no z-fighting).

Coordinates raw (frame_model.py adds FY), right side +x, the front -z. Art 2 texels per px (K), letters from
frame_model.PAL / the iron ramp (lowercase, frame_iron_art.py) plus EXTRA. Faces as frame_model.py's: north / south
as seen from the front / back, east back -> front, west front -> back, up rows front -> back.
"""
import math
from frame_radial_art import part, grid, K
import frame_engine_art as engine_art

EXTRA = {'f': (0xe0, 0x98, 0x68)}         # copper, lit (Q / R are its mid and shade)
HOSE = ('f', 'Q', 'R')
HZ = (-3.5, -3)                           # the harness's depth: 0.5 px on the chest's front


# the hoses' centre lines (right side; the left mirrors it), all 1.5 px round (HR) with a 1-texel ink outline
HR, OUTLINE = 0.75, 0.5
def top(cx):   # front: out of the core's top corner up to the shoulder strip, 0.75 px in from the arm (CHEST_X, cx)
    return [(1.75, 23.5), (cx - HR, 25.0), (cx - HR, 27)]
def low(y, side_x):                                   # front: out of its bottom corner to the waist (y .. y + 1.5)
    return [(1.75, 22.0), (4.5, y + HR), (side_x, y + HR)]


def _seg(p, a, b):
    """Distance from p to segment ab, and p's side of it (negative above / left of it: the lit side)."""
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    qx, qy = ax + t * dx, ay + t * dy
    n = (-dy, dx) if dx >= 0 else (dy, -dx)                                  # the normal pointing up
    side = -((px - qx) * n[0] + (py - qy) * n[1]) / math.hypot(*n)
    return math.hypot(px - qx, py - qy), side


def hoses_at(paths, bands=lambda x, y: False):
    """A painter for a plate's face: (x, y) in px in the face's plane (x mirrored: abs) -> its letter. Copper lit along
    a hose's upper edge, shaded along the lower, brass where bands(x, y), ink round it, '.' (see-through) elsewhere."""
    def at(x, y):
        x = abs(x)
        ink = False
        for path in paths:
            d, side = min((_seg((x, y), path[k], path[k + 1]) for k in range(len(path) - 1)), key=lambda d: d[0])
            if d <= HR:
                if bands(x, y): return 'E' if side < 0 else 'Y'
                return HOSE[0] if side < -HR / 3 else HOSE[2] if side > HR / 3 else HOSE[1]
            if d <= HR + OUTLINE: ink = True
        return 'X' if ink else '.'
    return at


# Every plate is a decal (2026-11-11, user: "you kept the other sides 3D"): 0.5 px off its face of the body, only its
# outward face painted, its edges see-through, so no plate shows a thickness. Their outward faces meet at the corners
# (the front's and the back's go 0.5 px over the chest's top to the shoulder strip's, the waist strip's runs from
# the front one's plane to the back one's), so a hose turns from one onto the next.
TOP_Y = 26.5          # the shoulder strip's face (the chest's top + 0.5)
# The slim build (Alex, CHEST_X 5.5; 2026-11-11): her arms start 0.5 px further in, so the hoses follow the chest's
# width (top: 1.5 px in from its side), and the gap under her arm is 0.5 px: the waist strip is a plane in its middle
# (x 5.25), off the abdomen's side and the arm cage's inner wall (no shared planes).
def side(cx):         # the waist strip's face and thickness: 0.5 px off the abdomen's side (x 5) where there is room
    return (5.5, 0.5) if cx - 5 >= 1 else ((5 + cx) / 2, 0)
BACK_Z = 3.5          # the back plate's face


def harness(low_y, cx):
    """The front plate: the core's porthole painted in the chest slot (x +-2, raw y 21-25: frame_engine_art.porthole,
    copper corners, an ink line round it), the four hoses out of its corners, a brass band where each leaves it and
    where the top pair turns over the shoulder."""
    x0, x1, y0, y1 = -cx, cx, low_y - 0.5, TOP_Y
    sx = side(cx)[0]
    port = engine_art.porthole(corner='Q')['north']                 # 8 x 8 texels over the 4 x 4 px slot
    at = hoses_at([top(cx), low(low_y, sx)], bands=lambda x, y: 2.0 <= x <= 2.5 and 20 < y < 25 or y >= 26 and x > cx - 2 * HR)

    def front(x, y):
        ax, cy = abs(x), y - 23
        if ax < 2 and abs(cy) < 2: return port[int((2 - cy) * K)][int((x + 2) * K)]
        if ax > sx and y < 20: return '.'                           # the lower pair turns onto the waist strip here
        c = at(x, y)
        if max(ax, abs(cy)) < 2.5 and c in '.X': return 'X'        # the ink round the porthole
        return c

    def paint(f, w, h):
        if f == 'north':   # seen from the front, row 0 at the top
            return [[front(x1 - (i + 0.5) / K, y1 - (j + 0.5) / K) for i in range(w)] for j in range(h)]
        return grid(w, h, '.')
    return part('harness', ((x0, y0, -3 - 0.5), (x1, y1, -3)), paint)


def strip_top(cx):
    """Over the shoulder (mirrored): the hose painted along the top face (x 4.5 - 6, its ink on the inner side,
    x 4 - 4.5, under the helmet's edge), from the front plate's face to the back one's."""
    hi, mid, lo = HOSE
    def paint(f, w, h):
        if f == 'up': return [['X', hi] + [mid] * (w - 3) + [lo] for _ in range(h)]   # columns from x 4 out
        return grid(w, h, '.')
    return part('strip_top', ((cx - 2 * HR - 0.5, TOP_Y - 0.5, -3.5), (cx, TOP_Y, BACK_Z)), paint, mirror=True)


def strip_side(low_y, cx):
    """Along the waist (mirrored), in the 1 px gap under the arm: the lower hose painted along the outer face, ink above
    and below, from the front plate's face to the back one's."""
    hi, mid, lo = HOSE
    rows = ['X', hi, mid, lo, 'X']                                   # top to bottom: y low_y + 2 .. low_y - 0.5
    def paint(f, w, h):
        if f == 'east': return [[c] * w for c in rows]
        return grid(w, h, '.')
    sx, t = side(cx)
    return part('strip_side', ((sx - t, low_y - 0.5, -3.5), (sx, low_y + 2, BACK_Z)), paint, mirror=True)


def harness_back(pack_x, up_y, low_y, pack_top=26, cx=6.0):
    """The back plate (behind the pack where the pack covers it): the top pair down from the shoulder strips to the
    pack's upper inlets, the lower pair in from the waist strips to its lower ones."""
    x0, x1, y0, y1 = -cx, cx, low_y - 0.5, TOP_Y
    sx = side(cx)[0]
    at = hoses_at([[(cx - HR, 27), (cx - HR, up_y + HR), (pack_x - 0.5, up_y + HR)],
                   [(cx + 0.5, low_y + HR), (pack_x - 0.5, low_y + HR)]])

    def clip(x, y):
        if abs(x) < pack_x and y < pack_top: return '.'             # behind the pack (its front's plane); whole above it
        if abs(x) > sx and y < 20: return '.'                        # the lower pair comes off the waist strip here
        return at(x, y)

    def paint(f, w, h):
        if f == 'south':   # seen from the back
            return [[clip(x0 + (i + 0.5) / K, y1 - (j + 0.5) / K) for i in range(w)] for j in range(h)]
        return grid(w, h, '.')
    return part('harness_back', ((x0, y0, 3), (x1, y1, BACK_Z)), paint)


def build(chest_x=6.0, pack_x=5, up_y=18, low_y=16, pack_top=26):
    """pack_x: the pack's half width; up_y / low_y: its inlets' heights (the back hoses end in them)."""
    cx = min(6, chest_x)                  # the hoses stay inside the arm boxes (from the chest's sides)
    return [harness(low_y, cx), strip_top(cx), strip_side(low_y, cx), harness_back(pack_x, up_y, low_y, pack_top, cx)]
