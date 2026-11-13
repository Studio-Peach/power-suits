"""The frame's helmet (the iron armour's, the one players see most), painted at 2 texels per px on the 9 x 9 x 9 box
(frame_model.py, HELMET_STYLE; 2026-11-12, user: "this is the default helmet, it has to look cool; currently it is a
bit flat"). The box stays a box (the armour is flat, like the engine): every face 18 x 18, its depth painted (a lit top
edge, light from the viewer's upper left, darker toward the bottom where it tucks into the chest, ridges as a lit row
over a shadow row). Seen most from behind and above (third person): the back and the top carry as much as the front.

Letters: the iron ramp and slate of frame_iron_art.py (z s p l e h g w / x d k m n), brass Y Z E and copper f Q R
from frame_model.PAL; 'V' is the visor glass (frame_model swaps in GLASS, its glint 'T').
Faces as frame_model.py's: north / south as seen from the front / back (north column 0 at +x, the viewer's left),
east back -> front, west front -> back (both as seen from that side), up rows front -> back, columns -x -> +x.
His eyes are behind rows 9-10 (head y 29.5-30 raw; row j is y 34.5 - (j + 0.5) / 2).
"""
import math

N = 18


def blank(c='e'):
    return [[c] * N for _ in range(N)]


def shade(g, top=True):
    """The box's depth: a lit top edge (and the row under it), the viewer's left column lit, the right shaded, the
    bottom two rows darker (into the chest's shadow)."""
    for i in range(N):
        if top: g[0][i], g[1][i] = 'g', 'h'
        g[-2][i], g[-1][i] = 'l', 'p'
    for j in range(2 if top else 0, N - 2):
        g[j][0], g[j][-1] = 'h', 'l'
    return g


def rect(g, i0, j0, i1, j1, c):
    for j in range(j0, j1):
        for i in range(i0, i1):
            g[j][i] = c


def ridge(g, j, i0, i1):
    """A horizontal ridge: a lit row over a shadow row."""
    for i in range(i0, i1):
        g[j][i], g[j + 1][i] = 'g', 's'


def seam(g, j, i0, i1):
    """A plate seam: a dark line with a lit row under it (the lower plate's edge catching the light)."""
    for i in range(i0, i1):
        g[j][i], g[j + 1][i] = 'z', 'h'


def bolt(g, i, j):
    g[j][i] = 'z'


def disc(g, cx, cy, r, fill, ring=None, rw=1.0, light=False):
    """A disc centred at texel coords (cx, cy); ring: its edge rw texels wide (lit top-left half if light)."""
    for j in range(N):
        for i in range(N):
            d = math.hypot(i + 0.5 - cx, j + 0.5 - cy)
            if d <= r:
                if ring and d > r - rw:
                    g[j][i] = ring if not light else ('h' if (i + 0.5 - cx) + (j + 0.5 - cy) < 0 else ring)
                elif fill:
                    g[j][i] = fill


def vents(g, i0, j0, i1, j1, a='l', b='x'):
    """Horizontal slats (the radiator's, unlit): alternating rows."""
    for j in range(j0, j1):
        for i in range(i0, i1):
            g[j][i] = a if (j - j0) % 2 == 0 else b


