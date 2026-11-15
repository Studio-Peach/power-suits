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
    back, top = wrap_back(back_style), top_crest()
    flow(f, side, back, top)
    outer = split_brow(f, side, back)
    east = side
    west = [r[::-1] for r in side]
    return dict(north=out(f), south=out(back), east=out(east), west=out(west), up=out(top), _outer=outer)


# Draft knob HELMET_BROW (2026-11-13, user: now the outer layer works, complete the visor in the inner layer and put
# the cap / brow over it in the outer one): 'inner' (as picked: the ridge painted on the helmet over the glass),
# 'outer' (the ridge over the glass, front and its wings on the sides, moved 0.5 px out onto the outer layer, so it
# stands over the visor like a cap's peak; the seam ring stays on the helmet), 'band' (the whole ring, the ridge and
# the seam round the sides and back, on the outer layer: a band round the head). Picked: 'outer' (2026-11-13, user;
# the band rejected), and under it the glass not raised (a first try ran it on up under the peak) but closed by a
# dark border as along its bottom: a dark row over the glass, a shadow row over that on the front, the border's
# corner on the side left out (rounded), as the bottom's.
BROW = os.environ.get('HELMET_BROW', 'outer')
assert BROW in ('inner', 'outer', 'band'), BROW


def split_brow(f, side, back):
    """Moves the brow (BROW) off the helmet's faces: returns it as 18 x 18 grids in the helmet's own texel coords
    ('.' elsewhere) for north / east / south (frame_helmet_art.layer puts them on the outer layer, a texel in), and
    fills what it leaves on the helmet: the glass (its back border on the side), plain steel."""
    grids = {k: [['.'] * N for _ in range(N)] for k in ('north', 'east', 'south')}
    if BROW == 'inner': return grids
    clean = shade(blank())
    def move(face, g, j, i, fill):
        grids[face][j][i] = g[j][i]
        g[j][i] = fill
    border = {5: 'p', 6: 'x'}                          # the glass's top border, as its bottom (rows 12 x, 13 p)
    for j in (5, 6):
        for i in range(N): move('north', f, j, i, border[j])
        for i in range(N):
            if BROW == 'band' or i >= 11:              # the side: its dark row over the glass, the corner left out
                move('east', side, j, i, 'x' if (j == 6 and i >= 13) else clean[j][i])
            if BROW == 'band': move('south', back, j, i, clean[j][i])
    if BROW == 'outer':                                # the wing's tail: its lit row over the seam, the seam's under it
        for i in (9, 10): move('east', side, 5, i, SEAM[0])
    if BROW == 'outer' and PEAK == 'visor':
        for j in (5, 6):                               # the peak over the visor only (its border column 12 on)
            for i in range(12): grids['east'][j][i] = '.'
        for i in range(12):                            # the seam a row down: its lit row level with the border's
            side[5][i], side[6][i], side[7][i] = clean[5][i], SEAM[0], SEAM[1]   # rounded corner, its dark row
        for i in range(N):                             # into the border's side; the ring across the back with it
            back[5][i], back[6][i], back[7][i] = clean[5][i], SEAM[0], SEAM[1]
        side[6][12] = SEAM[0]                          # the border's rounded corner filled by the seam's lit row
        for i in (10, 11): grids['east'][5][i] = 'g'   # the peak's wing: its lit row 1 px further back
    if BROW == 'outer' and PEAK_STYLE != 'steel':
        n, e = grids['north'], grids['east']
        for g in (n, e):                               # slate: a lit row over a shadow row
            for j in range(N):
                for i in range(N):
                    g[j][i] = {'g': 'n', 's': 'k'}.get(g[j][i], g[j][i])
        e[5][10] = '.'                                 # the wing a texel shorter
        mid = range(3, 15)                             # the third row, 6 px in the middle of the front (4 first; user:
                                                       # wider)
        if PEAK_STYLE == 'up':                         # a raised middle: lit row on top, the old lit row its body
            for i in mid: n[4][i], n[5][i] = 'n', 'm'
        else:                                          # a middle dipping over the glass: the old shadow its body
            for i in mid: n[6][i], n[7][i] = 'm', 'k'
    return grids


# Draft knob HELMET_PEAK_STYLE (2026-11-13, user: the brow in slate, the wings kept but shorter, a third row near the
# middle, to give it more shape from the front): 'steel' (as picked before), 'up' (picked: slate, the third row over
# the middle 6 px, a raised middle), 'down' (slate, the third row under the middle, dipping over the glass's top).
PEAK_STYLE = os.environ.get('HELMET_PEAK_STYLE', 'up')
assert PEAK_STYLE in ('steel', 'up', 'down'), PEAK_STYLE


# Draft knob HELMET_PEAK (2026-11-13, user: tell the brow from the seam): 'wing' (the peak's wings run 1.5 px back
# past the visor on the sides, into the seam in the same rows), 'visor' (picked: the peak over the visor, its border
# included, its lit row swept 1 px further back (user: "give the brow the winged edges again"); the seam (and the
# ring across the back) a row lower, its lit row level with the visor border's top, filling its rounded corner
# (user), its dark row running into the border's side).
PEAK = os.environ.get('HELMET_PEAK', 'visor')
assert PEAK in ('wing', 'visor'), PEAK


# Draft knob HELMET_FLOW (2026-11-13, user: the top and the back "feel a little disconnected from the rest of the
# faces"): the front and sides share a language (the ridge / seam band at rows 5-6 round the visor, bolts at row 3,
# the neck guard wrapping round), the top and back don't: the band dead-ends at the back corners, the crest breaks for
# the back's 2 lit edge rows (and changes colour there), the top's rivets don't line up with the side bolts, and the
# top's body is a step lighter than every other face (and the game shades a top face brightest anyway: a lid).
# Two concepts (2026-11-13, user: the brow crest was too much; crest and ring both is too much, try one without the
# crest and one without the ring): 'crest' (one crest, the top's colours, unbroken over the top-back edge down to the
# neck guard), 'ring' (no crest anywhere: the side seam carried across the back, a band round the whole head; the top
# plain). Both put the top's rivets in the side bolts' rows. 'none' is as picked 2026-11-12.
# Picked: 'ring' (2026-11-13, user).
FLOW = os.environ.get('HELMET_FLOW', 'ring')
assert FLOW in ('none', 'crest', 'ring'), FLOW


def flow(f, side, back, top):
    if FLOW == 'none': return
    # the top's rivets in the rows of the side bolts (side columns 3 / 14 from the back: top rows 14 / 3); with the
    # crest gone (ring) out to columns 3 / 14 as well, a square inset 3 texels from every edge (2026-11-13, user:
    # respace them now the line is gone; beside the crest they were at columns 5 / 12)
    for j in range(N):
        for i in (5, 12):
            if top[j][i] == 'p': top[j][i] = 'h'
    cols = (3, 14) if FLOW == 'ring' else (5, 12)
    for j in (3, 14):
        for i in cols: top[j][i] = 'p'
    if FLOW == 'crest':   # the top's columns (7 e, 8 g, 9 l, 10 e; -x lit, as the back seen from behind, column 0 at -x)
        for j in range(GUARD_ROWS[0][0]):
            back[j][7], back[j][8], back[j][9], back[j][10] = 'e', 'g', 'l', 'e'
    if FLOW == 'ring':
        clean = shade(blank())                         # the back's crest gone (its plain body back)
        for j in range(GUARD_ROWS[0][0]):
            for i in range(7, 11): back[j][i] = clean[j][i]
        for i in range(N): back[5][i], back[6][i] = SEAM
        side[5][0], side[6][0] = SEAM                 # (east column 0 is the back edge; west is its mirror)
        for j in range(1, N - 1):                      # the top's crest gone: its body, the edges kept
            for i in range(7, 11): top[j][i] = 'h'
        top[0][7:11], top[-1][7:11] = ['g'] * 4, ['l'] * 4


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


