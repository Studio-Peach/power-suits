"""The chaingun for the frame (frame_model.py, TOOL=gun): the third power tool brought over from the big suit.

PICKED (2026-11-22, reworked in the 2D-texture + 0.5 px cutout outer-layer system; user picked GUN_LOOK=2d_copper):
- Base cuff (6x4x6 cutout outer shell over 5x4x5 inner core, y top-4..top): keeps the beloved warm-black stacked-drum
  body with its two horizontal grooves cut out 0.5 px deep, revealing recessed wound copper motor coils (`inner='copper'`,
  no green cuff glow);
- Spinning 6 px barrel cluster (bone `bit`, y top-10..top-4, 10 px total matching rail cannon & flamethrower): four
  1.5x6x1.5 textured cylindrical gunmetal barrels + cold 1x5.5x1 central spinning axle, wrapped in ONE single 5x6x5
  0.5 px cutout outer layer (`rings_outer`) carrying the two slim clamp rings (cool mid ring + heated front ring with
  orange-heated corner bolts `H`, 1.0 px protruding tips);
- Overheat lighting matches the old big-suit chaingun (`tools/make-glowmasks.py`) exactly: upper barrel shafts, mid ring,
  central axle, and black barrel bores stay 100% cold; Stage 1 (`heat`, 30%+) lights the protruding tips orange ->
  yellow-hot; Stage 2 (`heat_barrel`, 55%+) lights the front outer-layer clamp ring (and its bolts) warm orange with a
  3-step alpha fade (210 -> 150 -> 90) right behind it.

Earlier picked design (2026-11-14 / 2026-11-20, GUN_LOOK=doom) and all earlier draft rounds are kept as knobs below.

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
          body_h=4, barrel_l=5, accent='vents', heat='dark', sleeve=False, head_scale=False):
    """The chaingun's parts on an arm centred at x c (right side) whose socket is at y top: the receiver (bone 'tool')
    and the barrels with their rings under it (bone 'bit': they spin). look: GUN_LOOK (below), 'old' the first drafts."""
    if look == '2d_doom': return build_2d_doom(c, top, heat)
    if look == '2d_legion': return build_2d_legion(c, top, heat)
    if look == '2d_vulcan': return build_2d_vulcan(c, top, heat)
    if look == 'r2_oldsuit': return build_r2_classic(c, top, heat, rings='oldsuit', cuff='orig', ring_metal='dark')
    if look == 'r2_2ring': return build_r2_classic(c, top, heat, rings='two', cuff='orig', ring_metal='dark')
    if look == 'r2_2d_cuff': return build_r2_classic(c, top, heat, rings='oldsuit', cuff='cutout', ring_metal='brass')
    if look == 'r2_2d_dark': return build_r2_classic(c, top, heat, rings='two', cuff='cutout', ring_metal='dark')
    if look == 'r3_oldsuit_tight': return build_r2_classic(c, top, heat, rings='oldsuit', cuff='cutout', ring_metal='dark', heat_zone='head_tight')
    if look == 'r3_oldsuit_soft': return build_r2_classic(c, top, heat, rings='oldsuit', cuff='cutout', ring_metal='dark', heat_zone='head_soft')
    if look == 'r3_2ring_tight': return build_r2_classic(c, top, heat, rings='two', cuff='cutout', ring_metal='dark', heat_zone='head_tight')
    if look == 'r3_orig_tight': return build_r2_classic(c, top, heat, rings='oldsuit', cuff='orig', ring_metal='dark', heat_zone='head_tight')
    if look == 'r4_oldsuit': return build_r4_outer_rings(c, top, heat, rings='oldsuit')
    if look == 'r4_2ring': return build_r4_outer_rings(c, top, heat, rings='two')
    if look in ('2d_copper', 'r6_copper'): return build_r4_outer_rings(c, top, heat, rings='two', inner='copper')
    if look == 'r6_copper_red': return build_r4_outer_rings(c, top, heat, rings='two', inner='copper_red', lit=(lamp != 'dark'))
    if look == 'r6_redstone': return build_r4_outer_rings(c, top, heat, rings='two', inner='redstone', lit=(lamp != 'dark'))
    if look != 'old': return doom_build(c, top, look, barrels, handle, top_art, drum, body_h, barrel_l, accent, heat, sleeve, head_scale)
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
    # Stage 1 ('heat', starts at 30%): barrel tips (exact old power_suit make-glowmasks.py colours: orange -> yellow-hot)
    '1': ('55585b', 'heat',        'ffc860', 255),  # legacy doom barrel tip
    '0': ('55585d', 'heat',        'ff6a1a', 255),  # legacy orange tip
    # Cylindrical 3-column shaded barrel tips (cold shades 1 step off lit 62686d / mid 4e5459 / shade 3a4045)
    '(': ('62686e', 'heat',        'ffd87a', 255),  # tip last row, lit edge: bright yellow-hot
    ')': ('4e545a', 'heat',        'ffc860', 255),  # tip last row, mid: yellow-hot (exact old ffc860)
    '[': ('3a4046', 'heat',        'f2b248', 255),  # tip last row, shade edge: warm yellow-hot
    ']': ('62686f', 'heat',        'ff7c24', 255),  # tip 2nd row, lit edge: bright orange
    '{': ('4e545b', 'heat',        'ff6a1a', 255),  # tip 2nd row, mid: orange (exact old ff6a1a)
    '}': ('3a4047', 'heat',        'e85814', 255),  # tip 2nd row, shade edge: deep orange
    '2': ('050506', 'heat',        'ff9a30', 255),  # (legacy doom bore)
    '3': ('0f0e0e', 'heat',        'ff6a1a', 225),  # (legacy doom muzzle underside)
    '$': ('1f1e1a', 'heat',        'ff8c2a', 230),  # (legacy doom muzzle rim)
    '&': ('2e2c28', 'heat',        'ff7a22', 220),  # (legacy doom muzzle outer rim)
    # Stage 2 ('heat_barrel', creeps back from 55%): exact old power_suit alphas (210 / 150 / 90) + front ring colours!
    '6': ('555859', 'heat_barrel', 'ff6a1e', 210),  # legacy under front ring
    '7': ('55585c', 'heat_barrel', 'ff5a18', 150),  # legacy 3rd row
    '8': ('555858', 'heat_barrel', 'ff4a14',  90),  # legacy 4th row
    '9': ('55595a', 'heat_barrel', 'e83c0f',  60),  # (legacy doom upper barrel)
    # Cylindrical 3-column shaded Stage 2 barrel creep (exact old alphas: 210 under ring, 150 above ring, 90 faint)
    'a': ('62686c', 'heat_barrel', 'ff7222', 210),  # under front ring, lit (alpha 210)
    'c': ('4e5458', 'heat_barrel', 'ff6a1e', 210),  # under front ring, mid (alpha 210)
    'e': ('3a4044', 'heat_barrel', 'e65214', 210),  # under front ring, shade (alpha 210)
    'i': ('62676d', 'heat_barrel', 'ff621c', 150),  # 3rd row from tip, lit (alpha 150)
    'j': ('4e5359', 'heat_barrel', 'ff5a18', 150),  # 3rd row from tip, mid (alpha 150)
    'o': ('3a3f45', 'heat_barrel', 'e04612', 150),  # 3rd row from tip, shade (alpha 150)
    'p': ('61686d', 'heat_barrel', 'ff5218',  90),  # 4th row from tip, lit (alpha 90)
    'r': ('4d5459', 'heat_barrel', 'ff4a14',  90),  # 4th row from tip, mid (alpha 90)
    's': ('394045', 'heat_barrel', 'e03a0e',  90),  # 4th row from tip, shade (alpha 90)
    '!': ('2e2c2b', 'heat_barrel', 'f0601e', 255),  # front ring mid (old H('7d888f') -> f0601e)
    '@': ('1f1e1e', 'heat_barrel', 'dd4c14', 255),  # front ring shade/corners (old H('6f797f') -> dd4c14)
    '#': ('2e2c29', 'heat_barrel', 'ff5e1a', 180),  # (legacy)
    '%': ('45413e', 'heat_barrel', 'ff7a2a', 255),  # front ring lit top bevel (old H('89939b') -> ff7a2a)
    'H': ('8a857d', 'heat_barrel', 'ff9a42', 255),  # front ring steel bolts (1 step off h=8a857c; glow bright orange when hot!)
    '^': ('0f0e0c', 'heat_barrel', 'e84c14', 165),  # (legacy)
}

# Export helper for tools/export-frame.py: mask -> {cold_rgb: glow_rgba}
HEAT_GLOW = {
    m: {_c(cold)[:3]: _c(glow)[:3] + (a,) for cold, mask, glow, a in HEAT_SPEC.values() if mask == m}
    for m in ('heat', 'heat_barrel')
}


def _heat_pal(heat):
    out = {}
    for ch, (cold, mask, glow, a) in HEAT_SPEC.items():
        cr, cg, cb, _ = _c(cold)
        if heat == 'hot' or (heat == 'warm' and mask == 'heat'):
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
               accent='vents', heat='dark', sleeve=False, head_scale=False):
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
        if sleeve:
            rows = ['DBBBBBBBBBBD', 'BhCCCCCCCChD',
                    'DCBBBCCCCCDE', 'EDElLLLLlEDE', 'DCBBBCCCCCDE', 'EDElLLLLlEDE', 'DCBBBCCCCCDE', 'EDDDDDDDDDDE']
        faces = dict(faces, north=rows, south=rows, east=rows, west=rows)
    if sleeve:
        faces = dict(faces,
                     up=['B' * 12] + ['B' + 'D' * 10 + 'B'] * 10 + ['B' * 12],
                     down=['D' * 12] + ['D' + 'E' * 10 + 'D'] * 10 + ['D' * 12])
    bw = 3.0 if sleeve else 2.5
    parts = [part('body', ((c - bw, t, -bw), (c + bw, top, bw)), faces)]
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
    # Scaled head (for 6x6 drum): 4x 1.5x1.5 barrels at +-1.25 (span 4.0, 1.0 gap), 4.5 collar, 5.5 muzzle (0.25 inset).
    bo, br = (1.25, 0.75) if (head_scale and barrels == '4') else (1.0, 0.5)
    at = {'4': ((-bo, -bo), (bo, -bo), (bo, bo), (-bo, bo)),
          '3': ((-1.5, 0), (0, 0), (1.5, 0)), '3z': ((0, -1.5), (0, 0), (0, 1.5))}[barrels]
    for k, (dx, dz) in enumerate(at):
        parts.append(part(f'barrel{k}', ((c + dx - br, t - L, dz - br), (c + dx + br, t, dz + br)), bfaces, 'bit'))
    y0 = t - L + 0.5                                         # the block's bottom
    mr = 2.75 if head_scale else 2.25
    cr = 2.25 if head_scale else 1.75
    parts.append(part('muzzle', ((c - mr, y0, -mr), (c + mr, y0 + 2, mr)),
                      {'north': mside, 'south': mside, 'east': mside, 'west': mside,
                       'up': mtop, 'down': mbot}, 'bit'))
    # the collar (a straight row of three reaches z / x +-2: it stands through the collar's sides, fine)
    parts.append(part('muzzle_collar', ((c - cr, y0 + 2, -cr), (c + cr, y0 + 2.5, cr)),
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


# ======================================================================================================================
# 2D-texture + 0.5 px cutout outer-layer redesign (2026-11-22, matching Rail Cannon 2d_hybrid_closed & Flamethrower
# halo_olive). Three distinct concepts behind GUN_LOOK:
# - 2d_doom:   warm-black tactical rotary (4 px cutout cuff w/ recessed emerald vents + 5.5 px 4-barrel rotor + 0.5 px
#              cutout muzzle shroud over hot barrel cluster);
# - 2d_legion: heavy shrouded mech autocannon (3.5 px charcoal/hazard-ochre cuff w/ recessed brass ammo feed + STATIC
#              perforated 5 px cutout cooling jacket + 6 px spinning rotary barrels glowing through the cooling slots);
# - 2d_vulcan: classic long-barrel Gatling minigun (compact 3 px blued-steel/brass cuff w/ brass feed + long 7 px
#              exposed 4-barrel rotor held by a single 0.5 px cutout skeletal clamp-ring & muzzle-brake cage).
# ======================================================================================================================

def _ring_up(lit, top_c, side_c, shade):
    """1-texel hollow top rim for a 0.5 px-proud outer cuff/shroud (inner area '.' so zero coplanar faces)."""
    def fn(w, h):
        g = [['.'] * w for _ in range(h)]
        for i in range(w):
            g[0][i] = lit if i < w - 1 else top_c
            g[h - 1][i] = side_c if i == 0 else shade
        for j in range(1, h - 1):
            g[j][0] = top_c
            g[j][w - 1] = shade
        return g
    return fn


def _cuff_dn_10():
    return ['dddddddddd'] + ['dkkkkkkkkd'] * 8 + ['dddddddddd']


def _barrel_down_3(w, h):
    return ['111', '121', '111']


def _make_2d_base_pal(heat):
    """Shared recessed gunmetal slate + copper + brass + emerald gun_light + HEAT_SPEC palette."""
    return ({k: _c(v) for k, v in {
        # Recessed neutral dark gunmetal slate core (never mixes bluish iron steel)
        'n': '4b5258', 'm': '3b4246', 'k': '2f3437', 'd': '25292c', 'X': '16181a', 'x': '08090a',
        # Rivets / machined bright steel
        'g': 'cfcac0', 'h': '8a857c',
        # Copper / brass ammo & internals
        'b': 'e2c572', 'Z': 'b09044', 'z': '6e5826',
        'f': 'e09868', 'Q': 'c07440', 'q': '7c4824',
        # Emerald gun_light (matches export-tools.py GLOW_MAPS['gun_light'])
        'W': 'c8ffc0', 'L': '3cf060', 'l': '1f8a34',
        # Cold barrel steel
        'K': '55585a',
    }.items()} | _heat_pal(heat) | {'.': '.'})


def build_2d_doom(c, top, heat='dark'):
    """Draft A (2d_doom): Warm-black tactical rotary chaingun in 2D + 0.5 px cutout language (9.5 px total)."""
    P = _make_2d_base_pal(heat) | {k: _c(v) for k, v in {
        'A': '857e72', 'B': '45413d', 'C': '2e2c2a', 'D': '1f1e1c', 'E': '0f0e0d',
    }.items()}
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    none = lambda w, h: ['.' * w] * h
    t = top - 4.0

    # 1. Cuff inner (5x4x5, y top-4..top): recessed dark gunmetal core + deep emerald vent bars + side drive mechanics
    in_fb = [
        'dkkkkkkkkd',
        'dmmmmmmmmd',
        'dXlLWWLlXd',   # upper glowing emerald louver bar (0.5 px deep inside outer slot)
        'dXmmmmmmXd',
        'dkkkkkkkkd',
        'dXlLWWLlXd',   # lower glowing emerald louver bar
        'dXkkkkkkXd',
        'dddddddddd',
    ]
    in_sd = [
        'dkkkkkkkkd',
        'dmmmmmmmmd',
        'dXkxkxkxXd',
        'dXlLWWLlXd',   # recessed emerald status vent matching front/back language
        'dXkxkxkxXd',
        'dkkkkkkkkd',
        'dmmmmmmmmd',
        'dddddddddd',
    ]
    # 2. Cuff outer (6x4x6, y top-4..top): warm-black armor sleeve w/ 0.5 px cutout vent windows & corner bolts
    out_fb = [
        'ABBBBBBBBBBA',
        'BhCCCCCCCCgD',
        'BCX......XCD',   # upper vent cutout exposing recessed emerald bar
        'BCCCCCCCCCCD',
        'BDDDDDDDDDDE',
        'BCX......XCD',   # lower vent cutout exposing recessed emerald bar
        'BhCCCCCCCCgD',
        'EEEEEEEEEEEE',
    ]
    out_sd = [
        'ABBBBBBBBBBA',
        'BhCCCCCCCCgD',
        'BCCCCCCCCCCD',
        'BCX......XCD',   # side drive cutout
        'BCX......XCD',
        'BDDDDDDDDDDE',
        'BhCCCCCCCCgD',
        'EEEEEEEEEEEE',
    ]
    parts = [
        part('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
            'north': in_fb, 'south': in_fb, 'east': in_sd, 'west': in_sd,
            'up': none, 'down': _cuff_dn_10(),
        }),
        part('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': out_fb, 'south': out_fb, 'east': out_sd, 'west': out_sd,
            'up': _ring_up('A', 'B', 'C', 'D'), 'down': none,
        }),
    ]

    # 3. Spinning 4-barrel cluster (4 x 1.5x5.5x1.5 at +-1.25, y top-9.5..top-4.0 -> 3x11 sides, bone 'bit')
    # Rows 0..4 exposed between cuff and muzzle shroud; 5..9 inside muzzle shroud (glow through slots); 10 = hot tip!
    bar_side = lambda w, h: ['9' * w, '8' * w, '7' * w, '6' * w, '6' * w,
                             '!' * w, '!' * w, '!' * w, '!' * w, '$' * w, '1' * w]
    bfaces = {'north': bar_side, 'south': bar_side, 'east': bar_side, 'west': bar_side,
              'up': none, 'down': _barrel_down_3}
    for k, (dx, dz) in enumerate(((-1.25, -1.25), (1.25, -1.25), (1.25, 1.25), (-1.25, 1.25))):
        parts.append(part(f'barrel{k}', ((c + dx - 0.75, top - 9.5, dz - 0.75),
                                         (c + dx + 0.75, t, dz + 0.75)), bfaces, 'bit'))

    # 4. Recessed central muzzle hub (3x2x3 at +-1.5, y top-9.0..top-7.0, zero coplanar w/ barrels)
    hub_sd = lambda w, h: ['@' * w] + ['!' * w] * (h - 2) + ['3' * w]
    hub_dn = lambda w, h: ['&' * w] + ['&' + '3' * (w - 2) + '&'] * (h - 2) + ['&' * w]
    parts.append(part('muzzle_hub', ((c - 1.5, top - 9.0, -1.5), (c + 1.5, top - 7.0, 1.5)), {
        'north': hub_sd, 'south': hub_sd, 'east': hub_sd, 'west': hub_sd,
        'up': lambda w, h: ['!' * w] * h, 'down': hub_dn,
    }, 'bit'))

    # 5. 0.5 px cutout muzzle shroud (5x2.5x5 at +-2.5, y top-9.0..top-6.5 -> 10x5 sides, bone 'bit')
    # Closed corners, clean top collar ring, interior cooling cutouts showing glowing barrels inside!
    muz_sd = [
        '@%%%%%%%%@',
        '%h#....#h@',
        '%!#....#!@',
        '%!!!!!!!!@',
        '3$$$$$$$$3',
    ]
    parts.append(part('muzzle_outer', ((c - 2.5, top - 9.0, -2.5), (c + 2.5, top - 6.5, 2.5)), {
        'north': muz_sd, 'south': muz_sd, 'east': muz_sd, 'west': muz_sd,
        'up': _ring_up('%', '%', '!', '@'), 'down': none,
    }, 'bit'))
    return parts


def build_2d_legion(c, top, heat='dark'):
    """Draft B (2d_legion): Heavy mech shrouded rotary autocannon (9.5 px total).
    Static 0.5 px-cutout perforated cooling jacket with hazard-ochre band wrapping spinning inner barrels, plus a
    recessed brass ammo feed window in the 3.5 px gunmetal cuff."""
    P = _make_2d_base_pal(heat) | {k: _c(v) for k, v in {
        'A': '7b828a', 'B': '4c5259', 'C': '33383e', 'D': '22262b', 'E': '14171a',
        'Y': 'e6a82e', 'y': 'b87e1a', 'o': '784f0e',
    }.items()}
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    none = lambda w, h: ['.' * w] * h
    t = top - 3.5

    # 1. Cuff inner (5x3.5x5, y top-3.5..top -> 10x7 sides): crisp separated brass ammo cartridges on outer side (east)
    in_ammo = [
        'dkkkkkkkkd',
        'dxZbbbfQxd',   # cartridge 1: dark link, bright brass casing, copper bullet tip
        'dxxxxxxxxd',   # crisp dark separator between rounds so each shell reads distinctly
        'dxZbbbfQxd',   # cartridge 2
        'dxxxxxxxxd',
        'dxZbbbfQxd',   # cartridge 3
        'dddddddddd',
    ]
    in_fb = [
        'dkkkkkkkkd',
        'dmmmmmmmmd',
        'dXkkkkkkXd',
        'dXlLWWLlXd',   # recessed glowing emerald ready bar
        'dXkkkkkkXd',
        'dmmmmmmmmd',
        'dddddddddd',
    ]
    in_west = [
        'dkkkkkkkkd',
        'dmmmmmmmmd',
        'dXkxkxkxXd',
        'dXmmmmmmXd',
        'dXkxkxkxXd',
        'dmmmmmmmmd',
        'dddddddddd',
    ]
    # 2. Cuff outer (6x3.5x6, y top-3.5..top -> 12x7 sides): dark tactical gunmetal + ochre accents + crisp cutouts
    out_east = [
        'ABBBBBBBBBBA',
        'BCX......XCD',   # cutout feed port framing the 3 separated brass cartridges
        'BCX......XCD',
        'BCX......XCD',
        'BCX......XCD',
        'BCX......XCD',
        'EEEEEEEEEEEE',
    ]
    out_fb = [
        'ABBBBBBBBBBA',
        'BhYyyyyyyYgD',   # industrial hazard-ochre top collar bar
        'BCCCCCCCCCCD',
        'BCCX....XCCD',   # centered cutout revealing recessed emerald ready bar
        'BCCCCCCCCCCD',
        'BhCCCCCCCCgD',
        'EEEEEEEEEEEE',
    ]
    out_west = [
        'ABBBBBBBBBBA',
        'BhYyyyyyyYgD',
        'BCCX....XCCD',
        'BCCX....XCCD',
        'BCCX....XCCD',
        'BhCCCCCCCCgD',
        'EEEEEEEEEEEE',
    ]
    parts = [
        part('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
            'north': in_fb, 'south': in_fb, 'east': in_ammo, 'west': in_west,
            'up': none, 'down': _cuff_dn_10(),
        }),
        part('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': out_fb, 'south': out_fb, 'east': out_east, 'west': out_west,
            'up': _ring_up('A', 'B', 'C', 'D'), 'down': none,
        }),
    ]

    # 3. STATIC perforated 2D-cutout cooling jacket (5x5x5, y top-8.5..top-3.5 -> 10x10 sides, bone 'tool')
    # Wide stacked cooling windows let the player see the spinning barrels & fiery overheat glow inside!
    shroud_side = [
        'ABBBBBBBBA',
        'BX......XD',   # upper cooling slot (2 texels tall)
        'BX......XD',
        'BhCCCCCCgD',   # mid structural rib w/ corner rivets
        'BX......XD',   # lower cooling slot (2 texels tall)
        'BX......XD',
        'BCCCCCCCCD',
        'oYYyYYyYYo',   # signature industrial hazard-ochre band near muzzle
        'oDyyDDyyDo',   # subtle dark hazard chevron ticks
        'EDDDDDDDDE',   # soot-rimmed muzzle lip (stops 1.0 px above barrel tips)
    ]
    parts.append(part('shroud_outer', ((c - 2.5, top - 8.5, -2.5), (c + 2.5, t, 2.5)), {
        'north': shroud_side, 'south': shroud_side, 'east': shroud_side, 'west': shroud_side,
        'up': none, 'down': none,
    }, 'tool'))

    # 4. Spinning 4-barrel cluster (4 x 1.5x6.0x1.5 at +-1.25, y top-9.5..top-3.5 -> 3x12 sides, bone 'bit')
    # Protrudes 1.0 px out the front of the static jacket so rotation & glowing yellow tips are unmistakable!
    bar_side = lambda w, h: ['9' * w, '8' * w, '8' * w, '7' * w, '7' * w, '6' * w,
                             '6' * w, '!' * w, '!' * w, '$' * w, '1' * w, '1' * w]
    bfaces = {'north': bar_side, 'south': bar_side, 'east': bar_side, 'west': bar_side,
              'up': none, 'down': _barrel_down_3}
    for k, (dx, dz) in enumerate(((-1.25, -1.25), (1.25, -1.25), (1.25, 1.25), (-1.25, 1.25))):
        parts.append(part(f'barrel{k}', ((c + dx - 0.75, top - 9.5, dz - 0.75),
                                         (c + dx + 0.75, t, dz + 0.75)), bfaces, 'bit'))

    # 5. Inner rotary muzzle binder hub (3x1.5x3 at +-1.5, y top-9.0..top-7.5, bone 'bit', zero coplanar w/ barrels)
    hub_sd = lambda w, h: ['@' * w, '!' * w, '3' * w]
    hub_dn = lambda w, h: ['&' * w] + ['&' + '3' * (w - 2) + '&'] * (h - 2) + ['&' * w]
    parts.append(part('muzzle_binder', ((c - 1.5, top - 9.0, -1.5), (c + 1.5, top - 7.5, 1.5)), {
        'north': hub_sd, 'south': hub_sd, 'east': hub_sd, 'west': hub_sd,
        'up': lambda w, h: ['!' * w] * h, 'down': hub_dn,
    }, 'bit'))
    return parts


def build_2d_vulcan(c, top, heat='dark'):
    """Draft C (2d_vulcan): Classic long-barrel Gatling minigun (10.0 px total: compact 3 px blued-steel/brass cuff +
    7 px exposed spinning 4-barrel rotor held by a single 0.5 px cutout skeletal clamp-ring & muzzle-brake cage)."""
    P = _make_2d_base_pal(heat) | {k: _c(v) for k, v in {
        'A': '7d8b99', 'B': '4c5764', 'C': '313942', 'D': '1e242b', 'E': '11151a',
    }.items()}
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    none = lambda w, h: ['.' * w] * h
    t = top - 3.0

    # 1. Compact 3 px cuff inner (5x3x5, y top-3..top -> 10x6 sides): 2 crisp separated brass cartridges on east
    in_ammo = [
        'dkkkkkkkkd',
        'dxZbbbfQxd',   # cartridge 1: link + brass case + copper tip
        'dxxxxxxxxd',   # dark separator
        'dxZbbbfQxd',   # cartridge 2
        'dmmmmmmmmd',
        'dddddddddd',
    ]
    in_fb = [
        'dkkkkkkkkd',
        'dmmmmmmmmd',
        'dXlLWWLlXd',
        'dXlLWWLlXd',
        'dmmmmmmmmd',
        'dddddddddd',
    ]
    in_west = [
        'dkkkkkkkkd',
        'dXkxkxkxXd',
        'dXmmmmmmXd',
        'dXkxkxkxXd',
        'dmmmmmmmmd',
        'dddddddddd',
    ]
    # 2. Compact 3 px cuff outer (6x3x6, y top-3..top -> 12x6 sides): blued-steel armor + warm brass lower drive band
    out_east = [
        'ABBBBBBBBBBA',
        'BCX......XCD',   # cutout framing brass cartridge feed
        'BCX......XCD',
        'BCX......XCD',
        'zZbbbbbbbbZz',   # tarnished brass drive collar band
        'EEEEEEEEEEEE',
    ]
    out_fb = [
        'ABBBBBBBBBBA',
        'BhCCCCCCCCgD',
        'BCCX....XCCD',   # centered emerald status bar cutout
        'BCCX....XCCD',
        'zZbbbbbbbbZz',   # matching brass collar band all round
        'EEEEEEEEEEEE',
    ]
    out_west = [
        'ABBBBBBBBBBA',
        'BhCCCCCCCCgD',
        'BCCX....XCCD',
        'BCCX....XCCD',
        'zZbbbbbbbbZz',
        'EEEEEEEEEEEE',
    ]
    parts = [
        part('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
           'north': in_fb, 'south': in_fb, 'east': in_ammo, 'west': in_west,
            'up': none, 'down': _cuff_dn_10(),
        }),
        part('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': out_fb, 'south': out_fb, 'east': out_east, 'west': out_west,
            'up': _ring_up('A', 'B', 'C', 'D'), 'down': none,
        }),
    ]

    # 3. Long 7 px spinning 4-barrel Gatling rotor (4 x 1.5x7.0x1.5 at +-1.25, y top-10.0..top-3.0 -> 3x14 sides)
    bar_side = lambda w, h: ['9' * w, '9' * w, '8' * w, '8' * w, '8' * w, '7' * w, '7' * w,
                             '7' * w, '6' * w, '6' * w, '!' * w, '!' * w, '$' * w, '1' * w]
    bfaces = {'north': bar_side, 'south': bar_side, 'east': bar_side, 'west': bar_side,
              'up': none, 'down': _barrel_down_3}
    for k, (dx, dz) in enumerate(((-1.25, -1.25), (1.25, -1.25), (1.25, 1.25), (-1.25, 1.25))):
        parts.append(part(f'barrel{k}', ((c + dx - 0.75, top - 10.0, dz - 0.75),
                                         (c + dx + 0.75, t, dz + 0.75)), bfaces, 'bit'))

    # 4. Single 0.5 px cutout skeletal clamp cage (5x6.5x5, y top-9.5..top-3.0 -> 10x13 sides, bone 'bit')
    # Alpha-0 leaves open air along the upper & lower barrel shafts, carving just a mid brass-banded clamp ring
    # (rows 5..6, matching mid_spindle) and a heavy slotted muzzle brake (rows 10..12, matching muzzle_hub)!
    cage_sd = [
        '..........',
        '..........',
        '..........',
        '..........',
        '..........',
        'zZbbbbbbZz',   # mid-shaft brass-banded barrel clamp ring (rows 5..6 -> y top-6.5..top-5.5)
        'E@ZZZZZZ@E',
        '..........',
        '..........',
        '..........',
        '@%%%%%%%%@',   # heavy slotted Gatling muzzle brake (rows 10..12 -> y top-9.5..top-8.0)
        '%h#....#h@',
        '3$$$$$$$$3',
    ]
    parts.append(part('cage_outer', ((c - 2.5, top - 9.5, -2.5), (c + 2.5, t, 2.5)), {
        'north': cage_sd, 'south': cage_sd, 'east': cage_sd, 'west': cage_sd,
        'up': none, 'down': none,
    }, 'bit'))

    # 5. Inner cores behind the two skeletal rings (+-1.5, zero coplanar w/ barrels)
    hub_sd = lambda w, h: ['@' * w] + ['!' * w] * max(0, h - 2) + ['3' * w]
    hub_dn = lambda w, h: ['&' * w] + ['&' + '3' * (w - 2) + '&'] * (h - 2) + ['&' * w]
    parts.append(part('mid_spindle', ((c - 1.5, top - 6.5, -1.5), (c + 1.5, top - 5.5, 1.5)), {
        'north': lambda w, h: ['!' * w] * h, 'south': lambda w, h: ['!' * w] * h,
        'east': lambda w, h: ['!' * w] * h, 'west': lambda w, h: ['!' * w] * h,
        'up': lambda w, h: ['@' * w] * h, 'down': lambda w, h: ['@' * w] * h,
    }, 'bit'))
    parts.append(part('muzzle_hub', ((c - 1.5, top - 9.5, -1.5), (c + 1.5, top - 8.0, 1.5)), {
        'north': hub_sd, 'south': hub_sd, 'east': hub_sd, 'west': hub_sd,
        'up': lambda w, h: ['!' * w] * h, 'down': hub_dn,
    }, 'bit'))
    return parts


def build_r2_classic(c, top, heat='dark', rings='oldsuit', cuff='orig', ring_metal='dark', heat_zone='full'):
    """Round 2/3 (2026-11-22, user: keep the original doom body, replace the chunky muzzle block with slim clamp rings
    like vulcan + the old big-suit chaingun's exposed-barrel silhouette: 4 long barrels, central axle, thin rings,
    protruding hot barrel tips; Round 3: tone overheat down to just the head so the barrel shafts stay cold).
    Total length 10.0 px (4.0 px body + 6.0 px spinning barrel cluster).
    - rings='oldsuit': thin 0.5 px rear collar under body + long exposed barrels + slim 4.5x1.0x4.5 front ring +
                       1.5 px protruding barrel tips (matches model/power_suit.bbmodel chaingun_plate_back/front);
    - rings='two':     slim mid clamp ring (0.5 px) + slim front clamp ring (1.0 px) + 1.0 px protruding barrel tips;
    - cuff='orig':     the exact original 6x4x6 warm-black stacked-drum body w/ emerald vents (GUN_ACCENT=vents);
    - cuff='cutout':   the exact same warm-black body pattern with 0.5 px cutout grooves recessing the emerald vents;
    - ring_metal='dark' (warm-black) | 'brass' (vulcan tarnished brass trim on cool rear/mid ring);
    - heat_zone='full' (R2) | 'head_tight' (tips + front ring only; shafts 100% cold) | 'head_soft' (+1 px fade)."""
    P = _make_2d_base_pal(heat) | {k: _c(v) for k, v in {
        'A': '857e72', 'B': '45413d', 'C': '2e2c2a', 'D': '1f1e1c', 'E': '0f0e0d',
    }.items()}
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    none = lambda w, h: ['.' * w] * h
    t = top - 4.0

    # 1. Body (4.0 px tall, y top-4..top)
    if cuff == 'orig':
        orig_side = [
            'DBBBBBBBBBBD',
            'BhCCCCCCCChD',
            'DCBBBCCCCCDE',
            'EDElLLLLlEDE',
            'DCBBBCCCCCDE',
            'EDElLLLLlEDE',
            'DCBBBCCCCCDE',
            'EDDDDDDDDDDE',
        ]
        orig_up = ['B' * 12] + ['B' + 'D' * 10 + 'B'] * 10 + ['B' * 12]
        orig_dn = ['D' * 12] + ['D' + 'E' * 10 + 'D'] * 10 + ['D' * 12]
        parts = [part('body', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': orig_side, 'south': orig_side, 'east': orig_side, 'west': orig_side,
            'up': orig_up, 'down': orig_dn,
        })]
    else:
        # Exact original warm-black stacked-drum body with ONLY the two emerald vent grooves cut out 0.5 px deep!
        # Uses exact same rich emerald 'L' as the original body (no white hot spot).
        in_side = [
            'DEEEEEEEED',
            'DCCCCCCCCD',
            'DCCCCCCCCD',
            'DElLLLLlED',   # recessed upper emerald vent bar (0.5 px deep, exact original emerald shade)
            'DCCCCCCCCD',
            'DElLLLLlED',   # recessed lower emerald vent bar (0.5 px deep)
            'DCCCCCCCCD',
            'EEEEEEEEEE',
        ]
        out_side = [
            'DBBBBBBBBBBD',
            'BhCCCCCCCChD',
            'DCBBBCCCCCDE',
            'EDE......EDE',   # exact same row 3 groove, alpha-0 cutout exposing recessed emerald bar!
            'DCBBBCCCCCDE',
            'EDE......EDE',   # exact same row 5 groove, alpha-0 cutout exposing recessed emerald bar!
            'DCBBBCCCCCDE',
            'EDDDDDDDDDDE',
        ]
        parts = [
            part('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
                'north': in_side, 'south': in_side, 'east': in_side, 'west': in_side,
                'up': none, 'down': ['D' * 10] + ['D' + 'E' * 8 + 'D'] * 8 + ['D' * 10],
            }),
            part('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
                'north': out_side, 'south': out_side, 'east': out_side, 'west': out_side,
                'up': _ring_up('B', 'B', 'C', 'D'), 'down': none,
            }),
        ]

    # 2. Spinning 6.0 px 4-barrel cluster (4 x 1.5x6.0x1.5 at +-1.25, y top-10.0..top-4.0 -> 3x12 sides, bone 'bit')
    if heat_zone == 'head_tight':
        # Strictly head-only heat: the entire barrel shaft behind the front ring stays 100% cold gunmetal ('K')!
        if rings == 'oldsuit':
            # Front ring covers rows 7..8; protruding tips are rows 9..11 (fade warm orange -> yellow-hot tip!)
            bar_rows = ['K'] * 7 + ['K', 'K', '6', '$', '1']
        else:
            # Front ring covers rows 8..9; protruding tips are rows 10..11
            bar_rows = ['K'] * 8 + ['K', 'K', '$', '1']
    elif heat_zone == 'head_soft':
        # Head + subtle 1 px warm bleed right behind the front ring; rest of shaft stays 100% cold gunmetal ('K').
        if rings == 'oldsuit':
            bar_rows = ['K'] * 5 + ['9', '8', '7', '6', '6', '$', '1']
        else:
            bar_rows = ['K'] * 6 + ['9', '8', '7', '6', '$', '1']
    else:
        if rings == 'oldsuit':
            bar_rows = ['9', '9', '8', '8', '7', '7', '6', '6', '!', '$', '1', '1']
        else:
            bar_rows = ['9', '9', '8', '8', '7', '7', '6', '6', '!', '!', '$', '1']
    bar_side = lambda w, h: [ch * w for ch in bar_rows[:h]]
    bfaces = {'north': bar_side, 'south': bar_side, 'east': bar_side, 'west': bar_side,
              'up': none, 'down': _barrel_down_3}
    for k, (dx, dz) in enumerate(((-1.25, -1.25), (1.25, -1.25), (1.25, 1.25), (-1.25, 1.25))):
        parts.append(part(f'barrel{k}', ((c + dx - 0.75, top - 10.0, dz - 0.75),
                                         (c + dx + 0.75, t, dz + 0.75)), bfaces, 'bit'))

    # 3. Slim central spinning axle between the 4 barrels (1.0 x 5.5 x 1.0 at +-0.5, stopping 0.5 px shy of tips)
    if heat_zone in ('head_tight', 'head_soft'):
        ax_sd = lambda w, h: ['D' * w] * h
        ax_dn = lambda w, h: ['3' * w] * h
    else:
        ax_sd = lambda w, h: ['D' * w] * max(0, h - 4) + ['6' * w, '!' * w, '!' * w, '@' * w][:h]
        ax_dn = lambda w, h: ['3' * w] * h
    parts.append(part('axle', ((c - 0.5, top - 9.5, -0.5), (c + 0.5, t, 0.5)), {
        'north': ax_sd, 'south': ax_sd, 'east': ax_sd, 'west': ax_sd,
        'up': none, 'down': ax_dn,
    }, 'bit'))

    # 4. Slim 4.5x4.5 clamp rings (0.25 px proud of the 4.0x4.0 barrel cluster -> 9 texels wide, clean & lightweight!)
    # Front clamp ring: heats up with the head (Stage 2 on upper bevel/sides, Stage 1 hot orange on bottom rim/underside)
    if heat_zone == 'head_tight':
        # Subtle warm-orange front ring (cool dark top rim so heat stays strictly toward the muzzle tip!)
        front_side = lambda w, h: ['D' + 'B' * (w - 2) + 'D', '@' + '!' * (w - 2) + '@']
        front_up = lambda w, h: [''.join('B' if i in (0, w - 1) or j in (0, h - 1) else 'D' for i in range(w)) for j in range(h)]
        front_dn = lambda w, h: [''.join('&' if i in (0, w - 1) or j in (0, h - 1) else '3' for i in range(w)) for j in range(h)]
    else:
        front_side = lambda w, h: (['@' + '%' * (w - 2) + '@', '3' + '$' * (w - 2) + '3'] if h == 2 else
                                   ['@' + '%' * (w - 2) + '@'])
        front_up = lambda w, h: [''.join('%' if i in (0, w - 1) or j in (0, h - 1) else '@' for i in range(w)) for j in range(h)]
        front_dn = lambda w, h: [''.join('&' if i in (0, w - 1) or j in (0, h - 1) else '3' for i in range(w)) for j in range(h)]

    # Cool rear / mid clamp ring (never glows hot; dark warm-black or vulcan tarnished brass)
    if ring_metal == 'brass':
        cool_side = lambda w, h: ['z' + 'b' * (w - 2) + 'z'] + ['E' + 'Z' * (w - 2) + 'E'] * (h - 1)
        cool_cap = lambda w, h: [''.join('b' if i in (0, w - 1) or j in (0, h - 1) else 'Z' for i in range(w)) for j in range(h)]
    else:
        cool_side = lambda w, h: ['D' + 'B' * (w - 2) + 'D'] + ['E' + 'C' * (w - 2) + 'E'] * (h - 1)
        cool_cap = lambda w, h: [''.join('B' if i in (0, w - 1) or j in (0, h - 1) else 'D' for i in range(w)) for j in range(h)]

    if rings == 'oldsuit':
        # Rear clamp ring (4.5 x 0.5 x 4.5, tucked right under body: old chaingun_plate_back)
        parts.append(part('ring_back', ((c - 2.25, t - 0.5, -2.25), (c + 2.25, t, 2.25)), {
            'north': cool_side, 'south': cool_side, 'east': cool_side, 'west': cool_side,
            'up': none, 'down': cool_cap,
        }, 'bit'))
        # Slim front clamp ring (4.5 x 1.0 x 4.5, 1.5 px back from tips: old chaingun_plate_front!)
        parts.append(part('ring_front', ((c - 2.25, top - 8.5, -2.25), (c + 2.25, top - 7.5, 2.25)), {
            'north': front_side, 'south': front_side, 'east': front_side, 'west': front_side,
            'up': front_up, 'down': front_dn,
        }, 'bit'))
    else:
        # Two slim rings along the shaft (mid 0.5 px + front 1.0 px, 1.0 px back from tips)
        parts.append(part('ring_mid', ((c - 2.25, top - 6.5, -2.25), (c + 2.25, top - 6.0, 2.25)), {
            'north': cool_side, 'south': cool_side, 'east': cool_side, 'west': cool_side,
            'up': cool_cap, 'down': cool_cap,
        }, 'bit'))
        parts.append(part('ring_front', ((c - 2.25, top - 9.0, -2.25), (c + 2.25, top - 8.0, 2.25)), {
            'north': front_side, 'south': front_side, 'east': front_side, 'west': front_side,
            'up': front_up, 'down': front_dn,
        }, 'bit'))
    return parts


def build_r4_outer_rings(c, top, heat='dark', rings='two', inner='copper_red', lit=False):
    """Round 4/5/6 (2026-11-22, user picked B `2ring`, heated orange front-ring bolts, and recessed copper / redstone
    inner cuff replacing the green vents):
    - Original warm-black stacked-drum cuff (5x4x5 inner + 6x4x6 cutout outer with 0.5 px recessed horizontal grooves);
      inner: 'emerald' (R4/R5) | 'copper' (pure copper motor windings) | 'copper_red' (copper coils + redstone trace) |
             'redstone' (dark stator + glowing redstone circuit traces); lit=True previews powered redstone glow;
    - 4 spinning 1.5x6.0x1.5 textured cylindrical barrels + cold central 1.0x5.5x1.0 axle (bone 'bit');
    - ONE single 5.0x6.0x5.0 (0.5 px proud) cutout outer layer (`rings_outer`, bone 'bit') painting the cool mid ring
      and heated front ring (including heated orange corner bolts 'H');
    - Exact old-suit heat lighting (tools/make-glowmasks.py)."""
    # Reserved dark redstone shades (use R/S/T so they never collide with HEAT_SPEC letters!)
    red_pal = ({'R': 'ff5a3a', 'S': 'e02010', 'T': '941008'} if lit else
               {'R': '6e2018', 'S': '521610', 'T': '360d0a'})
    P = _make_2d_base_pal(heat) | {k: _c(v) for k, v in ({
        'A': '857e72', 'B': '45413d', 'C': '2e2c2a', 'D': '1f1e1c', 'E': '0f0e0d',
        # Machined cylindrical gunmetal barrel ramp (lit / glint / mid / groove / shade)
        'G': '747b82', 'U': '62686d', 'M': '4e5459', 'N': '43494e', 'V': '3a4045', 'v': '2c3136',
        # Warm copper motor winding ramp (bright highlight -> deep coil shade)
        'F': 'f0b07a',
    } | red_pal).items()}
    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P)), bone=bone)
    none = lambda w, h: ['.' * w] * h
    t = top - 4.0

    # 1. Original warm-black stacked-drum body w/ 0.5 px recessed horizontal grooves (cuff_inner + cuff_outer)
    # Note: cuff_outer cuts cols 3..8 (out of 0..11), aligning straight onto cuff_inner cols 2..7 (out of 0..9).
    if inner == 'copper':
        # Pure machined copper motor windings (3 crisp wound copper coils per groove, symmetric across cols 2..7)
        slot_top = 'DEfQFFQfED'
        slot_bot = 'DEqFffFqED'
        mid_sep  = 'DCqQQQQqCD'
    elif inner == 'copper_red':
        # Copper motor coils flanking a recessed glowing redstone drive core in the center of each groove
        slot_top = 'DEfQRRQfED'
        slot_bot = 'DEQfSSfQED'
        mid_sep  = 'DCqqTTqqCD'
    elif inner == 'redstone':
        # Dark slate circuit channel with glowing crimson redstone traces & bright redstone nodes
        slot_top = 'DETSrrSTED'.replace('r', 'R')
        slot_bot = 'DESRTTRSED'
        mid_sep  = 'DCkkTTkkCD'
    else:
        slot_top = 'DElLLLLlED'
        slot_bot = 'DElLLLLlED'
        mid_sep  = 'DCCCCCCCCD'

    in_side = [
        'DEEEEEEEED',
        'DCCCCCCCCD',
        'DCCCCCCCCD',
        slot_top,       # row 3: visible through upper 0.5 px cutout groove
        mid_sep,        # row 4: recessed mechanical rib behind divider
        slot_bot,       # row 5: visible through lower 0.5 px cutout groove
        'DCCCCCCCCD',
        'EEEEEEEEEE',
    ]
    out_side = [
        'DBBBBBBBBBBD',
        'BhCCCCCCCChD',
        'DCBBBCCCCCDE',
        'EDE......EDE',
        'DCBBBCCCCCDE',
        'EDE......EDE',
        'DCBBBCCCCCDE',
        'EDDDDDDDDDDE',
    ]
    parts = [
        part('cuff_inner', ((c - 2.5, t, -2.5), (c + 2.5, top, 2.5)), {
            'north': in_side, 'south': in_side, 'east': in_side, 'west': in_side,
            'up': none, 'down': ['D' * 10] + ['D' + 'E' * 8 + 'D'] * 8 + ['D' * 10],
        }),
        part('cuff_outer', ((c - 3.0, t, -3.0), (c + 3.0, top, 3.0)), {
            'north': out_side, 'south': out_side, 'east': out_side, 'west': out_side,
            'up': _ring_up('B', 'B', 'C', 'D'), 'down': none,
        }),
    ]

    # 2. Spinning 6.0 px 4-barrel cluster (4 x 1.5x6.0x1.5 at +-1.25, y top-10.0..top-4.0 -> 3x12 sides, bone 'bit')
    if rings == 'oldsuit':
        bar_rows = ['UNV', 'GMV', 'UMV', 'NNv', 'GMV', 'prs', 'ijo', 'ace', 'ace', ']{}', ']{}', '()[']
        ring_rows = [
            'DBhBBBBhBD',
            '..........',
            '..........',
            '..........',
            '..........',
            '..........',
            '..........',
            '@%%%%%%%%@',
            '@!H!!!!H!@',   # corner bolts 'H' glow bright orange right along with the front ring!
            '..........',
            '..........',
            '..........',
        ]
    else:
        bar_rows = ['UNV', 'GMV', 'UMV', 'NNv', 'UMV', 'UMV', 'prs', 'ijo', 'ace', 'ace', ']{}', '()[']
        ring_rows = [
            '..........',
            '..........',
            '..........',
            '..........',
            'DBhBBBBhBD',   # rows 4..5: cool mid clamp ring w/ steel pins (never glows)
            'ECCCCCCCCE',
            '..........',
            '..........',
            '@%%%%%%%%@',   # rows 8..9: front clamp ring (1.0 px, glows exact old-suit orange in heat_barrel)
            '@!H!!!!H!@',   # corner bolts 'H' glow bright orange right along with the front ring!
            '..........',   # rows 10..11: open air around 1.0 px protruding tips
            '..........',
        ]

    bar_side = lambda w, h: bar_rows[:h]
    # Down bore face: shaded hot tip rim ('('/')'/'[') framing crisp black center bore ('x')!
    bar_dn = lambda w, h: ['(()', ')x[', ')[[']
    bfaces = {'north': bar_side, 'south': bar_side, 'east': bar_side, 'west': bar_side,
              'up': none, 'down': bar_dn}
    for k, (dx, dz) in enumerate(((-1.25, -1.25), (1.25, -1.25), (1.25, 1.25), (-1.25, 1.25))):
        parts.append(part(f'barrel{k}', ((c + dx - 0.75, top - 10.0, dz - 0.75),
                                         (c + dx + 0.75, t, dz + 0.75)), bfaces, 'bit'))

    # 3. Cold central spinning axle (1.0 x 5.5 x 1.0 at +-0.5, subtle machined shading — never glows!)
    ax_sd = lambda w, h: ['CD' if j % 3 == 1 else 'DE' for j in range(h)]
    parts.append(part('axle', ((c - 0.5, top - 9.5, -0.5), (c + 0.5, t, 0.5)), {
        'north': ax_sd, 'south': ax_sd, 'east': ax_sd, 'west': ax_sd,
        'up': none, 'down': lambda w, h: ['CD', 'DE'],
    }, 'bit'))

    # 4. ONE single 0.5 px cutout outer layer (`rings_outer`, 5.0x6.0x5.0 at +-2.5, bone 'bit') carrying the clamp rings!
    parts.append(part('rings_outer', ((c - 2.5, top - 10.0, -2.5), (c + 2.5, t, 2.5)), {
        'north': ring_rows, 'south': ring_rows, 'east': ring_rows, 'west': ring_rows,
        'up': none, 'down': none,
    }, 'bit'))
    return parts
