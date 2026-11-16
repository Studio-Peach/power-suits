#!/usr/bin/env python3
"""Builds model/power_frame.bbmodel and power_frame_slim.bbmodel: the Fallout-style exosuit FRAME (no armour) around a
real-scale pilot, Steve (the wide build) or Alex (the slim build, BUILD).

Run: python3 model/art/frame_model.py        (writes both into model/; no dependencies; BUILD=wide|slim for one)

Scale: 1 px = 1/16 block, the pilot exactly as vanilla (4x12x4 limbs, Alex's arms 3 wide, 8x12x4 torso, 8^3 head,
32 px tall), standing on 4 px platform soles (5x4x5) with the big suit's fists (sized down, 5x4x5) under his hands: his
limbs fit entirely in the frame's cage, and the fists and soles are its mechanical ends (2026-11-04, user: his feet
stand on the soles, the fists start where his hands end), so he stands 4 px up (36 px to his head's top) and the arms
reach 4 px past his hands. Soles and fists have the same 5x5 footprint round his 4x4 limbs. The frame is a dense,
mechanical cage around him, from the fist / sole up to the shoulder / hip, in line with its fist / sole, closed on all
four sides and painted after the Fallout 4 T-45's frame (steel members, gunmetal joints, brass bellows, a copper valve
on the chest: ARM_ART, LEG_ART, _torso), the pilot seen through small windows, mostly at his hands and feet. It stands
straight: the legs touch like vanilla's, the arms hang off a chest wider than the waist (the spacing, CHEST_X).
The torso is an exoskeleton: a chest box over an abdomen box, a belt.

SHELLS: every part is ONE box round the pilot's (an arm: fist and cage; a leg: sole and cage; the chest; the
abdomen; the belt), its frame painted on the faces and its gaps see-through texels (alpha 0), like the player skin's jacket
and sleeve layer. So the frame is flat (bars and plates are paint on the box's faces, no thickness of their own) and
the renderer must draw the faces' backs too (entityCutoutNoCull): through a gap you see the far side's bars.
Clearance to Steve is 0, never an overlap: see check() at the bottom (it also keeps the parts' solid texels apart).

Rig: the names and parent chain of power_suit.bbmodel (marine > body > torso > head / *_arm;
marine > *_leg), so the animation kit and the later armour can reuse them. Steve's limbs are rigid (vanilla), so
there is no elbow, knee, hand or ankle bone: each limb is one bone. Frame cubes are named fr_*, the pilot's st_*; each bone has a
`pilot_*` child group holding Steve's part (hide those to see the bare frame). The head has no frame at all: the helmet is armour, added later.

Drafts: give the part an env knob (os.environ.get), then build all its options into one review file with
frame_drafts.py (hidden proto_* groups, one Blockbench tab); once one is picked, the knob goes and its choice stays.
"""
import base64, glob, json, os, struct, uuid, zipfile, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
# Two BUILDS (2026-11-04, user, like vanilla's wide Steve and slim Alex arms): 'wide' -> power_frame.bbmodel and 'slim'
# -> power_frame_slim.bbmodel (its pilot Alex). They differ only in the chest's width and so where the arms hang
# (CHEST_X): limbs, waist, belt, boots, fists and paint are shared, so are the arm, leg and helmet armour; only a
# torso armour piece needs two widths. The game is to pick by the pilot's skin model. Without BUILD (and FRAME_OUT,
# which frame_drafts.py sets) the script writes both.
BUILD = os.environ.get('BUILD')
if BUILD is None and not os.environ.get('FRAME_OUT'):
    import subprocess, sys
    for _b in ('wide', 'slim'):
        subprocess.run([sys.executable, os.path.abspath(__file__)], env=dict(os.environ, BUILD=_b), check=True)
    sys.exit()
BUILD = BUILD or 'wide'
assert BUILD in ('wide', 'slim'), BUILD
OUT = os.environ.get('FRAME_OUT') or os.path.join(HERE, '..', 'power_frame' + ('_slim' if BUILD == 'slim' else '') + '.bbmodel')
# The rest pose is OPEN, not Steve's idle: a bulky suit can't close like a body, so the arms hang away from the torso
# and the legs stand apart. The splay (degrees, outward; env overrides are for trying values) turns Steve's limbs with
# their frame bones.
# 2026-11-04 (user): none. The arms hang straight off a chest wider than the legs (CHEST_X), so the fists clear the
# legs' sides. (Was arms 9 deg / legs 3 while his limbs touched his torso, then 4 / 2, then 2 / 1 as they moved out.)
ARM_SPLAY = float(os.environ.get('ARM_SPLAY', 0))
LEG_SPLAY = float(os.environ.get('LEG_SPLAY', 0))
# Spacing (2026-11-04, user). The frame is an entity you climb into and draws the pilot itself, so his limbs needn't sit
# where vanilla's do. Legs 0.25 px out (LEG_OUT), so their frame boxes touch, like vanilla's legs; the waist and belt
# line up with them (TX, as vanilla's torso with its legs). The torso is split: a chest wider than the waist (CHEST_X,
# per BUILD) with the arm boxes against its sides (ARM_OUT follows), so the straight arms' fists hang beside the legs
# with room to spare (wide 1 px, slim 0.5). Parts touch, so the limbs' inner sides (and the torso's sides) are painted
# without holes: two touching faces lie in one plane and would flicker wherever both are seen, but with solid walls
# that plane is shut in (the pilot's opaque limb fills each cage 0.25 px from its inner wall). (Until 2026-11-04: arms
# 0.75 / legs 0.5 with a 4 / 2 deg splay; then gaps of 1 px or more between the boxes, filled by gunmetal shoulder and
# hip blocks, arms up to 2.75 out: the gaps were dropped for touching walls, which needed no fillers.)
# (Tried and not picked, 2026-11-04: a bigger frame, torso 11 x 8 and legs 6 x 6, so armour could replace its boxes
# in place; with shoulder blocks in it, but pauldrons belong to the armour tiers: copper without, iron with.)
# Draft knob HELMET ('none' / 'glass'; 2026-11-04, user): the helmet, armour (not in the frame models), drafted here
# for its size and visor. The head's size (no neck: a 1 / 2 px neck with a collar ring or a post was tried and
# dropped): the big suit's, 9 x 9 x 9 like the skin's hat layer (the least that keeps its faces out of his head's
# planes), its bottom 0.5 px under the neck, tucked into the chest armour as vanilla's helmets tuck into chestplates.
# Its visor is glass, so his face shows 0.5 px behind it: partly transparent texels (in game a translucent pass of its
# own), picked over an open slot (the visor lights up in game: the glow needs a pane to sit on). In game the skin's hat
# layer (hair, hats) must hide under a helmet: it lies in the helmet's planes.
# In game since 2026-11-14 (step 3): the saved files carry the helmet (armor_head; the game hides it when the suit has
# none), so the exported model and texture hold everything the game draws. HELMET=none builds the bare frame.
HELMET = os.environ.get('HELMET', 'glass')
# Shoulder plates (2026-11-04, user: platforms over the shoulders where pauldrons go, as on the Fallout 4 frame): a
# 1 px plate on top of each arm, on the arm bone, so it swings with the arm and can never clip it (one on the torso
# would: the arm turns about the top of its shoulder, so a forward swing lifts its top corners up to 2.5 px), and a
# pauldron mounted on it swings with the arm too. 6 x 6: 1 px past the arm box's outer side, 0.5 front and back
# (picked over a 5 x 5 cap flush with the arm, which read as the cage's lid, and a 7 x 6 that read as a shelf). Its top
# also covers his shoulder's top, which showed through the cage's open top.
PLATE_OUT, PLATE_FB = 1, 0.5
# Draft knob SHOULDER (2026-11-12, user unsure about the 3D plates next to the 2D engine): 'plate' (the 3D plate above),
# 'decal' (the plate drawn flat round the arm's top like the engine's hoses: a 0.5 px decal over the top and the outer,
# front and back faces, a pauldron band with an ink edge, nothing sticking out) or 'bare' (no plate: a painted lid
# 0.1 px over his shoulder closes the cage's open top). See _decal(). Picked: decal (2026-11-12, user: "looks smooth";
# over the plate, and the bare lid I'd recommended). The plate stays for the iron pauldron's footprint (PLATE_OUT/_FB).
SHOULDER = os.environ.get('SHOULDER', 'decal')
assert SHOULDER in ('plate', 'decal', 'bare'), SHOULDER
DECAL = 0.5   # the decal's offset from the arm box (outer side, front, back, top)
assert HELMET in ('none', 'glass'), HELMET
# Draft knob HELMET_STYLE (2026-11-12, user: the default helmet, the one players see most, looks flat): 'suit' (the
# big suit's helmet sampled onto the box at 1 texel per px) or a new one painted at 2 (frame_helmet_art.py): 'A'
# sentinel (slit visor, crest), 'B' diver (a porthole), 'C' wraparound visor. Picked: C (2026-11-12, user; with the
# old helmet's chin grille back, a slate neck guard wrapping the sides, no ear discs; B out: an easter-egg helmet is
# BioShock's already).
HELMET_STYLE = os.environ.get('HELMET_STYLE', 'C')
# The pane's colour and opacity, RGBA hex (env GLASS to try others): the big suit's visor glass colour (262c34,
# tools/make-glowmasks.py) at 80 % (2026-11-04, user, over 60 % and a pale blue at 35 % that read washed out): his face
# a faint silhouette, clear only up close. In game the visor lights up (the glow layer tints it by the suit's state,
# the HUD colour, green by default): a lit pane is that glow drawn over it at part strength, so his face still shows.
_hex = lambda h: tuple(int(h[i:i + 2], 16) for i in range(0, len(h), 2))
GLASS = _hex(os.environ.get('GLASS', '262c34c8'))
GLINT = _hex(os.environ.get('GLINT', 'e8f4ff78'))   # a glint across it, top left to bottom right
# The glass in a shadow (draft, 2026-11-15: the spartan's brow casting its shadow on the visor, letter 'W'): darker and
# denser, still see-through (so it goes to the glass pass with the rest).
GLASS_SHADE = _hex(os.environ.get('GLASS_SHADE', '14181de0'))
FY = 2   # he stands on the 4 px soles (his feet at y 4): everything above the soles is lifted 2 px from the numbers below
LEG_OUT = 0.25
CHEST_X = {'wide': 6.0, 'slim': 5.5}[BUILD]   # the chest's half width
ARM_OUT = CHEST_X - 3.75                      # the arm box's inner wall (3.75 + ARM_OUT) against the chest's side
# The room between his torso and the torso boxes' sides is the frame's: painted solid members, the chest closed on top
# (shoulder platforms) and at the sides.
TX, TZ = 4.75 + LEG_OUT, 3   # the abdomen box's (the waist's) half width, the torso boxes' half depth
assert (TX * 2) % 1 == 0 and (CHEST_X * 2) % 1 == 0, (TX, CHEST_X)   # fronts are 2 texels per px: whole texels outside his torso
# Knob ARMOR: the iron armour ('none' / 'iron' / 'game'): helmet, torso, arms, legs. See ARMOR_BOX. 'none' builds the
# bare frame, 'iron' the frame fully armoured (the pieces replace its boxes: a review). 'game' (the saved files' default
# since 2026-11-14, frame step 6c; the game shows what's worn, one piece per part): both, each part's frame cubes in a
# `frame_<bone>` group and its piece in `armor_<bone>`, and the engine's front both ways (`engine_open` under a bare
# chest, `engine_armored` under the breastplate). The checks skip pairs that are never drawn together (ALT: a part's
# frame and its piece, the engine's two fronts); every mix of worn and bare parts is checked.
ARMOR = os.environ.get('ARMOR', 'game')
assert ARMOR in ('none', 'iron', 'game'), ARMOR
# Draft knob ARMOR_FORM (2026-11-12, user: no mix of 3D and 2D armour; the engine went 2D, the armour should too):
# 'solid' (the pieces as built 11-04/05: the waist 0.5 px shallower than the chest, a step band between them, the
# pauldron a box 1 px proud) or 'flat' (nothing proud of the frame's boxes: the waist as deep as the chest, the step
# band painted on it, the pauldron a decal like the frame's shoulder plate). See frame_iron_art.py, flat.
# Picked: flat (2026-11-12, user: "looks sick").
ARMOR_FORM = os.environ.get('ARMOR_FORM', 'flat')
assert ARMOR_FORM in ('solid', 'flat'), ARMOR_FORM
# Where the iron pauldron ends (built y; the shoulder plate's top is at 29, the arm's cage 16-28 over the fist 12-16):
# 9 of the arm's 16 px, past the elbow, leaving 4 px of forearm over the fist (2026-11-04, user; picked over 18, which
# left 2 px and read as a whole sleeve). See ARMOR_BOX.
# (Tried and dropped, 2026-11-04, user: a guard round the helmet like the old suit's chest (a collar ring, pauldrons
# 2 px taller beside the head, a plate behind it). The old suit's head barely moved and its chest was deeper than its
# helmet; the frame's head turns 50 deg from the body and pitches 90, its 9 px helmet's corners sweeping 6.4 px from
# the neck over a 6 px deep chest, so every guard was cut by the helmet or jutted far past the chest.)
PAULDRON = 20
STEVE_PNG = {'wide': 'assets/minecraft/textures/entity/player/wide/steve.png',
             'slim': 'assets/minecraft/textures/entity/player/slim/alex.png'}[BUILD]

def steve_skin():
    """Vanilla's default Steve skin (the slim build: Alex's), read from the Minecraft jar the build already unpacked (run ./gradlew build once).
    Its hat / jacket / pants layers are empty, so only the base boxes are modelled (an overlay would clip the frame)."""
    jars = sorted(glob.glob(os.path.join(HERE, '..', '..', 'build', 'moddev', 'artifacts', 'minecraft-patched-*.jar')))
    assert jars, 'no Minecraft jar in build/moddev/artifacts: run ./gradlew build first'
    with zipfile.ZipFile(jars[-1]) as z:
        return unpng(z.read(STEVE_PNG))

def unpng(data):
    """Decodes an 8-bit PNG (palette, grey, RGB or RGBA; not interlaced) to rows of RGBA tuples."""
    pos, chunks, idat = 8, {}, b''
    while pos < len(data):
        n, t = struct.unpack('>I4s', data[pos:pos + 8])
        d = data[pos + 8:pos + 8 + n]
        if t == b'IDAT': idat += d
        else: chunks[t] = d
        pos += 12 + n
    w, h, depth, ctype, _, _, inter = struct.unpack('>IIBBBBB', chunks[b'IHDR'])
    assert depth == 8 and inter == 0, (depth, inter)
    bpp = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw, rows, prev = zlib.decompress(idat), [], bytearray(w * bpp)
    for y in range(h):
        i = y * (w * bpp + 1)
        ft, line = raw[i], bytearray(raw[i + 1:i + 1 + w * bpp])
        for x in range(len(line)):
            a = line[x - bpp] if x >= bpp else 0
            b, c = prev[x], (prev[x - bpp] if x >= bpp else 0)
            if ft == 1: line[x] = (line[x] + a) & 255
            elif ft == 2: line[x] = (line[x] + b) & 255
            elif ft == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif ft == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(line)
        prev = line
    pal = [tuple(chunks[b'PLTE'][i:i + 3]) for i in range(0, len(chunks.get(b'PLTE', b'')), 3)]
    trns = chunks.get(b'tRNS', b'')
    def px(line, x):
        v = line[x * bpp:(x + 1) * bpp]
        if ctype == 3: return pal[v[0]] + (trns[v[0]] if v[0] < len(trns) else 255,)
        if ctype == 0: return (v[0],) * 3 + (255,)
        if ctype == 4: return (v[0],) * 3 + (v[1],)
        if ctype == 2: return tuple(v) + (255,)
        return tuple(v)
    return [[px(line, x) for x in range(w)] for line in rows]