# ================================================================ the helmet styles (frame step 7b, 2026-11-14)
# The big suit's five Easter-egg helmets (item/HelmetStyle, design sec. 4c) redrawn for the frame: the same 9 x 9 x 9
# box at 2 texels per px as C, flat (no layer yet), its steel in the eight steel shades so the paint takes it (as the
# big suit's style shells did), what mustn't take paint in other colours (EXTRA: a red, a silver). First drafts, one
# each, after the big suit's and their originals.
EXTRA = {'r': (0x9a, 0x2a, 0x22), 'o': (0x5e, 0x18, 0x14),                       # a red mark (not the fire's reserved reds)
         'i': (0xc8, 0x3c, 0x2a),                                                   # its lit red (the diver's valve)
         't': (0xc8, 0xcc, 0xd0), 'u': (0x9a, 0xa0, 0xa6), 'v': (0x6b, 0x71, 0x78)}   # silver (grille, hoses): unpainted
# Gold (the robot's, 2026-11-15, user: a gold recipe of its own, so it keeps its colour: no paint): eight shades
# '0' (darkest) .. '7' (brightest), one per steel shade z s p l e h g w (GOLD maps them), so a style is drawn in the
# steel letters and swapped at the end. Digits: the only letters free in frame_model's PAL + the iron's; none of
# them a reserved glow colour (make-glowmasks.py).
GOLD = dict(zip('zsplehgw', '01234567'))
EXTRA.update({'0': (0x3a, 0x2a, 0x0c), '1': (0x5e, 0x42, 0x0f), '2': (0x8a, 0x5e, 0x12), '3': (0xb0, 0x7a, 0x14),
              '4': (0xd4, 0x9a, 0x1a), '5': (0xe9, 0xb8, 0x27), '6': (0xf8, 0xd8, 0x4a), '7': (0xff, 0xf7, 0xa8)})


def rrect(g, i0, j0, i1, j1, c, cut=1):
    """A rectangle (i1 / j1 exclusive) with its corners cut by `cut` texels (a rounded look)."""
    for j in range(max(j0, 0), min(j1, N)):            # (a rectangle may run off the face: a visor wrapping on)
        for i in range(max(i0, 0), min(i1, N)):
            di = min(i - i0, i1 - 1 - i)
            dj = min(j - j0, j1 - 1 - j)
            if di + dj >= cut:
                g[j][i] = c


