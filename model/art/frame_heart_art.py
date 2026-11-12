"""The heart engine: the frame's engine (frame_model.py, ENGINE=heart) after Shiro Tomoe's in Tailenders (2026-11-11,
user: his heart replaced by an engine, "exhaust in the back and an iron ball of sorts in the front"; it replaces the
radial firebox and the copper core and pipes, ENGINE=firebox).

Three things read as his engine, here in boxes:
- the iron ball on the sternum: Minecraft has no spheres, so it is stepped (a plate, a smaller cap on it, a bolt on
  that: 1 + 1 + 0.5 px proud; the plate and the hoses' front runs 1 deep, so their faces stay off the helmet's front
  plane, z -4.5), painted round (dark iron, lit top left, a brass rivet ring, a white bolt);
- two fat hoses (1.5 px, the front runs 1.5 x 1) out of its top corners, up the chest and over the shoulders like braces, down the
  back: they sit in the 2 px strip between the head (x +-4, the helmet +-4.5) and the arm boxes (from CHEST_X), the
  only way over: the shoulder plates swing with the arms, and under the arms there is 1 px or less (0.5 slim);
- on the back each hose ends in a muffler, its exhaust a short stack leaning back (EXH=X) or a tailpipe turned down
  and back (EXH=Y, motorcycle-style; clear of the legs swung back, it is above their pivot).

Draft knobs (frame_model.py passes them): BALL A (in the chest slot) | B (low on the sternum, at the chest / abdomen
seam, as his) | C (B, bigger); EXH X | Y; HOSE cream (his: pale yellow, an orange stripe outside) | brass | copper.

Coordinates raw (frame_model.py adds FY), right side +x, the front -z. Art 2 texels per px (K), letters from
frame_model.PAL / the iron ramp (lowercase, frame_iron_art.py) plus EXTRA. Faces as frame_model.py's: north / south
as seen from the front / back, east back -> front, west front -> back, up rows front -> back. A box built to be turned
(the hoses, the stack) is drawn upright: its length along y.
"""
import math
from frame_radial_art import part, grid, disc, K

EXTRA = {'a': (0xf2, 0xe2, 0xa8), 'b': (0xd8, 0xc0, 0x7a), 'c': (0xa0, 0x86, 0x4c),   # cream hose: lit, mid, shade
         'o': (0xe0, 0x78, 0x2c),                                                       # its orange stripe
         'f': (0xe0, 0x98, 0x68)}                                                       # copper, lit
HOSES = {'cream': ('a', 'b', 'c', 'o'), 'brass': ('E', 'Y', 'Z', None), 'copper': ('f', 'Q', 'R', None)}
BALLS = {  # plate half width, plate y range, cap half width, cap y range, bolt y
    'A': (3, (20, 26), 2, (21, 25), 22),
    'B': (3, (17, 23), 2, (18, 22), 19),
    'C': (4, (16, 24), 3, (17, 23), 19)}
H = 1.5            # the hose's cross-section
CLAMP = 'X'        # the clamp rings at a hose's ends


def _shade(w, h, ramp, across='cols'):
    """A face lit on its first column (or row), shaded on its last."""
    hi, mid, lo = ramp
    if across == 'cols': return [[hi] + [mid] * (w - 2) + [lo] if w > 2 else [hi, lo][:w] for _ in range(h)]
    return [[hi] * w] + [[mid] * w for _ in range(h - 2)] + [[lo] * w]


