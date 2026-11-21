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
- **Face columns don't share a direction** (frame_model.py's faces, the helmet art's): north (front) runs +x -> -x,
  south (back) and up (top) -x -> +x, east back -> front, west front -> back; up rows front -> back, down rows back
  -> front. Anything that crosses an edge (a channel, a seam, a stripe) must be matched by world position, not by
  column number: front column i is x = 4.5 - (i + 0.5) / 2 on the helmet, top column i is x = -4.5 + (i + 0.5) / 2.
  2026-11-15: a spartan option lit off the front's column numbers put the channel's dark wall on the other side of
  the top's, so the streak jumped where the faces meet (the user caught it). Check edges in a 3D view, never in the
  flat face grids alone.

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

## Sea engine (2026-11-16)
- The tidal engine has its own body, `frame_sea_art.py` (knob `SEA`, `A` default / `none`; group `engine_sea` with
  `sea_open` / `sea_armored`; the renderer shows it for the tidal engine and `engine` for the others). User: the
  engines' light and particles are good but shouldn't follow the firebox's shape; 3D on the back, 2D (flat) on the
  front and sides. Drafted three (A diver, B prismarine conduit housing, C drum with a window of water), A picked
  ("it looks great"); B and C were not kept. It reuses the heart's harness routing (over the
  shoulders, down the waist, into the back body's sides) with its own paint.
