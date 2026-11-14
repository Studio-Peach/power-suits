# Power Suits: the frame and its engine (script-built, branch `experimental/frame-concept`)

The frame is the experimental successor to the big suit: an exosuit the player's own Steve / Alex stands in, built
entirely by script (SKILL.md §0). What it taught us, so the next round starts where this one stopped. The files below
live on `experimental/frame-concept`. In game since 2026-11-14 (step 1 of 8: the frame and its pilot; see "In game" at
the end and `docs/guide.md` Notes).

## Files
- `model/art/frame_model.py` builds `model/power_frame.bbmodel` (Steve, `BUILD=wide`) and `power_frame_slim.bbmodel`
  (Alex, `BUILD=slim`); `FRAME_OUT=` writes one elsewhere. Its header and comments carry every decision with the date
  and the user's words. `frame_drafts.py` builds a draft round into one file (`/tmp/frame/draft.bbmodel`).
- Engine (`ENGINE=heart`, off by default so the saved files don't show it yet): `frame_heart_art.py` (the front: core
  and hoses as decals), `frame_motor_art.py` (the back: `BACK=blower`, picked; `vtwin`, `inline` drafts),
  `frame_engine_art.py` (porthole core art, the twin-cylinder pack `BACK=pistons` drawn at any size),
  `frame_radial_art.py` (the radial firebox, superseded; its `part()` / `grid()` / `disc()` helpers are shared).
  `FIRE=lit|dark` paints the fire burning (review) or in the reserved coal colours (the in-game texture).
- Checks: `check()` / `check_armor()` run on every build; `model/art/engine_sweep.py` sweeps the head, arm and leg
  against the `en_*` cubes (build with `HELMET=glass` so it has a helmet to swing).

## Coordinates
- The art scripts use **raw** coordinates; the model is lifted `FY = 2` (the 4 px soles). A sweep or a Blockbench
  readout shows built coordinates (raw + 2): the caps' tops are raw y 27.5, Blockbench 29.5.
- 1 px = 1/16 block, the model faces -z, right side +x, 2 texels per px.

## Envelopes (what any part on the torso must clear)
- **The helmet** (9 x 9 x 9, raw y 25.5 up, x / z +-4.5; head pivot raw 26, yaw +-50, pitch +-90): above raw 25.5
  nothing may sit in front of z 4.5 (it clips the helmet at rest); turned 50 deg its back corners sweep a circle of
  radius 6.36, so anything above 25.5 behind the head nearer than that is met when the head turns. The picked back
  parts stand there (supercharger, exhaust caps): the worn helmet's tilt / turn limit is an open decision for the
  renderer. A face in one of the helmet's planes (front z -4.5, back 4.5, sides x 4.5) facing the same way fails
  `check_armor` (a hose and its collar did, in the front plane); back to back is allowed.
- **The arms** start at the chest's sides (`CHEST_X`: 6 wide, 5.5 slim) and swing about x: nothing beyond the chest's
  width (decals included: the slim build's hoses ran into Alex's arms until the layout followed `CHEST_X`).
- **The legs** swing +-60 about the hip (raw y 14): parts low on the back meet them (the full-size pack at -60).
- **The gap under the arm** is 1 px (wide) or 0.5 px (slim) beside the abdomen (x 5): a strip there is a decal, a
  zero-thickness plane in the middle of the slim gap (both sides are planes the arm cage and abdomen use).

## Engine decisions (2026-11-11)
- The front is 2D: a porthole core painted into the chest slot, four copper hoses drawn flat (lit / mid / shade across
  them, a 1-texel ink outline, brass bands), carried over the shoulders, along the waist and down the back by decal
  strips into inlets painted as the hose (ink, three coppers, ink). The rotated 3D ball-and-hose draft is f688cc9.