# ---------------------------------------------------------------- textures (written without PIL)
def png(w, h, px):
    raw = b''.join(b'\x00' + b''.join(bytes(px[y][x]) for x in range(w)) for y in range(h))
    def chunk(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) + \
        chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')

TW, TH = 128, 128   # (widened to 256 below) the one texture (Bedrock / GeckoLib models have one): the pilot's
# 64x64 skin top left, the shells below and right
# The frame's bar colour (the old cube frame's side faces), with a little pixel grain, no noise.
BAR = (0x4c, 0x53, 0x5c)
def bar(i, j): return tuple(min(k + (6 if (i + j) % 3 == 0 else 0), 255) for k in BAR) + (255,)

# ---------------------------------------------------------------- fist art, taken from the big suit
# The fist is the big suit's (power_suit.bbmodel: fist_r, 7x5x7) sized down to the frame's arm (5x4x5). Its art is
# the suit's own painted faces, resampled by picking columns / rows (not scaling), so the finger lines stay whole
# pixels. The suit's texture is its grey base (paint swaps the steel shades), so the frame's fists are that grey too.
# (The big suit's banded cuff over it, forearm_r, sized down to 5x4x5, was the gauntlet's top until 2026-11-04: the
# user gave its room to the frame's cage.)
SUIT = os.path.join(HERE, '..', 'power_suit.bbmodel')
# per cube: the suit cube, the frame size per face (w, h), and which of the suit face's columns / rows to keep
GAUNT = {
    'fist': ('fist_r', {
        'north': ([0, 1, 3, 5, 6], [0, 2, 3, 4]), 'east': ([0, 1, 3, 5, 6], [0, 2, 3, 4]),
        'south': ([0, 1, 3, 5, 6], [0, 2, 3, 4]), 'west': ([0, 1, 2, 3, 6], [0, 2, 3, 4]),
        'up': ([0, 1, 3, 5, 6], [0, 1, 3, 5, 6]), 'down': ([0, 1, 3, 5, 6], [1, 2, 3, 4, 5])}),
}
# The soles have their own art (the fist's read as hands on feet), in the suit's colours (sampled from forearm_r /
# fist_r): a platform sole, a seam over a thick three-row slate sole, lugs underneath (picked from drafts A slate /
# B steel sabaton / C mechanical ankle / D platform; its steel upper, a cuff like the gauntlet's, went with it).
# One letter per texel; rows top to bottom as the face shows. East is the outer side of the right boot (its last column
# at the toe), west the inner; the left boot mirrors them.
PAL = {'A': (0x58, 0x60, 0x6a), 'B': (0x75, 0x7c, 0x85), 'C': (0x9f, 0xa4, 0xa9), 'D': (0x3c, 0x42, 0x4c),
       'K': (0x4c, 0x55, 0x59), 'M': (0x1f, 0x23, 0x26)}
# The sole is 5x4x5: its footprint round his leg is the fist's round his arm (5x5 round 4x4).
# The tread: lines across the sole (along x) every other row, run out to the edges so their ends are the notches on
# the outer / inner sides; with 5 rows it starts and ends on a line, so both sides read line / gap / line from back to
# front and the back's bottom row is the back line, a plain dark strip. The face UVs run: east back -> front, west
# front -> back, north outer -> inner, the sole's rows back -> front and columns inner -> outer. The front's bottom row
# is the sole's front row seen edge on: only its corners are fixed (they meet the side notches), the rest is the
# front's design: a toe lug across the toe's foot, its end the sole's front line (picked from drafts plain / toe lug /
# bumper / riveted).
SIDE = ['DDDDD', 'KKKKK', 'MMMMM', 'MKMKM']
FRONT = ['DDDDD', 'KKKKK', 'MMMMM', 'MKKKM']   # the seam, the sole and toe lug
assert FRONT[-1][0] == FRONT[-1][-1] == 'M', "the front row's corners meet the side notches"
BOOT = {
    'north': FRONT,
    'south': SIDE[:3] + ['MMMMM'],
    'east': SIDE, 'west': SIDE,
    'up': ['DDDDD'] * 5,                                                        # inside the shell: never seen
    'down': ['MMMMM', 'KKKKK'] * 2 + [FRONT[-1][::-1]],                        # the tread, rows back -> front
}
FACES = ('north', 'east', 'south', 'west', 'up', 'down')
# where each part's art is drawn in the SOURCE canvas the shells copy from (not the texture): (u, v, w, h)
GAUNT_UV = {}
for row, (part, (_, picks)) in enumerate(GAUNT.items()):
    u = 0
    for f in FACES:
        w, h = len(picks[f][0]), len(picks[f][1])
        GAUNT_UV[part, f] = (u, 8 + row * 8, w, h)
        u += w
u = 0
for f in FACES:
    GAUNT_UV['boot', f] = (u, 8 + len(GAUNT) * 8, len(BOOT[f][0]), len(BOOT[f]))
    u += len(BOOT[f][0])
# The tool socket (2026-11-13, user: the big suit's playbook, the left hand replaced by a socket, which leaves the
# tools more room). The left arm (the big suit's tool arm) has no fist: its box ends where his hand does (raw 14: the
# whole fist's 4 px gone, user), its underside the socket: a steel plate, bolts in its corners, the cyan contact in the
# middle (the big suit's empty socket). His hand's bottom face lies in that plane, so it isn't drawn (the frame draws
# the pilot; the plate covers it). A tool (TOOL) hangs straight under it: the big suit's tools had a socket base each
# (7 x 1 x 7), here the plate is the base for all of them (2026-11-13, user: a 1 px base read as a step, then a 1 px
# socket ring left the arm a px longer than the fist-less arm should be). Only its underside is used ('+' the contact).
SOCKET = {f: ['DKDKD'] for f in ('north', 'east', 'south', 'west')}
SOCKET.update(up=['DDDDD'] * 5, down=['XBBBX', 'BAAAB', 'BA+AB', 'BAAAB', 'XBBBX'])
CONTACT = (0x2c, 0xe3, 0xd9)   # the big suit's socket cyan
u = 0
for f in FACES:
    GAUNT_UV['socket', f] = (u, 8 + (len(GAUNT) + 1) * 8, len(SOCKET[f][0]), len(SOCKET[f]))
    u += len(SOCKET[f][0])
SOCKET_Y = 14   # the left arm's bottom (raw): the socket, at his hand's bottom

# ---------------------------------------------------------------- shells
# A limb's faces are composed top to bottom from its painted frame (ARM_ART / LEG_ART: PAL letters, '#' a bar texel,
# '.' a window) over the fist's or the sole's art, in the same face column order as theirs (north outer -> inner,
# east back -> front, south inner -> outer, west front -> back).
# 'T' is a bar texel that tucks into its neighbour (hidden in it); the clearance check skips it.
# Texel density per face: `rows` texel rows per px up the sides (the legs: 2, so the cage can end on a half pixel,
# under the belt, while the sole's rows stay whole; every art row is drawn twice) and the arms' top face 2 texels
# per px, so its rim is 0.5 px (a 1 px rim would lie in the plane of his arm's top and overlap it, so flicker).
# (Until 2026-11-04 the cage was plain bars, open on its inner side; then the user asked for the frame dense and
# mechanical like the Fallout 4 T-45's, his reference: the pilot seen only through small windows, mostly at his hands
# and feet.)
def _rim(n):
    """The top face, n x n texels, rows front -> back, columns inner -> outer: the band and bar tops. The bands'
    inner ends tuck (the splay dips them into the chest's struts)."""
    return ['T' + '#' * (n - 1)] + ['.' * (n - 1) + '#'] * (n - 2) + ['T' + '#' * (n - 1)]
BELT_X = TX   # the belt's half width: the torso box's
def _belt():
    """The belt (the hip, on the body bone: the torso can bend over it): a ring round his pelvis, x +-BELT_X, y 16..17,
    z -3..3; its top and bottom are rims (front and back rows, the half-px side columns)."""
    n = round(BELT_X * 4)   # half-px columns
    rim = lambda c: ['#' * n] + [c + '.' * (n - 2) + c] * 4 + ['#' * n]
    # underneath, the side columns are 'T': at the splay each leg's top outer corner rises 0.1 px past the belt's
    # bottom, 0.003 px inside its side column (hidden in the ring)
    return {'north': ['#' * n], 'south': ['#' * n], 'east': ['#' * 6], 'west': ['#' * 6], 'up': rim('#'), 'down': rim('T')}

# ---------------------------------------------------------------- armour (draft: ARMOR)
# The armour is SEALED: each piece is a closed box, every face solid (the see-through texels are the frame's only).
# It REPLACES the frame part in place (2026-11-04, user): the piece is that part's box exactly, painted as armour, and
# the frame's box isn't drawn under it, so the suit stays the frame's size. (Refitted first as overlays, each piece
# its frame box plus 0.25-0.5 px over the frame: too thick.) The limbs keep the frame's fists and soles (their art
# at the bottom of the piece's faces: the box is one, as the frame's), the belt stays the frame's. Pieces touch where
# the frame's boxes do (legs at the crotch, arms against the chest, waist on the belt): those faces meet back to back
# with the pieces on either side, shut in like the frame's touching walls. What must never happen is two faces in one
# plane facing the same way (they flicker): check_armor().
# Its look is the big suit's (power_suit.bbmodel, the marketing pictures): plates in its mid steel, everything
# between them (waist, upper arms, knees, inner legs) its dark slate under-armour, the helmet its helmet.
import frame_iron_art as iron
ARMPAL = {c: tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for c, h in iron.PAL.items()}   # steel + slate letters

# The paint: frame_iron_art.py (its letters join ARMPAL there).

SUIT_HELMET = ['helmet_shell', 'visor', 'helmet_brow', 'cheek_l', 'cheek_r', 'chin_guard']
def _helmet(visor='painted'):
    if HELMET_STYLE != 'suit':
        import frame_helmet_art as helmet_art
        sub = {'V': GLASS, 'T': GLINT, 'W': GLASS_SHADE}
        # Draft knob HELMET_BACK (C's back): 'plain' / 'guard' / 'crest' / 'vents' (frame_helmet_art.wrap_back)
        back = os.environ.get('HELMET_BACK', 'guard')
        return {f: [[sub.get(c, c) for c in r] for r in rows] for f, rows in helmet_art.faces(HELMET_STYLE, back).items()}
    return _helmet_suit(visor)

def _helmet_suit(visor='painted'):
    """The big suit's helmet (power_suit.bbmodel: a 9 px shell round the pilot's head, a 7x5 visor, the brow band,
    cheeks and chin guard standing 0.75 px proud) as ONE 9x9x9 box: each face is the old helmet seen straight from
    that side (the front-most cube's face at every texel), so the proud parts are painted flat. Underside slate.
    visor: 'painted' as the old one, 'glass' (HELMET) a tinted pane (GLASS) with a glint."""
    m = json.load(open(SUIT))
    img = unpng(base64.b64decode(m['textures'][0]['source'].split(',', 1)[1]))
    cs = [e for e in m['elements'] if e['name'] in SUIT_HELMET]
    X0, X1 = -4.5, 4.5
    Y0, Y1 = min(e['from'][1] for e in cs), max(e['to'][1] for e in cs)
    Z0, Z1 = min(e['from'][2] for e in cs), max(e['to'][2] for e in cs)
    def sample(e, f, a, b):   # the texel of face f of cube e at fractions a (across, as the face's u runs) / b (down)
        fc = e['faces'][f]
        assert not fc.get('rotation'), (e['name'], f)
        u0, v0, u1, v1 = fc['uv']
        u, v = u0 + a * (u1 - u0), v0 + b * (v1 - v0)
        return tuple(img[min(int(v), len(img) - 1)][min(int(u), len(img[0]) - 1)][:3])
    n = 9
    xs = [X1 - (i + .5) * (X1 - X0) / n for i in range(n)]            # north columns: x+ -> x-
    ys = [Y1 - (j + .5) * (Y1 - Y0) / n for j in range(n)]
    zs = [Z0 + (i + .5) * (Z1 - Z0) / n for i in range(n)]            # front -> back
    inside = lambda e, k, t: e['from'][k] <= t <= e['to'][k]
    def view(f, cols, axis, pick):
        rows = []
        for y in ys:
            row = []
            for c in cols:
                hit = [e for e in cs if inside(e, 1, y) and inside(e, axis, c)]
                e = pick(hit)
                (fx, fy, fz), (tx, ty, tz) = e['from'], e['to']
                b = (ty - y) / (ty - fy)
                a = {'north': (tx - c) / (tx - fx) if axis == 0 else 0, 'south': (c - fx) / (tx - fx),
                     'east': (tz - c) / (tz - fz), 'west': (c - fz) / (tz - fz)}[f]
                if e['name'] == 'visor' and visor != 'painted':
                    row.append(GLASS)
                else:
                    row.append(sample(e, f, a, b) + (255,))
            rows.append(row)
        return rows
    faces = {'north': view('north', xs, 0, lambda h: min(h, key=lambda e: e['from'][2])),
             'south': view('south', xs[::-1], 0, lambda h: max(h, key=lambda e: e['to'][2])),
             'east': view('east', zs[::-1], 2, lambda h: max(h, key=lambda e: e['to'][0])),
             'west': view('west', zs, 2, lambda h: min(h, key=lambda e: e['from'][0]))}
    top = []
    for z in zs:
        row = []
        for x in xs[::-1]:
            hit = [e for e in cs if inside(e, 0, x) and inside(e, 2, z)]
            e = max(hit, key=lambda e: e['to'][1])
            (fx, _, fz), (tx, _, tz) = e['from'], e['to']
            row.append(sample(e, 'up', (x - fx) / (tx - fx), (z - fz) / (tz - fz)) + (255,))
        top.append(row)
    faces['up'] = top
    faces['down'] = ['k' * n] * n
    if visor == 'glass':   # the glint: a short diagonal across the pane's top left corner (one across the whole pane
        # read as a scar on his face)
        pane = [(i, j) for j, r in enumerate(faces['north']) for i, c in enumerate(r) if c == GLASS]
        i0, j0 = min(i for i, _ in pane), min(j for _, j in pane)
        for i, j in pane:
            if (i - i0) + (j - j0) == 2: faces['north'][j][i] = GLINT
    return faces

