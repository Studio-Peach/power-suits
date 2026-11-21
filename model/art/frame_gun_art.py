"""The chaingun for the frame (frame_model.py, TOOL=gun): the third power tool brought over from the big suit.

PICKED (2026-11-14, user: "this is the one"; updated 2026-11-20, user: `GUN_ACCENT=vents` + overheat glow): GUN_LOOK=doom
(after the Doom 2016 chaingun, .scratch/gun/ref_doom.png), GUN_BARRELS=4, GUN_TOP=stack, GUN_ACCENT=vents, GUN_HEAT=dark:
a warm-black 5 x 4 x 5 body, a lit top edge and two bolts a side over the band / groove pair three times with emerald vent
slits in the two upper grooves (`gun_light`); four 1 x 1 px barrels on the spinning bone, no ring halfway; the stepped
muzzle (collar, 4.5 x 2 block, chamfer, bolts, solid sides with no front vents so the barrel assembly heats uniformly) painted with reserved cold
shades (`HEAT_SPEC`) that `tools/export-frame.py` turns into `power_frame_glow_heat` and `power_frame_glow_heat_barrel`.
Built by doom_build() below; the sections before it are the earlier rounds (GUN, GUN_BODY), kept as knobs.

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


def build(c, top, lamp='red', kind='A', body='ref', look='old', barrels='4', handle='paint', top_art='rust', drum='dark',
          body_h=4, barrel_l=5, accent='vents', heat='dark'):
    """The chaingun's parts on an arm centred at x c (right side) whose socket is at y top: the receiver (bone 'tool')
    and the barrels with their rings under it (bone 'bit': they spin). look: GUN_LOOK (below), 'old' the first drafts."""
    if look != 'old': return doom_build(c, top, look, barrels, handle, top_art, drum, body_h, barrel_l, accent, heat)
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


# A new reference (GUN_LOOK; 2026-11-14, user: not convinced by the GUN_BODY drafts; reference .scratch/gun/ref_doom.png,
# the Doom (2016) chaingun, turned barrels-down in .scratch/gun/doom_rot.png). Its parts on the slot, as the rancher's:
# - the receiver: a boxy rear housing at the arm (rows 0-2: a panel and a round dial on the outer side), then the
#   ribbed drum (a lit ring, the band with the reference's 'XX' plate on the outer side, the carrier ring at the bottom);
# - the gun's top (the back): the carry handle along it; its bottom (the front): the ammo box, rust-orange (the
#   reference's warm underside: its accent colour, as the chainsaw's orange) with the bent copper feed pipe;
# - the barrels: three round the axis (the reference's), a dark clamp ring halfway and the muzzle block, chunky, its
#   corners lit green (the reference's two green lights: the signature), the barrels' ends 0.5 px under it.
# All in the reference's warm black (a brown-black, worn silver edges), not the frame's blue-grey steel.
# Drafts: doom (as above) | doom4 (B's four barrels, picked before, in the block) | doom3d (doom, the carry handle a
# real loop 1 px proud on the back: the reference's silhouette). 'old' the bodies above (GUN, GUN_BODY).
DOOM = {k: _c(v) for k, v in {
    'A': '857e72', 'B': '45413d', 'C': '2e2c2a', 'D': '1f1e1c', 'E': '0f0e0d',   # warm black: worn edge .. deepest
    'K': '55585a', 'x': '050505',                                                # barrels, a bore
    'o': 'c2581f', 'u': '7a2e12', 'v': '41180b',                                 # the rusty underside: glow, rust, shade
    'f': 'd9a060', 'Q': 'a8703a', 'q': '6b4422',                                 # the copper pipe
    'g': 'cfcac0', 'h': '8a857c',                                                # the dial, the XX marks
    'W': 'c8ffc0', 'L': '3cf060', 'l': '1f8a34'}.items()} | {'.': '.'}          # the muzzle's green lights
D_OUTER = ['ACCCCCCCuv',       # (back -> front) the housing: its top edge worn, a panel with a dial, the ammo box's rust
           'ACBBBBDCov',
           'ACBgCDDCou',
           'DBBBBBBBBD',       # the drum's rear ring
           'DBDBDBDBCE',       # its band: the XX marks, embossed (light on dark read as a checkerboard grille)
           'DDBDDDBDCE',
           'DBDBDBDBCE',
           'EDDDDDDDDE']       # the carrier ring
D_INNER = ['vuCCCCCCCA',       # (front -> back) the same housing, a plain panel; the drum's band ribbed
           'voCDBBBBCA',
           'uoCDDDDDCA',
           'DBBBBBBBBD',
           'DCBBCCCCDE',
           'EDDDDDDDDE',
           'DCBBCCCCDE',
           'EDDDDDDDDE']
D_BACK = ['DCCDABDCCD',        # (inner -> outer) the carry handle along the gun's top, its shadow beside it
          'DCCDABDCCD',
          'DCCDABDCCD',
          'DBBBBBBBBD',
          'DCBBCCCCDE',
          'EDDDDDDDDE',
          'DCBBCCCCDE',
          'EDDDDDDDDE']
D_FRONT = ['vuooooouuv',       # (outer -> inner) the ammo box's underside in rust, the copper pipe out of it, bending
           'vuoofQouuv',
           'DCCCfQqqCD',
           'DBBBBBBBBD',
           'DCBBCCCCDE',
           'EDDDDDDDDE',
           'DCBBCCCCDE',
           'EDDDDDDDDE']
D_FACES = {'south': D_BACK, 'east': D_OUTER, 'west': D_INNER, 'north': D_FRONT, 'up': ['D' * 10] * 10,
           'down': ['EDDDDDDDDE'] + ['DC' + 'E' * 6 + 'CD'] * 8 + ['EDDDDDDDDE']}


# Round 3 (2026-11-14, user: keep the four barrels; no XX; the top half reworked: the rust ammo box and the copper pipe
# didn't read, "can't tell what the brass part is"). The drum (rows 3-7) is the same on every side now, plain; the top
# half (rows 0-2, the rear housing at the arm) GUN_TOP:
# - plain: a dark housing, a lit top edge, a bolt at each end, a shadow seam under it;
# - vents: the same, cut with vertical vent slits (the reference's rear block);
# - fins: the drive motor: cooling fins running along the gun (lit / dark columns), as a real rotary gun's rear;
# 'rust' round 2's (XX dropped). The back keeps the carry handle down its middle (or the 3D loop, GUN_HANDLE=3d).
DRUM = ['DBBBBBBBBD', 'DCBBCCCCDE', 'EDDDDDDDDE', 'DCBBCCCCDE', 'EDDDDDDDDE']
TOPS = {
    'plain': dict(side=['DBBBBBBBBD', 'BhCCCCCChD', 'EDDDDDDDDE'],
                  back=['DBBDABDBBD', 'BhCDABDChD', 'EDDDABDDDE']),
    'vents': dict(side=['DBBBBBBBBD', 'BCECECECCD', 'BCECECECCD'],
                  back=['DBBDABDBBD', 'BECDABDECD', 'BECDABDECD']),
    'fins':  dict(side=['DADADADADE'] + ['DBDBDBDBDE'] * 2,     # (the fins' ends lit, their sides dimmer: all-lit
                  back=['DADDABDADE'] + ['DBDDABDBDE'] * 2)}    # stripes outshone the muzzle)


# Round 4 (2026-11-14, user: plain picked, but "a bit plain, too uniform between the two halves"): the drum in its own
# metal, shaded round (dark edges, a highlight left of the middle: the housing is flat and matte, the drum a turned
# part), under a deep seam row that splits the halves. GUN_DRUM: bronze (the reference's warm drum metal) | steel (the
# iron armour's) | polished (the housing's black, worn bright); 'dark' round 3's (the housing's paint, banded).
DRUMS = {'bronze':   dict(R='a0785a', r='7a5a44', s='5a4234', t='3e2d24', y='22180f'),
         'steel':    dict(R='9fa4a9', r='757c85', s='58606a', t='3c424c', y='22262e'),
         'polished': dict(R='8a847a', r='635e57', s='48443f', t='2e2c2a', y='151413')}
CYLD = 'tsrRrsssty'                      # a side's columns, round
DRUM_ROUND = ['E' * 10,                  # the seam between the halves
              'srrRrrrrrs',              # the drum's front lip, lit
              CYLD, CYLD,
              'ytttttttty']              # its bottom edge into the barrel carrier

# Round 5 (2026-11-14, user: not the drum, the top half was to be replaced; the drum stays round 3's banded black).
# The housing set apart from the drum by its tone and shape, the back's carry handle cut into each (cols 3-6):
# - steel: the iron armour's steel (the arm's metal running into the gun; the black drum below);
# - panel: a lighter matte grey (the reference's rear block is lighter than its drum), worn top edge, bolts;
# - angular: the black, a chamfered plate (lit bevels narrowing to the arm: the reference's angled cowl).
DOOM.update({k: _c(v) for k, v in {'M': '9fa4a9', 'm': '757c85', 'n': '58606a', 'N': '3c424c', 'Z': '22262e',
                                    'P': '6a655e', 'p': '57534d'}.items()})
# The housing a real half: rows 0-3 (as drawn first, rows 0-2, it read as a band over the drum); the drum rows 4-7
# (DRUM4: its ring, a band, a groove, a band).
DRUM4 = ['DBBBBBBBBD', 'DCBBCCCCDE', 'EDDDDDDDDE', 'DCBBCCCCDE']
def _handle(rows, edge='D'): return [r[:3] + edge + 'AB' + edge + r[7:] for r in rows]
for _k, _side in {'steel': ['MmmmmmmmmN', 'mgnnnnnngN', 'mnnnnnnnnN', 'NNNNNNNNNZ'],
                  'panel': ['APPPPPPPPB', 'PgppppppgB', 'PppppppppB', 'BBBBBBBBBD'],
                  'angular': ['DDDABBADDD', 'DDABBBBADD', 'DABBBBBBAD', 'ABCCCCCCBA']}.items():
    TOPS[_k] = dict(side=_side, back=_handle(_side, 'Z' if _k == 'steel' else 'D'), drum=DRUM4)

# Round 6 (2026-11-14, user: none of the tops yet; an ammo counter in red pixel digits, like the Halo rifle's?). The
# back (the gun's top: the face the third-person view sees, the arm hanging) becomes the counter's display, in place of
# the carry handle; the other sides are the plain top over the banded drum. Two seven-segment digits, 3 x 5 texels (the
# smallest that read at the model's 2 texels a px; 00-99, '--' endless), upright with the arm hanging. In game the
# segments would be tiny glowing cubes the renderer shows / hides from a synced count; drawn here as paint ("60").
# GUN_COUNTER: dim (unlit segments a dark red, an LED display) | off (unlit segments black) | raised (dim, in a display
# housing 0.5 px proud of the back, 4.5 x 3.5: Halo's counter module).
DOOM.update({k: _c(v) for k, v in {'R': 'ff5a3c', 'r': '3c1611'}.items()})
SEGS = {'a': [(0, 0), (1, 0), (2, 0)], 'b': [(2, 0), (2, 1), (2, 2)], 'c': [(2, 2), (2, 3), (2, 4)],
        'd': [(0, 4), (1, 4), (2, 4)], 'e': [(0, 2), (0, 3), (0, 4)], 'f': [(0, 0), (0, 1), (0, 2)],
        'g': [(0, 2), (1, 2), (2, 2)]}
DIGITS = {'0': 'abcdef', '1': 'bc', '2': 'abged', '3': 'abgcd', '4': 'fgbc', '5': 'afgcd', '6': 'afgedc', '7': 'abc',
          '8': 'abcdefg', '9': 'abcdfg', '-': 'g'}


def digit(ch, dim):
    """A digit's 3 x 5 texels: lit segments 'R', unlit ones 'r' (dim) or the window's black 'E'."""
    g = [['E'] * 3 for _ in range(5)]
    for sg, cells in SEGS.items():
        for x, y in cells:
            if sg in DIGITS[ch]: g[y][x] = 'R'
            elif dim and g[y][x] != 'R': g[y][x] = 'r'
    return [''.join(r) for r in g]


def counter(text, dim, w):
    """The display, w wide (10 the back face, 9 the raised housing) x 7: a bezel (lit top), the digits in a black
    window, 2 / 1 texels apart. Rows reversed left to right: the gun is on the left arm, which mirrors the art."""
    a, b = digit(text[0], dim), digit(text[1], dim)
    gap = 'E' * (w - 8)
    rows = ['D' + 'B' * (w - 2) + 'D'] + ['D' + a[j] + gap + b[j] + 'D' for j in range(5)] + ['D' * (w - 1) + 'E']
    return [r[::-1] for r in rows]

# Round 7 (2026-11-14, user: drop the counter, too big, and it can't be smaller at 2 texels a px; "the last four rows
# of the body, repeat them a third time, leaving just the top different"): GUN_TOP=stack, every side the drum's band /
# groove pair three times (rows 2-7) under the plain top's two rows (a lit edge, a bolt at each end). The back the same
# (the painted carry handle would be a 2-row stub there).
STACK = ['DBBBBBBBBD', 'BhCCCCCChD'] + ['DCBBCCCCDE', 'EDDDDDDDDE'] * 3
TOPS['stack'] = dict(side=STACK[:2], back=STACK[:2], drum=STACK[2:])

def doom_faces(top, drum='dark', show='60'):
    if top in ('dim', 'off', 'raised'):   # the counter (GUN_COUNTER): the plain top on the sides, the display on the back
        side = TOPS['plain']['side'] + DRUM
        back = (counter(show, top != 'off', 10) + ['EDDDDDDDDE'] if top != 'raised' else
                ['DCCCCCCCCD'] * 3 + DRUM)   # (under the housing)
        return dict(D_FACES, east=side, west=side, north=side, south=back)
    if drum != 'dark':
        t = TOPS[top]
        return dict(D_FACES, east=t['side'] + DRUM_ROUND, west=t['side'] + DRUM_ROUND, north=t['side'] + DRUM_ROUND,
                    south=t['back'] + DRUM_ROUND)
    if top == 'rust':
        f = dict(D_FACES)
        f['east'] = D_OUTER[:3] + DRUM
        return f
    t = TOPS[top]
    d = t.get('drum', DRUM)
    return dict(D_FACES, east=t['side'] + d, west=t['side'] + d, north=t['side'] + d, south=t['back'] + d)

def ring_d(w, h):        # the clamp ring's side, dimmer than ring() (a bright ring read as a white band)
    return ['B' * (w - 1) + 'C'] + ['C' * (w - 1) + 'D'] * (h - 1)


# Round 2 (2026-11-14, user: the four barrels; no clamp ring halfway; a more detailed muzzle, its green light in the
# middle of each side; three barrels maybe, but straight, not turned). GUN_BARRELS=4 (the square) | 3 (a straight row
# across, x: all three seen from behind) | 3z (the row front to back, z: the reference's side view); GUN_HANDLE=paint
# (on the back's art) | 3d (the loop, doom3d). The muzzle, stepped: a collar 3.5 x 0.5 x 3.5 where the barrels go in,
# the block 4.5 x 2 x 4.5 (a lit chamfer round its top, a bolt at each upper corner of a side, the green light 1 x 3 in
# a dark housing in each side's middle, a shadow row under it), the barrels' ends 0.5 px under it.
def muzzle_side(w, h):   # 9 x 4: chamfer, bolts, the light in its housing (cols 3-5), the bottom's shadow
    m = w // 2
    rows = ['D' + 'B' * (w - 2) + 'D',
            'B' + 'h' + 'C' * (m - 3) + 'EWE' + 'C' * (w - m - 4) + 'h' + 'D'] + \
           ['B' + 'C' * (m - 2) + 'ELE' + 'C' * (w - m - 3) + 'D'] * (h - 3) + \
           ['E' + 'D' * (m - 2) + 'ElE' + 'D' * (w - m - 3) + 'E']
    assert all(len(r) == w for r in rows), rows
    return rows


def muzzle_top(w, h):    # the chamfer round the top, a bolt head inset at each corner, the collar's shadow inside
    return [''.join('B' if i in (0, w - 1) or j in (0, h - 1) else 'h' if i in (1, w - 2) and j in (1, h - 2)
                    else 'C' if i in (1, w - 2) or j in (1, h - 2) else 'D' for i in range(w)) for j in range(h)]


def muzzle_bottom(w, h):  # the face the barrels poke through: a rim, recessed dark inside
    return [''.join('C' if i in (0, w - 1) or j in (0, h - 1) else 'E' for i in range(w)) for j in range(h)]


def collar(w, h):        # the collar's side: lit top row, dark under
    return ['C' * (w - 1) + 'D'] + ['D' * (w - 1) + 'E'] * (h - 1)


# Round 8 (2026-11-14, user: now that tool bodies have their own heights, see the chaingun's lower): GUN_BODY_H (px)
# the body's height, the stack's band / groove pair repeated to fill it (3 px: twice); GUN_BARREL_L the barrels'
# length (5: the gun 1 px higher | 6: the muzzle where it was).
#
# Round 9 (2026-11-20, user: emerald hints on the base + restore the old suit's overheating glow on the barrels/muzzle;
# follow-up: no front vents on the muzzle so the whole barrel assembly heats up uniformly):
# GUN_ACCENT: 'vents' (default: emerald slits tucked into the base's horizontal grooves) | 'strip' | 'twins' | 'muzzle'.
# GUN_HEAT: 'dark' (game default: reserved shades 1 step off cold metal so cold barrels look identical, lit by
#           export-frame.py into power_frame_glow_heat + power_frame_glow_heat_barrel) |
#           'hot' (review preview: blends the full overheat glow directly onto the texture).
BASE_ACCENTS = {
    'strip': ['DBBBBBBBBD', 'BhCCCCCChD',
              'DCBEWWECDE', 'EDDELLEDDE', 'DCBELLECDE', 'EDDELLEDDE', 'DCBEllECDE', 'EDDDDDDDDE'],
    'vents': ['DBBBBBBBBD', 'BhCCCCCChD',
              'DCBBCCCCDE', 'EDElLLlEDE', 'DCBBCCCCDE', 'EDElLLlEDE', 'DCBBCCCCDE', 'EDDDDDDDDE'],
    'twins': ['DBBBBBBBBD', 'BhCCCCCChD',
              'DEWECCEWED', 'DELEDDELED', 'DELECCELED', 'DELEDDELED', 'DElECCElED', 'EDDDDDDDDE'],
}

# Reserved heat colours (all 1 step off K / x / B / C / D / E and unused elsewhere in power_frame.png):
# letter -> (cold hex, mask name, glow hex, glow alpha)
HEAT_SPEC = {
    # Stage 1 ('heat', starts at 30%): barrel tips, bores, muzzle bottom rim & underside (uniform around the front)
    '1': ('55585b', 'heat',        'ffc860', 255),  # barrel tip (row 9, 0.5 px past muzzle): yellow-hot
    '2': ('050506', 'heat',        'ff9a30', 255),  # barrel bore (down face): orange-yellow
    '3': ('0f0e0e', 'heat',        'ff6a1a', 225),  # muzzle recessed underside + bottom corners: hot orange
    '$': ('1f1e1a', 'heat',        'ff8c2a', 230),  # muzzle bottom rim (row 3): bright orange
    '&': ('2e2c28', 'heat',        'ff7a22', 220),  # muzzle underside outer rim
    # Stage 2 ('heat_barrel', creeps back from 55%): muzzle sides & top, collar, exposed barrels (rows 3->0) uniformly
    '6': ('555859', 'heat_barrel', 'ff6a1e', 220),  # barrel row 3 (above collar)
    '7': ('55585c', 'heat_barrel', 'ff5a18', 170),  # barrel row 2
    '8': ('555858', 'heat_barrel', 'ff4a14', 115),  # barrel row 1
    '9': ('55595a', 'heat_barrel', 'e83c0f',  60),  # barrel row 0 (under base)
    '!': ('2e2c2b', 'heat_barrel', 'ff6a1e', 210),  # muzzle_collar top/side + muzzle top inner ring + muzzle lower side
    '@': ('1f1e1e', 'heat_barrel', 'f05818', 185),  # muzzle_collar shade + muzzle top centre + muzzle side shade edge
    '#': ('2e2c29', 'heat_barrel', 'ff5e1a', 180),  # muzzle upper side wall (uniform across full width)
    '%': ('45413e', 'heat_barrel', 'ff5a18', 155),  # muzzle top chamfer & lit side edge (no cold grey outline)
    '^': ('0f0e0c', 'heat_barrel', 'e84c14', 165),  # muzzle_collar bottom corner
}

# Export helper for tools/export-frame.py: mask -> {cold_rgb: glow_rgba}
HEAT_GLOW = {
    m: {_c(cold)[:3]: _c(glow)[:3] + (a,) for cold, mask, glow, a in HEAT_SPEC.values() if mask == m}
    for m in ('heat', 'heat_barrel')
}


def _heat_pal(heat):
    out = {}
    for ch, (cold, _, glow, a) in HEAT_SPEC.items():
        cr, cg, cb, _ = _c(cold)
        if heat == 'hot':
            gr, gg, gb, _ = _c(glow)
            f = a / 255.0
            out[ch] = (round(cr * (1 - f) + gr * f), round(cg * (1 - f) + gg * f), round(cb * (1 - f) + gb * f), 255)
        else:
            out[ch] = (cr, cg, cb, 255)
    return out


def barrel_heated(w, h):  # 2 x 10: rows 0..3 creep up from collar, 4..8 inside muzzle, 9 = tip past muzzle
    # Rows 0..3 are exposed between base and collar; 4..8 sit inside collar/muzzle; row 9 pokes 0.5 px below muzzle.
    rows = ['9' * w, '8' * w, '7' * w, '6' * w] + ['K' * w] * max(0, h - 5) + ['1' * w]
    return rows[:h]


def muzzle_side_solid(w, h):  # 9 x 4: clean solid muzzle (no front vents); heats uniformly across its full width
    rows = ['@' + '%' * (w - 2) + '@',
            '%' + 'h' + '#' * (w - 4) + 'h' + '@'] + \
           ['%' + '!' * (w - 2) + '@'] * (h - 3) + \
           ['3' + '$' * (w - 2) + '3']
    assert all(len(r) == w for r in rows), rows
    return rows


def muzzle_top_heated(w, h):  # heats uniformly across the whole muzzle top (very visible from cockpit)
    return [''.join('%' if i in (0, w - 1) or j in (0, h - 1) else 'h' if i in (1, w - 2) and j in (1, h - 2)
                    else '!' if i in (1, w - 2) or j in (1, h - 2) else '@' for i in range(w)) for j in range(h)]


def muzzle_bottom_heated(w, h):  # recessed underside glows orange uniformly so the four yellow-hot barrel tips pop
    return [''.join('&' if i in (0, w - 1) or j in (0, h - 1) else '3' for i in range(w)) for j in range(h)]


def collar_heated(w, h):
    return ['!' * (w - 1) + '@'] + ['@' * (w - 1) + '^'] * (h - 1)


def doom_build(c, top, look, barrels='4', handle='paint', top_art='rust', drum='dark', body_h=4, barrel_l=5,
               accent='vents', heat='dark'):
    if look == 'doom4': barrels = '4'                       # (round 1's names)
    if look == 'doom3d': handle = '3d'
    P = DOOM | {k: _c(v) for k, v in DRUMS.get(drum, {}).items()} | _heat_pal(heat)
    part = lambda name, box, faces, bone='tool', rot=0: dict(drill.part(name, box, _paint(faces, P), rot), bone=bone)
    t, L = top - body_h, barrel_l
    faces = doom_faces(top_art, drum)
    if body_h != 4:
        assert top_art == 'stack', 'only the stack is drawn for other heights'
        n = round(body_h * 2)
        assert n % 2 == 0 and n >= 4, n
        rows = STACK[:2] + STACK[2:4] * ((n - 2) // 2)
        faces = dict(faces, north=rows, south=rows, east=rows, west=rows)
    if accent in BASE_ACCENTS:
        assert body_h == 4, 'base accents are drawn for 4 px body'
        rows = BASE_ACCENTS[accent]
        faces = dict(faces, north=rows, south=rows, east=rows, west=rows)
    parts = [part('body', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), faces)]
    one = lambda ch: (lambda w, h: [ch * w] * h)
    heated = accent != 'muzzle' or heat == 'hot'
    if heated:
        bfaces = {'north': barrel_heated, 'south': barrel_heated, 'east': barrel_heated, 'west': barrel_heated,
                  'up': one('D'), 'down': one('2')}
        mside = muzzle_side if accent == 'muzzle' else muzzle_side_solid
        mtop, mbot, mcol, mcol_up = muzzle_top_heated, muzzle_bottom_heated, collar_heated, one('!')
    else:
        bfaces = {'north': one('K'), 'south': one('K'), 'east': one('K'), 'west': one('K'), 'up': one('D'), 'down': one('x')}
        mside, mtop, mbot, mcol, mcol_up = muzzle_side, muzzle_top, muzzle_bottom, collar, one('C')
    at = {'4': ((-1, -1), (1, -1), (1, 1), (-1, 1)),        # centres (dx, dz), all 1 x 1 px, none turned
          '3': ((-1.5, 0), (0, 0), (1.5, 0)), '3z': ((0, -1.5), (0, 0), (0, 1.5))}[barrels]
    for k, (dx, dz) in enumerate(at):
        parts.append(part(f'barrel{k}', ((c + dx - 0.5, t - L, dz - 0.5), (c + dx + 0.5, t, dz + 0.5)), bfaces, 'bit'))
    y0 = t - L + 0.5                                         # the block's bottom
    parts.append(part('muzzle', ((c - 2.25, y0, -2.25), (c + 2.25, y0 + 2, 2.25)),
                      {'north': mside, 'south': mside, 'east': mside, 'west': mside,
                       'up': mtop, 'down': mbot}, 'bit'))
    # the collar (a straight row of three reaches z / x +-2: it stands through the collar's sides, fine)
    parts.append(part('muzzle_collar', ((c - 1.75, y0 + 2, -1.75), (c + 1.75, y0 + 2.5, 1.75)),
                      {'north': mcol, 'south': mcol, 'east': mcol, 'west': mcol, 'up': mcol_up, 'down': one('E')}, 'bit'))
    if top_art == 'raised':   # the counter's housing, 4.5 x 3.5, 0.5 px proud of the back, centred on it
        disp = counter('60', True, 9)
        parts.append(part('counter', ((c - 2.25, top - 3.75, 2.5), (c + 2.25, top - 0.25, 3)),
                          {'south': lambda w, h: disp, 'north': one('.'),
                           'east': lambda w, h: ['B'] + ['D'] * (h - 1), 'west': lambda w, h: ['B'] + ['D'] * (h - 1),
                           'up': one('B'), 'down': one('E')}))
    if handle == '3d':   # the carry handle, a loop 1 px proud of the back over the housing (rows 0-2 + 1 px)
        side_e = lambda w, h: ['AB'] + ['B.'] * (h - 2) + ['BD']      # (back -> front: the bar, then the gap)
        side_w = lambda w, h: ['BA'] + ['.B'] * (h - 2) + ['DB']
        parts.append(part('handle', ((c - 0.5, top - 2.5, 2.5), (c + 0.5, top - 0.5, 3.5)),
                          {'south': lambda w, h: ['A' * (w - 1) + 'B'] + ['B' * (w - 1) + 'D'] * (h - 1),
                           'north': one('.'), 'east': side_e, 'west': side_w,
                           'up': lambda w, h: ['C' * w, 'A' * w], 'down': lambda w, h: ['D' * w, 'E' * w]}))
    return parts
