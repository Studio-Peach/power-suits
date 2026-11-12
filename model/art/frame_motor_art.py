"""Motor-engine backs for the heart engine (frame_model.py, ENGINE=heart, draft knob BACK): 2026-11-11, user, after
the twin-cylinder pack's straight exhausts (column / stack / stub): "none of these evoke that cool mechanical vibe of
a motor engine". So the back is drawn as a motor, not a steam engine: finned cylinders, chrome headers blued by the
heat near the heads, intake trumpets, a supercharger.
- blower (picked; see blower()): a hot-rod V8 (Mad Max): a thin engine block, the fire window in its back, a ribbed
  supercharger on its top, the old suit's exhausts and caps standing out of its back either side;
- vtwin: a motorcycle's: a polished crankcase, the fire in its round cover's porthole, two finned cylinders in a V
  with chrome rocker boxes, a chrome drag pipe down each side;
- inline: a race engine: a block of four finned cylinders over a fire slit, four chrome velocity stacks on top,
  header pipes out of its sides into a collector down each side.
Each keeps the fire (the reserved coal colours, F I J: lit by the burn state in game) and copper inlets on its body's
sides 1 px from the front, where the hoses end (body_x, up_y, low_y). Nothing behind the arm boxes (x <= 6), nothing
below the leg pivots' reach.

Coordinates raw (frame_model.py adds FY), right side +x, the back +z. 2 texels per px. Letters: frame_model.PAL,
the iron ramp (lowercase: chrome w g h e l p s z, slate x d k m n) and EXTRA (heat tint). Faces as frame_model.py's:
north / south as seen from the front / back (south column 0 at -x), east back -> front, west front -> back, up rows
front -> back. Parts turned (rot) are drawn upright: their length along y.
"""
from frame_radial_art import part, grid, disc
from frame_engine_art import _fire

EXTRA = {'a': (0xc8, 0xa0, 0x50),   # heat tint: gold
         'b': (0x7a, 0x6a, 0xa0),   # violet
         'c': (0x4f, 0x6f, 0x9f)}   # blue
TZ = 3


def rows(*rs): return [list(r) for r in rs]


def fins(w, h, lit='g', fin='h', gap='p', shade='l'):
    """Cooling fins: light fin edges over dark gaps, lit on the left, shaded on the right."""
    g = [[fin if j % 2 == 0 else gap] * w for j in range(h)]
    for j in range(h):
        if j % 2 == 0: g[j][0], g[j][-1] = lit, shade
    return g