def hose_upright(ramp, stripe, clamp_ends=(True, True)):
    """A hose segment drawn upright (length along y): lit on its left, shaded on its right, an orange stripe down the
    middle of its outer (east) side, clamp rings at its ends."""
    def paint(f, w, h):
        if f in ('up', 'down'):
            g = grid(w, h, ramp[2]); g[h // 2][w // 2] = 'X'      # the open end, dark inside
            return g
        g = _shade(w, h, ramp)
        if stripe and f == 'east':
            for j in range(h): g[j][w // 2] = stripe
        if clamp_ends[0]: g[0] = [CLAMP] * w
        if clamp_ends[1]: g[-1] = [CLAMP] * w
        return g
    return paint


def hose_along_z(ramp, stripe):
    """The segment over the shoulder (length along z, front to back)."""
    def paint(f, w, h):
        if f in ('north', 'south'): return grid(w, h, ramp[2])
        if f == 'up': return _shade(w, h, ramp)                    # columns across x, rows along z
        if f == 'down': return grid(w, h, ramp[2])
        g = _shade(w, h, ramp, across='rows')                      # east / west: columns along z, rows across y
        if stripe and f == 'east': g[h // 2] = [stripe] * w
        return g
    return paint


DOME = 'kmnple'      # the ball's iron, dark -> lit (the iron ramp's slate and steel letters)


def bevel(f, w, h, c):
    """The texels a box loses to an octagon with c-texel corners (the box drawn front-on, its depth along z): the
    front / back faces' corners, the side faces' ends. Transparent (cutout), so the ball reads round, not square."""
    if f in ('north', 'south'): return lambda i, j: min(i, w - 1 - i) + min(j, h - 1 - j) < c
    if f in ('east', 'west'): return lambda i, j: j < c or j >= h - c
    return lambda i, j: i < c or i >= w - c


def dome(w, h, lift=0):
    """A face shaded as a dome lit from the top left: the DOME ramp by the light on a sphere over the face."""
    g = grid(w, h, 'm')
    for j in range(h):
        for i in range(w):
            nx, ny = (i + 0.5 - w / 2) / (w / 2), (j + 0.5 - h / 2) / (h / 2)
            z = math.sqrt(max(0.0, 1 - min(1.0, nx * nx + ny * ny)))
            light = 0.55 * z - 0.35 * nx - 0.45 * ny            # 0 .. ~1
            g[j][i] = DOME[max(0, min(len(DOME) - 1, int(light * 4) + lift))]
    return g


def cut(paint, c):
    def f_(f, w, h):
        g = paint(f, w, h)
        gone = bevel(f, w, h, c)
        return [['.' if gone(i, j) else g[j][i] for i in range(w)] for j in range(h)]
    return f_


def ball(spec):
    """Three stepped octagons (plate, cap, bolt), shaded as one dome: the plate its dark rim, the cap the lit crown."""
    pw, (py0, py1), cw, (cy0, cy1), by = BALLS[spec]
    P = []

    def plate(f, w, h):
        if f in ('east', 'west', 'up', 'down', 'south'):
            g = grid(w, h, 'k')
            if f in ('up', 'west'): g = grid(w, h, 'm')
            return g
        g = dome(w, h, lift=-1)
        n = 8                                                     # the brass rivet ring
        for k in range(n):
            a = 2 * math.pi * (k + 0.5) / n
            i, j = int(w / 2 + (w / 2 - 1.6) * math.cos(a)), int(h / 2 + (h / 2 - 1.6) * math.sin(a))
            g[j][i] = 'Y'
        return g
    P.append(part('ball_plate', ((-pw, py0, -4), (pw, py1, -3)), cut(plate, 3 if pw == 3 else 4)))

    def cap(f, w, h):
        if f != 'north': return grid(w, h, 'n' if f in ('up', 'west') else 'm')
        return dome(w, h, lift=1)
    P.append(part('ball_cap', ((-cw, cy0, -5), (cw, cy1, -4)), cut(cap, 2 if cw == 2 else 3)))

    def bolt(f, w, h):
        if f != 'north': return grid(w, h, 'h')
        g = grid(w, h, 'w')
        g[-1] = ['h'] * w
        for j in range(h): g[j][-1] = 'h'
        g[h // 2][w // 2 - 1] = 'p'                                # the bolt's slot
        return g
    P.append(part('ball_bolt', ((-1, by, -5.5), (1, by + 2, -5)), cut(bolt, 1)))
    return P


def fitting(f, w, h):
    """A gunmetal fitting where a hose turns: lit top row, a dark band, a brass bolt on its faces."""
    g = grid(w, h, 'N')
    if f not in ('up', 'down'):
        g[0] = ['O'] * w
        g[-1] = ['X'] * w
        g[h // 2][w // 2] = 'Y'
    else:
        g[0] = ['O'] * w
    return g


def hoses(spec, ramp, stripe, chest_x):
    """The right hose (mirrored): from the ball's top corner a straight run up and out to the strip beside the head,
    a fitting at the chest's top front corner, the run over the shoulder, a fitting at the back corner, down the back
    into the muffler. Everything sits on the shell, not in it (frame_model.check: no part through the frame's bars);
    the fittings are 2 px deep against the hose's 1.5, so no face of theirs lies in a hose's plane (no z-fighting)."""
    pw, (py0, py1), *_ = BALLS[spec]
    x0, x1 = 4.5, min(6, chest_x)                                 # beside the helmet (+-4.5), inside the arm box
    xc, top = (x0 + x1) / 2, 26                                   # the chest's top (raw)
    P = []
    # in the plate's top outer corner, its collar under the helmet's bottom (raw 25.5): the collar's front is in the
    # helmet front's plane (z -4.5), so it must not reach up to it (ball A, in the chest slot)
    p0 = (pw - 0.25, min(py1 - 2.0, 23))
    p1 = (xc, top)                                                # inside the front fitting
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.floor(math.hypot(dx, dy) * K) / K                   # short of p1: its top corner stays inside x 6, off the arm's swing
    rot = round(-math.degrees(math.atan2(dx, dy)), 3)
    P.append(part('hose_front', ((p0[0] - H / 2, p0[1], -4), (p0[0] + H / 2, p0[1] + L, -3)),
                  hose_upright(ramp, stripe, (False, False)), mirror=True, rot=[0, 0, rot], origin=(p0[0], p0[1], -3.5)))
    # a brass collar where it leaves the ball
    P.append(part('hose_collar', ((p0[0] - 1, p0[1] + 0.5, -4.5), (p0[0] + 1, p0[1] + 1.5, -3)),
                  lambda f, w, h: [['E'] * w] + [['Z'] * w for _ in range(h - 1)], mirror=True,
                  rot=[0, 0, rot], origin=(p0[0], p0[1], -3.5)))
    P.append(part('fit_front', ((x0, top - 0.5, -5), (x1, top + H, -3)), fitting, mirror=True))
    P.append(part('hose_top', ((x0, top, -3), (x1, top + H, 3)), hose_along_z(ramp, stripe), mirror=True))
    P.append(part('fit_back', ((x0, top - 0.5, 3), (x1, top + H, 5)), fitting, mirror=True))
    P.append(part('hose_back', ((x0, 22, 3), (x1, top - 0.5, 3 + H)), hose_upright(ramp, stripe, (False, False)),
                  mirror=True))
    return P


def exhaust(spec):
    """A muffler on the lower back under each hose, its exhaust out of the back half of its top (X) or bottom (Y)."""
    P = []

    def muffler(f, w, h):
        """Dark iron like the ball (one machine), brass straps, the stack's hole in its top's back outer corner."""
        if f == 'up':
            g = grid(w, h, 'm'); g[h - 3][w - 3] = g[h - 2][w - 3] = 'x'
            return g
        if f == 'down': return grid(w, h, 'k')
        g = _shade(w, h, ('n', 'm', 'k'))
        for j in (1, h - 3): g[j] = ['Y'] * w                     # straps
        g[0] = ['p'] * w
        g[-1] = ['d'] * w
        return g
    P.append(part('muffler', ((3.5, 17, 3), (6, 22, 6.5)), muffler, mirror=True))

    def pipe(open_face):
        def paint(f, w, h):
            if f == open_face: return [['P'] * w, ['P', 'x', 'P'], ['P'] * w][:h]
            if f in ('up', 'down'): return grid(w, h, 'p')
            g = _shade(w, h, ('h', 'l', 'p'))
            end = range(0, 2) if open_face == 'up' else range(h - 2, h)
            for j in end: g[j] = ['P'] * w                          # soot at the mouth
            g[2 if open_face == 'up' else h - 3] = ['Y'] * w        # a brass band under it
            return g
        return paint
    if spec == 'X':   # a short stack out of the top's back outer corner, leaning back 20 deg (away from the helmet)
        P.append(part('stack', ((4.5, 21.5, 4.75), (6, 27.5, 6.25)), pipe('up'), mirror=True,
                      rot=[20, 0, 0], origin=(5.25, 22, 5.5)))
    else:             # a tailpipe out of its bottom, turned down and back 50 deg
        P.append(part('tailpipe', ((4.5, 13.5, 4.75), (6, 17.5, 6.25)), pipe('down'), mirror=True,
                      rot=[-50, 0, 0], origin=(5.25, 17.5, 5.5)))
    return P


def build(ball_spec='B', exh='X', hose='cream', chest_x=6.0):
    assert ball_spec in BALLS and exh in ('X', 'Y') and hose in HOSES, (ball_spec, exh, hose)
    *ramp, stripe = HOSES[hose]
    return ball(ball_spec) + hoses(ball_spec, ramp, stripe, chest_x) + exhaust(exh)
