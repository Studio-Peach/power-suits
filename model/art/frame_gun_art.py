"""The chaingun for the frame (frame_model.py, TOOL=gun): the third power tool brought over from the big suit.

2026-11-14 (user: the chaingun next; reference .scratch/gun/ref.png, a matte black six-barrel minigun: a cylinder
receiver under a flat top plate with a carry handle, a khaki drive motor and a bent feed pipe under it, a rear grip
with a red trigger (left out: see OUTER), the barrels held by a carrier at the receiver, a clamp ring halfway and a disc at the muzzle).
Built in the tools' slot (power-suits-frame.md, Tools): the body (the receiver) takes the fist's place, 5 x 4 x 5, and
the barrels grow from its bottom, straight down the arm, on the `bit` bone (they spin about the arm's axis, y).
The reference turned barrels-down as the chainsaw was: the gun's rear at the top (the arm), its muzzle at the bottom,
its top (the carry handle) facing back (raised to fire, the arm's back faces up), its bottom (the motor) the front.

Drafts (GUN):
- A six: six 1 x 1 px barrels round the axis (the reference's), a ring halfway and one near the muzzle (the barrels
  1 px past it), all black;
- B four: four barrels in a square (no turned boxes: they read as pixels, not as six round ones);
- C steel: A in the frame's iron steel instead of black (the colour test: black is the reference's, steel the armour's).
The body's paint is the same in all three.

Coordinates raw, right arm (+x; the left mirrors), centred on the arm's axis (x c, z 0). Faces as frame_drill_art.py
(north / south as seen from the front / back, east back -> front, west front -> back, up / down rows front -> back).
"""
import math
import frame_drill_art as drill

_c = drill._c
# The gun's metal: A lit edge, B lit, C body, D shade, E deepest (bores, gaps). 'black' the reference's matte black
# (a blue-grey black, so its shading still reads), 'steel' the iron armour's ramp (frame_iron_art.PAL).
METAL = {'black': dict(A='6a7077', B='454a50', C='2e3237', D='202327', E='131517'),
         'steel': dict(A='9fa4a9', B='757c85', C='58606a', D='3c424c', E='22262e')}
OTHER = {'Y': 'a89160', 'b': 'd9c17a', 'Z': '6a5838', 'f': 'e09868', 'Q': 'c07440',   # brass cases (lit, mid, shade), copper tips
         'g': 'cdcfcf', 'h': '9fa4a9', 'p': '58606a',        # bolts and the feed pipe (bare steel)
         'T': 'cdbd93', 't': 'a99a73', 'U': '7a6e52',        # the drive motor's khaki
         'x': '0b0c0d'}                                       # a bore


def pal(metal, lamp):
    W_, L_, _ = drill.LAMPS[lamp]
    return {k: _c(v) for k, v in (METAL[metal] | OTHER | {'W': W_, 'L': L_}).items()} | {'.': '.'}


# The receiver, 10 x 8 texels a side (row 0 at the arm: the gun's rear; row 7 its front, where the barrels leave).
# back (the gun's top, inner -> outer): the top plate, its edge lit, the carry handle along it (two feet, the grip
# between, lit on its left), bolts at the plate's front corners
BACK = ['DCCCCCCCCD',
        'CBBBDDBBBD',
        'CBBDABDBBD',
        'CBBDABDBBD',
        'CBBDABDBBD',
        'CBBBDDBBBD',
        'CgBBBBBBgD',
        'DDDDDDDDDE']
# the outer side (back -> front: column 0 the gun's top): the plate's edge down the back, a silver hex bolt at its
# front end (the reference's), the cylinder's panel seam, the motor's khaki end at the front, the carrier ring along
# the bottom
OUTER = ['BCCCCCCCDD',
         'BCCCCCCCCD',   # (no red trigger: next to the front's lamp the two read as eyes over the motor's mouth)
         'BCDCCCCCCD',
         'BCDCCCTTTT',   # the motor's end (it runs to the front's outer edge)
         'BCDCCCTttt',
         'gCDCCCtttU',
         'BCDCCCUUUU',
         'EDDDDDDDDE']
# the inner side (front -> back): the cylinder, its seam and two rivets, the plate's edge at the back
INNER = ['DCCCCCCCCB',
         'DCCCCCCCCB',
         'DCCCCCDCCB',
         'DCpCCCDCCB',
         'DCCCCCDCCB',
         'DCpCCCDCCB',
         'DCCCCCDCCB',
         'EDDDDDDDDE']
# the front (the gun's bottom, outer -> inner): the khaki drive motor
# under the receiver's rear (a block on the outer half: lit top, shade under, an end bolt; centred with the lamp over
# it, the first draft read as a face), its feed pipe running down and in
FRONT = ['DCCCCCCCCD',
         'CCCCCCCCCD',
         'CCCCCCCCCD',
         'TTTTtCCCCD',
         'TttttUCCCD',
         'tgtttUCCCD',
         'UUUUhhhpCD',
         'EDDDDDDhpE']
UP = ['D' * 10] * 10
# underneath, the front of the receiver round the barrels: the carrier's face, a dark ring, the bores' shadow
DOWN = ['EDDDDDDDDE'] + ['DC' + 'E' * 6 + 'CD'] * 8 + ['EDDDDDDDDE']
BODY = {'south': BACK, 'east': OUTER, 'west': INNER, 'north': FRONT, 'up': UP, 'down': DOWN}