# Boxes, right side (the left mirrors), in the frame's numbers (helmet / torso / arms lifted by FY; legs raw, like the
# soles): the frame's boxes (see the model building below), heights here as built (with FY).
# - helmet: 0.5 px round his head, its bottom 0.5 px under his neck, in the chest.
# - torso (2026-11-04, user: stepped, one piece, over a straight one at the chest's width): the chest box over the
#   waist (the frame's abdomen box), the waist 0.5 px shallower front and back (z +-2.5, flush with the legs; user's
#   edit), so the chest stands proud of it all round.
# - arm: the whole arm box, from the fist up to 0.1 px over the shoulder (28.1: at 28 its top would lie in his arm's),
#   with or without a pauldron (2026-11-04, user's edit; first it stopped under the pauldron).
# - pauldron (the iron tier's add-on; 2026-11-04, user: the shoulder plate's footprint down over most of the arm, then
#   his edit: 1 px off its inner side, 5 x 6): one box on the arm bone over the arm piece, from the plate's top (29)
#   down to PAULDRON (20), 1 px out at the side, 0.5 front and back, its inner wall 1 px off the arm's, so the arm
#   piece shows between it and the chest. That keeps it clear of the helmet: a 50 deg head turn sweeps the helmet's
#   corners 6.4 px from the neck (the wide build's pauldron starts at 7, the slim's at 6.5; flush with the arm, at 6
#   / 5.5, the corners cut into its top).
# - legs: the leg box, but up to the waist (17), replacing the belt too: the frame's leg stops 0.5 px under the belt
#   (room for a stride), and with sealed armour that slit showed his trousers, his leg's top in a stride. The leg's
#   top meets the waist's bottom back to back; in a stride it turns up into the waist.
# - hip (the leg piece's, as vanilla's leggings have a body part): the belt gone, a leg swung away bared his pelvis
#   under the waist (y 16-17). A slate block on the body bone round it, inside the legs at rest (x +-4.75, z +-2.25:
#   0.25 inside their walls, 0.25 round him), from 0.1 px under his torso's bottom up 0.1 px into the waist (at 17
#   its top would lie in the leg tops' plane).
ARMOR_BOX = {'helmet': ((-4.5, 25.5, -4.5), (4.5, 34.5, 4.5)),
             'chest': ((-CHEST_X, 20, -TZ), (CHEST_X, 26, TZ)),
             'waist': ((-TX, 15, -TZ + 0.5), (TX, 20, TZ - 0.5)),
             'pauldron': ((4.75 + ARM_OUT, PAULDRON - FY, -2.5 - PLATE_FB), (8.75 + ARM_OUT + PLATE_OUT, 27, 2.5 + PLATE_FB)),
             'arm': ((3.75 + ARM_OUT, 10, -2.5), (8.75 + ARM_OUT, 26.1, 2.5)),
             'leg': ((-0.25 + LEG_OUT, 0, -2.5), (4.75 + LEG_OUT, 17, 2.5)),   # raw (legs)
             'hip': ((-4.75, 13.9, -2.25), (4.75, 15.1, 2.25))}
ARMOR_BOX['arm_socket'] = ((3.75 + ARM_OUT, SOCKET_Y, -2.5), (8.75 + ARM_OUT, 26.1, 2.5))   # the left arm's
# The waist steps in (2026-11-05, user: more steps from the chest down to the waist): a band halfway between the chest
# and the waist at the sides (wide: 12 -> 11 -> 10 px across; slim 11 -> 10.5 -> 10) and 0.25 px shallower than the
# chest front and back, y 20-22, over the waist (y 17-20). Picked over one step (the waist straight under the chest)
# and two 1 px bands down to a waist pinched to 9 px with the hips flaring out under it.
WAIST_STEPS = [((-(CHEST_X + TX) / 2, 18, -2.75), ((CHEST_X + TX) / 2, 20, 2.75))]   # raw y (built - FY)
# the flat pauldron (arm coordinates, as ARMOR_BOX['pauldron']): from its old inner edge to 0.5 past the arm outside,
# 0.5 front and back, from PAULDRON up to 0.5 over the arm's top
PAULDRON_DECAL = ((4.75 + ARM_OUT, PAULDRON - FY, -3), (9.25 + ARM_OUT, 26.5, 3))
ARMOR_BOX['waist'] = ((-TX, 15, -TZ + 0.5), (TX, 18, TZ - 0.5))
if ARMOR_FORM == 'flat':   # the waist up to the chest and as deep as it, the step band painted on its top 2 px
    ARMOR_BOX['waist'] = ((-TX, 15, -TZ), (TX, 20, TZ))
def _dims(box): return [round(box[1][k] - box[0][k]) for k in range(3)]   # its art's texels (one per px, ~)

def _legrows(face): return face[:1] + [r for r in face[1:] for _ in range(2)]   # the half-px top row once, the rest twice

# The paint, after the user's reference (2026-11-04: the threezero 1/6 Fallout 4 T-45 frame figure; it replaced a
# denser paint of rails and bands). What makes that frame read: light members over a dark inside, the holes in them
# rimmed with grime (depth without geometry), dark gunmetal at the joints (a bolted hub on the knee's and elbow's outer
# sides, the knee cap, the wrists, the hips), ribbed brass bellows above the knees and on the upper arms, and on the
# torso a copper valve in a ring on the chest, a ribbed black column down a brown leather abdomen. The members are the
# big suit's steel greys (picked over the figure's off-white bone), the accents as the figure's. One letter per texel
# (PAL; '.' a window, 'T' a tucked bar).
PAL.update({'N': (0x3a, 0x3d, 0x41), 'O': (0x62, 0x67, 0x6c), 'X': (0x1b, 0x1c, 0x1f),          # gunmetal joints
            'Q': (0xc0, 0x74, 0x40), 'R': (0x80, 0x44, 0x26),                                        # copper
            'L': (0x5e, 0x3e, 0x2c), 'H': (0x40, 0x29, 0x1d),                                        # leather
            'Y': (0xa8, 0x91, 0x60), 'Z': (0x6a, 0x58, 0x38),                                        # brass bellows
            'W': (0xb4, 0xb9, 0xbe), 'V': (0x87, 0x8e, 0x96), 'U': (0x5f, 0x66, 0x70), 'G': (0x30, 0x34, 0x3a)})  # steel
GRAIN = set('WVU')   # the members get bar()'s light pixel grain (no noise: random grain read as stone)
BAR = PAL['V']       # rims and the belt ('#') in the members' colour
# Arms: 12 rows of cage over the fist, top (shoulder) first; columns as the frame's faces (north outer -> inner, east
# back -> front, south inner -> outer, west front -> back). Shoulder cap, ribbed bellows on the upper arm, a bolted
# elbow band (hub on the outer side), the forearm a cage with a dark piston between slits / an oval window where his
# hand is, gunmetal wrist. The inner side (west: against the chest) has no holes (see the spacing).
ARM_ART = {
    'north': ['WWWWT', 'WVVVU', 'YYYYY', 'ZZZZZ', 'YYYYY', 'WVOVU', 'UNXNG', 'WG.GU', 'W...U', 'W...U', 'WG.GU', 'NNNNN'],
    'east':  ['VVVVW', 'UVVVW', 'YYYYY', 'ZZZZZ', 'YYYYY', 'VNONW', 'UOXOW', 'VNONW', 'V.N.W', 'V.N.W', 'VGNGW', 'NNNNN'],
    'west':  ['VVVVV', 'UVVVU', 'YYYYY', 'ZZZZZ', 'YYYYY', 'UNNNU', 'UGGGU', 'UGNGU', 'UGNGU', 'UGNGU', 'UVVVU', 'NNNNN'],
    'south': ['TWWWW', 'UVVVW', 'YYYYY', 'ZZZZZ', 'YYYYY', 'UVOVW', 'GNXNU', 'UG.GW', 'U...W', 'U...W', 'UG.GW', 'NNNNN']}
# Legs: one row per px from the hip (the top row is half a px: the cage is 11.5 px), drawn at 2 texel rows per px;
# columns as the arms'. Gunmetal hip band, the thigh a cage round a dark piston, bellows above the knee, the knee a
# bolted cap in front (an X plate read as a checkerboard at 3 x 3) and a bolted hub outside, the shin a long cage with
# an oval window over his shoe. The inner side (west: against the other leg) has no holes.
LEG_ART = {
    'north': ['NNNNT', 'WVVVU', 'W.N.U', 'YYYYY', 'ZZZZZ', 'WNNNU', 'WNONU', 'WNNNU', 'WVVVU', 'WG.GU', 'W...U', 'UUUUG'],
    'east':  ['NNNNN', 'UVVVW', 'U.N.W', 'YYYYY', 'ZZZZZ', 'VNONW', 'VOXOW', 'VNONW', 'UVVVW', 'UG.GW', 'U...W', 'GUUUU'],
    'west':  ['NNNNN', 'UVVVU', 'UGNGU', 'YYYYY', 'ZZZZZ', 'UNNNU', 'UGGGU', 'UNNNU', 'UVVVU', 'UGVGU', 'UGVGU', 'GGGGG'],
    'south': ['TNNNN', 'UVVVW', 'U.N.W', 'YYYYY', 'ZZZZZ', 'UNNNW', 'UGGGW', 'UNNNW', 'UVVVW', 'UG.GW', 'U...W', 'GUUUU']}
# Draft knob BANDS (2026-11-12, user: get rid of the brownish bands on the arms and legs): the brass bellows rows
# 'brass' (as drawn above), 'steel' (the ribs in the members' steel), 'gunmetal' (in the joints' gunmetal) or 'cage'
# (no band: the cage's window rows carry on, a bar each side and a rod down the middle; the inner side stays closed).
# Picked: cage (2026-11-12, user: gunmetal looked cool but like armour; the frame is only what the armour goes on).
BANDS = os.environ.get('BANDS', 'cage')
assert BANDS in ('brass', 'steel', 'gunmetal', 'cage'), BANDS
if BANDS != 'brass':
    _CAGE_ROW = {'north': 'W.N.U', 'east': 'V.N.W', 'south': 'U.N.W', 'west': 'UGNGU'}
    _RIB = {'steel': {'Y': 'V', 'Z': 'U'}, 'gunmetal': {'Y': 'O', 'Z': 'N'}}.get(BANDS)
    for _art in (ARM_ART, LEG_ART):
        for _f, _rows in _art.items():
            _art[_f] = [r if set(r) - set('YZ') else (_CAGE_ROW[_f] if _RIB is None else ''.join(_RIB[c] for c in r))
                        for r in _rows]
# Draft knob LEATHER (2026-11-12, user: leather accents on the cage, the frame being the inner piece the pilot wears,
# leather in its recipe; the armour goes on over it): 'none', 'straps' (a leather strap round the upper arm and the
# thigh, in the cage rows where the bands were, a brass buckle in front), 'lining' (those cage rows backed with dark
# leather: leather sleeves under the bars) or 'pads' (the elbow and knee joints' gunmetal in leather, bolts kept).
# Round 2 (user: lining is the best but flat, one shade where the torso has two, and it hides his body, which the cage
# showed): in the window rows under the shoulder / hip (rows 2-4; the legs' row 2 was a window already), the torso's
# two leathers, his body still showing: 'half' (the lining in the top two rows, the dark one in the shadow of the bar
# above, the bottom row open), 'back' (lined on the back face only, light-dark-light; front and outside open) or
# 'laced' (a lace across each face, light from the top of the first window over the rod to dark at the bottom of the
# second, his body round it).
# Round 3 (user: half is the best of those; try it split the other way, the leather replacing the bar down the middle
# or beside it on one side, the other side open): 'strip' (the middle rod in leather, both windows open) or 'side'
# (the first window of each face in leather, the second open). Dark leather in the top row (the bar's shadow), light
# under it, as in half.
# Round 4 (user: work on side, the limb's sides different): 'wrap': the front and back windows beside the outer side
# in leather, the other open; the outer side's rod gone, leather in both its windows, so the leather turns the corners
# into the front and back pieces with his body showing in the middle of the side (the inner side is closed anyway).
# Picked: wrap (2026-11-12).
LEATHER = os.environ.get('LEATHER', 'wrap')
assert LEATHER in ('none', 'straps', 'lining', 'pads', 'half', 'back', 'laced', 'strip', 'side', 'wrap'), LEATHER
if LEATHER in ('half', 'back', 'laced', 'strip', 'side', 'wrap'):
    def _win(row, col, c):   # the row with its window column col (0: the first, 1: the second) or the rod (col 'rod')
        if col == 'rod': return row[:2] + c + row[3:] if row[2] == 'N' else row
        holes = [i for i, ch in enumerate(row) if ch == '.']
        return row[:holes[col]] + c + row[holes[col] + 1:] if len(holes) > col else row
    for _art in (ARM_ART, LEG_ART):
        for _f, _rows in _art.items():
            _rows = list(_rows)
            if LEATHER == 'half':
                _rows[2], _rows[3] = _rows[2].replace('.', 'H'), _rows[3].replace('.', 'L')
            elif LEATHER == 'back' and _f == 'south':
                for j, c in ((2, 'L'), (3, 'H'), (4, 'L')): _rows[j] = _rows[j].replace('.', c)
            elif LEATHER == 'laced':
                _rows[2], _rows[3] = _win(_rows[2], 0, 'L'), _win(_rows[3], 'rod', 'L')
                _rows[4] = _win(_rows[4], 1, 'H')
            elif LEATHER in ('strip', 'side'):
                for j, c in ((2, 'H'), (3, 'L'), (4, 'L')):
                    _rows[j] = _win(_rows[j], 'rod' if LEATHER == 'strip' else 0, c)
            elif LEATHER == 'wrap':   # columns: north outer -> inner, south inner -> outer, east back -> front
                for j, c in ((2, 'H'), (3, 'L'), (4, 'L')):
                    r = _rows[j]
                    if _f == 'north': r = _win(r, 0, c)
                    elif _f == 'south': r = _win(r, 1, c)
                    elif _f == 'east': r = _win(_win(_win(r, 'rod', '.'), 0, c), 1, c)
                    _rows[j] = r
            _art[_f] = _rows
elif LEATHER != 'none':
    for _art, _band, _joint in ((ARM_ART, (2, 3, 4), (5, 6, 7)), (LEG_ART, (3, 4), (5, 6, 7))):
        for _f, _rows in _art.items():
            _rows = list(_rows)
            if LEATHER == 'straps':
                _rows[_band[-2]] = 'LLYLL' if _f == 'north' else 'LLLLL'
            elif LEATHER == 'lining':
                for j in _band: _rows[j] = _rows[j].replace('.', 'H')
            else:
                for j in _joint: _rows[j] = _rows[j].replace('N', 'H').replace('O', 'L')
            _art[_f] = _rows

# Draft knob TORSO_LEATHER (2026-11-12, user: compare with no leather at all, the chest included; with LEATHER=none):
# 'keep', 'open' (the leather over his torso, front and back, gone: windows, his shirt through them; on the sides,
# beside him, steel) or 'steel' (all of it in the members' steel). Kept: the leather (user, 2026-11-12: wrap with the
# torso's leather; without it the frame read as a grey robot cage, closer to armour).
TORSO_LEATHER = os.environ.get('TORSO_LEATHER', 'keep')
assert TORSO_LEATHER in ('keep', 'open', 'steel'), TORSO_LEATHER