- The back is a hot-rod blower: a 10 x 8 x 2.5 block flat on the back, the fire window in it (the part that lights:
  keep it uncovered), a ribbed supercharger over its whole top (its top at the helmet's bottom), the big suit's
  exhaust art and caps at the frame's density standing out of the block's back (smoke from the cap holes).
- Light: the core's fire and the fire window are painted in the reserved coal colours of `tools/make-glowmasks.py`
  (`FIRE=dark`), so the fire glowmask lights them by the burn state as on the suit; the smoke code (`ExhaustSmoke`)
  needs the frame's cap positions when the frame goes in game.

## Shoulders (2026-11-12)
- The shoulder plate is a decal too (`SHOULDER=decal`, picked over the 3D 6 x 1 x 6 plate and a bare lid): drawn on
  0.5 px off the arm's top, outer side, front and back, a steel band with an ink edge, 5 rows deep at the outer corner
  running out to 3 at the chest. Next to the 2D engine the 3D plate read as a ledge.

## Limbs (2026-11-12)
- The frame is the inner piece the pilot wears; armour goes on over it, so the limbs stay a cage: the brass bellows
  bands are gone (`BANDS=cage`; steel / gunmetal ribs read as armour). Leather in the torso's two shades wraps the outer
  corners (`LEATHER=wrap`): the front and back windows beside the outer side and both outer-side windows (its rod
  removed), his body showing between. One flat shade, or leather over every window, read flat and hid him.

## Iron armour (2026-11-12)
- Sealed stays: "sealed" is a game mechanic (a full set with the helmet makes the pilot immune to most outside
  debuffs), so the armour covers the whole frame; the frame shows only where a piece is missing.
- Flat, like the engine (`ARMOR_FORM=flat`): the pieces are the frame's boxes (the waist as deep as the chest, the
  step band painted on its top 2 px), the pauldron a decal 0.5 px off the arm piece (from its old inner edge, x 7 /
  6.5 slim, clear of the helmet's corners turned 50 deg; checked as one box: texel by texel the check ran minutes).
- The engine under it, tiered: the upper hoses hidden by the breastplate, the lower pair out from under its painted
  bottom edge over the waist; the core replaced by a radiator grille decal (`GUARD=hot`: three slats in the fire's
  reserved coal colours, hottest in the middle, dark slots) in a dark slate surround (in steel it vanished), so it
  glows with the burn state.
- `ALLOW_CLASH=1` builds a model that fails the checks, for a survey before a refit (never for a saved file).
- The helmet (`HELMET_STYLE=C`, `model/art/frame_helmet_art.py`): the 9 x 9 x 9 box painted at 2 texels per px (the
  big suit's helmet sampled at 1 read flat): a wraparound glass visor under a brow ridge, the old helmet's chin grille,
  a crest over the top, a slate neck guard (2 plates, the bottom 3 px) wrapping round onto the sides; no ear discs.
  In third person the blower hides the back's bottom: detail there is only seen from the side.
  Its outer layer (`HELMET_EXTRA=layer`, 2026-11-13): one see-through box 0.5 px out all round, like a player's hat
  layer, painted only on its sides: a 2D radio on the left with two antenna lines (the taller's tip on the layer's top
  edge: nothing past the layer) and a camera on the right. Its four blank faces share one see-through texel
  (`compact`, so they take no texture room). It replaced `gear`, the same art as 3D boxes (a closed radio body, a
  camera with its lens facing forward and a rounded tail; 4 cubes, kept as a knob option): the user preferred the
  flat layer's look, in line with the flat armour and engine. A layered brow cap was dropped: its
  swept side is painted into the helmet instead, the winged ridge over the glass, the side seam run into it in the
  same two rows and shaded like it (`HELMET_SEAM=ridge`, its dark row a step lighter). Bolts only on the sides, as
  the top's rivets (none on the front or back). The seam rings the whole head (`HELMET_FLOW=ring`, 2026-11-13: carried
  across the back, so the top and back stopped reading as separate from the front and sides); no crest (with the ring
  it was too much; a crest down the forehead more so), the top plain with 4 rivets in a square 3 texels in from its
  edges, in the side bolts' rows. `crest` (an unbroken crest over the top and down the back, no ring) stays a knob.
  The brow (the ridge over the glass and its wings) is on the outer layer, 0.5 px proud like a cap's peak
  (`HELMET_BROW=outer`, 2026-11-13; `band`, the whole ring out there, read as a hat brim from behind); under it the glass
  is closed by a dark border as along its bottom (a dark row, a shadow row on the front, the side's corner left out:
  rounded), not run on up under the peak. The peak is over the visor only, its lit row swept 1 px back (the wing),
  and the seam a row lower than the peak (`HELMET_PEAK=visor`): its lit row level with the border's top, filling its
  corner, its dark row running into the border's side, so peak and seam read apart. The peak is slate (a lit row over a
  shadow row, `HELMET_PEAK_STYLE=up`), its wings a texel shorter, a third row over its middle 6 px on the front (a
  raised middle, for shape from the front; `down`, dipping over the glass, kept as a knob).