def outline(g, c, inside='V'):
    """Every texel next to an `inside` texel (4-neighbours) that isn't one becomes c: a border round the glass."""
    pts = [(i, j) for j in range(N) for i in range(N) if g[j][i] != inside and any(
        0 <= i + di < N and 0 <= j + dj < N and g[j + dj][i + di] == inside for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for i, j in pts:
        g[j][i] = c


def plain_top():
    top = blank('h')
    for i in range(N): top[0][i], top[-1][i] = 'g', 'l'
    for j in range(N): top[j][0], top[j][-1] = 'h', 'e'
    return top


def sides(east):
    return out(east), out([r[::-1] for r in east])


# ---------------------------------------------------------------- protector (Subject Delta, BioShock 2)
def protector_r1():
    """The diver (draft B, 2026-11-12: left out of the default as "BioShock's already", so this is where it goes): a
    riveted porthole with a brass bezel over the face, behind three steel bars (the big suit's protector), smaller
    portholes on the sides, the hatch on top, the copper air port at the back."""
    d = diver()
    f = [list(r) for r in d['north']]
    for j in range(N):                                                    # three bars over the glass: the middle
        if any(f[j][i] in 'VTZ' for i in (8, 9)): f[j][8], f[j][9] = 'h', 'l'   # one 2 texels (on the centre line),
        for i in (5, 12):                                                 # the outer two 1, glass 2 wide between
            if f[j][i] in 'VTZ': f[j][i] = 'h'
    d['north'] = out(f)
    return d


# Round 2 (2026-11-14, user's reference: Subject Delta, .scratch/helm7/diver/ref.jpg): the Big Daddy's face, not a
# generic diving helmet: a wide oval porthole high on the front (its brass bezel lit top-left, his eyes behind it),
# two small portholes under it at the cheeks, two brass straps from the bezel down to the collar between them; the
# helmet bolted onto its corselet (a riveted collar band round the bottom, brass bolts); the air hoses (silver ribs)
# into brass collars on the sides and down the back's corners toward the tanks; the lamp housing on top (a brass
# ring, its lens). The shell in the steel shades (Delta's copper is a paint away: PAINT=orange / brown).
# Draft knob DIVER_GRILLE (the main porthole's bars): 'bars' (two brass bars, between his eyes, running on down as
# the straps), 'grid' (the two and one across the window above his eyes: Delta's panes), 'none' (open glass).
DIVER_GRILLE = os.environ.get('DIVER_GRILLE', 'bars')   # picked: bars (2026-11-14, user)
assert DIVER_GRILLE in ('bars', 'grid', 'none'), DIVER_GRILLE
# The main porthole (2026-11-14, user: the hand-drawn one came out too tall and uneven left to right; the first
# pass's, traced as an ellipse, looked much better): DIVER_MAIN, a brass bezel lit top-left round the glass, rivets
# round it in mirrored pairs, the grille's bars over it. E / Y / Z: the fittings' lit / mid / shade (light from the
# upper left; DIVER_METAL), V glass. His eyes are behind rows 9-10.
DIVER_MAIN = (9.0, 9.5, 7.0, 4.6)    # the main porthole's bezel: centre column, row, x / y radius (texels): round
                                     # his eyes (rows 9-10; 2026-11-14, user: at row 7.5 it sat too high)
DIVER_RIM = 1.2
# The cheeks' portholes and the straps under the window are gone (2026-11-14, user, round 7: 'none' picked over 4 x 4
# corner ports, half hidden by the chest's top; the straps running on down past the window looked off).
# Draft knob DIVER_METAL (2026-11-14, user: the brass looks out of place, there is no brass anywhere else on the
# frame): what the diver's fittings (the window's bezel and bars, the hose collars, the valve wheel, the bolts, the
# lamp's ring) are made of: 'slate' (the under-armour's, as C's brow and neck guard: unpainted), 'steel' (the shell's
# own shades: they take the paint with it), 'silver' (the hoses' unpainted silver), 'brass' (as drafted).
DIVER_METAL = os.environ.get('DIVER_METAL', 'slate')   # picked: slate (2026-11-14, user)
assert DIVER_METAL in ('slate', 'steel', 'silver', 'brass'), DIVER_METAL
METAL = {'slate': {'E': 'n', 'Y': 'm', 'Z': 'k'}, 'steel': {'E': 'g', 'Y': 'h', 'Z': 's'},
         'silver': {'E': 't', 'Y': 'u', 'Z': 'v'}, 'brass': {}}
# Round 9 (2026-11-14, user: the window is locked in, but the rest of the front looks bare and the faces don't read as
# one design). One language on every face: each carries one round fitting in the window's bezel (the same rim, lit
# top-left, the same metal): the window on the front, the hose ports on the sides, the air valve on the back, the
# lamp on top; and the corselet band (bolted) round the bottom of all four sides, the front included.
# (DIVER_LOOK, what tied them together besides: a riveted seam round the dome or rings of rivets round the fittings;
# dropped with the rings, below.)
# Round 11 (2026-11-14, user): windows on the sides and the top too, as real diving helmets had several (they won't show
# his face, but with the helmet on every one lights up, the visor's glow: the deep-sea look): round, in the front
# window's bezel, at its height on the sides (all lined up), the top's in the middle. The hose ports went with them:
# the hoses come up the back's corners and turn in to the air valve, which is back (user: "I liked that idea"): the
# round-5 handwheel, in red, a nod to Valve's logo (unpainted, as the hunter's red).
# (DIVER_PORTS, the side and top windows' bars: picked bars, then the windows went, below.)
# Round 19 (2026-11-15, user): the side and top windows gone again, the front's alone; the front's two tones carried
# round the sides and the back (the lower section a step darker under a seam line, level with where the front's
# cheek panels meet the corners); bolts along that division on the sides; the top's rivets as the standard helmet's
# (a square 3 texels in); the hoses no longer from the neck: oxygen hoses from fittings on the sides, beside the
# window as the reference's, back round the corners into the valve (gone again, below).
DIVER_VALVE = [                      # the air valve's handwheel (rim, four spokes, the hub), 6 x 6, lit upper left
    '.EEYY.',
    'EZ.EZY',
    'E.EY.Z',
    'YEYZYZ',
    'YZ.Y.Z',
    '.YZZZ.',
]
VALVE_RED = {'E': 'i', 'Y': 'r', 'Z': 'o'}
VALVE_AT = (6, 4)                    # its top left (column, row) on the back: rows 4-9, just over the seam
# (The oxygen hoses, from fittings beside the window on the sides round the corners into the valve, went again:
# 2026-11-15, user: "maybe less is more"; they were f8b1c5d.)
SPLIT = 10                           # the seam row round the sides and back (the front's panels meet its corners here)
# The bolts along the seam, above it (2026-11-15, user): two a face, 3 texels in from the edges, as the top's rivets
# and the back's (either side of the valve) (user: four, evenly spaced at 1 / 6 / 11 / 16, looked squished; 3 / 7 /
# 10 / 14 weren't even); the top's rivets' shade ('p', user: the darker ones read as another kind).
SIDE_BOLTS = (3, 14)                 # east columns
BACK_BOLTS = (3, 14)
BOLT_ROW = SPLIT - 2                 # on the upper plate, a row clear of the seam (2026-11-15, user: tried on the other
                                     # side of it, picked; under it, row 12, they were b86b412's 'below')
# Round 12 (2026-11-14, user, after the reference's little camera on Delta's helmet top): the camera over the front
# window, its lens facing forward on the front face, its body running back over the top face. Its lens is painted,
# not glass (user: it doesn't light up with the windows). The front and the top meet along a full row (no rounded
# corners at the shared edge: holes there). Drafted as a box in the outer layer's 0.5 px (0f89ec6), on the outer layer
# itself (3fae2cd: it looked like it floats, no sides) and flat; picked: flat (2026-11-15, user: 3D elements are
# deliberately avoided), the box's art painted into the helmet, its front all four of the box's rows (user: as the box
# looks from the front), one row clear of the window's rim.
CAM_FRONT = [                        # front face rows 0-3, columns 6-11 (3 px wide over the window's middle): the
    'nnnnnn',                        # lit top row on the edge with the top's; the lens dark, a silver glint, in a dark
    'mkuxkk',                        # ring
    'mkxxkk',
    '.kkkk.',                        # its bottom corners rounded off (2026-11-15, user)
]
CAM_TOP = [                          # top face rows 0-3 (front -> back), as seen from the front (lit on the viewer's
    'nnnnnn',                        # left): its lit front edge on the helmet's edge row
    'nmmmmk',
    'nmmmmk',
    'kkkkkk',
]
CAM_COL = 6


# The rings (2026-11-15, user: the rings with the bolts don't look good, something less rustic; drafted: the seam and
# the band without rivets / bolts, both as slate trim, or the slate collar alone; picked: the collar alone, "the bald
# one"): no ring round the dome. Then the slate collar band went too (2026-11-15, user): the standard helmet's slate
# neck guard back on the back, wrapping the sides' back corners (as the hunter's).


# The face (2026-11-15, user, from the reference: Delta's helmet is split in three, seams running from the window's
# ends down and in under it to meet below it, then one seam down the middle; the two lower panels hold the cheek
# lights): the cheek panels, wrapping round onto the sides; the cheek lights in them as lamps, not glass (user:
# distinctly lights), lit when the suit is powered (user): painted in the fire's reserved coal colours (F I), so the
# fire glowmask lights them with the engine as the radiator guard's slats; the front's collar band gives way to the
# panels.
# The front's right cheek panel (the left mirrors it), row: its columns 0..n-1 (a texel of shell between it and the
# window's bezel: drawn as a line hugging the bezel it ran into the bezel's shaded lower right, and single-texel
# diagonals read as dots): the window's section is the dome, the window and a tongue down the middle (columns 7-10).
# The panels are a step darker, their edge against the upper section a dark seam line.
WISH_PANEL = {10: 1, 11: 2, 12: 3, 13: 4, 14: 6, 15: 7, 16: 7, 17: 7}
CHEEK_LAMP = [                                  # in each lower panel (rows 14-17, columns 1-4 / 13-16): a slate rim
    '.EE.',                                     # round a 2 x 2 lamp, hottest in its upper left
    'EFFZ',
    'EFIZ',
    '.ZZ.',
]


def panel(g, mask):
    """A plate a step darker than the shell over the texels in mask, its edge against the rest a dark seam line (the
    face's own edges don't count)."""
    for i, j in mask:
        edge = any(0 <= i + di < N and 0 <= j + dj < N and (i + di, j + dj) not in mask
                   for di, dj in ((1, 0), (-1, 0), (0, -1), (0, 1)))
        if g[j][i] in 'ehl': g[j][i] = 'p' if edge else 'l'


def bezel(g, cx, cy, rx, ry, rim, inner):
    """A round fitting: its rim (E lit upper left, Z shaded lower right, Y between) round an inside painted by
    inner(i, j)."""
    for j in range(N):
        for i in range(N):
            x, y = (i + 0.5 - cx) / rx, (j + 0.5 - cy) / ry
            if math.hypot(x, y) > 1: continue
            if math.hypot((i + 0.5 - cx) / (rx - rim), (j + 0.5 - cy) / (ry - rim)) > 1:
                g[j][i] = 'E' if x + y < -0.45 else 'Z' if x + y > 0.45 else 'Y'
            else:
                g[j][i] = inner(i, j)


def protector():
    f = shade(blank())
    grille = {'bars': 'Y', 'grid': 'Y', 'none': 'V'}[DIVER_GRILLE]
    cx, cy, rx, ry = DIVER_MAIN
    bezel(f, cx, cy, rx, ry, DIVER_RIM,
          lambda i, j: grille if i in (7, 10) else 'Y' if (DIVER_GRILLE == 'grid' and j == 6) else 'V')
    glint(f)
    mask = {(i, j) for j, n in WISH_PANEL.items() for i in range(n)}
    mask |= {(N - 1 - i, j) for i, j in mask}
    for j in range(14, N):                                               # the tongue down to the bottom (over the
        for i in range(7, 11): f[j][i] = 'e' if j < N - 1 else 'l'        # face's darker bottom rows)
    panel(f, mask)
    for j, row in enumerate(CHEEK_LAMP):
        for i, c in enumerate(row):
            if c != '.': f[14 + j][1 + i] = f[14 + j][13 + i] = c
    lower = {(i, j) for j in range(SPLIT, N) for i in range(N)}          # the sides' and back's lower section
    e = shade(blank())
    panel(e, lower)
    for i in SIDE_BOLTS: e[BOLT_ROW][i] = 'p'
    neck_guard(e, GUARD_WRAP)
    east, west = sides(e)
    b = shade(blank())
    panel(b, lower)
    neck_guard(b, [N] * len(GUARD_ROWS))
    for i in BACK_BOLTS: b[BOLT_ROW][i] = 'p'
    for j, row in enumerate(DIVER_VALVE):                                # the valve's red handwheel, mid-back
        for i, c in enumerate(row):
            if c != '.': b[VALVE_AT[1] + j][VALVE_AT[0] + i] = VALVE_RED[c]
    top = plain_top()
    for j in (3, 14):                                                    # the standard helmet's rivets: a square
        for i in (3, 14): top[j][i] = 'p'                                # 3 texels in from the edges
    for art, g in ((CAM_FRONT, f), ([r[::-1] for r in CAM_TOP], top)):   # (the top's columns run -x -> +x, the
        for j, row in enumerate(art):                                    # front's +x -> -x: lit side kept)
            for i, c in enumerate(row):
                if c != '.': g[j][CAM_COL + i] = c
    d = dict(north=out(f), south=out(b), east=east, west=west, up=out(top))
    m = METAL[DIVER_METAL]
    return {k: [''.join(m.get(c, c) for c in r) for r in v] for k, v in d.items()}


# ---------------------------------------------------------------- spartan (the Master Chief, Halo)
# Rounds 2-9 (2026-11-15, in git: 88eecc6 .. cbee522): every detail of the references (.scratch/helm7/spartan/ref*.jpg)
# was "way too busy"; a band, prongs and a snout on a plain shell (from the old suit's) "absolute dogwater, not cool at
# all"; outer-layer parts disliked (flat, the paint doing it, as the other helmets).
# Round 10 (2026-11-15, user: "make this helmet one of our stars", ref.png again): restarted from the reference's face
# read as big shapes in value, drawn texel by texel (half maps, mirrored): a brow over the visor whose lower edge has
# the reference's three parts (the centre tab hanging down over the visor, the lip either side, the wings a row lower
# at the corners), its deep shadow row under it; the visor wide, wrapping round the corners onto the sides (user: likes
# the wrap), its bottom closed in at the corners by the cheeks rising to the lamps (two silver dots on a slate plate
# round each front corner) and dipping in two lobes either side of the slate mouthpiece (a lit top in the visor's
# notch, widest under it, its bottom rounded in to 2 texels); the cheeks' lit edges falling from the lamps to the mouthpiece (the reference's V jaw) over a
# narrow chin plate. The top's centre channel (the reference's recessed strip between two ridges) runs from the brow
# tab over the top and down the back to a band round the back; the brow's lip sweeps back along the sides and down
# into that band (ref2's line), so the head reads as one piece; a seam behind the lamps closes the cheek piece.
# Round 18 (2026-11-15): the user's own paint over round 16 in Blockbench (their first texture edit), carried here
# texel for texel: the black under the brow a slate band (the reference's dark recess, the mouthpiece's and lamps'
# slate, no "eyebrows"), the visor's border one row all round (over the mouthpiece too), the mouthpiece two rows
# with the chin plate's lit top right under it, the lobes a texel narrower; the channel lit as a groove on the top
# and back (from behind: lit rim and dark wall on the left, lit wall on the right), down the brow its dark wall in
# line; the side's wrap
# shallower, a shadow row under the brow's line all along its sweep, the cheek piece's seam further forward and its
# side lamp dot gone. Full 18-texel rows (the channel's lighting isn't a mirror image). Faces as frame_model.py's.
# The faces' columns run opposite ways (the front's from +x, the top's and back's from -x): the channel's dark wall
# is one strip at x -1.25 on all three, so its streak runs on unbroken over the front edge (user, 2026-11-15). A
# 'groove' option lit off the front's column numbers moved it to the other side at the edge (dropped).
# Round 19 (2026-11-15, the user's second paint, over round 18): the slate band gone, the brow its own lit lower edge
# right over the visor's border, the tab's shadow under its lit top, the channel's floor down the brow a step darker;
# the glass over the mouthpiece again (no border there), the lobes as round 16, the lamps a row lower, a dark line
# under the mouthpiece. (SPARTAN_TAB dropped with it.)
# Round 21 (2026-11-15, the user's third paint, "a shape I really like"; the shadowed glass not liked): the tab 6 wide,
# hanging a row into the visor over its border, its own lit bottom edge, the border under it.
# Round 23 (2026-11-15, the user's fourth paint after the SPARTAN_TOP drafts, "ready"): the front's corner columns a
# step darker over the visor (the dome rolling round). The picked spartan: SPARTAN_TOP / SPARTAN_BROW / _SHADOW stay
# at their defaults (flat / user / none; kept as knobs for the record).
# Brow depth drafts (2026-11-15, user: "is there a technique for that kind of depth on the brow in pixel art?"):
# SPARTAN_BROW 'user' (round 19: a lit lower edge) | 'form' (shaded as a rounded overhang lit from above: its top
# lit, its face mid, its bottom turning under dark, the tab darkest) | 'plate' (a raised plate: a seam over it, a lit
# top edge, a shaded bottom edge); SPARTAN_BROW_SHADOW 'none' | 'glass' (the brow's shadow cast on the visor: its
# top glass row in the shade glass 'W', the tab's shadow a row deeper and a texel right, away from the light). The
# corners (columns 0 and 17) keep the user's texels, where the side's line meets them.
SPARTAN_BROW = os.environ.get('SPARTAN_BROW', 'user')
SPARTAN_BROW_SHADOW = os.environ.get('SPARTAN_BROW_SHADOW', 'none')   # 'glass' not liked (user, 2026-11-15)
BROW_ROWS = {'form': {3: 'g' * 16, 4: 'e' * 16, 5: 'llllll' + 'pppp' + 'llllll'},
             'plate': {2: 'ppppp' + 'glllpg' + 'ppppp', 3: 'g' * 16, 4: 'e' * 16, 5: 'llllll' + 'pppp' + 'llllll'}}
# The upper section's colour (2026-11-15, user: "the colouring of the top part is a bit too flat"): draft knob
# SPARTAN_TOP 'flat' (round 21) | 'grain' (the iron armour's: a few 1-texel marks a step off the field, one per ~30
# texels, never on a line; at the armour's one per 12 the big fields read speckled) | 'wear' (the reference's worn edges: some lit edge texels at the brightest shade, a lit
# scuff under some of them) | 'dome' (planes: the top's outer three columns and the upper section's vertical
# corners a step darker, so the dome rolls over instead of standing as flat faces); '+' joins them (dome+wear).
SPARTAN_TOP = os.environ.get('SPARTAN_TOP', 'flat')


def spartan_upper(face, i, j):
    """Is texel (i, j) of a face in the helmet's upper section (over the visor and the brow's line)?"""
    if face == 'up': return True
    if face == 'north': return j <= 5
    if face == 'south': return j <= 8
    return j <= (8 if i < 4 else 7 if i < 8 else 6)                         # east: the brow's line


def spartan_top_colour(faces, kind):
    import random
    ramp = 'zsplehgw'
    step = lambda c, k: ramp[max(0, min(7, ramp.index(c) + k))]
    for name, g in faces.items():
        rng = random.Random('spartan' + name)
        field = lambda i, j: g[j][i] in 'eh' and all(0 <= i + a < N and 0 <= j + b < N and g[j + b][i + a] == g[j][i]
                                                     for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        upper = [(i, j) for j in range(N) for i in range(N) if spartan_upper(name, i, j)]
        if kind == 'grain':
            spots = [(i, j) for i, j in upper if field(i, j)]
            for i, j in rng.sample(spots, min(len(spots), len(upper) // 30)):
                g[j][i] = step(g[j][i], rng.choice((1, -1)))
        elif kind == 'wear':
            edges = [(i, j) for i, j in upper if g[j][i] == 'g']
            for i, j in edges:
                if rng.random() < 0.3:
                    g[j][i] = 'w'
                    if j + 1 < N and g[j + 1][i] in 'eh' and rng.random() < 0.5: g[j + 1][i] = step(g[j + 1][i], 1)
        elif kind == 'dome':
            cols = {'up': (0, 1, 2, 15, 16, 17), 'north': (0, 1, 16, 17), 'south': (0, 1, 16, 17), 'east': (0, 1, 16, 17)}[name]
            for i, j in upper:
                if i in cols and g[j][i] in 'eh' and (name == 'up' or j >= 2) and not (name == 'up' and j in (0, N - 1)):
                    g[j][i] = step(g[j][i], -1)


SPARTAN_FRONT = [
 'gggggglllllpgggggg',   # 0 the channel down the brow (cols 5-12): lit rim, its floor, dark wall
 'hhhhhglllllpghhhhh',
 'leeeeeglllpgeeeeel',   # 2-4 the corners a step darker (user, round 23: the dome rolling round)
 'leeeeeeggggeeeeeel',   # 3 the tab's lit top
 'lhhhhheeeeeehhhhhl',
 'gggggghhhhhhgggggg',   # 5 the brow's lit lower edge; the tab (6 wide) hanging on down
 'xxxxxxggggggxxxxxx',   # 6 the visor's border; the tab's lit bottom edge over it (user, round 21)
 'VTVVVVxxxxxxVVVVVV',   # 7 the border under the tab (the glass a row lower there); the glint: the user's two texels
 'TVVVVVVVVVVVVVVVVV',
 'VVVVVVVVVVVVVVVVVV',
 'VVVVVVVVVVVVVVVVVV',
 'xxVVVVVVVVVVVVVVxx',   # 11 the glass over the mouthpiece
 'ggxVVVVnnnnVVVVxgg',   # 12 the lobes; the mouthpiece's lit top
 'nngxxxnkkkknxxxgnn',   # 13 the cheeks' lit edges; the mouthpiece
 'tkegggxxxxxxgggekt',   # 14 the lamps; a dark line under the mouthpiece
 'tkeeeephhhhpeeeekt',
 'lleeeephhhhpeeeell',   # 16 chin
 'ppllllpeeeepllllpp',
]

# east (column 0 at the back, 17 at the front; the neck guard's texels left plain: neck_guard() paints them)
SPARTAN_SIDE = [
 'gggggggggggggggggg',
 'hhhhhhhhhhhhhhhhhh',
 'eeeeeeeeeeeeeeeeee',
 'eeeeeeeeeeeeeeeeee',
 'eeeeeeeeeeeeeeeeee',
 'eeeeeeeeeeeeeeeegg',
 'eeeeeeeeggggggggxx',   # 6 the wing's lip run back
 'eeeeggggllllllxxVV',   # 7 a shadow row under the lip all along its sweep
 'gggglllleeeeeexVVV',
 'lllleeeeeeeeeexVVV',
 'eeeeeeeeeeeeeeexVV',   # 10 the wrap 2-3 texels deep
 'eeeeeeeeeeeeeeeexx',
 'eeeeeeeeeeeeeepggg',   # 12 the cheek piece's back seam; the lamp plate, its dot a row lower (user, round 19)
 'eeeeeeeeeeeeeephnn',
 'eeeeeeeeeeeeeephkt',
 'eeeeeeeeeeeeeephkt',
 'llllllllllllllllll',
 'pppppppppppppppppp',
]

SPARTAN_BACK = [
 'ggggggplllllgggggg',   # 0 the channel down the back (its rim / wall / floor as the top's)
 'hhhhhgplllllghhhhh',
 'heeeegplllllgeeeeh',
 'heeeegplllllgeeeeh',
 'heeeeegplllgeeeeeh',
 'heeeeeeggggeeeeeeh',   # 5 the tab
 'heeeeeeeeeeeeeeeeh',
 'heeeeeeeeeeeeeeeeh',
 'gggggggggggggggggg',   # 8 the band round the back
 'llllllllllllllllll',
 'heeeeeeeeeeeeeeeeh',
 'heeeeeeeeeeeeeeeeh',
 'heeeeeeeeeeeeeeeeh',
 'heeeeeeeeeeeeeeeeh',
 'heeeeeeeeeeeeeeeeh',
 'heeeeeeeeeeeeeeeeh',
 'llllllllllllllllll',
 'pppppppppppppppppp',
]


# Round 17 (2026-11-15, user: "a fun part": the sections read well, the mouthpiece's from side to side under the
# visor and the top's from the back to the front; put them on the outer layer, for depth against the visor and the
# rest of the helmet). The layer's texels are the helmet's own (the layer is 0.5 px out, its texel (j + 1, i + 1) over
# the helmet's (j, i), its edge rows / columns carrying the art on round the corners), so from the front nothing
# moves; the helmet keeps its paint under them (an icon or a model without the layer looks the same). The visor's
# 1-texel dark border stays on the helmet: the raised parts' edges stand over it.
# Draft knob SPARTAN_LAYER ('+' joined, 'none' for the flat round 16):
#   jaw     the lower section: every front texel under the visor (its border excepted: the lamps, cheeks, mouthpiece,
#           chin) and the cheek piece round the sides (in front of its back seam, which stays on the helmet as the
#           shadow behind it)
#   cap     the upper section, the whole shell over the visor: the front's brow (lip, tab, wings), the top, the sides
#           over the brow's line, the back down to its band (the shadow row under the band stays on the helmet)
#   channel the centre strip only: the brow's tab, the channel over the top and down the back to its tab
# Dropped (2026-11-15, user: "I guess there is a reason I didn't like it before"): flat again, as the other helmets;
# the knob stays for the record (r17 sheet: .scratch/helm7/spartan/r17_spartan_layer.jpg).
SPARTAN_LAYER = os.environ.get('SPARTAN_LAYER', 'none')


def spartan_layer(f, e, b, t, parts):
    """The outer art ({face: rows, '.' see-through}) for the sections in parts, cut from the helmet's faces."""
    glassy = lambda g, i, j: g[j][i] in 'VT' or (g[j][i] == 'x' and any(
        0 <= i + di < N and 0 <= j + dj < N and g[j + dj][i + di] in 'VT' for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1))))
    pick = {k: set() for k in ('north', 'east', 'south', 'up')}
    if 'jaw' in parts:
        pick['north'] |= {(i, j) for j in range(12, N) for i in range(N) if not glassy(f, i, j)}
        pick['east'] |= {(i, j) for j in range(12, N) for i in range(12, N) if not glassy(e, i, j)}
    if 'cap' in parts:
        pick['north'] |= {(i, j) for j in range(7) for i in range(N) if not glassy(f, i, j)}
        line = lambda i: 8 if i < 4 else 7 if i < 8 else 6                # the side's line: the brow's lip, stepping
        pick['east'] |= {(i, j) for i in range(N) for j in range(line(i) + 1) if not glassy(e, i, j)}   # down
        pick['south'] |= {(i, j) for j in range(9) for i in range(N)}     # back to the band (row 8)
        pick['up'] |= {(i, j) for j in range(N) for i in range(N)}
    if 'channel' in parts:
        pick['north'] |= {(i, j) for j, (a, b_) in enumerate([(5, 13)] * 2 + [(6, 12)] * 2 + [(7, 11)] * 3) for i in range(a, b_)}
        pick['up'] |= {(i, j) for j in range(N) for i in range(6, 12)}
        pick['south'] |= {(i, j) for j, (a, b_) in enumerate([(6, 12)] * 5 + [(7, 11)]) for i in range(a, b_)}
    src = dict(north=f, east=e, south=b, up=t)
    return {k: [[src[k][j][i] if (i, j) in pick[k] else '.' for i in range(N)] for j in range(N)] for k in pick}


def spartan():
    f = [list(r) for r in SPARTAN_FRONT]
    for j, row in BROW_ROWS.get(SPARTAN_BROW, {}).items():
        if j == 4: row = 'hh' + row[2:-2] + 'hh'                         # (the user's lit wing ends kept)
        f[j][1:17] = list(row) if j != 5 else list(row[:5] + 'l' + row[6:10] + 'l' + row[11:])
    if SPARTAN_BROW_SHADOW == 'glass':
        for i in range(N):
            if f[7][i] == 'V': f[7][i] = 'W'
        for i in range(8, 12): f[8][i] = 'W'
    e = [list(r) for r in SPARTAN_SIDE]
    if SPARTAN_BROW_SHADOW == 'glass':
        for i in range(N):
            if e[7][i] == 'V': e[7][i] = 'W'
    b = [list(r) for r in SPARTAN_BACK]
    assert all(len(g) == N and all(len(r) == N for r in g) for g in (f, e, b))
    neck_guard(e, GUARD_WRAP)
    neck_guard(b, [N] * len(GUARD_ROWS))
    t = plain_top()
    for j in range(N):                                                    # the channel front to back: a lit rim
        t[j][5], t[j][6], t[j][12] = 'g', 'p', 'g'                        # and dark wall on the left, the floor,
        for i in range(7, 12): t[j][i] = 'e'                              # a lit wall on the right (user's)
    if SPARTAN_TOP != 'flat':
        for kind in SPARTAN_TOP.split('+'):
            spartan_top_colour(dict(north=f, east=e, south=b, up=t), kind)
    parts = [p for p in SPARTAN_LAYER.split('+') if p != 'none']
    outer = spartan_layer(f, e, b, t, parts) if parts else None
    east, west = sides(e)
    return dict(north=out(f), south=out(b), east=east, west=west, up=out(t), _outer=outer)


# ---------------------------------------------------------------- noble (Emile's EVA helmet, Halo: Reach)
def noble():
    """A visor over nearly the whole front (rounded corners, wrapping onto the sides), a steel band round the head
    over it (lit edge, body, shadow), a short chin under it; a red mark on each side behind the glass."""
    f = shade(blank())
    rrect(f, -1, 4, 19, 16, 'V', cut=2)                                   # (running on round the corners)
    outline(f, 'x')
    for i in range(N): f[1][i], f[2][i], f[3][i] = 'g', 'e', 's'           # the band
    for i in (5, 12): f[17][i] = 'p'
    glint(f)
    e = shade(blank())
    for i in range(N): e[1][i], e[2][i], e[3][i] = 'g', 'e', 's'
    rect(e, 15, 5, 18, 15, 'V')                                           # the wrap: the front's rows at the corner,
    rect(e, 14, 6, 15, 14, 'V')                                           # its back end rounded
    outline(e, 'x')
    rect(e, 6, 6, 10, 12, 'r')                                            # the red mark: its own shaded edge
    for j in range(6, 12): e[j][9] = 'o'
    for i in range(6, 10): e[11][i] = 'o'
    neck_guard(e, GUARD_WRAP)
    east, west = sides(e)
    b = shade(blank())
    for i in range(N): b[1][i], b[2][i], b[3][i] = 'g', 'e', 's'
    neck_guard(b, [N] * len(GUARD_ROWS))
    top = plain_top()
    for j in range(N): top[j][0] = 'g'
    return dict(north=out(f), south=out(b), east=east, west=west, up=out(top))


# ---------------------------------------------------------------- robot (Guy-Manuel's helmet, Daft Punk)
# Round 2 (2026-11-15, ref .scratch/helm7/robot/ref.jpg, the xcoser replica: front, side, back): the reference's big
# shapes: one tall dark visor over nearly the whole front (its top corners rounded off, the dome), a thin frame over
# it, a deep chin band under it; round the corners the visor wraps onto the sides as a D, an ear fin following its
# back edge with the disc (a ring round a lit boss) and the engraved panel under it; on the top and back a raised
# panel (two grooves front to back, closing over the back's band), the standard neck guard. All in gold (user: its
# own recipe with gold, so it doesn't take the paint): drawn in the steel letters, swapped to GOLD at the end.
# Draft knob ROBOT_WRAP: 'wrap' (the glass round the corners onto the sides, as the reference) | 'frame' (a gold
# strip down each front corner, the glass on the front and top only, the side plain round the ear plate).
ROBOT_WRAP = os.environ.get('ROBOT_WRAP', 'frame')   # picked: frame (2026-11-15, user)
# ROBOT_GUARD: the standard neck guard 'slate' (as every helmet) | 'gold' (its shades swapped into the gold).
ROBOT_GUARD = os.environ.get('ROBOT_GUARD', 'slate')
ROBOT_DISC_Y = float(os.environ.get('ROBOT_DISC_Y', '7'))   # the ear disc's centre row (texel coords)
ROBOT_DISC = ['.pppp.',   # the ear disc: a rim lit top-left, shaded bottom-right, round a sunk centre
              'pgggep',
              'pgllep',
              'pgllep',
              'peeelp',
              '.pppp.']
ROBOT_CROWN = int(os.environ.get('ROBOT_CROWN', '11'))   # the glass's last full row on the top (rows front -> back)
# Round 4 (2026-11-15, user: frame picked; "rework the mouth border"): draft knob ROBOT_MOUTH, the visor's bottom edge
# over the chin band: 'shadow' (round 3: a dark border row under the glass) | 'lip' (no border: the chin's lit lip
# right under the glass, its corners rounded) | 'curve' (the glass's bottom rounded up into the corners, the lip
# following it, the chin rising at the sides as the reference's) | 'square' (the glass's corners square, a straight
# lip). Rows of the front's glass from row 12 (columns, end exclusive).
ROBOT_MOUTH = os.environ.get('ROBOT_MOUTH', 'lip')
ROBOT_MOUTHS = {'shadow': {13: (3, 15)}, 'lip': {13: (3, 15)}, 'curve': {12: (3, 15), 13: (5, 13)},
                'square': {}}


def robot():
    wrap = ROBOT_WRAP == 'wrap'
    f, e, top = shade(blank()), shade(blank()), plain_top()
    for j in range(N):                                                    # the top's raised panel: two grooves front
        top[j][3], top[j][4], top[j][14], top[j][15] = 'p', 'h', 'p', 'h'  # to back (the glass covers their front)
    # The glass runs up over the top of the head (round 3, user: "the defining feature"): the front's from its top
    # edge down to the chin band, carried on over the top's front rows, rounded off at its back end (the dome).
    if wrap:
        fr = {**{j: (0, 18) for j in range(0, 13)}, 13: (1, 17)}
        tr = {**{j: (0, 18) for j in range(0, 6)}, 6: (1, 17), 7: (3, 15)}
        er = {**{j: (12, 18) for j in range(0, 7)}, 7: (13, 18), 8: (13, 18), 9: (14, 18), 10: (14, 18),
              11: (15, 18), 12: (16, 18)}                                 # east: its back edge slanting down to the
    else:                                                                 # cheek (top row 0 = the top's column 17)
        fr = {j: (2, 16) for j in range(0, 14)}
        fr.update(ROBOT_MOUTHS[ROBOT_MOUTH])
        k = ROBOT_CROWN                                                   # round 4 (user): further back over the top
        tr = {**{j: (2, 16) for j in range(0, k)}, k: (3, 15), k + 1: (5, 13)}
        er = {}
    for g, rows in ((f, fr), (top, tr), (e, er)):
        for j, (a, b_) in rows.items():
            if b_ > a: rect(g, a, j, b_, j + 1, 'V')
        outline(g, 'x')
    for i in range(N):                                                    # the chin band: its lit top, mid, shade
        f[15][i], f[16][i], f[17][i] = ('g' if ROBOT_MOUTH == 'shadow' else 'e'), 'e', 'l'
    if ROBOT_MOUTH != 'shadow':                                           # the chin's lit lip right under the glass
        for i in range(N):                                                # (no dark border under it), the chin's
            low = [j for j in range(N) if f[j][i] == 'V']                 # gold below it
            if not low: continue
            for j in range(low[-1] + 1, 15):
                f[j][i] = 'g' if j == low[-1] + 1 else 'e'
        for j in range(12, 15):                                           # a border texel left beside the lip (the
            for i in range(N):                                            # rounded corners): the lip's too
                if f[j][i] == 'x' and j + 1 < N and f[j + 1][i] in 'ge' and 1 < i < 16: f[j][i] = 'g'
    glint(f)
    x0, x1, y0, y1 = 5, 13, 3, 15                                         # the ear plate behind the glass's D: a
    rect(e, x0, y0, x1, y1, 'e')                                          # raised slab, lit top / back edges, shaded
    for i in range(x0, x1): e[y0][i], e[y1 - 1][i] = 'g', 'p'             # front / bottom (light from the viewer's
    for j in range(y0 + 1, y1 - 1): e[j][x0], e[j][x1 - 1] = 'h', 'l'     # upper left)
    for i in range(x0 - 1, x1): e[y0 - 1][i] = e[y0 - 1][i] if i < 0 else 'p'   # its seam round the top / back
    for j in range(y0, y1): e[j][x0 - 1] = 'p'
    cx, cy = (x0 + x1) / 2, ROBOT_DISC_Y                                  # the reference's disc: a rim round a
    for j, r in enumerate(ROBOT_DISC):                                    # (drawn, not traced: at 6 texels a traced
        for i, c in enumerate(r):                                         # ring read as an X)
            if c != '.': e[round(cy) - 3 + j][int(cx) - 3 + i] = c
    for i in range(x0 + 1, x1 - 1):                                       # the engraved panel under it (its LED
        e[y1 - 4][i], e[y1 - 2][i] = 'p', 'p'                             # grid: dots between two grooves)
        e[y1 - 3][i] = 'h' if (i - x0) % 2 else 'p'
    neck_guard(e, GUARD_WRAP)
    b = shade(blank())
    for j in range(0, 9):                                                 # the raised panel's grooves down the back
        b[j][3], b[j][4], b[j][14], b[j][15] = 'p', 'h', 'p', 'h'          # (a dark line, its lit far wall)
    for i in range(4, 15): b[9][i], b[10][i] = 'p', 'h'                   # closing over the band
    b[9][3] = b[9][14] = 'p'
    neck_guard(b, [N] * len(GUARD_ROWS))
    if ROBOT_GUARD == 'gold':                                             # the neck guard in gold too
        for g, reach in ((e, GUARD_WRAP), (b, [N, N])):
            for j in range(12, N):
                for i in range(N):
                    g[j][i] = {'n': 'l', 'm': 'p', 'x': 's', 'k': 's'}.get(g[j][i], g[j][i])
    east, west = sides(e)
    gold = lambda rows_: [''.join(GOLD.get(c, c) for c in r) for r in rows_]
    return dict(north=gold(f), south=gold(b), east=gold(east), west=gold(west), up=gold(top))


# ---------------------------------------------------------------- hunter (Samus, Smash Bros. Ultimate)
# Round 2 (2026-11-14, user: "they ain't great, we gotta start somewhere", one by one; the hunter first, after
# .scratch/helm7/hunter_ref.png, Samus's Varia helmet): a smooth dome split by a centre seam that meets an arched
# forehead plate over the visor; the visor wide over the eyes, its bottom closing in under the cheek guards to a narrow
# stem down the middle to the chin (a T); the red cheek guards either side of the stem.
# Round 3 (2026-11-14, user: "fantastic first pass"): the stem's lower half plated over in silver, as the reference's
# (the full T of the first option and the shorter glass of the second, reconciled); the ear guards on the outer layer
# (0.5 px proud, see layer()), the hoses running from under the cheek guards along each side into them instead of
# round the neck; on the back the centre seam stops on the plate line (an inverted T) and the default helmet's slate
# neck guard fills the bottom.


def hose(g, j, i0, i1):
    """A corrugated silver hose running across a face in rows j, j + 1: a rib every other column (lit over its
    shade), the grooves dark."""
    for i in range(i0, i1):
        g[j][i], g[j + 1][i] = ('t', 'u') if i % 2 == 0 else ('v', 'v')


HUNTER_EAR = (9.0, 9.5, 3.8)    # the ear guard on the sides (east texel coords: centre column back -> front, row,
                                # radius): in the middle of the side, high (2026-11-14, user), over the forehead
                                # line's end; the hose climbs to it diagonally
# Draft knob HUNTER_EARS (2026-11-14, user: the raised ears next to the flat hoses feel off, "the disparity"): 'flat'
# (the ears painted on the side, like the hoses) or 'raised' (the hoses up on the outer layer with the ears: the side's
# diagonal runs and the front's stubs). Picked: flat (2026-11-14, user: "both damn good", but the raised hoses end
# abruptly at the front). So the hunter has no outer layer.
HUNTER_EARS = os.environ.get('HUNTER_EARS', 'flat')
HOSE_ROW = 14                   # the hoses' top row (rows 14-15: clear of the pauldrons, which hide the side's bottom
                                # 2 px in a side view)


def hunter():
    f = shade(blank())
    for j in range(0, 3): f[j][8], f[j][9] = 'p', 'h'                     # the dome's centre seam (a groove)
    for k in range(8):                                                    # the forehead plate's arch: from the seam's
        a, b_ = 7 - k, 10 + k                                             # foot out and down to the visor's corners
        j = 3 + k // 2
        for i in (a, b_):
            f[j][i] = 'p'
            if j + 1 < N: f[j + 1][i] = 'h' if f[j + 1][i] not in 'p' else f[j + 1][i]
    for i in (8, 9): f[3][i] = 'p'
    rows = {7: (2, 16), 8: (1, 17), 9: (1, 17), 10: (1, 17), 11: (2, 16), 12: (4, 14), 13: (6, 12),
            14: (7, 11), 15: (7, 11)}
    for j, (a, b_) in rows.items(): rect(f, a, j, b_, j + 1, 'V')
    outline(f, 'x')
    for j in range(N):                                                    # the cheek guards' raised edge: a lit texel
        for i in range(N):                                                # under / beside the visor's border
            if f[j][i] == 'x' and j + 1 < N and f[j + 1][i] not in 'Vx' and j >= 11:
                f[j + 1][i] = 'g' if i < 9 else 'h'
    for i in range(7, 11):                                                # the stem's lower half plated in silver: a
        f[14][i], f[15][i] = ('t' if 7 < i < 10 else 'u'), 'v'            # lit plate over its shadow, its ends a step
                                                                          # darker (2026-11-14, user's edit: even)
    hose(f, HOSE_ROW, 0, 4); hose(f, HOSE_ROW, 14, 18)                    # the hoses out from under the cheek guards
    for i in (4, 13):
        f[HOSE_ROW][i] = f[HOSE_ROW + 1][i] = 'p'                         # the guards' lower corners over them
    glint(f)
    e = shade(blank())
    for i in range(N): e[6][i] = 'p'                                      # the forehead plate's line run round (level
    for i in range(N): e[7][i] = 'h'                                      # with the arch's ends at the front corners)
    cx, cy, r = HUNTER_EAR
    path = []                                                             # the hose: from the front corner up and
    for i in range(N - 1, -1, -1):                                        # back to the ear diagonally (a row up every
        j = HOSE_ROW - (N - 1 - i) // 2                                   # 2 columns), ending under it
        if math.hypot(i + 0.5 - cx, j + 1 - cy) < r - 1: break
        path.append((i, j))
        e[j][i], e[j + 1][i] = ('t', 'u') if i % 2 == 0 else ('v', 'v')
    neck_guard(e, GUARD_WRAP)
    b = shade(blank())
    for j in range(0, 6): b[j][8], b[j][9] = 'p', 'h'                     # the seam down the back, stopping on the
    for i in range(N): b[6][i] = 'p'                                      # plate line (_|_)
    for i in range(N): b[7][i] = 'h'
    neck_guard(b, [N] * len(GUARD_ROWS))
    top = plain_top()
    for j in range(N): top[j][8], top[j][9] = 'p', 'h'
    ear = [['.'] * N for _ in range(N)]                                   # the ear guard, on the outer layer: a
    disc(ear, cx, cy, r, 'e', ring='s', rw=1.0)                           # rounded plate: a dark rim, lit inside it
    for j in range(N):                                                    # on the top-left, shaded on the bottom-
        for i in range(N):                                                # right (a dome), a dark dot in the middle
            d = math.hypot(i + 0.5 - cx, j + 0.5 - cy)
            if ear[j][i] == 'e' and r - 2.2 < d:
                ear[j][i] = 'g' if (i + 0.5 - cx) + (j + 0.5 - cy) < -1 else 'p' if (i + 0.5 - cx) + (j + 0.5 - cy) > 1 else 'e'
    disc(ear, cx, cy, 1.0, 'l')
    for i, j in path:                                                     # the hose's silver collar where it goes in
        for jj, c in ((j, 't'), (j + 1, 'v')):                            # (the rim over the hose's end)
            if ear[jj][i] != '.': ear[jj][i] = c
    empty = lambda: [['.'] * N for _ in range(N)]
    outer = {'east': empty(), 'north': empty(), 'south': empty()}
    clean = shade(blank())
    if HUNTER_EARS == 'raised':                                           # the hoses up onto the layer with the ears:
        hoses = [(j, i) for i, j0 in path for j in (j0, j0 + 1)]          # the side's diagonal run, the front's stubs
        for j, i in hoses:
            outer['east'][j][i], e[j][i] = e[j][i], clean[j][i]
        for j in (HOSE_ROW, HOSE_ROW + 1):
            for i in list(range(0, 4)) + list(range(14, 18)):
                outer['north'][j][i], f[j][i] = f[j][i], clean[j][i]
    for j in range(N):                                                    # the ears: on the layer, or flat on the side
        for i in range(N):
            if ear[j][i] != '.':
                if HUNTER_EARS == 'flat': e[j][i] = ear[j][i]
                else: outer['east'][j][i] = ear[j][i]
    east, west = sides(e)
    return dict(north=out(f), south=out(b), east=east, west=west, up=out(top),
                _outer=outer if HUNTER_EARS != 'flat' else None)


STYLES = {'A': sentinel, 'B': diver, 'C': wrap, 'protector': protector, 'spartan': spartan, 'noble': noble,
          'robot': robot, 'hunter': hunter}


def faces(style, back='plain'):
    d = STYLES[style](back) if style == 'C' else STYLES[style]()
    d.pop('_outer', None)
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
    # 2026-11-13 (user: close it like the camera): the body is a closed box (all round but the inner side against the
    # helmet): its top carries on the side's lit top row, its bottom the ink bottom row, its front and back the
    # side's edge columns. The antennas rise above its top, so they can't share its box (its top would be at their
    # tips): they stay a flat plane in the side's plane, trimmed to their own columns.
    body, aerials = west[7:], [r[2:5] for r in west[:7]]
    edge = [r[0] for r in body]                        # the front column (the back one is the same)
    assert edge == [r[-1] for r in body]
    return [_part('radio', ((-5, 29, 0.5), (-4.5, 32, 3.5)),
                  dict(west=body, up=['n'] * 6, down=['x'] * 6, north=edge, south=edge)),
            _part('radio_aerials', ((-5, 32, 1.5), (-5, 35.5, 3)), dict(west=aerials))]


def camera():
    """A helmet camera on the right side (x+), opposite the radio (2026-11-12, user, after a Halo Reach helmet's: a
    rounded housing, the lens forward, a red lamp): one box 0.5 px off the side, the housing on its side face and
    the lens again on its front face. The lamp is the fire's reserved red, so in game
    it lights with the engine (the fire glowmask)."""
    east = ['.nnnJJ',                                    # columns back -> front (as seen from the right); the
            'nmmmxx',                                    # front column solid, as the front face it meets (user:
            'nmmmxg',                                    # see-through texels there didn't line up with it; no
                                                         # mount tail behind it, user); the back corners rounded
            'nmmmxx',
            '.kkkkk']
    # its front, the housing's full height and depth, from the helmet's side out to the housing's plane (a 1 px lens
    # plate, then one 0.5 px past the housing, didn't line up with it, user): the lamp, the lens, the bottom
    front = ['J', 'x', 'g', 'x', 'k']                  # (one texel across: the housing is 0.5 px off the side)
    # forward, beside the visor at eye level (not mirroring the radio, user). One box 0.5 px off the side, like the
    # radio: its east face is the housing, its north face the front, so the two meet edge to edge by construction
    # (2026-11-13, user: it was a zero-thick side plate plus a zero-deep front plate, the same faces in two cubes; as
    # separate plates 0.25 px apart they had shown a gap). Closed all round but the inner side against the helmet
    # (2026-11-13, user: fill out the top and bottom, then the back): the top carries on the side's top row (the lamp,
    # then lit slate), the bottom its bottom row (dark slate). The rounded back (the back column shorter by a texel at
    # top and bottom) is a second box, the tail, behind the housing's (user: one box's back face left see-through
    # spots in those corners): the housing's back shows only its top and bottom rows above and below the tail.
    tail = [r[0] for r in east[1:-1]]                  # the back column between the rounded corners
    housing = [r[1:] for r in east]
    up = list('JJnnn')                                 # rows front -> back, one texel across
    down = list('kkkkk')                               # rows back -> front
    back = ['n', '.', '.', '.', 'k']                   # the tail covers the middle rows
    return [_part('camera', ((4.5, 28.5, -1), (5, 31, 1.5)), dict(east=housing, north=front, up=up, down=down, south=back)),
            _part('camera_tail', ((4.5, 29, 1.5), (5, 30.5, 2)), dict(east=tail, up=['n'], down=['k'], south=['m'] * 3))]


def _round(g, j, i):
    """The texel the layer's corner column carries on with, next to an edge texel g[j][i]: the same, but a hose keeps
    its ribs going (a rib's lit / mid texel is followed by a groove, a groove by a rib)."""
    c = g[j][i]
    if c in 'tu': return 'v'
    if c == 'v':
        bottom = j > 0 and g[j - 1][i] in 'tuv'
        return 'u' if bottom else 't'
    return c


def layer(style='C'):
    """Draft (2026-11-13, user: the gear's 3D boxes vs one see-through outer layer round the helmet, painted 2D, as
    the extras began): one box 0.5 px out from the helmet all round, like a player's hat layer, its only paint the
    radio's and the camera's side art where their boxes' outer faces were (those lie in its side planes, x +-5), so
    nothing moves. 0.5 px out on top too, so the taller antenna is a texel shorter (user: respect the layer's bounds;
    as boxes it reached 1 px over the helmet's top), its tip on the layer's top edge. Lost against the
    boxes: the camera's lens face forward, the radio's and the camera's tops, bottoms, fronts and backs (edge on,
    from the front or back, they vanish)."""
    x0, y0, z0, x1, y1, z1 = -5, 25, -5, 5, 35, 5
    W, H, D = round((x1 - x0) * 2), round((y1 - y0) * 2), round((z1 - z0) * 2)
    east, west = [list(r) for r in _grid(D, H)], [list(r) for r in _grid(D, H)]
    def stamp(g, art, col, row):
        for j, line in enumerate(art):
            for i, c in enumerate(line):
                if c != '.': g[row + j][col + i] = c
    row = lambda y: round((y1 - y) * 2)                 # the row whose top edge is at y
    # the brow (HELMET_BROW; first: the radio and camera go over the band): the helmet's texel (j, i) is the layer's (j + 1, i + 1) (both 2 per px, the layer 0.5 px
    # bigger each way); at the layer's corners (its first / last column, outside the helmet's faces) each band row
    # carries on round the corner in its colour
    if style == 'C':
        o = wrap(os.environ.get('HELMET_BACK', 'guard'))['_outer']
    else:                                              # a style's own outer art (the hunter's ear guards), no gear
        o = STYLES[style]().get('_outer')
        if o is None:
            return []
    north, south = [list(r) for r in _grid(W, H)], [list(r) for r in _grid(W, H)]
    for face, g in (('north', north), ('east', east), ('south', south)):
        for j in range(N):
            for i in range(N):
                if o[face][j][i] != '.': g[j + 1][i + 1] = o[face][j][i]
            if face != 'east':                         # an edge texel carries on round the corner (a full row:
                if o[face][j][0] != '.': g[j + 1][0] = _round(o[face], j, 0)     # both ends; the hunter's hoses:
                if o[face][j][-1] != '.': g[j + 1][-1] = _round(o[face], j, N - 1)   # theirs)
        if face == 'east':                             # the side's band meets the front's / back's corner texel
            for j in range(N):
                if o['east'][j][-1] != '.': east[j + 1][-1] = _round(o['east'], j, N - 1)
                if o['east'][j][0] != '.': east[j + 1][0] = _round(o['east'], j, 0)
    up = [list(r) for r in _grid(W, D)]
    if o.get('up'):                                    # a style's top (the spartan's cap): rows front -> back, its
        for j in range(N):                             # edge rows / columns carried on to the layer's edges
            for i in range(N):
                if o['up'][j][i] != '.': up[j + 1][i + 1] = o['up'][j][i]
            for i in (0, N - 1):
                if o['up'][j][i] != '.': up[j + 1][0 if i == 0 else W - 1] = o['up'][j][i]
        for i in range(W):
            up[0][i], up[D - 1][i] = up[1][i], up[D - 2][i]
    for j in range(N):                                 # west: the east mirrored (columns front -> back)
        for i in range(N):
            if o['east'][j][i] != '.': west[j + 1][W - 2 - i] = o['east'][j][i]
        if o['east'][j][-1] != '.': west[j + 1][0] = _round(o['east'], j, N - 1)
        if o['east'][j][0] != '.': west[j + 1][-1] = _round(o['east'], j, 0)
    for p in (radio() if style == 'C' else []):        # west: columns front -> back (z0 up)
        (a, b), art = p['box'], p['faces']['west']
        top = b[1]
        if top > y1:                                   # the aerials: drop shaft rows under the tip to fit
            cut = round((top - y1) * 2)
            art, top = art[:1] + art[1 + cut:], y1
        stamp(west, art, round((a[2] - z0) * 2), row(top))
    for p in (camera() if style == 'C' else []):       # east: columns back -> front (z1 down)
        (a, b), art = p['box'], p['faces']['east']
        stamp(east, art, round((z1 - b[2]) * 2), row(b[1]))
    if style != 'C':                                   # a style's art on the faces' top row carries on over the
        for g in (north, south, east, west):           # layer's own top row (the cap meets the top's edge); not
            g[0] = list(g[1])                          # its bottom row (0.5 px under the helmet, in the chest)
    part = _part('layer', ((x0, y0, z0), (x1, y1, z1)), dict(up=[''.join(r) for r in up],
                                                            east=[''.join(r) for r in east],
                                                            west=[''.join(r) for r in west],
                                                            north=[''.join(r) for r in north],
                                                            south=[''.join(r) for r in south]))
    part['hollow'] = True
    return [part]


def extras(kind, style='C'):
    if kind == 'layer':                       # (built only when asked: a style without outer art has none)
        return layer(style)
    return {'none': [], 'cap': cap(), 'radio': radio(), 'both': cap() + radio(),
            'all': cap() + radio() + camera(), 'gear': radio() + camera()}[kind]