def _torso():
    """The torso's two boxes, the chest (y 22-28, x +-CHEST_X) over the abdomen (y 17-22, x +-TX), drawn as one face
    and split: front / back 2 texels per px across (the frame's edge members outside his torso, his torso's 8 px drawn
    twice each, the other edge), 11 rows (y 27-28 first); sides 6 across. The edge members are wide side struts (no
    holes: through one you'd look into the empty box beside his torso; grime instead), the sides closed (the arms hang
    beside them), the chest's top closed outside his torso (shoulder platforms), its underside where it overhangs the
    abdomen (a ledge).
    Front: a yoke over the shoulders, a dark ring round a copper valve on the chest, its pipe down into the abdomen: a
    ribbed black column between brown leather, a 1 px window each side; a bolted waist bar. Back: the yoke, shoulder
    blades with a window each beside the ribbed spine, leather lower back."""
    def edge(j):              # the left edge member's row j (outer column first)
        n = round(((CHEST_X if j < 6 else TX) - 4) * 2)   # its texels: the chest's rows (0-5) are wider
        if n == 1: return 'V' if j < 10 else 'G'
        return {0: 'W' * n, 5: 'U' * n, 10: 'G' + 'V' * (n - 1)}.get(j, 'V' + ('G' if 2 <= j <= 3 else 'N' if j >= 6 else 'U') * (n - 2) + 'U')
    def face(chest): return [edge(j) + ''.join(c * 2 for c in s) + edge(j)[::-1] for j, s in enumerate(chest)]
    front = face((
        'WWWWWWWW', 'W.UNNU.W', 'VUNQRNUV', 'VUNRRNUV', 'VG.NN.GV', 'UUURRUUU',
        'HLXNNXLH', '.LXOOXL.', '.LXNNXL.', 'HLXOOXLH', 'GVOVVOVG'))
    back = face((
        'WWWWWWWW', 'VUWNNWUV', 'V.UOOU.V', 'V.UNNU.V', 'VUUOOUUV', 'UGLNNLGU',
        'LHLOOLHL', 'L.LNNL.L', 'L.LOOL.L', 'LHLNNLHL', 'GVOVVOVG'))
    side = ['VVVVVV', 'VNNNNV', 'VNNNNV', 'UUUUUU', 'WWWWWW', 'VOVVOV', 'UUUUUU', 'LHGGHL', 'LHGGHL', 'LLLLLL', 'GVVVVG']
    if TORSO_LEATHER != 'keep':   # the leather out (see TORSO_LEATHER); the sides can't open (an empty box behind)
        over = {'L': '.', 'H': '.'} if TORSO_LEATHER == 'open' else {'L': 'V', 'H': 'U'}
        front, back = ([''.join(over.get(c, c) for c in r) for r in f] for f in (front, back))
        side = [r.replace('L', 'V').replace('H', 'U') for r in side]
    W, n = len(front[0]), round((CHEST_X - 4) * 2)
    up = [p * n + '.' * (W - 2 * n) + p * n for p in 'WVVVVU']   # rows front -> back
    k = round((CHEST_X - TX) * 2)
    chest = {'north': front[:6], 'south': back[:6], 'east': side[:6], 'west': side[:6], 'up': up,
             'down': ['U' * k + '.' * (W - 2 * k) + 'U' * k] * 6}
    w = len(front[6])
    abdomen = {'north': front[6:], 'south': back[6:], 'east': side[6:], 'west': side[6:], 'up': ['.' * w] * 6,
               'down': ['.' * w] * 6}
    return chest, abdomen

SHELLS = {'arm_shell': dict(cage=dict(ARM_ART), below=['fist'], rows=1, up=_rim(10)),
          'leg_shell': dict(cage={f: _legrows(r) for f, r in LEG_ART.items()}, below=['boot'], rows=2, up=['.' * 5] * 5),
          'belt_shell': dict(faces=_belt())}
SHELLS['chest_shell'], SHELLS['abdomen_shell'] = (dict(faces=f) for f in _torso())
if ARMOR != 'none':
    _cw, _tw, _d, _wd = round(CHEST_X * 2), round(TX * 2), round(TZ * 2), round(TZ * 2) - 1
    SHELLS.update({
        'helmet_armor': dict(faces=_helmet(HELMET)),
        'chest_armor': dict(faces=iron.chest(_cw, _d, round((CHEST_X - 4) * 2))),
        'waist_armor': dict(faces=(iron.waist if ARMOR_FORM == 'solid' else iron.waist_flat)(
            *_dims(ARMOR_BOX['waist'])[::2], _dims(ARMOR_BOX['waist'])[1])),
        **{f'waist{i}_armor': dict(faces=iron.waist_step(*_dims(b))) for i, b in enumerate(WAIST_STEPS)},
        'pauldron_armor': dict(faces=iron.pauldron(*_dims(ARMOR_BOX['pauldron'])) if ARMOR_FORM == 'solid' else
                               iron.pauldron_decal(*[round((PAULDRON_DECAL[1][k] - PAULDRON_DECAL[0][k]) * 2) for k in range(3)])),
        'hip_armor': dict(faces=iron.hip(_dims(ARMOR_BOX['hip'])[0], 5)),
        'arm_armor': dict(cage=iron.arm(), below=['fist'], rows=1, up=iron.arm()['up']),
        'leg_armor': dict(cage=iron.leg(), below=['boot'], rows=1, up=iron.leg()['up'])})
elif HELMET != 'none': SHELLS['helmet_armor'] = dict(faces=_helmet(HELMET))
# Draft knob HELMET_EXTRA ('none' / 'cap' / 'radio' / 'both' / 'all' / 'gear' / 'layer'; 2026-11-12, user): the
# helmet's outer layer, decals on the head bone (frame_helmet_art.extras), placed in the texture's free room. 'layer'
# (2026-11-13): the same gear painted on one see-through box round the helmet (frame_helmet_art.layer).
import frame_helmet_art as helmet_art
# Picked: 'gear' (radio + camera; the layered cap dropped, its swept side painted into the helmet, user 2026-11-12),
# then 'layer' (2026-11-13, user: the 2D layer "has that je ne sais quoi"; one cube for the gear, paint only, like
# the armour and the engine; the boxes' forward lens and edges given up).
PAL.update(helmet_art.EXTRA)   # the styles' red and silver (frame step 7b)
# the outer layer: helmet C's gear and brow, or a style's own outer art (the hunter's ear guards; none: no layer)
HELMET_EXTRAS = helmet_art.extras(os.environ.get('HELMET_EXTRA', 'layer'), HELMET_STYLE) if 'helmet_armor' in SHELLS else []
# (a layer's glass, the diver's camera lens, is the helmet's glass: V / T resolved as on the helmet)
_glassy = lambda faces: {f: [[{'V': GLASS, 'T': GLINT, 'W': GLASS_SHADE}.get(c, c) for c in r] for r in rows] for f, rows in faces.items()}
for _p in HELMET_EXTRAS: SHELLS[f"hx_{_p['name']}"] = dict(faces=_glassy(_p['faces']), compact=_p.get('hollow', False))
# The helmet styles (frame step 7b, design sec. 4c): each picked style's helmet built beside the standard one, in its
# own group under armor_head (helm_<style>; the standard helmet and its layer in helm_standard), the game showing the
# worn style's (PowerSuitRenderer; a style without art shows the standard). The saved files (ARMOR=game) carry the
# picked ones (env HELMET_VARIANTS, comma separated; '' none). Picked so far: hunter (2026-11-14), protector (the
# diver, 2026-11-15), robot (Guy-Manuel, gold, 2026-11-15), spartan (Master Chief, 2026-11-15).
HELMET_VARIANTS = [v for v in os.environ.get('HELMET_VARIANTS', 'hunter,protector,spartan,robot' if ARMOR == 'game' else '').split(',') if v] \
    if 'helmet_armor' in SHELLS and HELMET_STYLE != 'suit' else []
HELMET_VARIANT_EXTRAS = {}
for _v in HELMET_VARIANTS:
    SHELLS[f'helmet_{_v}_armor'] = dict(faces={f: [[{'V': GLASS, 'T': GLINT, 'W': GLASS_SHADE}.get(c, c) for c in r] for r in rows]
                                               for f, rows in helmet_art.faces(_v).items()})
    HELMET_VARIANT_EXTRAS[_v] = helmet_art.extras('layer', _v)
    for _p in HELMET_VARIANT_EXTRAS[_v]:
        SHELLS[f"hx_{_v}_{_p['name']}"] = dict(faces=_glassy(_p['faces']), compact=_p.get('hollow', False))

def _plate():
    """The shoulder plate at 2 texels per px: a steel plate, its top lit along the front and outer edges, a
    gunmetal mounting rail across it (front to back) with a dark bolt at each end, bolts in its corners; its sides a lit
    and a shadowed row. Its underside is open over the arm box (his arm's top and the cage's rim are in its plane),
    closed where it overhangs."""
    W, D = round((5 + PLATE_OUT) * 2), round((5 + 2 * PLATE_FB) * 2)   # columns inner -> outer, rows front -> back
    up = [['V'] * W for _ in range(D)]
    for i in range(W): up[0][i], up[-1][i] = 'W', 'U'
    for j in range(D): up[j][0], up[j][-1] = ('U', 'W') if 0 < j < D - 1 else (up[j][0], up[j][-1])
    rail = W // 2 - 1
    for j in range(1, D - 1): up[j][rail], up[j][rail + 1] = 'N', 'O'
    up[1][rail] = up[1][rail + 1] = up[-2][rail] = up[-2][rail + 1] = 'X'
    for i, j in ((1, 1), (W - 2, 1), (1, D - 2), (W - 2, D - 2)): up[j][i] = 'X'
    side = lambda n: ['W' * n, 'U' * n]
    a, b = round(PLATE_FB * 2), round(PLATE_OUT * 2)   # overhang texels front / back and outside
    down = ['G' * W] * a + ['.' * (W - b) + 'G' * b] * (D - 2 * a) + ['G' * W] * a
    return {'north': side(W), 'south': side(W), 'east': side(D), 'west': side(D), 'up': [''.join(r) for r in up],
            'down': down}
def _decal(bare=False):
    """SHOULDER=decal: the shoulder plate drawn on, 2 texels per px, only the outward faces painted (see-through
    elsewhere: a decal, SKILL.md sec. 0). The top as the plate's (lit front and outer edges, rail and bolts), then down
    the outer, front and back faces a steel band with a lit top row and an ink edge under it, deepest at the outer
    corner (5 rows) and running out to 3 at the chest (the inner side, against the chest, stays bare).
    bare: only the top, a plain steel lid (the cage's cap colours, no rail or bolts)."""
    W, D, H = 10 if bare else 11, 10 if bare else 12, 1 if bare else 7   # columns inner -> outer, rows front -> back
    up = [['V'] * W for _ in range(D)]
    for i in range(W): up[0][i], up[-1][i] = 'W', 'U'
    for j in range(1, D - 1): up[j][0], up[j][-1] = 'U', 'W'
    if not bare:
        rail = W // 2 - 1
        for j in range(1, D - 1): up[j][rail], up[j][rail + 1] = 'N', 'O'
        up[1][rail] = up[1][rail + 1] = up[-2][rail] = up[-2][rail + 1] = 'X'
        for i, j in ((1, 1), (W - 2, 1), (1, D - 2), (W - 2, D - 2)): up[j][i] = 'X'
    up = [''.join(r) for r in up]
    none = lambda n: ['.' * n] * H
    if bare: return {'north': none(W), 'south': none(W), 'east': none(D), 'west': none(D), 'up': up, 'down': ['.' * W] * D}
    def band(depths, bolts=()):   # one column per depth: lit row, steel, ink under it, see-through below
        rows = [['.'] * len(depths) for _ in range(H)]
        for i, d in enumerate(depths):
            for j in range(d):
                rows[j][i] = 'W' if j == 0 else 'X' if j == d - 1 else 'V'
        for i in bolts: rows[2][i] = 'N'
        return [''.join(r) for r in rows]
    side = [3 + round(2 * i / (W - 1)) for i in range(W)]          # inner -> outer: 3 .. 5 rows
    return {'north': band(side[::-1], bolts=(1,)), 'south': band(side, bolts=(W - 2,)),   # north outer -> inner
            'east': band([5] * D, bolts=(2, D - 3)), 'west': none(D), 'up': up, 'down': ['.' * W] * D}
SHELLS['shoulder_plate'] = dict(faces={'plate': _plate, 'decal': _decal, 'bare': lambda: _decal(bare=True)}[SHOULDER]())

# Draft knob ENGINE ('none' / 'firebox'; 2026-11-05, user): the engine as parts round the torso, not only a backpack:
# the furnace and its exhausts on the back, a core in front, pipes between them through the sides. The armour is
# fitted to it later.
# - core: in the frame's slot (the dark ring round the copper valve on the chest, x +-2, raw y 21-25; user, after
#   drafts with it lower on the chest / on the waist / a porthole above the slot), 1 px proud so it reads as a
#   separate piece (picked over inset in the shell and half sunk). The slot is above raw 21.5, where the helmet's
#   1.5 px overhang sweeps down in front of the chest when the head pitches: it passes through the core from about
#   10 deg down (the user's call: proud reads better; engine_sweep.py has the angles). Its paint: frame_engine_art.py,
#   a porthole in a brass ring with copper corners and sides (user: to go with the pipes; picked over the frame's
#   gunmetal, which read as out of place, see-through corners, brass and steel).
# - pipes: two each side (2026-11-05, user), down the front to the abdomen, where there is room, then out to its
#   sides (user: rather than straight out along the chest): the top one from the core's top corner out 2 px, down
#   and across at y 18-19; the bottom one from under the core's bottom (user: not its side), down and across at
#   y 16-17, so they nest without crossing, 1 px apart. Round the sides they go on as thin pipes (0.4 px, in the
#   0.5-1 px between the abdomen and the arm: the engine is its own part, not paint on the frame; user) back to the
#   pack's copper inlets. Proud above raw 21.5 like the core: the helmet looking down passes through their tops too.
# - back: the radial firebox (frame_radial_art.py; 2026-11-07, user, picked from six drafts, commit 7a24d3f): an
#   aircraft radial engine on a mounting plate the abdomen's width (raw 15-26, 1 px deep, the side pipes' inlets on
#   its sides), seven finned cylinders round a hub with the fire in its porthole, two exhaust stubs under it. It
#   replaced a 10 x 11 x 5 twin-cylinder pack with the old suit's exhausts leaning back out of its top (2026-11-05):
#   those rose right behind the helmet, so looking up 20-30 deg swung its back into them; the radial's top cylinder
#   ends at raw 25.5. The helmet still sinks into the plate from behind when the head pitches back (engine_sweep.py),
#   so in game the worn helmet's tilt back is to be limited (the camera free), a decision for the renderer.
# - heart (draft, 2026-11-11, user: after Shiro Tomoe's engine heart in Tailenders, replacing the radial firebox, the
#   core and the pipes): an iron ball in the chest slot, copper hoses painted flat on a harness, two over the
#   shoulders and two to the waist, into the twin-cylinder pack with the old exhausts on the back (frame_heart_art.py).
# In game since 2026-11-14 (step 4): the saved files carry the engine (the heart, BACK=blower; the game shows the
# `engine` group only with an engine installed) with its fire dark (FIRE=dark below): the in-game texture, lit by the
# fire glowmask. ENGINE=none builds the bare frame, FIRE=lit shows it burning for a review.
ENGINE = os.environ.get('ENGINE', 'heart')
assert ENGINE in ('none', 'firebox', 'heart'), ENGINE
import frame_engine_art as engine_art
import frame_radial_art as radial_art
import frame_heart_art as heart_art
PAL.update(radial_art.EXTRA)
PAL.update(heart_art.EXTRA)
ENGINE_META = {}   # the radial's parts: their mirror / turn / shared paint (frame_radial_art.part)
PAL.update({'F': (0xff, 0xdc, 0x6e), 'I': (0xff, 0x96, 0x32), 'J': (0xd2, 0x46, 0x19)})   # fire, lit (see engine_art)
# Draft knob FIRE (2026-11-11): 'lit' paints the fire burning (review), 'dark' in the reserved coal colours of
# tools/make-glowmasks.py, as the texture has them in game, where the fire glowmask lights them by the burn state
# (SuitGlowLayer): an engine that is off.
FIRE = os.environ.get('FIRE', 'dark')
if FIRE == 'dark': PAL.update({'F': (0x3f, 0x21, 0x1b), 'I': (0x37, 0x1d, 0x19), 'J': (0x2f, 0x1a, 0x17)})
LIT = {(0x3f, 0x21, 0x1b): (0xff, 0xdc, 0x6e), (0x37, 0x1d, 0x19): (0xff, 0x96, 0x32), (0x2f, 0x1a, 0x17): (0xd2, 0x46, 0x19)}