def grille(g, j0):
    """The old helmet's chin grille (2026-11-12, user: "iconic"; power_suit.bbmodel's, its 9 texels at 2 per px):
    four vertical bars and three dark slots between the cheeks, 2 px tall from row j0, the bars lit at the top and
    darker down, the middle slot on the centre line."""
    bar, slot = ['h', 'e', 'l', 'p'], ['x', 'x', 'd', 'd']
    for k in range(4):
        for i in range(2, 16):
            g[j0 + k][i] = slot[k] if ((i - 2) // 2) % 2 == 1 else bar[k]


def out(g): return [''.join(r) for r in g]


def glint(g):
    """A short diagonal across the glass's top left corner (the viewer's: column 0 is his left)."""
    pane = [(i, j) for j in range(N) for i in range(N) if g[j][i] == 'V']
    if not pane: return
    i0, j0 = min(i for i, _ in pane), min(j for _, j in pane)
    for i, j in pane:
        if (i - i0) + (j - j0) == 2: g[j][i] = 'T'


def top_crest(rivets=True):
    """The top: lit, a raised crest down the middle front to back (a lit column, a shaded one), rivets beside it."""
    g = blank('h')
    for i in range(N): g[0][i], g[-1][i] = 'g', 'l'
    for j in range(N): g[j][0], g[j][-1] = 'h', 'e'
    for j in range(N): g[j][8], g[j][9] = 'g', 'l'
    for j in range(N): g[j][7], g[j][10] = 'e', 'e'
    if rivets:
        for j in (3, 8, 13): g[j][5], g[j][12] = 'p', 'p'
    return g


# ---------------------------------------------------------------- A: sentinel (a T-45-ish slit visor, a crest)
def sentinel():
    f = shade(blank())
    for j in range(2, 6): f[j][8], f[j][9] = 'h', 'l'                       # the crest coming down the forehead
    ridge(f, 6, 1, 17)                                                    # the brow ridge
    rect(f, 2, 8, 16, 12, 'V')                                            # the visor slit (2 px), framed
    for j in range(8, 12): f[j][1], f[j][16] = 'x', 'x'
    for i in range(1, 17): f[12][i] = 'x'
    rect(f, 2, 13, 16, 16, 'e')
    vents(f, 6, 13, 12, 16)                                              # the mouth grille
    for i in (5, 12): f[13][i] = f[15][i] = 'p'
    bolt(f, 3, 14); bolt(f, 14, 14)
    glint(f)
    side = shade(blank())
    seam(side, 5, 1, 17)                                                  # the crown plate over the sides
    # (no ear disc: 2026-11-12, user: helmets don't usually have them)
    for j in range(7, 15): side[j][15] = 'p'                              # the cheek plate's edge (front)
    east = side
    west = [r[::-1] for r in side]                                        # its front is column 0
    back = shade(blank())
    for j in range(2, 11): back[j][8], back[j][9] = 'h', 'l'
    seam(back, 11, 1, 17)                                                 # the neck guard
    vents(back, 5, 13, 13, 16, 'p', 'x')
    for i in (2, 15): bolt(back, i, 13)
    return dict(north=out(f), south=out(back), east=out(east), west=out(west), up=out(top_crest()))


# ---------------------------------------------------------------- B: diver (a porthole, BioShock / dieselpunk)
def diver():
    f = shade(blank())
    disc(f, 9, 10, 7.5, None, ring='p', rw=2.2, light=True)               # the porthole's steel ring
    disc(f, 9, 10, 5.4, 'V', ring='Z', rw=1.0)                            # the brass bezel, the glass
    for a in range(8):                                                    # bolts round the ring
        t = a * math.pi / 4 + math.pi / 8
        i, j = int(9 + 6.4 * math.cos(t)), int(10 + 6.4 * math.sin(t))
        if 0 <= i < N and 0 <= j < N: f[j][i] = 'z'
    glint(f)
    side = shade(blank())
    disc(side, 10, 10, 4.5, None, ring='p', rw=1.5, light=True)
    disc(side, 10, 10, 2.8, 'V', ring='Z', rw=1.0)
    east = side
    west = [r[::-1] for r in side]
    back = shade(blank())
    disc(back, 9, 11, 4.5, 'R', ring='z', rw=1.0)                          # the air hose's copper port
    disc(back, 9, 11, 3.0, 'Q', ring='f', rw=1.0)
    disc(back, 9, 11, 1.4, 'x')
    seam(back, 4, 1, 17)
    for i in (3, 14): bolt(back, i, 7)
    top = blank('h')
    for i in range(N): top[0][i], top[-1][i] = 'g', 'l'
    for j in range(N): top[j][0], top[j][-1] = 'h', 'e'
    disc(top, 9, 9, 5.5, 'e', ring='p', rw=1.3, light=True)               # the hatch
    for i in range(5, 13): top[8][i], top[9][i] = 'g', 's'                # its handle
    return dict(north=out(f), south=out(back), east=out(east), west=out(west), up=out(top))


# ---------------------------------------------------------------- C: wraparound visor (glass round the front corners)
# (2026-11-12, user: C picked as the basis; with the old helmet's chin grille back, B out: an easter-egg helmet is
# BioShock's already.)
# The side seam's two rows (top, bottom): 'seam' as the armour's (a dark line over the lit plate edge) or 'ridge'
# shaded as the visor's ridge it runs into (lit over dark: one band round the helmet). Env HELMET_SEAM.
import os
# (ridge: its dark row a step lighter than the wing's, user: the two dark rows read the same)
SEAM = {'seam': ('p', 'h'), 'ridge': ('h', 'p')}[os.environ.get('HELMET_SEAM', 'ridge')]   # picked: ridge


def wrap(back_style='plain'):
    f = shade(blank())
    ridge(f, 5, 1, 17)
    for i in range(N): f[5][i], f[6][i] = 'g', 's'   # the ridge (its lit edge, the dark row under it) over the
                                              # visor, the whole width (2026-11-12, user: it stopped short of the
                                              # corners), on round them below
    rect(f, 0, 7, 18, 12, 'V')                                            # the visor across the whole front
    for i in range(0, 18): f[12][i], f[13][i] = 'x', 'p'
    grille(f, 14)
    # (no bolts on the front: tried on the forehead's corners, 2026-11-12, user: without)
    glint(f)
    side = shade(blank())
    rect(side, 13, 7, 18, 12, 'V')                                        # the glass wraps the front corner
    for i in range(13, 18): side[12][i] = 'x'
    for j in range(7, 12): side[j][12] = 'x'
    # the ridge over the glass, winged (2026-11-12, user: the layered cap didn't convince; its swept side, in the
    # helmet's own paint), and the crown seam become one with it (user: not stacked over it): the seam (its dark line,
    # the lit plate edge under it) in the ridge's two rows (5-6) from the back; over the glass, its border and a texel
    # behind (cols 11-17), the ridge (lit row over the dark one), its lit row running 1 px further back
    for i in range(1, 11): side[5][i], side[6][i] = SEAM          # in the ridge's two rows (user: line them up)
    for i in range(11, 18): side[5][i], side[6][i] = 'g', 's'
    for i in (9, 10): side[5][i] = 'g'        # the wing's tail: its lit row 1 px further back (lost once, user)
    # the crown seam (2026-11-12, user: back, but like the other seams, not black, with bolts above it, as the back's)
    for i in (3, 14): side[3][i] = 'p'          # bolts as the top's rivets (user), a row lower than first drawn
    # (no ear disc, no side vents: 2026-11-12, user: helmets don't usually have ear discs; the neck guard wraps here)
    if back_style == 'guard': neck_guard(side, GUARD_WRAP)
    east = side
    west = [r[::-1] for r in side]
    return dict(north=out(f), south=out(wrap_back(back_style)), east=out(east), west=out(west), up=out(top_crest()))


def bands(g, rows):
    """Stepped plates (a neck guard): each from row r, a lit top edge, its body, a shadow row where the next one
    tucks under it."""
    for r, h in rows:
        for i in range(1, 17):
            g[r][i] = 'g'
            for j in range(r + 1, r + h - 1): g[j][i] = 'e' if j < 16 else g[j][i]
            g[r + h - 1][i] = 'z'


# The neck guard (2026-11-12, user: slate, wrapping a little round the sides): two stepped plates over the back's
# bottom 3 px in the under-armour's slate (a lit top edge, the body, a dark row where the next tucks under), across the
# whole back and round the back corners onto the sides, each lower one reaching further forward (texels from the back).
GUARD_ROWS = [(12, 3), (15, 3)]   # (first three plates from row 8: too tall, user; now the vents draft's size)
GUARD_WRAP = [5, 7]


def neck_guard(g, reach):
    """Paint the guard into a back face (reach N: all across) or a side (east as drawn: column 0 at the back; reach
    per plate), the plate's front end a dark column (its edge)."""
    for (r, h), n in zip(GUARD_ROWS, reach):
        for i in range(n):
            for j in range(r, r + h):
                g[j][i] = 'n' if j == r else 'x' if j == r + h - 1 else 'm'
            if n < N and i == n - 1:
                for j in range(r + 1, r + h): g[j][i] = 'k' if j < r + h - 1 else 'x'


def crest(g, j0, j1):
    for j in range(j0, j1): g[j][8], g[j][9] = 'h', 'l'


def wrap_back(style='plain'):
    """The back (seen most, from behind in third person; 2026-11-12, user: draft some): 'plain' (the first draft: a
    seam, two bolts, the crest stopping above it), 'guard' (a neck guard of three stepped plates over the bottom
    half, the crest above it), 'crest' (the guard, the crest running down over it to the bottom: one ridge over the
    whole head), 'vents' (a slatted vent panel, the radiator's slats unlit, the crest down to it, a two-plate guard)."""
    b = shade(blank())
    if style == 'plain':
        crest(b, 2, 12)
        seam(b, 12, 1, 17)
        for i in (4, 13): bolt(b, i, 8)
    elif style == 'guard':
        neck_guard(b, [N] * len(GUARD_ROWS))
        crest(b, 2, GUARD_ROWS[0][0])   # (no bolts: 2026-11-12, user)
    elif style == 'crest':
        bands(b, [(8, 3), (11, 3), (14, 3)])
        crest(b, 2, 18 if style == 'crest' else 8)
        if style == 'crest':
            for j in (8, 11, 14): b[j][8], b[j][9] = 'g', 'h'
        for i in (3, 14): bolt(b, i, 5)
    else:
        crest(b, 2, 5)
        rect(b, 4, 5, 14, 11, 'x')                                        # the vent panel: dark frame, 5 slats
        for j in range(6, 10):
            for i in range(5, 13): b[j][i] = 'l' if j % 2 == 0 else 'x'
        for i in range(4, 14): b[11][i] = 'h'                             # its lower lip catching the light
        bands(b, [(12, 3), (15, 3)])
        for i in (2, 15): bolt(b, i, 7)
    return b


STYLES = {'A': sentinel, 'B': diver, 'C': wrap}


def faces(style, back='plain'):
    d = STYLES[style](back) if style == 'C' else STYLES[style]()
    d['down'] = ['k' * N] * N
    return d


# ---------------------------------------------------------------- the outer layer (HELMET_EXTRA)
# (2026-11-12, user: the sides have just one floating line; an outer layer like the chest's, small details: a cap over
# the visor's upper rim, a radio with an antenna on the side.) Decals as the engine's: thin plates 0.5 px off the
# helmet, only their outward faces painted, the rest see-through. Raw coordinates of the head bone (the helmet is
# x / z +-4.5, y 25.5 - 34.5). They stay inside a 6.4 px radius of the neck below the pauldrons' top (raw 26.5), so
# the head still turns 50 deg clear of them; nothing goes more than 1 px over the helmet's top.
def _grid(w, h, c='.'): return [c * w for _ in range(h)]


def _part(name, box, faces):
    (x0, y0, z0), (x1, y1, z1) = box
    W, H, D = (round((b - a) * 2) for a, b in ((x0, x1), (y0, y1), (z0, z1)))
    size = {'north': (W, H), 'south': (W, H), 'east': (D, H), 'west': (D, H), 'up': (W, D), 'down': (W, D)}
    out = {f: faces.get(f) or _grid(*size[f]) for f in size}
    for f, (w, h) in size.items():
        assert len(out[f]) == h and all(len(r) == w for r in out[f]), (name, f, w, h)
    return dict(name=name, box=box, faces=out)


def cap():
    """A brow cap over the visor's top rim (the glass is rows 7-11: raw y 31 down), 0.5 px off the front and round the
    front corners past the glass's wrap and its border (3.5 px back), 1.5 px tall, its bottom edge 0.5 px over the
    glass: a lit top edge, the plate, a dark lip shading the glass; behind the glass it slopes off (1.5 px)."""
    W, D = 20, 10
    north = ['g' * W, 'h' + 'e' * (W - 2) + 'l', 'x' * W]
    # rows painted per column, back -> front: full depth over the whole glass and its border on the side (2026-11-12,
    # user: cover the full visor width; it tapered off over the glass), then the first draft's slope (1, 2, 2 rows)
    # behind it (a single step there changed its silhouette)
    taper = [1, 2, 2] + [3] * (D - 3)
    east = [''.join(('g' if j == 0 else 'x' if j == taper[i] - 1 else 'e') if j < taper[i] else '.'
                    for i in range(D)) for j in range(3)]
    west = [r[::-1] for r in east]
    return [_part('cap', ((-5, 30.5, -5), (5, 32, 0)), dict(north=north, east=east, west=west))]


def radio():
    """A radio on the left side (x-), toward the back, all on one plate 0.5 px off the side: a slate box (3 x 3 px), a
    speaker grille, a brass dial, a copper lamp, and two antenna lines drawn up out of its top, the taller ending
    1 px over the helmet's top (2026-11-12, user: no 3D antenna, a few lines out of the 2D radio, short, at most a
    pixel past the helmet's top: helmets keep within their upper bound)."""
    west = ['....E.',                                     # columns front -> back (as seen from the left)
            '....l.',
            '....l.',
            '..E.l.',
            '..l.l.',
            '..l.l.',
            '..l.l.',
            'nnnnnn',
            'mxmxmm',
            'mxmxYm',
            'mxmxmm',
            'mmmmfm',
            'xxxxxx']
    return [_part('radio', ((-5, 29, 0.5), (-4.5, 35.5, 3.5)), dict(west=west))]


def camera():
    """A helmet camera on the right side (x+), opposite the radio (2026-11-12, user, after a Halo Reach helmet's: a
    rounded housing, the lens forward, a red lamp): drawn on a plate 0.5 px off the side, and
    the lens again on a small plate facing forward at its front end. The lamp is the fire's reserved red, so in game
    it lights with the engine (the fire glowmask)."""
    east = ['...nnnJJ',                                  # columns back -> front (as seen from the right); the
            '..nmmmxx',                                  # front column solid, as the front plate it meets (user:
            '..nmmmxg',                                  # see-through texels there didn't line up with it; no
                                                         # mount tail behind it, user)
            '..nmmmxx',
            '...kkkkk']
    # its front, the housing's full height and depth, from the helmet's side out to the housing's plane (a 1 px lens
    # plate, then one 0.5 px past the housing, didn't line up with it, user): the lamp, the lens, the bottom
    front = ['J', 'x', 'g', 'x', 'k']                  # (one texel across: the housing's plate is 0.5 px off the side)
    # forward, beside the visor at eye level (not mirroring the radio, user). One box 0.5 px off the side, like the
    # radio: its east face is the housing, its north face the front, so the two meet edge to edge by construction
    # (2026-11-13, user: it was a zero-thick side plate plus a zero-deep front plate, the same faces in two cubes; as
    # separate plates 0.25 px apart they had shown a gap). Its top and bottom (2026-11-13, user: fill them out)
    # carry on the side's top and bottom rows over its 0.5 px: the lamp then the lit slate on top, the dark slate
    # under it, the housing's length only (the side's see-through back columns stay open). Its back and inner side
    # stay see-through.
    up = list('JJnnn...')                              # rows front -> back, one texel across
    down = list('...kkkkk')                            # rows back -> front
    return [_part('camera', ((4.5, 28.5, -1), (5, 31, 3)), dict(east=east, north=front, up=up, down=down))]


def extras(kind):
    return {'none': [], 'cap': cap(), 'radio': radio(), 'both': cap() + radio(),
            'all': cap() + radio() + camera(), 'gear': radio() + camera()}[kind]