# New bodies (GUN_BODY; 2026-11-14, user: B's four barrels, but not the body: 'ref' above, the reference's parts
# painted on, read as a black box with a khaki patch). Drafts, all black, the four barrels under them:
# - drum: the receiver as the reference's round housing: every side shaded as a cylinder (dark at its edges, lit left
#   of the middle: from any side the corners read round), a riveted panel seam round it, the barrel carrier a lit
#   band round its bottom; the top plate a flat strip down the back. Nothing else;
# - belt: drum, an ammo belt running down the outer side into it (brass cases, copper tips, dark links: the gun's
#   signature colour, as the chainsaw's orange; it feeds from the arm, the ammo from the pilot's inventory);
# - split: the drive motor over the barrel carrier: its top half ribbed (cooling ribs), a dark seam, the bottom half
#   a plain heavy band with a bolt at each end.
CYL = 'DCBAABCCDE'                       # a side's columns, shaded round
def _drum(seam_bolts=(2, 7)):
    seam = ''.join('p' if i in seam_bolts else 'D' for i in range(10))   # (dark 'E' with bright bolts read as a visor slit)
    return ['D' * 9 + 'E', CYL, CYL, seam, CYL, CYL, 'A' * 9 + 'B', 'D' * 9 + 'E']
DRUM_BACK = ['DCCBggBCDE'] + ['DCCBAABCDE'] * 5 + ['A' * 9 + 'B', 'D' * 9 + 'E']   # the top plate strip, two bolts
def _belt(rows):   # the outer side's columns 4-8 (back -> front): a round a row (a link, case, tip), lit and shaded in
    # turn, the belt from the top edge (the arm) into the carrier band
    return [r[:4] + ('EbbYf' if j % 2 == 0 else 'EYZZQ' if j < 6 else r[4:9]) + r[9:] if j < 6 else r for j, r in enumerate(rows)]
RIB = 'DACACACACE'
SPLIT = ['D' * 9 + 'E', RIB, RIB, RIB, 'E' * 10, 'A' * 9 + 'B', 'ChCCCCCChD', 'D' * 9 + 'E']
def bodies(kind):
    if kind == 'ref': return BODY
    if kind == 'split':
        f = dict(south=SPLIT, east=SPLIT, west=SPLIT, north=SPLIT)
    else:
        d = _drum()
        f = dict(south=DRUM_BACK, east=_belt(d) if kind == 'belt' else d, west=d, north=d)
    return f | {'up': UP, 'down': DOWN}


def _paint(faces, P):
    for f, rows in faces.items(): assert callable(rows) or all(len(r) == len(rows[0]) for r in rows), f
    return lambda f, w, h: [[P[ch] for ch in r] for r in (faces[f](w, h) if callable(faces[f]) else faces[f])]


def barrel(w, h):   # a barrel's side: one colour (2026-11-14, user; the lit / shaded columns read as stripes)
    return ['C' * w] * h


def ring(w, h):     # a ring's side: a lit top row over the body, the corner column shaded
    return ['A' * (w - 1) + 'B'] + ['C' * (w - 1) + 'D'] * (h - 1)


def ring_cap(w, h):  # its top / bottom: the plate, an edge round it
    return [''.join('D' if i in (0, w - 1) or j in (0, h - 1) else 'C' for i in range(w)) for j in range(h)]


def build(c, top, lamp='red', kind='A', body='ref'):
    """The chaingun's parts on an arm centred at x c (right side) whose socket is at y top: the receiver (bone 'tool')
    and the barrels with their rings under it (bone 'bit': they spin)."""
    metal = 'steel' if kind == 'C' else 'black'
    P = pal(metal, lamp)
    part = lambda name, box, faces, bone='tool', rot=0: dict(drill.part(name, box, _paint(faces, P), rot), bone=bone)
    t = top - 4                                            # the receiver's bottom: the barrels hang from it
    parts = [part('body', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), bodies(body))]
    # the barrels' length, px (1 past the muzzle ring): 5 (2026-11-14, user: shorter; the first drafts' 7 hung far
    # under the arm)
    L = 5
    bore = lambda w, h: ['x' * w] * h
    cap = lambda w, h: ['D' * w] * h
    bfaces = {'north': barrel, 'south': barrel, 'east': barrel, 'west': barrel, 'up': cap, 'down': bore}
    if kind == 'B':                                        # four, square round the axis
        for k, (dx, dz) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1))):
            parts.append(part(f'barrel{k}', ((c + dx - 0.5, t - L, dz - 0.5), (c + dx + 0.5, t, dz + 0.5)), bfaces, 'bit'))
    else:                                                  # six round it at 1.5 px, each turned to face out
        for k in range(6):
            a = 30 + 60 * k                                # (30: none on the x / z axes, clear of the rings' sides)
            # placed on +x then turned about the axis (the bone's origin) by a: frame_model turns it -rot about y
            parts.append(part(f'barrel{k}', ((c + 1.0, t - L, -0.5), (c + 2.0, t, 0.5)), bfaces, 'bit', rot=a))
    rf = {'north': ring, 'south': ring, 'east': ring, 'west': ring, 'up': ring_cap, 'down': ring_cap}
    for name, y in (('ring_mid', t - 2), ('ring_muzzle', t - L + 1)):
        parts.append(part(name, ((c - 2.25, y - 0.5, -2.25), (c + 2.25, y, 2.25)), rf, 'bit'))
    return parts