def suit_faces(name, cols=None, rows=None):
    """A big-suit cube's painted faces as rows of RGBA (its UV flips applied, as it shows on the suit); cols / rows
    pick the texels kept per face ({face: list}), to size it down without scaling. Reserved fire colours lit."""
    m = json.load(open(SUIT))
    img = unpng(base64.b64decode(m['textures'][0]['source'].split(',', 1)[1]))
    e = next(x for x in m['elements'] if x['name'] == name)
    out = {}
    for f in FACES:
        u0, v0, u1, v1 = (int(c) for c in e['faces'][f]['uv'])
        face = [img[v][min(u0, u1):max(u0, u1)] for v in range(min(v0, v1), max(v0, v1))]
        if u1 < u0: face = [r[::-1] for r in face]
        if v1 < v0: face = face[::-1]
        if rows and f in rows: face = [face[j] for j in rows[f]]
        if cols and f in cols: face = [[r[i] for i in cols[f]] for r in face]
        out[f] = [[LIT.get(tuple(p[:3]), tuple(p[:3])) + (p[3],) for p in r] for r in face]
    return out

ENGINE_BOX, EXHAUST = {}, None
# Draft knob PACK (2026-11-11, user: the pack scaled down to the frame, from the big suit's; A picked): its width,
# height, depth (px), its upper and lower inlets' heights (raw). Its top stays flush with the chest's (raw 26).
PACKS = {'full': (10, 11, 5, 18, 16),       # as 4eec4a8
         'A': (8, 9, 4, 21, 18),
         'B': (8, 8, 3, 22, 19),
         'C': (6, 8, 3, 22, 19)}
PACK = os.environ.get('PACK', 'A')
# Draft knob BACK (2026-11-11, user: the pack's exhausts "don't evoke that cool mechanical vibe of a motor engine"):
# 'pistons' the twin-cylinder pack (PACK, EXH), or a motor (frame_motor_art.py): 'blower' (picked, 2026-11-11),
# 'vtwin', 'inline'.
BACK = os.environ.get('BACK', 'blower')
import frame_motor_art as motor_art
PAL.update(motor_art.EXTRA)
if ENGINE == 'heart':
    if BACK == 'pistons':
        PW_, PH_, PD, UP_Y, LOW_Y = PACKS[PACK]
        PX, PACK_TOP = PW_ / 2, 26
    else:
        MOTOR, PX, UP_Y, LOW_Y, PACK_TOP = motor_art.build(BACK, suit_faces, CHEST_X)
        for p in MOTOR:
            k = 'mt_' + p['name']
            ENGINE_BOX[k] = p['box']
            ENGINE_META[k] = p
            if p['faces']: SHELLS[f'en_{k}'] = dict(faces=p['faces'])
    # Under the armour (frame_heart_art.FRONT_LOW_Z): the waist strip in a plane between the step band and the arm.
    # Draft knob GUARD ('ring' / 'grille' / 'radiator' / 'hot'): the core's guard (frame_heart_art.bezel). Picked:
    # hot (2026-11-12, user), with flat armour.
    GUARD = os.environ.get('GUARD', 'hot')
    # ('game': both fronts, ht_ the open one, ha_ the armoured; one name per part, so their strips are their own)
    for armored, prefix in ((False, 'ht_'), (True, 'ha_')) if ARMOR == 'game' else ((ARMOR != 'none', 'ht_'),):
        for p in heart_art.build(CHEST_X, PX, UP_Y, LOW_Y, PACK_TOP, armored=armored, guard=GUARD,
                                 side_x=(WAIST_STEPS[0][1][0] + CHEST_X) / 2, flat=ARMOR_FORM == 'flat'):
            k = prefix + p['name']
            ENGINE_BOX[k] = p['box']
            ENGINE_META[k] = p
            if p['faces']: SHELLS[f'en_{k}'] = dict(faces=p['faces'])