def chrome(w, h, heat=0, heat_at='bottom', mouth=None):
    """A chrome pipe face: highlight, chrome, shade across; the heat tint (gold, violet, blue) over `heat` rows at one
    end; soot at the mouth."""
    ramp = ['w', 'g'] + ['h'] * max(0, w - 3) + ['e'] if w >= 3 else ['w', 'e'][:w] if w == 2 else ['g']
    g = [list(ramp) for _ in range(h)]
    tint = ['a', 'b', 'c']
    for k in range(min(heat, h)):
        j = h - 1 - k if heat_at == 'bottom' else k
        for i in range(w): g[j][i] = tint[min(2, k * 3 // max(1, heat))] if i else 'w'
    if mouth is not None:
        j = 0 if mouth == 'top' else h - 1
        g[j] = ['P'] * w
    return g


def pipe(name, box, heat_at='bottom', heat=3, mouth='top', rot=None, origin=None, mirror=True):
    def paint(f, w, h):
        if f in ('up', 'down'):
            if (f == 'up') == (mouth == 'top'):
                g = grid(w, h, 'P')
                if w > 2 and h > 2: g[h // 2][w // 2] = 'X'
                return g
            return grid(w, h, 'p')
        return chrome(w, h, heat, heat_at, mouth)
    return part(name, box, paint, mirror=mirror, rot=rot, origin=origin)


def inlets(side, D, H, y1, ys):
    """Copper inlets on a body's side face (east: columns back -> front; west: front -> back), in its front 1 px, as
    the hose arriving there (frame_heart_art: 1.5 px from y up, an ink line above and below; user 2026-11-11: they
    were 1 px tall, the hose wider)."""
    for y in ys:
        j0 = round((y1 - (y + 2)) * 2)                      # from the ink row over the hose down
        for k, c in enumerate(('X', 'f', 'Q', 'R', 'X')):
            j = j0 + k
            if not 0 <= j < H * 1: continue
            if j == 0: c = 'f'          # at the body's top edge the hose is still coming down: copper (its ink is on the top)
            for i in range(2):
                side['east'][j][D - 1 - i] = c
                side['west'][j][i] = c


def door(w, h):
    """The fire window: a steel frame, the coals behind two grate bars, an ash lip."""
    fire = ('J', 'J', 'I', 'I', 'F', 'F', 'F')
    fr = [fire[round(k * (len(fire) - 1) / max(1, h - 4))] for k in range(h - 3)]
    return [['G'] + ['W'] * (w - 2) + ['G']] + [['G'] + list(r) + ['G'] for r in _fire(w - 2, rows=fr, bars={1, w - 4} if w >= 7 else set())] + \
        [['G'] + ['U'] * (w - 2) + ['G'], ['X'] * w]


def put(g, x, y, block):
    for j, r in enumerate(block):
        for i, c in enumerate(r):
            if c != ' ' and 0 <= y + j < len(g) and 0 <= x + i < len(g[0]): g[y + j][x + i] = c


# ---------------------------------------------------------------- blower (hot-rod V8)
# 2026-11-11, user, picked over vtwin and inline: but the supercharger and scoop on top were too tall, no zoomies
# ("not a fan of the rods at the sides"), the block flatter and thinner ("so it doesn't look like a block appended to
# the back of the suit"), and an exhaust for the smoke (the game puffs it up out of two pipe tops, ExhaustSmoke).
# Then (user: the short stubs had no hole; "bring back the style of the old exhausts and the little box on top", the
# exhausts "extruding out of the back of the engine a bit, as if the two columns painted on were 3D"): the old suit's
# exhaust pipes and caps, their art at the frame's density (its 3 x 11 px pipe -> 1.5 x 11, every row doubled; its
# 4 x 1 x 4 cap -> 2 x 1 x 2, the hole in its top), where the block's cylinder columns were painted, sunk 0.5 px into
# it and standing 1 px out of its back, up past its top. Their caps' tops (raw y 27.5, x +-3.5, z 6) are where the
# frame's smoke comes from. Everything at or above the helmet's bottom (raw 25.5) stays behind its back (z >= 4.5).
def blower(suit_faces=None, cx=6.0):
    # Then (user): wider, the exhausts shorter, the supercharger on the block's top, off the fire window (the part that
    # lights up); then the block taller, the exhausts wider, the supercharger standing on the block (it hung behind it):
    # a 10 x 8 x 2.5 block (the abdomen's width), the fire window across most of its back between the pipes, the
    # supercharger on its top, the pipes 2 px round under 2.5 px caps.
    P = []
    # then (user): no scoop; it went 1 px higher, but there the supercharger is level with the helmet's back (raw
    # 25.5 up: everything behind z 4.5) and only fit on the back half of the block's top, hanging off its back; so
    # back down (user): the supercharger on the block's whole top, its own top at the helmet's bottom.
    # then (user: the hoses down the back showed 1 px of their 1.5 beside the block, which covers x 4.5-5; keep it 10
    # wide, "it's fine if the cable connects at the top as well a bit"): above the block they show whole
    # (frame_heart_art.harness_back), their inner half lands on its top corners (copper there), the outer half goes
    # on down beside it into the side inlets
    X, Y0, Y1, Z1 = 5, 16, 24, 5.5                          # the block: 10 x 8 x 2.5
    W, H, D = 20, 16, 5
    PX0, PX1 = 2.5, 4.5                                     # the pipes (right side), on whole texels of its back

    def block(f, w, h):
        if f == 'south':                                    # column 0 at -x
            g = grid(w, h, 'N')
            g[0] = ['O'] * w
            for c in (round((X - PX1) * 2) - 1, round((X - PX0) * 2), round((X + PX0) * 2) - 1, round((X + PX1) * 2)):
                if 0 <= c < w:
                    for j in range(1, h - 1): g[j][c] = 'X' # the pipes' shadow beside them (inside the block's sides)
            put(g, (w - 8) // 2, 2, door(8, 11))            # the fire window, between the pipes
            put(g, 0, 13, rows('O' * w, ('N' + 'NYN' * w)[:w - 1] + 'N', 'X' * w))
            return g
        if f in ('east', 'west'):
            g = grid(w, h, 'N'); g[0] = ['O'] * w; g[-1] = ['X'] * w
            return g
        if f == 'up':                                       # rows front -> back; where the hoses land: copper (the hose's
            g = grid(w, h, 'N'); g[0] = ['O'] * w           # 1.5 px in from the chest's side cx, over the block), and the
            n = round((X - (cx - 1.5)) * 2)                 # ink line along its inner side beside it (slim: 1 px lands)
            for i in range(n):
                for c in (i, w - 1 - i): g[0][c], g[1][c] = 'Q', 'R'
            for c in (n, w - 1 - n): g[0][c] = g[1][c] = 'X'
            return g
        return grid(w, h, 'X')
    b = part('block', ((-X, Y0, TZ), (X, Y1, Z1)), block)
    inlets(b['faces'], D, H, Y1, (22, 18))
    P.append(b)

    def blow(f, w, h):                                      # 4 x 1.5 x 2.5: ribbed, a belt and pulley on its back
        if f == 'south':
            g = grid(w, h, 'O')
            for j in range(h): g[j][0], g[j][-1] = 'N', 'X'
            g[h // 2][w // 2 - 1], g[h // 2][w // 2] = 'h', 'p'
            g[0] = ['W'] * w
            return g
        if f in ('east', 'west', 'north'):
            return [['W'] * w] + [['O' if j % 2 else 'N'] * w for j in range(1, h)]
        if f == 'up':
            g = grid(w, h, 'N'); g[0] = ['O'] * w
            return g
        return grid(w, h, 'X')
    P.append(part('supercharger', ((-2, Y1, TZ), (2, Y1 + 1.5, Z1)), blow))

    # the exhausts: the old suit's pipe and cap art at the frame's 2 texels per px (its rows doubled, its middle
    # column too: 2 px round; the cap's middle column and row: 2.5 px), one plain row left out (10 px tall)
    keep = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10]
    wide = [0, 1, 1, 2]
    old = suit_faces('exhaust_r', cols={f: wide for f in ('north', 'south', 'east', 'west', 'up', 'down')},
                     rows={**{f: keep for f in ('north', 'south', 'east', 'west')}, 'up': wide, 'down': wide})
    cw = [0, 1, 2, 2, 3]
    cap = suit_faces('exhaust_cap_r', cols={f: cw for f in ('north', 'south', 'east', 'west', 'up', 'down')},
                     rows={'up': cw, 'down': cw})
    dbl = lambda g: [r for r in g for _ in range(2)]
    pipe_art = {f: (dbl(old[f]) if f not in ('up', 'down') else old[f]) for f in old}
    cap_art = {f: (dbl(cap[f]) if f not in ('up', 'down') else cap[f]) for f in cap}
    P.append(part('exhaust', ((PX0, Y0 + 0.5, 5), (PX1, Y0 + 10.5, 7)), lambda f, w, h: pipe_art[f], mirror=True))
    P.append(part('exhaust_cap', ((PX0 - 0.25, Y0 + 10.5, 4.75), (PX1 + 0.25, Y0 + 11.5, 7.25)), lambda f, w, h: cap_art[f],
                  mirror=True))
    return P, X, 22, 18, Y1


# ---------------------------------------------------------------- V-twin (motorcycle)
def vtwin():
    P = []
    X, Y0, Y1, Z0, Z1 = 3, 17, 21, 3, 7.5                   # the crankcase: 6 x 4 x 4.5
    W, H, D = 12, 8, 9

    def case(f, w, h):
        if f == 'south':                                    # its round cover, the fire in its porthole
            g = grid(w, h, 'l')
            g[0] = ['g'] * w; g[-1] = ['p'] * w
            disc(g, w / 2, h / 2, 3.9, 'g', ring='e', rw=0.8)
            disc(g, w / 2, h / 2, 2.6, 'F', ring='Y', rw=0.9)
            disc(g, w / 2, h / 2, 1.6, 'I', ring='J', rw=0.6)
            g[h // 2 - 1][w // 2 - 1] = g[h // 2][w // 2] = 'F'
            for i, j in ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)): g[j][i] = 'Y'
            return g
        if f in ('east', 'west'):
            g = [['g'] * w] + [['h'] * w for _ in range(h - 3)] + [['e'] * w, ['p'] * w]
            return g
        if f == 'up':
            g = grid(w, h, 'h'); g[0] = ['g'] * w
            return g
        return grid(w, h, 'p')
    c = part('crankcase', ((-X, Y0, Z0), (X, Y1, Z1)), case)
    inlets(c['faces'], D, H, Y1, (20, 18))
    P.append(c)

    def cyl(f, w, h):                                       # 3 x 6 x 3, finned all round
        if f in ('up', 'down'): return grid(w, h, 'p')
        return fins(w, h)
    def head(f, w, h):                                      # the rocker box: chrome, a lit top edge, two bolts
        if f == 'up':
            g = grid(w, h, 'g'); g[0] = ['w'] * w
            g[1][1] = g[h - 2][w - 2] = 'Y'
            return g
        if f == 'down': return grid(w, h, 'p')
        return [['w'] * w] + [['g'] + ['h'] * (w - 2) + ['e'] for _ in range(h - 2)] + [['l'] * w]
    # their feet apart (the two mirrored cylinders must not overlap: their faces would share planes)
    O = (1.75, 21, 6.25)
    P.append(part('cylinder', ((0.25, 20.5, 4.75), (3.25, 26.5, 7.75)), cyl, mirror=True, rot=[0, 0, -22], origin=O))
    P.append(part('rocker', ((0, 26.5, 4.5), (3.5, 28, 8)), head, mirror=True, rot=[0, 0, -22], origin=O))
    # a drag pipe down each side: from beside the head down past the crankcase, blued at the top, sooty at the mouth
    P.append(pipe('header', ((3.5, 24, 6), (4.5, 26.5, 7)), heat_at='top', heat=3, mouth=None, rot=[0, 0, -40],
                  origin=(4, 26.5, 6.5)))
    P.append(pipe('drag_pipe', ((4.5, 15, 6), (5.5, 24.5, 7)), heat_at='top', heat=0, mouth='bottom'))
    return P, X, 20, 18, 21


# ---------------------------------------------------------------- inline (race engine)
def inline():
    P = []
    X, Y0, Y1, Z1 = 4, 17, 25, 7                            # the block: 8 x 8 x 4
    W, H, D = 16, 16, 8

    def block(f, w, h):
        if f == 'south':
            g = grid(w, h, 'N')
            g[0] = ['O'] * w
            for k in range(4): put(g, 1 + k * 4 - (1 if k > 1 else 0) + (1 if k > 1 else 0), 1, fins(3, 7))
            put(g, 2, 8, rows('G' + 'W' * 10 + 'G'))
            put(g, 2, 9, [['G'] + list(r) + ['G'] for r in _fire(10, rows=('J', 'I', 'F'), bars={2, 7})])
            put(g, 2, 12, rows('G' + 'U' * 10 + 'G'))
            put(g, 0, 13, rows('O' * 16, 'NYNNYNNYYNNYNNYN', 'X' * 16))
            return g
        if f in ('east', 'west'):
            g = grid(w, h, 'N'); g[0] = ['O'] * w
            put(g, 0, 13, rows('O' * 8, 'N' * 8, 'X' * 8))
            return g
        if f == 'up':
            g = grid(w, h, 'N'); g[0] = ['O'] * w
            return g
        return grid(w, h, 'X')
    b = part('block', ((-X, Y0, TZ), (X, Y1, Z1)), block)
    inlets(b['faces'], D, H, Y1, (22, 18))
    P.append(b)

    def stem(f, w, h): return chrome(w, h) if f not in ('up', 'down') else grid(w, h, 'p')
    def flare(f, w, h):
        if f == 'up':
            g = grid(w, h, 'X')
            for j in range(h):
                for i in range(w):
                    if i in (0, w - 1) or j in (0, h - 1): g[j][i] = 'g'
            return g
        if f == 'down': return grid(w, h, 'h')
        return [['w'] * w]
    for k, x in enumerate((-3, -1, 1, 3)):                  # velocity stacks: a stem and a flared lip, chrome
        P.append(part(f'stack{k}', ((x - 0.5, 25, 5.5), (x + 0.5, 26.5, 6.5)), stem))
        P.append(part(f'lip{k}', ((x - 0.75, 26.5, 5.25), (x + 0.75, 27, 6.75)), flare))
    # headers: two pipes out of each side of the block into a collector down its side, blued where they leave it
    for k, y in enumerate((23, 20.5)):
        P.append(pipe(f'header{k}', ((4, y, 5.5), (5.5, y + 1, 6.5)), heat_at='top', heat=0, mouth=None,
                      rot=None))
    # the collector 1.5 deep round the 1 px headers (no shared planes where they join)
    P.append(pipe('collector', ((5, 15.5, 5.25), (6, 24, 6.75)), heat_at='top', heat=2, mouth='bottom'))
    return P, X, 22, 18, 25


DESIGNS = {'blower': blower, 'vtwin': vtwin, 'inline': inline}


def build(design, suit_faces=None, chest_x=6.0):
    """(parts, body half width, upper inlet y, lower inlet y, body top y). suit_faces: frame_model's reader of the big suit's art."""
    return blower(suit_faces, chest_x) if design == 'blower' else DESIGNS[design]()