## Tools (2026-11-13, the drill first)
- The left hand is a socket (the big suit's playbook): the left arm's box ends where his hand does (raw 14), its
  underside the socket plate. A tool (`TOOL=drill`, `model/art/frame_drill_art.py`) hangs on a `tool` bone there, the
  spinning part on `tool_bit` under it.
- **A tool's body takes the fist's place** (`DRILL_FIT=fist`): a 5 x 4 x 5 block flush with the arm (raw y 10-14),
  so both arms match in width and length from behind, and the tool grows only from its bottom (the drill's bit). A body
  0.5 px round the arm's end like the shoulder plate (`sleeve`, kept as a knob) made the tool arm look a different size.
  The same slot fits every later tool.
- Simple blocks, elements painted (as the engine, shoulders, helmet): a 3D housing and an L-shaped guard cuff with a
  lamp (4dad9e4) didn't feel right; the user replaced them with one block. The drill's paint: a slate base band (lit
  top row, two bolts a face, a 2 x 1 status lamp at the front's outer end: highlight + lit, LAMP red idle / green
  spinning), a dark seam, a steel motor with a copper winding window (`DRILL_ART=B`, picked over vents and fins).
- A face whose art is all see-through isn't drawn (texture None) and `quads()` skips it, so the clearance check
  doesn't count it as a shared plane.
- The chainsaw (`TOOL=saw`, `model/art/frame_saw_art.py`): the body in the fist's place, a 6 px bar straight down in
  the arm's y-z plane and the chain its own box round it (`tool_bit`, so it runs). Bodies in the frame's grey palette
  (slate / copper / brass cowls, cooling fins, heat shields, sprockets) never read as a chainsaw. What did
  (`SAW_LOOK=rancher`, 2026-11-14, from a Husqvarna 455 Rancher photo, "zero notes"): the real saw's parts mapped onto
  the block with the bar down (its front at the bottom, its handles facing back, the clutch side outward), in its
  **orange** with grey handles: the wrap-around handle a band round the body, the rear handle and the hand guard on
  the back, the muffler and two bar nuts on the outer side, vent slits inside, spikes along the front's bottom. The
  colour does most of the work: it is the only body that stands out from the grey armour in third person. Lesson: for
  a tool people must recognise, start from a photo of the real thing (rotated to the tool's pose and downsampled to
  the face's texels, `.scratch/saw/ph_*.png`), and use its signature colour even outside the palette.
- The chaingun (`TOOL=gun`, `model/art/frame_gun_art.py`, picked 2026-11-14 after seven rounds): from the Doom 2016
  chaingun (`.scratch/gun/ref_doom.png`), but only its parts that read at 5 x 4 x 5: four square barrels, a stepped
  muzzle block with a **green light in each side's middle** (the signature colour, on the spinning bone), and a warm
  black body that is one ribbed drum (band / groove three times) under a 2-row top (lit edge, bolts). What didn't
  read and went: the reference's rust ammo box and bent copper pipe (the user couldn't tell what "the brass part" was),
  an embossed 'XX' plate (a checkerboard), a clamp ring halfway, a two-tone housing over the drum (steel / grey /
  chamfered tops all looked off). A red seven-segment ammo counter (Halo) was drafted and dropped: 3 x 5 texels is the
  smallest legible digit at 2 texels a px, so two digits fill a whole face (smaller needs finer pixels or a light bar).
  Lessons: a reference gives the tool's signature, not a parts list; when the user says "the top half", ask or draft
  both halves (round 4 replaced the drum by mistake).
- The flamethrower (`TOOL=flame`, `model/art/frame_flame_art.py`, picked 2026-11-14 after eight rounds): from the big
  suit's (perforated barrel, red tank with a hazard band, blue pilot light). Its parts hang side by side under the
  body: the perforated 3 x 3 barrel at the front, the red tank behind it with daylight between. Under them is the
  matchstick: a slate rod down from the tank, then a foot forward under the barrel, its blue head at the bore (the
  user's word; "meet the fire hole"). The body is a **solid pump**: a strap, and the copper fuel line painted round
  it from the tank through a red valve wheel into the barrel, centred on its faces. What didn't work: the tank as
  the body; a plain steel body (B: "wasted space"); any see-through fire in the body (glowing slots, holes, a porthole,
  a grille: "see-through doesn't make sense for a flamethrower"); the tank strapped on the arm.
- **A tool's body height is its own** (2026-11-14, user: "not all tools benefit from the same tall base"): the
  flamethrower's is 2 px (`FLAME_BODY_H`), and the freed px went to the barrel, the muzzle kept 9 px under the socket
  (`MUZZLE_DROP`). Its body, barrel and tank are painted for any size (`pump_faces`, `barrel_rows`, `tank_rows`): the
  holes keep the 5 px barrel's rhythm (a hole, two plain rows), and three a row apart looked smushed. The others
  stay 4 px (reviewed 2026-11-14): the drill's band + motor and the chainsaw's Husqvarna body each need it, and the
  chaingun's drum at 3 px (`GUN_BODY_H=3`, the pair twice; `GUN_BARREL_L` kept as a knob) lost the stacked weight the
  user asked for: kept at 4. The drill and chainsaw still hard-code it.
- **A down face's rows run back -> front** in the frame's art (up faces front -> back; checked from straight below):
  the matchstick's head, written front -> back on its bottom, came out at the back, off from its sides.

## In game (2026-11-14, step 1: the frame and its pilot)
- The frame took over the `power_suit` entity's looks (user: replace, not a second entity; the pilot drawn by the frame;
  code poses, not baked animations; tools without frame art reuse something easy until they get their round).
- `tools/export-frame.py` exports the saved files (no Blockbench): the st_* cubes stay out, the game draws the pilot with
  vanilla's player parts in his skin (`client/PilotLayer`) at the pilot_* bones, which the exporter moves to vanilla's
  part pivots (head: bottom centre; body, legs: top centre; arms 2 px under the top, 1 px in from the inner side). It
  adds `right_hand` (the held item's grip, in the right fist). Only the skin's base layer: its outer layer (0.25 px
  out) lies in the cage walls' planes.
- Wide or slim follows the pilot's skin (`PlayerSkin.model()`); an empty frame (or a mob inside) is the wide build.
- Step 2, the cockpit (drafts shot in game, user picked): looking down shows nothing of the body (the legs alone
  floated as two squares a block under the view; the chest's top, 4 px under the eyes, filled it like a table top);
  the empty right hand is his skin arm where vanilla draws it with the frame's arm shell round it (the exporter's
  `view/frame_arm`: the right arm's cubes about the pilot's arm pivot); third person 5 blocks back.
- Step 3, the helmet: the saved files carry it now (`HELMET` defaults to `glass`; the game hides `armor_head` without
  one). Rebuilding them also brought the left hand's socket in (the files were last saved before it, at e521b9b).
  The cutout pass draws a texel opaque or not at all, so the exporter splits the glass (alpha strictly between 0 and
  255) into `power_frame_glass` (a translucent pass, `HelmetGlassLayer`, after his face) and its glowmask
  `power_frame_glow_visor` (the visor's colour faded in by opacity, `SuitGlowLayer.VISOR_GLOW` 0.45: his eyes still
  show through, faintly). His hat layer hides under the helmet (it lies in the helmet's planes).
- Step 4, the engine: the saved files carry it (`ENGINE=heart`, `FIRE=dark`: the texture holds the dead coals); the
  game shows the `engine` group with any engine installed. The exporter lights the coal colours into
  `power_frame_glow_fire` and writes them white -> grey into `power_frame_glow_core` for the tidal engine and the star
  reactor (tinting the fire's yellow -> red mask violet came out pink). Smoke from the caps' tops (`ExhaustSmoke`: 29.5 px
  up, 6 back, 3.5 out). The helmet clipping the blower looking up stays (user, 2026-11-14: "the cost of gameplay").
- Not yet in game (later steps): the tools and the iron armour. Re-run the exporter after rebuilding the saved files.