if ENGINE == 'heart' and BACK == 'pistons':
    # the back: the twin-cylinder pack and the old suit's exhausts (commit 4eec4a8, where their picks are told;
    # 2026-11-11, user: "the original firebox with the furnace face and exhausts", over the radial)
    ENGINE_BOX['pack'] = ((-PX, 26 - PH_, TZ), (PX, 26, TZ + PD))
    # Draft knob EXH (2026-11-11, user: the old exhausts didn't line up with the holes in the pack, were a little
    # too big and leaned; integrate them): straight up out of the cylinders' heads, flush with the pack's back, the
    # pack's top painted round their feet. 'column': the cylinder goes on up as the stack, 2 px wide (its width),
    # 1.5 deep, 3 tall; 'stack': a 1 px pipe, 4 tall; 'stub': a 1 px pipe, 2 tall, under a 1.5 px cap.
    EXH = os.environ.get('EXH', 'column')
    CW = max(3, round(PW_ * 2) // 4) / 2                   # the cylinders' width (frame_engine_art.back_pistons_sized)
    EXH_X = PX - 0.5 - CW / 2                              # their centre (they stand 1 texel in from its sides)
    EW, ED, EH = {'column': (CW, 1.5, 3), 'stack': (1, 1, 4), 'stub': (1, 1, 2)}[EXH]
    EXH_Z = TZ + PD - ED / 2
    EXHAUST = dict(base=26, x=EXH_X, z=EXH_Z, lean=0)
    ENGINE_BOX['exhaust'] = ((EXH_X - EW / 2, 26, TZ + PD - ED), (EXH_X + EW / 2, 26 + EH, TZ + PD))
    exhaust = engine_art.stack_sized(EXH, round(EW * 2), round(EH * 2), round(ED * 2))
    if EXH == 'stub':
        ENGINE_BOX['exhaust_cap'] = ((EXH_X - 0.75, 26 + EH, TZ + PD - 1.25), (EXH_X + 0.75, 26.5 + EH, TZ + PD + 0.25))
        exhaust_cap = engine_art.stack_cap(3, 1, 3)
    rgba = lambda c: (ARMPAL[c] if c in ARMPAL else PAL[c]) + (255,)
    if PACK == 'full': art = engine_art.back_pistons()
    else:   # the exhausts' holes in its top (columns from -x, rows front -> back), both sides
        hx0 = round((EXH_X - EW / 2 + PX) * 2)
        holes = [(c0, round((TZ + PD - ED - TZ) * 2), round(EW * 2), round(ED * 2)) for c0 in (hx0, round(PW_ * 2) - hx0 - round(EW * 2))]
        art = engine_art.back_pistons_sized(round(PW_ * 2), round(PH_ * 2), round(PD * 2), holes)
    pack = {f: [[rgba(c) for c in r] for r in rows_] for f, rows_ in art.items()}
    # the hoses' copper inlets on its sides (UP_Y, LOW_Y), 1 px from its front (east runs back -> front)
    Q = PAL['Q'] + (255,)
    for f in ('east', 'west'):
        n = len(pack[f][0])
        for y in (UP_Y, LOW_Y):
            for j in range((25 - y) * 2, (26 - y) * 2):
                for i in (range(n - 2, n) if f == 'east' else range(0, 2)): pack[f][j][i] = Q
    rgbaf = lambda faces: {f: [[rgba(c) for c in r] for r in rows_] for f, rows_ in faces.items()}
    SHELLS.update({'en_pack': dict(faces=pack), 'en_exhaust': dict(faces=rgbaf(exhaust))})
    if EXH == 'stub': SHELLS['en_exhaust_cap'] = dict(faces=rgbaf(exhaust_cap))
if ENGINE == 'firebox':
    ENGINE_BOX['core'] = ((-2, 21, -TZ - 1), (2, 25, -TZ))
    Z = (-TZ - 1, -TZ)                              # the front pipes' depth: 1 px proud, as the core
    PIPES = {'pipe_t0': ((2, 24), (4, 25)), 'pipe_t1': ((3, 18), (4, 24)), 'pipe_t2': ((4, 18), (TX, 19)),
             'pipe_b0': ((1, 16), (2, 21)), 'pipe_b1': ((2, 16), (TX, 17))}
    for k, ((x0, y0), (x1, y1)) in PIPES.items():
        ENGINE_BOX[k] = ((x0, y0, Z[0]), (x1, y1, Z[1]))
    for k, y in (('pipe_ts', 18), ('pipe_bs', 16)):   # round the side, from the front pipe's end to the back's inlet
        ENGINE_BOX[k] = ((TX, y, Z[0]), (TX + 0.4, y + 1, TZ + 1))
    SHELLS['en_core'] = dict(faces=engine_art.porthole(corner='Q'))
    for k, box in ENGINE_BOX.items():
        if k.startswith('pipe'): SHELLS[f'en_{k}'] = dict(faces=engine_art.pipe_box(*[round((box[1][i] - box[0][i]) * 2) for i in range(3)]))
    for p in radial_art.build():
        k = 'fb_' + p['name']
        ENGINE_BOX[k] = p['box']
        ENGINE_META[k] = p
        if p['faces']: SHELLS[f'en_{k}'] = dict(faces=p['faces'])
# Knob TOOL ('none' / 'drill' / 'saw' / 'gun' / 'flame'; 2026-11-13, user: the big suit's power tools, sized down and redesigned, the drill
# first): the tool in the left arm's socket (SOCKET), on a `tool` bone under it. Tools are the exception to the simple
# boxes (user, 2026-11-13): they may be models of several parts. The drill: frame_drill_art.py; the chainsaw:
# frame_saw_art.py (its drafts SAW=A|B|C); the chaingun ('gun'): frame_gun_art.py; the flamethrower ('flame'):
# frame_flame_art.py.
# The tools' status lamp (LAMP: red | green for a review, dark: the reserved colours the game lights, frame_drill_art).
# 'all' (the saved files' default since 2026-11-14, step 5: the game shows the installed one): every tool at once, each
# on its own bones, named as the game's tools (GAME_BONES), in one texture.
TOOL = os.environ.get('TOOL', 'all')
assert TOOL in ('none', 'drill', 'saw', 'gun', 'flame', 'rail', 'tnt', 'em', 'all'), TOOL
TOOLS = ('drill', 'saw', 'gun', 'flame', 'rail', 'tnt', 'em') if TOOL == 'all' else () if TOOL == 'none' else (TOOL,)
# Each tool's bones: (the tool, its moving part) named as the game's (PowerTool.suitBone; the drill's bit and the chain
# spin / run by animation, the chaingun's barrels in code: ToolRotors).
GAME_BONES = {'drill': ('drill', 'drill_bit'), 'saw': ('chainsaw', 'chainsaw_chain'),
              'gun': ('chaingun', 'chaingun_barrels'), 'flame': ('flamethrower', 'flamethrower_bit'),
              'rail': ('rail_cannon', 'rail_fork_out'), 'tnt': ('tnt_launcher', 'tnt_launcher_drum'),
              'em': ('em_projector', 'em_projector_poles')}
EXTRA_BONES = {'rail': {'fork_in': 'rail_fork_in'}}   # a tool's other moving bones (the rail cannon's inner prong)
SHELLS['arm_socket_shell'] = dict(SHELLS['arm_shell'], below=[], end='socket')
if ARMOR != 'none': SHELLS['arm_socket_armor'] = dict(SHELLS['arm_armor'], below=[], end='socket')
def _tool_parts(TOOL):
  TOOL_PARTS = []
  if TOOL == 'drill':
    import frame_drill_art as drill_art
    TOOL_PARTS = drill_art.build(6.25 + ARM_OUT, SOCKET_Y, os.environ.get('LAMP', 'dark'), os.environ.get('DRILL_ART', 'B'),
                                 os.environ.get('DRILL_BASE', 'open'), os.environ.get('DRILL_FIT', 'fist'),
                                 os.environ.get('DRILL_BAND', 'slate'))
  if TOOL == 'saw':
    import frame_saw_art as saw_art
    TOOL_PARTS = saw_art.build(6.25 + ARM_OUT, SOCKET_Y, os.environ.get('LAMP', 'dark'), os.environ.get('SAW', 'B'),
                               os.environ.get('SAW_ART', 'B'), os.environ.get('SAW_FINS', 'A'),
                               os.environ.get('SAW_COWL', 'slate'), os.environ.get('SAW_BARREL', 'copper'),
                               os.environ.get('SAW_BAR', 'box'), os.environ.get('SAW_LOW', 'fins'),
                               os.environ.get('SAW_LOOK', 'rancher'))
# The chaingun (frame_gun_art.py): picked 2026-11-14 (user: "this is the one"): GUN_LOOK=doom, GUN_BARRELS=4,
# GUN_TOP=stack (the defaults); the other knobs are the rounds' drafts, kept to rebuild them.
  if TOOL == 'gun':
    import frame_gun_art as gun_art
    TOOL_PARTS = gun_art.build(6.25 + ARM_OUT, SOCKET_Y, os.environ.get('LAMP', 'dark'), os.environ.get('GUN', 'A'),
                               os.environ.get('GUN_BODY', 'ref'), os.environ.get('GUN_LOOK', 'doom'),
                               os.environ.get('GUN_BARRELS', '4'), os.environ.get('GUN_HANDLE', 'paint'),
                               os.environ.get('GUN_COUNTER') or os.environ.get('GUN_TOP', 'stack'), os.environ.get('GUN_DRUM', 'dark'),
                               float(os.environ.get('GUN_BODY_H', '4')), float(os.environ.get('GUN_BARREL_L', '5')))
# The flamethrower (frame_flame_art.py): picked 2026-11-14 after eight rounds (user: "definitely 5 tall"): FLAME=D (the
# barrel at the front, the red tank behind it, both under the body), FLAME_BODY=pump at FLAME_BODY_H=2, the 7 px barrel
# FLAME_HOLES=even, FLAME_TANK_H=5 (the defaults); the other knobs are the rounds' drafts, kept to rebuild them.
# FLAME_PILOT=dark (the reserved pilot colours, as in game) | lit (review).
  if TOOL == 'flame':
    import frame_flame_art as flame_art
    TOOL_PARTS = flame_art.build(6.25 + ARM_OUT, SOCKET_Y, os.environ.get('FLAME', 'D'), os.environ.get('FLAME_PILOT', 'dark'),
                                   os.environ.get('FLAME_GLOW', 'lit'), os.environ.get('FLAME_BODY', 'pump'),
                                   float(os.environ.get('FLAME_BODY_H', '2')), os.environ.get('FLAME_HOLES', 'even'),
                                   float(os.environ.get('FLAME_TANK_H', '5')), float(os.environ.get('FLAME_TANK_W', '3')))
# The rail cannon (frame_rail_art.py; 2026-11-15, the big suit's as the reference): RAIL=A gap | B core | C split,
# RAIL_CORE=dark | lit, RAIL_L the prongs' length. A picked (user, 2026-11-15): in TOOL=all; B, C kept as knobs.
  if TOOL == 'rail':
    import frame_rail_art as rail_art
    TOOL_PARTS = rail_art.build(6.25 + ARM_OUT, SOCKET_Y, 'dark', os.environ.get('RAIL', 'A'),
                                os.environ.get('RAIL_CORE', 'dark'), float(os.environ.get('RAIL_L', '6')))
# The TNT launcher (frame_tnt_art.py) and the EM projector (frame_em_art.py): the big suit's designs (user, 2026-11-15).
  if TOOL == 'tnt':
    import frame_tnt_art as tnt_art
    TOOL_PARTS = tnt_art.build(6.25 + ARM_OUT, SOCKET_Y)
  if TOOL == 'em':
    import frame_em_art as em_art
    TOOL_PARTS = em_art.build(6.25 + ARM_OUT, SOCKET_Y)
  return TOOL_PARTS
TOOL_PARTS = {t: _tool_parts(t) for t in TOOLS}
for t, parts_ in TOOL_PARTS.items():
    for p in parts_: SHELLS[f"tl_{t}_{p['name']}"] = dict(faces=p['faces'])
# where each shell's faces sit in the texture (below / beside nothing else), one strip per shell
SHELL_AT = {'arm_shell': (0, 64), 'leg_shell': (0, 80),
            'chest_armor': (35, 87), 'waist_armor': (128, 40), 'helmet_armor': (70, 112), 'arm_armor': (128, 0),
            'leg_armor': (224, 40), 'pauldron_armor': (192, 0), 'hip_armor': (192, 12),
            'waist0_armor': (128, 47), 'waist1_armor': (128, 54)}
# the engine's parts in the free block right of the skin (u 64-127, v 0-63), one strip each
SHELL_AT.update({'en_pack': (136, 57), 'en_exhaust': (64, 8), 'en_exhaust_cap': (64, 20), 'en_core': (64, 24),
                 'en_pipe_t0': (64, 34), 'en_pipe_t1': (64, 52), 'en_pipe_t2': (96, 34), 'en_pipe_b0': (84, 52),
                 'en_pipe_b1': (96, 38), 'en_pipe_ts': (64, 64), 'en_pipe_bs': (100, 64)})
if ENGINE_META:   # the radial's parts, shelf-packed below the texture's old bottom (it grows to 256 tall)
    TH = 256
    _u, _v, _rh = 0, 128, 0
    for k in [k for k in ENGINE_META if f'en_{k}' in SHELLS]:
        fs = SHELLS[f'en_{k}']['faces']
        w, h = sum(len(fs[f][0]) if fs[f] else 0 for f in FACES), max(len(fs[f]) for f in FACES)   # (a flat part's edges: no rows)
        if _u + w > 256: _u, _v, _rh = 0, _v + _rh, 0
        SHELL_AT[f'en_{k}'] = (_u, _v)
        _u, _rh = _u + w, max(_rh, h)
def shell_art(part, f):
    """The face's rows: letters ('#' bar, 'T' tucked bar, '.' hole, PAL colours) and (u, v) refs into the source
    canvas for the gauntlet / boot art copied below a limb's cage."""
    sp = SHELLS[part]
    if 'faces' in sp: return sp['faces'][f]
    if f == 'up': return sp['up']
    if f == 'down':
        u, v, w, h = GAUNT_UV[sp.get('end') or sp['below'][-1], 'down']
        return [[(u + i, v + j) for i in range(w)] for j in range(h)]
    rows = list(sp['cage'][f])
    for b in sp['below']:
        u, v, w, h = GAUNT_UV[b, f]
        rows += [[(u + i, v + j) for i in range(w)] for j in range(h) for _ in range(sp['rows'])]
    return rows

# The torso (out to the legs) and the belt don't fit beside the limbs' strips: a 256 wide texture, those on its right
# half.
TW = 256
SHELL_AT.update(belt_shell=(128, 32), chest_shell=(128, 80), abdomen_shell=(128, 92), shoulder_plate=(128, 104))

SHELL_UV, _used = {}, set()
# Parts without a fixed place (SHELL_AT None) go into the first free strip, scanning the texture row by row (the
# flat pauldron, 2026-11-12, outgrew the solid one's place).
if ARMOR_FORM == 'flat': SHELL_AT['pauldron_armor'] = None
for _k in SHELLS:
    if _k.startswith('tl_') or _k in ('arm_socket_shell', 'arm_socket_armor'): SHELL_AT[_k] = None
if HELMET_STYLE != 'suit': SHELL_AT['helmet_armor'] = None
for _p in HELMET_EXTRAS: SHELL_AT[f"hx_{_p['name']}"] = None
for _v in HELMET_VARIANTS:
    SHELL_AT[f'helmet_{_v}_armor'] = None
    for _p in HELMET_VARIANT_EXTRAS[_v]: SHELL_AT[f"hx_{_v}_{_p['name']}"] = None
# A compact part (the helmet's see-through outer layer) is mostly empty: its all-see-through faces take no room, they
# all map to one see-through texel (EMPTY_UV), so only its painted faces need a strip.
def _blank(part, f): return SHELLS[part].get('compact') and all(c == '.' for r in shell_art(part, f) for c in r)
EMPTY_UV = None
def _free_at(part):
    sizes = [shell_art(part, f) for f in FACES if not _blank(part, f)]
    w, h = sum(len(a[0]) if a else 0 for a in sizes), max(len(a) for a in sizes)
    S = [[0] * (TW + 1) for _ in range(TH + 1)]   # summed-area table of the used texels (each try is then O(1))
    for y in range(TH):
        for x in range(TW):
            S[y + 1][x + 1] = S[y][x + 1] + S[y + 1][x] - S[y][x] + ((x, y) in _used or (x < 64 and y < 64))
    for v in range(0, TH - h + 1):
        for u in range(0, TW - w + 1):
            if S[v + h][u + w] - S[v][u + w] - S[v + h][u] + S[v][u] == 0: return u, v
    raise AssertionError(('no room', part, w, h))
for part, at in sorted(SHELL_AT.items(), key=lambda kv: kv[1] is None):
    if part not in SHELLS: continue
    u, v = at or _free_at(part)
    for f in FACES:
        if _blank(part, f):
            if EMPTY_UV is None:   # a texel left free (so see-through) in the strip's row, past its end
                SHELL_AT['_empty'] = None
                SHELLS['_empty'] = dict(faces={g: ['.'] if g == 'north' else [] for g in FACES})
                EMPTY_UV = _free_at('_empty')
                del SHELL_AT['_empty'], SHELLS['_empty']
                _used.add(EMPTY_UV)
            SHELL_UV[part, f] = (*EMPTY_UV, 1, 1)
            continue
        art = shell_art(part, f)
        w, h = (len(art[0]) if art else 0), len(art)
        SHELL_UV[part, f] = (u, v, w, h)
        cells = {(u + i, v + j) for i in range(w) for j in range(h)}
        assert u + w <= TW and v + h <= TH and not cells & _used and all(x >= 64 or y >= 64 for x, y in cells), (part, f)
        _used |= cells
        u += w

def paint_shells(px, src):
    for part in SHELLS:
        for f in FACES:
            if _blank(part, f): continue
            u, v, w, h = SHELL_UV[part, f]
            for j, line in enumerate(shell_art(part, f)):
                for i, c in enumerate(line):
                    if c == '.': px[v + j][u + i] = (0, 0, 0, 0)
                    elif c in ('#', 'T'): px[v + j][u + i] = bar(i, j)
                    elif c in ARMPAL: px[v + j][u + i] = ARMPAL[c] + (255,)
                    elif len(c) == 4: px[v + j][u + i] = c                      # a colour (the helmet's)
                    elif isinstance(c, str) and c in GRAIN:
                        px[v + j][u + i] = tuple(min(k + (6 if (i + j) % 3 == 0 else 0), 255) for k in PAL[c]) + (255,)
                    elif isinstance(c, str): px[v + j][u + i] = PAL[c] + (255,)
                    else: px[v + j][u + i] = src[c[1]][c[0]]

def shell_slabs(part, a, b):
    """The shell's solid texels ('T' aside) as thin boxes (right side coordinates) with their (face, column, row), for
    the clearance check: a hole may pass through another part, a bar may not."""
    (x0, y0, z0), (x1, y1, z1) = a, b
    t, out = 0.01, []
    for f in FACES:
        art = shell_art(part, f)
        if not art: continue
        n, m = len(art[0]), len(art)
        cw = (z1 - z0 if f in ('east', 'west') else x1 - x0) / n
        rh = (z1 - z0 if f in ('up', 'down') else y1 - y0) / m
        for j, line in enumerate(art):
            for i, c in enumerate(line):
                if c in ('.', 'T'): continue
                ya, yb = y1 - (j + 1) * rh, y1 - j * rh
                if f == 'north': out.append(((x1 - (i + 1) * cw, ya, z0), (x1 - i * cw, yb, z0 + t), (f, i, j)))
                elif f == 'south': out.append(((x0 + i * cw, ya, z1 - t), (x0 + (i + 1) * cw, yb, z1), (f, i, j)))
                elif f == 'east': out.append(((x1 - t, ya, z1 - (i + 1) * cw), (x1, yb, z1 - i * cw), (f, i, j)))
                elif f == 'west': out.append(((x0, ya, z0 + i * cw), (x0 + t, yb, z0 + (i + 1) * cw), (f, i, j)))
                elif f == 'up': out.append(((x0 + i * cw, y1 - t, z0 + j * rh), (x0 + (i + 1) * cw, y1, z0 + (j + 1) * rh), (f, i, j)))
                else: out.append(((x0 + i * cw, y0, z0 + j * rh), (x0 + (i + 1) * cw, y0 + t, z0 + (j + 1) * rh), (f, i, j)))
    return out

def paint_gauntlet(px):
    m = json.load(open(SUIT))
    img = unpng(base64.b64decode(m['textures'][0]['source'].split(',', 1)[1]))
    assert len(img[0]) == m['resolution']['width'], 'suit texture and UV resolution differ'
    els = {e['name']: e for e in m['elements']}
    for part, (src, picks) in GAUNT.items():
        for f in FACES:
            u0, v0, u1, v1 = (int(c) for c in els[src]['faces'][f]['uv'])
            face = [img[v][min(u0, u1):max(u0, u1)] for v in range(min(v0, v1), max(v0, v1))]
            if u1 < u0: face = [r[::-1] for r in face]        # as it shows on the suit (its UV flips applied)
            if v1 < v0: face = face[::-1]
            cols, rows = picks[f]
            u, v, w, h = GAUNT_UV[part, f]
            for j, sy in enumerate(rows):
                for i, sx_ in enumerate(cols):
                    px[v + j][u + i] = face[sy][sx_]
    for f in FACES:
        u, v, w, h = GAUNT_UV['boot', f]
        for j, line in enumerate(BOOT[f]):
            for i, ch in enumerate(line):
                px[v + j][u + i] = PAL[ch] + (255,)
    for f in FACES:
        u, v, w, h = GAUNT_UV['socket', f]
        for j, line in enumerate(SOCKET[f]):
            for i, ch in enumerate(line):
                px[v + j][u + i] = (CONTACT if ch == '+' else PAL[ch]) + (255,)

def model_tex():   # Steve's real skin at 0,0 + the shells (their gauntlet / boot art copied from a source canvas)
    px = [[(0, 0, 0, 0)] * TW for _ in range(TH)]
    for y, row in enumerate(steve_skin()):
        px[y][:len(row)] = row
    src = [[(0, 0, 0, 0)] * 64 for _ in range(32)]
    paint_gauntlet(src)
    paint_shells(px, src)
    return png(TW, TH, px)

def b64(b): return 'data:image/png;base64,' + base64.b64encode(b).decode()

# ---------------------------------------------------------------- model building
def uid(): return str(uuid.uuid4())

groups, elements = [], []
def group(name, origin, parent, visible=True):
    g = {'name': name, 'uuid': uid(), 'export': True, 'locked': False, 'scope': 0, 'selected': False, 'visibility': visible,
         'origin': [origin[0], origin[1] + FY, origin[2]], 'rotation': [0, 0, 0], 'bedrock_binding': '', 'color': 0, 'children': [],
         'reset': False, 'shade': True, 'mirror_uv': False, 'autouv': 0, 'isOpen': True, 'primary_selected': False}
    groups.append(g)
    g['_parent'] = parent
    if parent is not None: parent['children'].append(g)
    return g

def cube(g, name, a, b, raw=False):
    """A cube in bone g, its faces filled in by the caller (painted / steve)."""
    (x0, y0, z0), (x1, y1, z1) = a, b
    if not raw: y0, y1 = y0 + FY, y1 + FY
    e = {'name': name, 'box_uv': False, 'render_order': 'default', 'locked': False, 'export': True, 'scope': 0,
         'allow_mirror_modeling': True, 'from': [min(x0, x1), min(y0, y1), min(z0, z1)],
         'to': [max(x0, x1), max(y0, y1), max(z0, z1)], 'autouv': 0, 'color': 1, 'origin': list(g['origin']),
         'faces': {}, 'type': 'cube', 'uuid': uid()}
    elements.append(e)
    e['_g'] = g
    g['children'].append(e['uuid'])
    return e

def painted(g, side, part, name, a, b, raw=False):
    """A shell's cube (right side coordinates) with its art; the left one is the mirror image (east / west swap,
    every face's u reversed), so both sides read the same."""
    r = side == 'r'
    e = cube(g, name, *((a, b) if r else mir(a, b)), raw=raw)
    e['_shell'] = True
    for f in FACES:
        src = f if r else {'east': 'west', 'west': 'east'}.get(f, f)
        u, v, w, h = SHELL_UV[part, src]
        e['faces'][f] = {'uv': [u, v, u + w, v + h] if r else [u + w, v, u, v + h], 'texture': 0}
    return e

def hollow(g, side, part, name, a, b, raw=False):
    """A shell: a painted cube whose see-through texels the clearance check ignores (it checks shell_slabs)."""
    e = painted(g, side, part, name, a, b, raw=raw)
    e['_args'] = (part, side, a, b, 0 if raw else FY)
    slab_up(e)
    return e

def slab_up(e):
    part, side, a, b, dy = e['_args']
    slabs = []
    for p, q, tid in shell_slabs(part, (a[0], a[1] + dy, a[2]), (b[0], b[1] + dy, b[2])):
        if side == 'l': p, q = mir(p, q)
        slabs.append({'name': e['name'], 'from': [min(p[i], q[i]) for i in range(3)], 'to': [max(p[i], q[i]) for i in range(3)],
                      'origin': e['origin'], 'uuid': uid(), '_g': e['_g'], '_tid': tid})
    e['_hollow'] = slabs

def steve(g, name, a, b, box):
    """Steve's part: a box-UV cube at the skin's (u, v) for a w x h x d box, faces laid out as Blockbench's box UV does
    (east = the part's right side at u, north = front, west, south = back; up / down flipped), so it reads like vanilla."""
    u, v, w, h, d = box
    e = cube(g, name, a, b)
    e['box_uv'] = True
    e['uv_offset'] = [u, v]
    f = e['faces']
    for k, uv in {'east': [u, v + d, u + d, v + d + h], 'north': [u + d, v + d, u + d + w, v + d + h],
                  'west': [u + d + w, v + d, u + 2 * d + w, v + d + h], 'south': [u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h],
                  'up': [u + d + w, v + d, u + d, v], 'down': [u + d + 2 * w, v, u + d + w, v + d]}.items():
        f[k] = {'uv': uv, 'texture': 0}
    return e

# the 64x64 skin's boxes (u, v, w, h, d); the left limbs have their own areas (not mirrors of the right ones)
# (the slim build's pilot, Alex, has 3 px arms: on the inner side of the cage, as vanilla's slim arms hug the torso)
AW = 3 if BUILD == 'slim' else 4
STEVE = {'head': (0, 0, 8, 8, 8), 'torso': (16, 16, 8, 12, 4), 'arm_r': (40, 16, AW, 12, 4), 'arm_l': (32, 48, AW, 12, 4),
         'leg_r': (0, 16, 4, 12, 4), 'leg_l': (16, 48, 4, 12, 4)}
def mir(a, b): return (-a[0], a[1], a[2]), (-b[0], b[1], b[2])

root = group('marine', (0, 0, 0), None)
body = group('body', (0, 14, 0), root)
torso = group('torso', (0, 14, 0), body)
head = group('head', (0, 26, 0), torso)

# ---------- head: no frame. The helmet is a separate armour piece (a later step); the bone is here for it.
pilot = group('pilot_head', (0, 26, 0), head)
steve(pilot, 'st_head', (-4, 26, -4), (4, 34, 4), STEVE['head'])

# ---------- torso: an exoskeleton, not a ribcage: load-bearing members from the belt up to the shoulders, no hoops
# (its art: _torso()).
hollow(torso, 'r', 'chest_shell', 'fr_chest_shell', (-CHEST_X, 20, -TZ), (CHEST_X, 26, TZ))
hollow(torso, 'r', 'abdomen_shell', 'fr_abdomen_shell', (-TX, 15, -TZ), (TX, 20, TZ))
pilot = group('pilot_torso', (0, 14, 0), torso)
steve(pilot, 'st_torso', (-4, 14, -2), (4, 26, 2), STEVE['torso'])

# ---------- belt (the hip): a ring outside Steve's pelvis, on the body bone (its art: _belt())
hollow(body, 'r', 'belt_shell', 'fr_belt_shell', (-BELT_X, 14, -3), (BELT_X, 15, 3))

# ---------- limbs (right side defined, left mirrored). Steve's limbs don't bend, so each limb is ONE rigid bone.
for side in ('r', 'l'):
    s = 1 if side == 'r' else -1
    nm = 'right' if s > 0 else 'left'
    sx = lambda a, b: (a, b) if s > 0 else mir(a, b)
    # leg: Steve's leg x 0..4, hip pivot (±2, 14)
    leg = group(f'{nm}_leg', ((2 + LEG_OUT) * s, 14, 0), root)
    leg['rotation'] = [0, 0, LEG_SPLAY * s]
    # One box: the sole and the cage above it (its art: SHELLS, _cage, BOOT). The sole is 5x4x5 under his foot, placed
    # on his leg as the fist is on his arm (0.25 px inside, 0.75 px outside, 0.5 px front and back), 3 px under his
    # foot's bottom; the cage is in line with it, from the sole (y 4) up. It turns with the leg, so the sole tilts with
    # the splay (outer edge 0.1 px up at 2 deg). It stops at y 15.5, 0.5 px under the belt: its top band's outer end
    # rises as the leg splays.
    hollow(leg, side, 'leg_shell', f'fr_leg_shell_{side}', (-0.25 + LEG_OUT, 0, -2.5), (4.75 + LEG_OUT, 15.5, 2.5), raw=True)
    p = group(f'pilot_{nm}_leg', ((2 + LEG_OUT) * s, 14, 0), leg)
    steve(p, f'st_leg_{side}', *sx((0 + LEG_OUT, 2, -2), (4 + LEG_OUT, 14, 2)), STEVE[f'leg_{side}'])
    # arm: Steve's arm x 4..8 (his hand at the bottom, y 14), shoulder pivot (±6, 26)
    arm = group(f'{nm}_arm', ((6 + ARM_OUT) * s, 26, 0), torso)
    arm['rotation'] = [0, 0, ARM_SPLAY * s]
    # One box: the fist (the big suit's, sized down: 5x4x5 over his hand, so 2 px past it) and the cage above it, up to
    # his shoulder's top. Its footprint is 0.5 px round his arm front and back, 0.25 px inside (the closest encloses()
    # allows) and 0.75 px outside.
    # the left arm (the tool arm) ends in the socket instead of the fist (SOCKET)
    hollow(arm, side, 'arm_socket_shell' if side == 'l' else 'arm_shell', f'fr_arm_shell_{side}',
           (3.75 + ARM_OUT, SOCKET_Y if side == 'l' else 10, -2.5), (8.75 + ARM_OUT, 26, 2.5))
    for t, parts_ in (TOOL_PARTS.items() if side == 'l' else ()):   # each tool, its pivot on the arm's axis at the
        # socket (a drill's bit spins about y)
        tg = group(GAME_BONES[t][0], (-(6.25 + ARM_OUT), SOCKET_Y, 0), arm)
        bones = {'tool': tg, 'bit': group(GAME_BONES[t][1], (-(6.25 + ARM_OUT), SOCKET_Y, 0), tg)}   # the bit moves, the rest not
        for key, name in EXTRA_BONES.get(t, {}).items(): bones[key] = group(name, (-(6.25 + ARM_OUT), SOCKET_Y, 0), tg)
        for tp in parts_:
            g_ = bones[tp.get('bone', 'tool')]
            e = painted(g_, 'l', f"tl_{t}_{tp['name']}", f"tl_{t}_{tp['name']}", *tp['box'])
            if tp['rot']: e['rotation'], e['origin'] = [0, -tp['rot'], 0], list(g_['origin'])
            for f in FACES:   # a face all see-through isn't drawn (the drill's open base: its bottom lies in the socket's plane)
                if all(c == '.' for r in tp['faces'][f] for c in r): e['faces'][f]['texture'] = None
    p = group(f'pilot_{nm}_arm', ((6 + ARM_OUT) * s, 26, 0), arm)
    st = steve(p, f'st_arm_{side}', *sx((4 + ARM_OUT, 14, -2), (4 + AW + ARM_OUT, 26, 2)), STEVE[f'arm_{side}'])
    if side == 'l': st['faces']['down']['texture'] = None   # in the socket's plane, under it (SOCKET)
    # the shoulder plate on the arm box's top, its inner side over the arm box's inner wall
    if SHOULDER == 'plate':
        painted(arm, side, 'shoulder_plate', f'fr_shoulder_plate_{side}',
                (3.75 + ARM_OUT, 26, -2.5 - PLATE_FB), (8.75 + ARM_OUT + PLATE_OUT, 27, 2.5 + PLATE_FB))
    elif SHOULDER == 'decal':   # 3.5 px of the arm's top, 0.5 off it outside, front, back and above
        hollow(arm, side, 'shoulder_plate', f'fr_shoulder_plate_{side}',
               (3.75 + ARM_OUT, 23, -2.5 - DECAL), (8.75 + ARM_OUT + DECAL, 26 + DECAL, 2.5 + DECAL))
    else:   # the lid: 0.1 px over his arm's top (in its plane it would flicker)
        hollow(arm, side, 'shoulder_plate', f'fr_shoulder_plate_{side}',
               (3.75 + ARM_OUT, 26, -2.5), (8.75 + ARM_OUT, 26.1, 2.5))

# ---------------------------------------------------------------- clearance check, in the posed rest pose
# Every cube in world space (its own rotation, then each bone's, all about z), as an xy quad plus a z range. Fails on
# any overlap deeper than EPS between the frame and Steve, or between frame cubes of different limbs (touching is fine).
EPS = 1e-3
def world(e):
    import math
    (x0, y0, z0), (x1, y1, z1) = e['from'], e['to']
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    def rot(pts, origin, deg):
        if not deg: return pts
        a = math.radians(deg); c, sn = math.cos(a), math.sin(a)
        return [(origin[0] + (x - origin[0]) * c - (y - origin[1]) * sn, origin[1] + (x - origin[0]) * sn + (y - origin[1]) * c)
                for x, y in pts]
    pts = rot(pts, e['origin'], e.get('rotation', [0, 0, 0])[2])
    g = e['_g']
    while g is not None:
        pts = rot(pts, g['origin'], g['rotation'][2])
        g = g['_parent']
    return pts, (z0, z1)

def overlap(a, b):
    (pa, za), (pb, zb) = a, b
    if min(za[1], zb[1]) - max(za[0], zb[0]) <= EPS: return False
    for poly in (pa, pb):   # separating axis test on the quads' edge normals
        for i in range(4):
            (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % 4]
            n = (y0 - y1, x1 - x0)
            ln = (n[0] ** 2 + n[1] ** 2) ** 0.5
            pr = lambda P: [(x * n[0] + y * n[1]) / ln for x, y in P]
            A, B = pr(pa), pr(pb)
            if min(max(A), max(B)) - max(min(A), min(B)) <= EPS: return False
    return True

def limb(e):
    g = e['_g']
    while g is not None and g['name'] not in ('right_leg', 'left_leg', 'right_arm', 'left_arm'):
        g = g['_parent']
    return g['name'] if g else 'core'

def turn(e):   # a cube's total turn in world space (its own, then its bones'; all about z)
    t, g = e.get('rotation', [0, 0, 0])[2], e['_g']
    while g is not None:
        t, g = t + g['rotation'][2], g['_parent']
    return t

def encloses(sh, st, W, margin=0.25):
    """In the shell's own frame (its world turn undone), Steve's part, cut to the shell's height, sits inside it with
    `margin` to spare at the sides and front / back (so no face of his lies in a face of the shell: no z-fighting)."""
    import math
    margin -= 1e-6
    a = math.radians(-turn(sh)); c, sn = math.cos(a), math.sin(a)
    rot = lambda P: [(x * c - y * sn, x * sn + y * c) for x, y in P]
    S, P = rot(W[sh['uuid']][0]), rot(W[st['uuid']][0])
    x0, x1 = min(x for x, _ in S), max(x for x, _ in S)
    y0, y1 = min(y for _, y in S), max(y for _, y in S)
    xs = [x for x, y in P if y0 <= y <= y1]
    for (xa, ya), (xb, yb) in zip(P, P[1:] + P[:1]):   # where his outline crosses the shell's top and bottom
        for yc in (y0, y1):
            if (ya - yc) * (yb - yc) < 0: xs.append(xa + (xb - xa) * (yc - ya) / (yb - ya))
    (za, zb), (zc, zd) = W[sh['uuid']][1], W[st['uuid']][1]
    return (not xs or (min(xs) >= x0 + margin and max(xs) <= x1 - margin)) and za <= zc - margin and zb >= zd + margin

def to_world(e, pts):
    """3D points of cube e (its coordinates) in world space: its own turn, then its bones' (all about z)."""
    import math
    def rot(P, o, deg):
        if not deg: return P
        a = math.radians(deg); c, sn = math.cos(a), math.sin(a)
        return [(o[0] + (x - o[0]) * c - (y - o[1]) * sn, o[1] + (x - o[0]) * sn + (y - o[1]) * c, z) for x, y, z in P]
    pts = rot(pts, e['origin'], e.get('rotation', [0, 0, 0])[2])
    g = e['_g']
    while g is not None:
        pts = rot(pts, g['origin'], g['rotation'][2])
        g = g['_parent']
    return pts

def quads(e):
    (x0, y0, z0), (x1, y1, z1) = e['from'], e['to']
    fs = [[(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
          [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],
          [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)]]
    # a flat cube (a plane, e.g. the slim build's waist strip) has faces with no area: no plane of their own
    # a face not drawn (texture None: his hand's bottom in the socket) has no plane either
    names = ('north', 'south', 'west', 'east', 'down', 'up')
    fs = [f for f, n in zip(fs, names) if len({p for p in f}) == 4 and e.get('faces', {}).get(n, {}).get('texture', 0) is not None]
    return [to_world(e, f) for f in fs]

def coplanar(A, B, eps=1e-3, area=0.05):
    """Do quads A and B lie in one plane (within eps) and overlap there by more than `area` px each way? (The frame's
    texel slabs are 0.01 px thick: their edges are no faces.)"""
    sub = lambda p, q: tuple(p[k] - q[k] for k in range(3))
    dot = lambda p, q: sum(p[k] * q[k] for k in range(3))
    crs = lambda p, q: (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0])
    nrm = lambda p: tuple(c / dot(p, p) ** 0.5 for c in p)
    n = nrm(crs(sub(A[1], A[0]), sub(A[3], A[0])))
    m = nrm(crs(sub(B[1], B[0]), sub(B[3], B[0])))
    if abs(abs(dot(n, m)) - 1) > 1e-6 or abs(dot(n, sub(B[0], A[0]))) > eps: return False
    u = nrm(sub(A[1], A[0])); v = crs(n, u)
    P = [(dot(sub(p, A[0]), u), dot(sub(p, A[0]), v)) for p in A]
    Q = [(dot(sub(p, A[0]), u), dot(sub(p, A[0]), v)) for p in B]
    for poly in (P, Q):
        for i in range(4):
            (xa, ya), (xb, yb) = poly[i], poly[(i + 1) % 4]
            ax = (ya - yb, xb - xa)
            ln = (ax[0] ** 2 + ax[1] ** 2) ** 0.5
            if ln < 1e-9: continue
            pr = lambda R: [(x * ax[0] + y * ax[1]) / ln for x, y in R]
            a_, b_ = pr(P), pr(Q)
            if min(max(a_), max(b_)) - max(min(a_), min(b_)) <= area: return False
    return True

def _centre(e):
    q = [p for f in quads(e) for p in f]
    return tuple(sum(p[k] for p in q) / len(q) for k in range(3))

def check_armor():
    """The sealed pieces: each encloses Steve's part of its bone (0.1 px to spare, so no face of his lies in one of
    its faces), and no face of a piece shares a plane with any other face (Steve's, the frame's solid texels', another
    piece's) unless the two meet back to back, their boxes on either side of the plane (touching boxes: shut in).
    Overlapping other solid parts is fine (each hides the other's faces inside it)."""
    bad = []
    pieces = [e for e in elements if e.get('_armor')]
    others = [x for e in elements for x in e.get('_hollow', [e])]
    W = {x['uuid']: world(x) for x in others + pieces}
    side = lambda A, P: sum((P[k] - A[0][k]) * n for k, n in enumerate(_normal(A)))
    for a in pieces:
        for st in elements:
            if a['_armor'] != 'addon' and st['name'].startswith('st_') and limb(st) == limb(a) \
                    and st['_g']['_parent'] is a['_g']['_parent'] \
                    and not encloses(a, st, W, margin=0.1):
                bad.append((a['name'], 'does not enclose', st['name']))
        fa, ca = [A for x in a.get('_hollow', [a]) for A in quads(x)], _centre(a)
        planes = {}                                    # the piece's faces by plane, so each other face is tested only
        for A in fa:                                   # against the piece's faces in its own plane (a hollow piece,
            planes.setdefault(_plane_key(A), []).append(A)   # the helmet's layer, is thousands of texel slabs: testing
        for o in others:                               # every pair took ~12 min a build)
            if o['name'] == a['name'] or apart(a, o): continue
            co = _centre(o)
            for B in quads(o):
                axis, k = _plane_key(B)
                near = [A for kk in (k - 1, k, k + 1) for A in planes.get((axis, kk), ())]
                if any(coplanar(A, B) and side(A, ca) * side(A, co) >= 0 for A in near):
                    bad.append((a['name'], 'shares a plane with', o['name']))
                    break
    return bad

PLANE_BIN = 0.05   # px; wider than coplanar()'s eps, so two faces in one plane fall in the same or the next bin


def _plane_key(A):
    """A face's plane, coarsely: the axis its normal is closest to and its distance from the origin along the normal
    (turned to point along that axis), in PLANE_BIN steps. Faces coplanar() calls one plane share the axis and have
    keys at most one step apart."""
    n = _normal(A)
    axis = max(range(3), key=lambda k: abs(n[k]))
    ln = sum(c * c for c in n) ** 0.5 * (1 if n[axis] > 0 else -1)
    return axis, round(sum(A[0][k] * n[k] for k in range(3)) / ln / PLANE_BIN)


def _normal(A):
    u = [A[1][k] - A[0][k] for k in range(3)]; v = [A[3][k] - A[0][k] for k in range(3)]
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])