- Light: letters T S y q are reserved dark teals in the texture (`SEA_DARK`, `SEA_GLOW=lit` paints them lit for a
  review); `export-frame.py` writes `power_frame_glow_sea`, `SuitGlowLayer` scales it by the tidal shimmer.
  Bubbles: `ExhaustSmoke` VALVE_* (the tank valves' tops).
- Star reactor (`frame_star_art.py`, knob `STAR` A / none; group `engine_star`): eight draft rounds, the story is in its
  docstring (discs and cages "too far out", "grounded in technology, no wheels", then the Sandevistan: "mechanical,
  not boney", "slick black and purple", the chain A picked). Chest: the lens. The module screens + head + base are
  SEGMENTS, each its own glowmask (`export-frame.py star_masks`), lit in a climbing pulse by `SuitLights.getStarSegments`.
  The texture grew to 320 rows for the three engines. No afterimage trail (user: not wanted); the ender motes stay as they are.
- Star reactor, the restart (2026-11-16, rounds 20-26, `STAR=E` with `STAR_PYLONS=1`, in game): the chain was dropped
  ("start from scratch, do something more similar to the firebox and tidal engines"). Built their way: the lens with
  four glass lines (the tidal engine's harness code, `frame_sea_art`, in violet) into a back body painted in their
  housings' vocabulary. Picked E (a beacon case) over C (the blower-like block) and D (a column), then given D's pylons
  (charge cells), the case narrowed to 5 px to fit them inside the chest's width. User corrections worth keeping:
  "more forward" meant detached (standing 1 px off the back on the links), not deeper; the lines go into the BODY's
  sides, not the pylons; every visible face is painted, bottoms and the pylons' inner sides included (a plain face
  reads "unpainted"); a lone bright texel (a line's spark) reads as a rogue pixel; a 6 x 7 pane round a 6-row star left
  an odd corner. Metal: netherite (own letters `{ } [ ] ( ) < >`, not the iron ramp's, which the paint swaps;
  `STAR_METAL=iron` for comparison): the reactor is the late-game engine (netherite ingots and a Nether Star in its
  recipe). The pulse: `segment_of()` assigns lit texels by part and row (pylon cells bottom-up, the pane, the rim's hole).
- Review the bare and armoured fronts from a `SEA_GLOW=lit` game build (hide `engine`, show `engine_sea`, toggle
  `sea_open` / `sea_armored`); `ARMOR=none` drafts show the open front only.

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
- **A tool's body takes the fist's place** (`DRILL_FIT=fist`, 2026-11-13): originally a 5 x 4 x 5 block flush with
  the arm at raw y 10-14. **Revisited 2026-11-20 (`SOCKET_LIFT=3`, `TOOL_SLEEVE=1`):** at raw 14 the tool arm hung
  past the knees/ankles (21-22.5 px vs 17 px legs). Lifting the socket +3 px to raw 17 (built 19, leaving a 1 px steel
  cuff below the iron pauldron) and widening every tool's base to 6 x 6 (0.5 px proud all round, matching the pauldron
  and bare shoulder plate) brings tool tips up near the empty fist (built y 8.5-12), encloses Steve's hand inside every
  tool body (flamethrower pump 6 x 3 x 6 with 6 px barrel and 4 px tank; TNT octagonal 6 x 1 x 6 collar + 6 x 3 x 6
  drum with `drum_N=5.0`), and reads as a heavy attachment clamped around the forearm instead of replacing it.
  **Scaled heads (`HEAD_SCALE=1`, 2026-11-21):** drill 4.5->3->1.5, chainsaw 5x6 bar / 6 chain, chaingun 1.5 barrels /
  4.5 collar / 5.5 muzzle, flamethrower 4x4 barrel / 4x1.5 tank, rail prongs +-3->+-2.5 x 4 deep, EM 4x4 spinning core
  + flush r=2..3 prongs (2.5 coil / 2.0 shaft+tip). User: right move; revisit individual tool art later to make full use
  of the wider 6x6 area.
- **Standalone tool models (2026-11-21, `tools/export-tools.py`):** each tool now ships as its own `.bbmodel`
  (`model/tools/<tool>.bbmodel`), `.geo.json` (`geckolib/models/tool/<tool>(_r).geo.json`, with `_r` only for handed
  tools `drill`, `chainsaw`, `flamethrower`), compact 64x64 texture (`textures/tool/<tool>.png`), and only its own
  glowmasks (`textures/tool/<tool>_glow_<mask>.png`), centered at the socket `(0, 0, 0)`. `power_frame(_slim).bbmodel`
  defaults to `TOOL=none` and emits empty `left_socket` / `right_socket` locator bones (`ToolLayer` + `CockpitViewRenderer`
  attach standalone tools via `ToolModelRenderer`, fixing dual-wield shared-glowmask bleed and dropping all 22 suit-sized
  tool glowmasks + 4 `view/frame_tool*.geo.json` files). `frame_drafts.py` still accepts `TOOL=<name>|all` for full-suit
  review sheets and clearance checks.
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
  `power_frame_glow_fire` and writes them white -> grey into `power_frame_glow_core` for the star
  reactor (tinting the fire's yellow -> red mask violet came out pink). Smoke from the caps' tops (`ExhaustSmoke`: 29.5 px
  up, 6 back, 3.5 out). The helmet clipping the blower looking up stays (user, 2026-11-14: "the cost of gameplay").
- Step 5a, the tools: `TOOL=all` (the saved files' default) builds every tool at once on the left arm, each on bones
  named as the game's tool (`GAME_BONES`: drill / drill_bit, chainsaw / chainsaw_chain, chaingun / chaingun_barrels,
  flamethrower), shell keys `tl_<tool>_<part>`; the game shows the installed one (a tool without frame art: the
  drill's). The build takes ~25 s with ARMOR=game (see Build time below). The exporter keeps an animation whose
  bones the frame all has (drill_run, chainsaw_run); the others are written empty.
- Step 5b, aiming: raised, the left arm swings forward 90 deg less the view's pitch and turns with the head
  (PowerSuitRenderer.raiseTool); the muzzle is the shoulder (8.25 px left, 28 up) plus 20.5 px along the view
  (SocketAim). The cockpit draws his left arm, the frame's left arm and the tool (`view/frame_tool`: about
  pilot_left_arm's pivot) where vanilla draws a left hand, turned about the shoulder toward the aim. A tool alone at
  the screen's corner (the big suit's way) had to sit 0.1 blocks from the camera at twice its size to hide its cut end.
- Step 5c, the tools' lights: the status lamp is painted in reserved dark colours (`LAMP=dark`, the saved files';
  red / green for reviews) and lit as two masks, red ready / green running; the chaingun's emerald base vents (`GUN_ACCENT=vents`,
  2026-11-20: moved from the muzzle to two horizontal slits in the base's grooves; muzzle sides left solid with no front vents),
  its two-stage uniform overheat glow (`HEAT_SPEC` / `HEAT_GLOW` in `frame_gun_art.py`, exported with per-texel alpha to
  `power_frame_glow_heat` and `power_frame_glow_heat_barrel` so barrel tips + muzzle bottom rim light from 30% and heat creeps
  uniformly back across the solid muzzle, collar and exposed barrels from 55%), and the flamethrower's pilot light (its reserved colours) have
  masks of their own (`TOOL_GLOW` in the exporter).
- Step 6 (decided 2026-11-14, Notion spec sec. 10): the frame is made on its own (golem-style blocks maybe later; the
  recipe stands), armour goes on the spawned frame one piece per part from its menu, pieces carry a tier (iron now,
  copper planned), protection per piece, sealed = all five pieces + helmet + powered. 6a items / slots / protection /
  seal (`entity/SuitArmour`), 6b the menu (vanilla's inventory screen, `.scratch/menu6b`), 6c the pieces on the frame:
  `ARMOR=game` (the saved files' default) builds the bare frame AND the iron pieces, each part's frame cubes moved into
  `frame_<bone>` (`unlink` regroups instead of dropping them), its piece in `armor_<bone>`, and the engine's front both
  ways (`engine_open` = the bare build's ht_ parts, `engine_armored` = ha_, `heart_art.build(armored=True)`). The
  renderer picks per part (`client/ArmourBones`). The checks skip pairs never drawn together (`ALT` / `apart`: a part's
  frame vs its piece, the two engine fronts), so every mix of worn and bare parts is checked. The one clash that found:
  a leg piece's top and outer side lay in the bare belt's planes; the belt and the hip block now go with the LEGS (the
  hip shows with either leg piece on), as the hip was drawn as the leg pieces' part. A full build takes ~25 s (Build time below).
- Step 7, paint (user, 2026-11-14, pick B of in-game mockups `.scratch/paint7/sheet.png`): the iron pieces (ar_*) and
  the helmet (ar_helmet / ar_hx_layer) take the dye by swapping their eight steel shades (the big suit's recipe and
  ramps; `tools/make-frame-paint.py`); the bare frame (fr_*) stays steel: its members' greys + grain mapped onto the
  ramp read as camouflage speckle. So: keep the armour and the helmet's shell in the steel shades only, everything
  that mustn't take paint (slate, brass, copper, gear) off them.
- Step 7b, helmet styles (2026-11-14): one style at a time from a reference picture the user gives (the five first
  drafts together "ain't great": a draft per reference works). Drafts `HELMET_STYLE=<style>` on Alex (`BUILD=slim`,
  user) with `PAINT=<dye>` in `frame_drafts.py` (painted as the game paints: judge a style in its colour too). A
  style's outer art is its `_outer` (helmet texel coords; `layer(style)` builds its layer, none without). The hunter
  (Samus, `.scratch/helm7/hunter_ref.png`): an arched forehead plate under a centre seam, a T visor whose stem's lower
  half is plated in silver, flat ear bulbs high mid-side fed by diagonal hoses from under the cheek guards (raised on
  the layer, the hoses' ends at the front read abrupt; ears raised over flat hoses read as a disparity), the back's
  seam stopping on the plate line (_|_) over the standard neck guard. The user edits texels in the draft tab: diff its
  texture against the draft file (glass texels differ by 1 from Blockbench's canvas rounding) and carry the edit into
  the generator. Picked styles go into the saved files with `HELMET_VARIANTS` (groups `helm_<style>`).
- The protector / diver (Subject Delta, `.scratch/helm7/diver/ref.jpg`, 2026-11-14/15, 24 rounds; reviewed on Steve,
  `BUILD=wide`, user): one wide oval window round his eyes with two bars (traced as an ellipse: hand-drawn it came out
  tall and lopsided), slate fittings (brass read out of place: nothing else on the frame is brass), a flat camera over
  the window running onto the top (a box, even in the outer layer's 0.5 px, is 3D: the user avoids 3D on the frame; on
  the hollow layer itself it floats, no sides), the reference's split in three as tone, not lines (the cheek panels a
  step darker with a dark edge; a seam line hugging the bezel merged into its shaded side and 1-texel diagonals read as
  dots), carried round the sides and back at row 10, cheek lamps in the fire's coal colours (lit with the engine), a
  red handwheel valve on the back (a nod to Valve), bolts two a face 3 texels in, as the top's rivets, the standard neck
  guard. Tried and dropped: cheek portholes and straps, brass, riveted / bolted rings ("rustic"), slate trim rings,
  windows on the sides and top, oxygen hoses ("less is more"). Lesson: the reference's signature (the window, the
  split, the lamps), not its parts list; on 18 texels four bolts can only space evenly at gaps of 3 or 5, and both
  looked off: two a face matched the rest.
- The spartan (Master Chief, `.scratch/helm7/spartan/ref.png`, 2026-11-15, 23 rounds; picked, in game; the helmet icons redrawn from the four styles' front faces): the
  user finished it by painting in Blockbench themselves (rounds 18-23: their texels carried into the generator exactly,
  full 18-texel maps in `SPARTAN_FRONT` / `_SIDE` / `_BACK`). What it is: a brow whose 6-wide tab hangs a row into the
  visor, a lit lower lip, the wide visor wrapping the corners, a 1-texel border, the slate mouthpiece over a chin
  plate, lamps on the cheek corners, the top's channel from the brow over the top to a band round the back, the
  brow's line sweeping down the sides with a shadow row under it. What didn't work: every detail of the reference
  ("way too busy"), a plain shell with a band and prongs ("dogwater"), parts on the outer layer (twice: the user
  avoids 3D on the frame), a thicker border under the brow (read as eyebrows), shadowed visor glass, moving parts to
  thin a border (grow the glass into it instead). Lessons: a fresh start from the reference's big shapes in value,
  drawn texel by texel, beat adding its parts; when the user paints, carry their texels exactly and offer changes as
  knobs beside them. Knobs kept for the record: `SPARTAN_LAYER`, `SPARTAN_BROW`, `SPARTAN_BROW_SHADOW` (glass
  `W`, `GLASS_SHADE`), `SPARTAN_TOP`.
- The robot (Guy-Manuel, `.scratch/helm7/robot/ref.jpg`, 2026-11-15, picked round 8, in game): gold in its own
  fixed shades (`GOLD`, letters '0'-'7', outside the steel ramp: it never takes the paint; made with a gold block).
  The visor is the reference's signature: it runs up the whole front, over the top's front half (its back edge square)
  and down the sides' front half (`ROBOT_OPEN=side`; round 5's `front`: glass on the front and over the top only, gold
  strips down the front corners), its bottom curving up into the corners over a deep chin (`ROBOT_MOUTH=curve`), a
  dark border all round it; an ear plate centred on each side from row 5 to the bottom edge, the glass stepping round
  it (a drawn disc: a traced 6-texel ring read as an X; the LED panel under it; at half height it read too different
  from round 5's); a raised panel on the top and back; no neck guard (it made the sides read square). Lit like the others, its big glass in amber blended into the
  gold, so its visor shows eyes-only faces as reactions to events instead (`ROBOT_FACES`, one colour: the visor's),
  dark when idle. Dropped: detailed icons and Minecraft's own sprites (out of place / too much), a scan bar.
- Re-run the exporter after rebuilding the saved files, then `make-frame-paint.py`.

## Build time (2026-11-15)
- The builds were slow (a saved-files build ~15 min, a draft with a painted helmet layer ~12 min) because of
  `check_armor`, not the texture packing: it tested every face of every armour piece against every other face, and a
  hollow piece (the helmet's outer layer) is checked as thousands of texel slabs, so ~44 million `coplanar()` calls.
  The piece's faces are now bucketed by plane (`_plane_key`: nearest axis + distance in `PLANE_BIN` steps) and each
  other face is tested only against its own and the neighbouring buckets: the same clashes found (checked against
  the old loop with eps loosened to 0.3: 13 clashes both), a saved-files build ~25 s, a layered draft ~8 s, a flat
  helmet draft under 1 s. Profile first (`python3 -m cProfile -s cumtime model/art/frame_model.py`) before guessing.

## Rail cannon (2026-11-15; reworked 2026-11-21 for 6x6 sleeve)
- `frame_rail_art.py`, TOOL=rail (now in TOOL=all): reworked 2026-11-21 for the wider 6x6 sleeved footprint (user
  picked `RAIL=gauss` over `coil` and `quad`; old drafts A/B/C kept as knobs; `RAIL_L` 6, `RAIL_CORE=dark|lit`):
  DOOM 2016 Gauss Cannon two-tone dark-slate + bolted light-steel 6x4x6 receiver with glowing blue capacitor windows on
  front/back (`RAIL_FLOW_0`), recessed horizontal copper induction pockets on the sides, a central glowing breech nozzle
  in the gap root, and 3-step sculpted twin rails (copper breech clamps -> vented mid rails with dark cockpit/back vents
  & glowing side windows `RAIL_FLOW_1` -> tapered dark-slate muzzle tips with `RAIL_FLOW_2` notches) framing a 1.5 px
  open see-through glowing channel. Outer fork on `rail_fork_out`, inner on `rail_fork_in` so `ToolRotors.railShake`
  spreads them around the breech as it charges.
- The core is the prongs' inner faces, painted in three bands of reserved dark blues (K / L per band, a shade apart:
  `frame_rail_art.CORE`), each its own glowmask (`TOOL_GLOW` rail_flow_0..2 -> `ToolLight.RAIL_FLOW_0..2`: the wave that
  runs toward the tips). The big suit's emitter light (`RAIL_EMIT`) has no frame texels yet. `muzzleInsetPixels` -1 (tips 10 px
  under the socket, 1 px past the chaingun's muzzle). `runAutopilotRail` shows it.

## TNT launcher and EM projector (2026-11-15; both reworked 2026-11-20)
- `frame_tnt_art.py` (TOOL=tnt, knob `TNT=wide` default | `flush` | `chunky` | `legacy`; reworked 2026-11-20 to match
  the big suit's round 5 launcher: a 5 x 1 x 5 dark-slate socket collar, a 6 x 3 x 6 fluted dark-slate octagonal drum
  built from three flush non-overlapping cubes on bone `tnt_launcher_drum` with four red TNT chamber ends recessed
  inside a 1-texel dark-slate rim on its down face (`ch_in=1.0, ch_out=2.5, ch_span=1.0`, keeping the top chamber
  hidden behind the barrel so no red peeks over it, 90 deg symmetric for `ToolRotors`), a 3.5 x 4 x 3.5 light-steel
  barrel, a 4 x 1 x 4 dark-slate muzzle ring flush with the drum front, and two 0.5 px fork-sight prongs with a 1 px
  gap; 9 px under the socket, `muzzleInsetPixels` 0).
- `frame_em_art.py` (TOOL=em, knob `EM=claw_b2` default | `claw_b1` | `claw` | `splay` | `corner` | `step` | `legacy`,
  `EM_GLOW=dark` | `lit`; reworked 2026-11-20: compact 5 x 3 x 5 vented steel/dark-iron housing over a 3 x 1 x 3
  dark-bezel redstone core and four cardinal flush copper-wound prongs with aligned glowing redstone tips at
  r=1.5..2.5; 7 px under the socket, `muzzleInsetPixels` 2; the core and four prongs share bone `em_projector_poles`
  and spin smoothly via `ToolRotors` / `EmProjectorEffects` while searching and holding, hub corner r 2.12 < 2.5
  housing). Both are in TOOL=all: every tool now has frame art.
- The lens / vents and the tips are reserved dark reds (`frame_em_art.RES`), lit by `TOOL_GLOW` em_core / em_arc
  (`ToolLight.EM_CORE` / `EM_ARC`). Seen in `runAutopilotFrame` (`ap_frame_tool_<tool>`) and `runAutopilotTnt`
  (`ap_tnt_drum_*`, `ap_tnt_husks_fp_*`).

## Two sockets, hands detachable (2026-11-15, user)
- Either arm ends in its hand or, with a power tool fitted, the socket the tool hangs from; both arms can carry one.
  Saved files (ARMOR=game) hold four looks per arm: `frame_<arm>` / `armor_<arm>` (the hand) and `frame_<arm>_socket` /
  `armor_<arm>_socket` (cubes `fr_arm_socket_shell_*`, `ar_arm_socket_*`, plus their own shoulder plate / pauldron: same
  texture strips), shown by `ArmourBones.show(bones, worn, toolMask)`. Every tool is built on both arms: the left arm's bones keep
  the game's names, the right's carry an `_r` (`drill_r`, `drill_bit_r`, `rail_fork_out_r`...; cubes `tl_<tool>_<part>_r`
  share the texture strips, built with side 'r'). `export-frame.py` copies the run animations as `<name>_r` (bones renamed).
- Clearance checks: `alt()` marks tool cubes 'tool', which are apart from the hand looks only (frame_model `apart`).
- Code: `suit.socket()` / `getSocketStack()` / `socketVisuals()` mean the arm being ticked or drawn (`onArm`), else the
  primary one: the left if it has a tool, else the right. Tools, goals and tests written for one socket are unchanged.
- Right arm = the main hand (its tool the attack button), left arm = the off hand (its tool the use button).
- Known limits: a tool on the right arm swallows the main hand's turn, so with the left a plain hand its off-hand item can't be
  used with right click; both arms' HUD readouts share their corners (two chaingun-style corners would overlap); the machine
  mind uses the primary tool only; the cockpit's right tool has its own exported view model (`frame_tool_r`,
  `frame_tool_r_slim`) so it uses the same det=+1 transform as the left arm without flipping triangle winding.