def check():
    items = [s for e in elements if not e.get('_armor') for s in e.get('_hollow', [e])]   # shells by their solid texels
    of = {s['uuid']: e for e in elements for s in e.get('_hollow', [])}
    W = {e['uuid']: world(e) for e in elements + items}
    bad = []
    for i, a in enumerate(items):
        for b in items[i + 1:]:
            if apart(a, b): continue
            if limb(a) == limb(b) and (a['uuid'] in of or b['uuid'] in of):   # a shell's texel and his part
                sh, st = (of[a['uuid']], b) if a['uuid'] in of else (of[b['uuid']], a)
                if st['name'].startswith(('fr_', 'ar_')) or encloses(sh, st, W): continue
            if limb(a) == limb(b) and {a['name'][:3], b['name'][:3]} & {'tl_'}:   # a tool (TOOL) on its own arm:
                o = b if a['name'].startswith('tl_') else a
                if o['name'].startswith(('fr_', 'ar_', 'tl_')): continue          # built on it (a collar wraps it)
                t_ = a if o is b else b                                          # his arm: inside it with room, or clear
                if encloses(t_, o, W) or not overlap(W[a['uuid']], W[b['uuid']]): continue
                bad.append((a['name'], b['name'])); continue
            fa, fb = a['name'].startswith(('fr_', 'ar_')), b['name'].startswith(('fr_', 'ar_'))
            if not (fa or fb): continue                                   # Steve against himself: vanilla's business
            if fa and fb and limb(a) == limb(b): continue                 # one limb's frame is built touching itself
            if overlap(W[a['uuid']], W[b['uuid']]): bad.append((a['name'], b['name']))
    return bad

# ---------------------------------------------------------------- armour (draft)
# One piece per bone, each in its own group (so a piece can be shown / hidden as one): helmet, torso, arms, legs. A
# piece replaces the frame cubes it covers (unlink drops them).
def _armor(bone, side, piece, name, raw=False, box=None, addon=False):
    g = next(x for x in groups if x['name'] == bone)
    ga = next((x for x in groups if x['name'] == f'armor_{bone}'), None) or \
        group(f'armor_{bone}', [g['origin'][0], g['origin'][1] - FY, g['origin'][2]], g)
    open_ = any('.' in r for rows in SHELLS[f'{piece}_armor']['faces'].values() for r in rows) \
        if 'faces' in SHELLS[f'{piece}_armor'] else False
    e = (hollow if open_ else painted)(ga, side, f'{piece}_armor', name, *(box or ARMOR_BOX[piece]), raw=raw)
    e['_armor'] = 'addon' if addon else True
def unlink(name):
    e = next(x for x in elements if x['name'] == name)
    if ARMOR == 'game':   # kept, in the part's frame group (shown while the part is bare)
        return regroup(e, f"frame_{e['_g']['name']}")
    elements.remove(e)
    e['_g']['children'].remove(e['uuid'])

def regroup(e, name):
    """Moves cube e into its bone's child group `name` (made at the bone's pivot: nothing moves)."""
    g = e['_g']
    ng = next((x for x in groups if x['name'] == name), None) or \
        group(name, [g['origin'][0], g['origin'][1] - FY, g['origin'][2]], g)
    g['children'].remove(e['uuid'])
    ng['children'].append(e['uuid'])
    e['_g'] = ng
    for slab in e.get('_hollow', []): slab['_g'] = ng
    return e

# ALT (ARMOR=game): what is never drawn together. A cube's alternative: (slot, variant), the slot an armour part (torso
# / arm / leg, per side), the variant 'frame' (shown while it's bare) or 'armour' (while worn); two cubes of one slot
# and different variants are never both drawn, so the checks skip them.
# The belt and its piece, the hip (the slate block round his pelvis), go with the LEGS (the hip is the leg pieces' part,
# as vanilla's leggings have a body part): the hip shows with either leg piece on, the belt with both legs bare. (With
# the belt kept under a leg piece, the piece's top and outer side lay in the belt's top and side planes.)
ALT_SLOT = {'torso': 'torso', 'body': 'hip', 'right_arm': 'arm_r', 'left_arm': 'arm_l', 'right_leg': 'leg_r', 'left_leg': 'leg_l'}
def alt(e):
    g = e['_g']
    if g['name'].startswith('helm_'):   # the helmet styles: one drawn at a time
        return 'head', g['name']
    if g['name'].startswith(('frame_', 'armor_')) and g['_parent']['name'] in ALT_SLOT:
        return ALT_SLOT[g['_parent']['name']], g['name'].split('_')[0]
    if g['name'] in ('engine_open', 'engine_armored'):
        return 'torso', 'frame' if g['name'] == 'engine_open' else 'armor'
    return None
def apart(a, b):
    """Never drawn together (ALT)."""
    x, y = alt(a), alt(b)
    if x is not None and y is not None and {x, y} & {('hip', 'frame')} and {x, y} & {('leg_r', 'armor'), ('leg_l', 'armor')}:
        return True   # the belt goes when a leg piece goes on
    return x is not None and y is not None and x[0] == y[0] and x[1] != y[1]
if 'helmet_armor' in SHELLS:
    _armor('head', 'r', 'helmet', 'ar_helmet')
    _gh = next(x for x in groups if x['name'] == 'armor_head')
    for _p in HELMET_EXTRAS:   # checked as boxes (painted, like the pauldron decal)
        e = (hollow if _p.get('hollow') else painted)(_gh, 'r', f"hx_{_p['name']}", f"ar_hx_{_p['name']}", *_p['box'])
        e['_armor'] = 'addon'
    if HELMET_VARIANTS:   # the standard helmet into helm_standard, each style's beside it (HELMET_VARIANTS)
        for e in [x for x in elements if x['_g'] is _gh]: regroup(e, 'helm_standard')
        for _v in HELMET_VARIANTS:
            _gv = group(f'helm_{_v}', [_gh['origin'][0], _gh['origin'][1] - FY, _gh['origin'][2]], _gh)
            e = painted(_gv, 'r', f'helmet_{_v}_armor', f'ar_helmet_{_v}', *ARMOR_BOX['helmet'])
            e['_armor'] = True
            for _p in HELMET_VARIANT_EXTRAS[_v]:
                e = (hollow if _p.get('hollow') else painted)(_gv, 'r', f"hx_{_v}_{_p['name']}", f"ar_hx_{_v}_{_p['name']}", *_p['box'])
                e['_armor'] = 'addon'
if ARMOR != 'none':
    for piece, frame in (('chest', 'fr_chest_shell'), ('waist', 'fr_abdomen_shell')):
        unlink(frame)
        _armor('torso', 'r', piece, f'ar_{piece}')
    for i, b in enumerate(WAIST_STEPS if ARMOR_FORM == 'solid' else []):
        _armor('torso', 'r', f'waist{i}', f'ar_waist{i}', box=b)
    unlink('fr_belt_shell')
    _armor('body', 'r', 'hip', 'ar_hip')
    for side, nm in (('r', 'right'), ('l', 'left')):
        for frame in (f'fr_arm_shell_{side}', f'fr_shoulder_plate_{side}', f'fr_leg_shell_{side}'): unlink(frame)
        _armor(f'{nm}_arm', side, 'arm_socket' if side == 'l' else 'arm', f'ar_arm_{side}')
        if ARMOR_FORM == 'solid': _armor(f'{nm}_arm', side, 'pauldron', f'ar_pauldron_{side}', addon=True)
        else:   # the decal: 0.5 px off the arm piece's top, outer side, front and back, its inner edge where the solid
            # pauldron's was (1 px off the arm's inner wall: clear of the helmet's corners turned 50 deg)
            g = next(x for x in groups if x['name'] == f'armor_{nm}_arm')
            # checked as its box, like the solid one (texel by texel, the check's pairs ran to minutes)
            e = painted(g, side, 'pauldron_armor', f'ar_pauldron_{side}', *PAULDRON_DECAL)
            e['_armor'] = 'addon'
        _armor(f'{nm}_leg', side, 'leg', f'ar_leg_{side}', raw=True)

# ---------------------------------------------------------------- engine (draft, ENGINE)
if ENGINE_BOX:
    _t = next(x for x in groups if x['name'] == 'torso')
    eng = group('engine', (0, 14, 0), _t)
    fronts = {'ht_': group('engine_open', (0, 14, 0), eng), 'ha_': group('engine_armored', (0, 14, 0), eng)} \
        if ARMOR == 'game' else {}
    for k, box in ENGINE_BOX.items():
        meta = ENGINE_META.get(k)
        if meta:   # a radial part (mirrored: the left one's turns about y and z flip)
            for side in (('r', 'l') if meta['mirror'] else ('r',)):
                s_ = 1 if side == 'r' else -1
                e = painted(fronts.get(k[:3], eng), side, 'en_fb_' + meta['shell'] if meta['shell'] else f'en_{k}',
                            f'en_{k}' + (f'_{side}' if meta['mirror'] else ''), *box)
                if meta['rot']:
                    rx, ry, rz = meta['rot']
                    e['rotation'] = [rx, ry * s_, rz * s_]
                    o = meta['origin']
                    e['origin'] = [o[0] * s_, o[1] + FY, o[2]]
            continue
        sides = ('r', 'l') if k.startswith(('pipe', 'exhaust')) else ('r',)
        for side in sides:
            e = painted(eng, side, f'en_{k}', f'en_{k}' + (f'_{side}' if len(sides) > 1 else ''), *box)
            if k.startswith('exhaust'):   # lean back about the pipe's foot, as on the old suit
                s_ = 1 if side == 'r' else -1
                e['rotation'] = [EXHAUST['lean'], 0, 0]
                e['origin'] = [EXHAUST['x'] * s_, EXHAUST['base'] + FY, EXHAUST['z']]

# ---------------------------------------------------------------- write the project
def outline(g):
    return {'uuid': g['uuid'], 'isOpen': True, 'children': [outline(c) if isinstance(c, dict) else c for c in g['children']]}

def tex(name, data, i):
    return {'name': name, 'path': '', 'folder': '', 'namespace': '', 'id': str(i), 'group': '', 'scope': 0,
             'width': TW, 'height': TH, 'uv_width': TW, 'uv_height': TH, 'particle': False, 'use_as_default': False,
             'layers_enabled': False, 'sync_to_project': '', 'file_format': 'png', 'render_mode': 'default',
             'render_sides': 'double', 'wrap_mode': 'limited', 'pbr_channel': 'color', 'fps': 7, 'force_translucent': False,
             'frame_time': 1, 'frame_order_type': 'loop', 'frame_order': '', 'frame_interpolate': False, 'visible': True,
             'internal': True, 'saved': False, 'uuid': uid(), 'source': b64(data)}

if __name__ == '__main__':
    bad = check() + check_armor()
    if os.environ.get('ALLOW_CLASH'):   # review a known-bad fit (a survey before a refit); never for a saved model
        if bad: print('CLASHES (allowed):', bad)
    else: assert not bad, bad
    for g in groups:
        g.pop('_parent', None)
    for e in elements:
        e.pop('_g', None)
        e.pop('_shell', None)
        e.pop('_hollow', None)
        e.pop('_args', None)
    model = {
        'meta': {'format_version': '5.0', 'model_format': 'bedrock', 'box_uv': False},
        'name': 'power_frame', 'model_identifier': 'power_frame', 'visible_box': [4, 4.5, 1.75],
        'variable_placeholders': '', 'variable_placeholder_buttons': [], 'unhandled_root_fields': {},
        'resolution': {'width': TW, 'height': TH},
        'elements': elements,
        'groups': [dict(g, children=[]) for g in groups],
        'outliner': [outline(root)],
        'textures': [tex('power_frame.png', model_tex(), 0)],
        'animations': [],
    }
    # groups' children lists hold only structure in the outliner, not in `groups`
    with open(OUT, 'w') as f:
        json.dump(model, f, indent=1)
    print(f'{len(elements)} cubes ({sum(e["name"].startswith("fr_") for e in elements)} frame, '
          f'{sum(e["name"].startswith("st_") for e in elements)} Steve), {len(groups)} groups -> {os.path.normpath(OUT)}')

