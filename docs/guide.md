# Power Suits

A Minecraft mod (Minecraft 26.3, NeoForge 26.3.0.76 + GeckoLib 5.5.7) that adds a power suit you climb into,
Fallout / Titanfall style. Mod id `power_suits`. Model and animations come from `model/power_suit.bbmodel`.

Working notes for agents: `AGENTS.md` (the design spec and roadmap are kept outside the repo).

## Playing it

| Action | How |
|---|---|
| Get the suit | Creative tab *Tools & Utilities*, or craft it from its parts (see *Crafting the suit* below) |
| Deploy | Right-click the ground with the item (needs a 3-block-tall space) |
| Climb in | Right-click the suit |
| Suit menu | Your inventory with the suit in it, **vanilla's inventory screen** with the suit's things in vanilla's places: **press your inventory key (E) inside the suit**, or sneak + right-click a parked suit. Round the suit's preview, like a body (it faces you, so its right side is on your left): helmet, right arm, right leg and the engine (the backpack) down the armour column, torso, left arm and left leg above the off-hand slot, which holds the **power tool socket**. In the crafting corner, under the suit's name: the fuel slot, the arrow and the **Power** key where the result would be (⏻: pushed in and green while on, out and grey while off); the small **Pack** key where the recipe book's button sits (greyed out from inside). Beside the menu, drawn like potion effects: **Hull** (%), **Fuel** (time at walking pace, or why it's dark: *No engine*, *Flooded*, *No fuel*, in red), **Sealed** (only while it is), then your own effects. Over any item, the swap-hands key (F) swaps it with the socket tool |
| Night vision | The powered visor lifts the dark when it's dark around you (a cave, any night outside), tinted in your visor colour like night-vision goggles; it fades in over a second and goes with the visor's power. **N** switches it on and off while you pilot a suit with a helmet or AR Glasses (rebind it in Options > Controls > Key Binds > Power Suits > *Night vision*); **NV** under the compass, right of the clock, while it's on. Only on your screen: nothing in the world is lit |
| Power switch | The suit's power switch, in its menu or on the **H** key while piloting (rebind it in Options > Controls > Key Binds > Power Suits > *Power switch*). Off, the suit acts exactly like one with nothing to burn (it slumps, the mind stops, the visor goes completely dark; the menu's Power key pops out) but keeps its fuel; it stays off when packed up. On again, it stands back up |
| Helmet | Right-click a suit with a Power Suit Helmet (or use the menu's helmet slot) to put it on. With the five armour pieces on it seals the suit (see *Armour*), and a helmet carries no mind of its own (only a souled Robot Helmet does: see *Companion*): without one the suit still runs with you inside (unsealed: fire, poison and water reach you, and you can eat), and an empty one stands powered down. Switching it off (below) or taking the helmet off parks a suit. Rogues always wear one. It wears like the armour pieces (durability 165, an iron helmet's) but never breaks off: worn out it stays on as "Power Suit Helmet (broken)" (styles too: "Spartan Helmet (broken)"), with no armour points and no seal, while the machine mind still runs (a parked suit doesn't die of scratches); an anvil with iron ingots repairs it (a style from the smithing table keeps its wear) |
| AR Glasses | Early-game head item: fits the suit's helmet slot (menu or right-click) and projects the floating HUD readouts and night vision (**N**) without the heavy steel helmet corners. Adds no armour, never seals the suit, runs no machine mind, never blocks eating or drinking, and takes no wear. A tiny indicator LED on the left temple arm lights up while the suit is powered |
| Armour | The bare frame has no armour of its own (you see its cage and the pilot in it): it takes one piece per part, drawn over that part in place of its frame, torso, each arm, each leg (an arm or leg piece fits either side), in the suit's armour slots. Tiers mix freely on one suit: **Copper** (early game, lighter silhouette without pauldrons or knee pads, never takes dye paint: torso +4, arm +1.5, leg +2 = 11; durability 176/121/165, repaired with copper ingots; **does not seal** the suit) and **Iron** (torso +6, arm +2, leg +3, plus helmet +2 = 18; durability 240/165/225, repaired with iron ingots; config `armour`). **All five iron pieces and the helmet** seal a running suit (*Sealed suit*). Put pieces on in the suit menu (shift-click sends a piece to its free slot). A bare part never exposes you: every hit lands on the hull, which takes less the more pieces are on. **Pieces wear** like vanilla armour (every worn piece loses max(1, damage / 4) durability per hit, times config `armour.wear`; hits that ignore armour, like `/kill` or the void, don't wear them): the menu's durability bars show it, an anvil with that tier's ingots repairs them, and a worn-out piece breaks and is gone (vanilla's break sound, bits of it flying), leaving that part bare and the suit unsealed (the helmet wears too, but stays on broken: *Helmet*) |
| Fuel | Put anything a furnace burns in the fuel slot; it lasts as many ticks as in a furnace (coal 1:20 of walking, blaze rod 2:00, lava bucket 16:40 and the bucket stays, planks 0:15) (for the standard Firebox engine; see *Engines* below) |
| Engines | The backpack is the suit's engine, swapped in the menu's engine slot. **Firebox** (a new suit has no engine: craft one): burns fuel, floods and dies when water covers it (no pack-up while flooded: drain the water or swap the engine). **Tidal Engine** (crafted with a Heart of the Sea; twin diving tanks that bubble under water): free while wet (its backpack under water, or in rain); on land it drinks water buckets (0:15) or bottles (0:05) from the fuel slot, so carry some to climb out of the water. **Star Reactor** (the late game's engine: netherite, diamonds and a Nether Star; a netherite beacon case between two glowing pylons, drawing in ender particles): a Nether Star in the fuel slot runs everything, tools included, forever (bullets still take fire charges). Each engine is its own backpack on the suit |
| Walk / run | WASD (3.0 blocks/s walk; S backs up at half speed) / sprint (6.25 blocks/s; double-tap W or tap Ctrl once, it keeps going while W is held) |
| Jump | Hold Space to charge (the suit crouches), release |
| Climb out | Shift |
| Pack it up | **Pack** key in the suit menu, from outside (keeps damage, name, fuel, tool, helmet, engine, armour and the power switch) |
| Install a tool | **The hands are detachable** (2026-11-15): each arm ends in a hand or, with a power tool (Chaingun, EM Projector, Mining Drill, Chainsaw, Flamethrower, TNT Launcher, Rail Cannon) fitted, in that tool, and **both arms can carry one at once**. The menu has a socket for each: the left arm's right of the suit preview (the suit faces you), the right arm's at the foot of the left column, the engine beside the left one. **The right arm is the main hand, so its tool is the attack button (left click)**; **the left arm is the off hand, its tool the use button (right click)**, as before. An arm without a tool is a plain hand: its items work as in vanilla. **While piloting, F moves tools between your hand and the sockets**: a tool in your hand goes to the first free socket (left, then right; both full: swaps with the left's), an empty hand takes the left's tool out first (a non-tool item with no tool fitted: vanilla's swap of the hands). In the menu, F over a tool does the same, F over a socket swaps the arms' tools. The first tool (left, then right) decides what the suit does on its own |
| Your hand | Works as normal while piloting: the suit's right hand holds your selected item; left click punches, fights and mines, right click places, opens doors, throws potions... 1.5 blocks extra reach. No eating or drinking (you're sealed in): food in your hand counts as nothing to do, so right click goes to the tool |
| Use the tool | Right-click when your hand has nothing to do (empty hand, a sword, aiming at the air with blocks...), like a shield in the off hand; hold it as long as you need. The tool arm raises while in use |
| EM Projector | Hold right-click on a dropped item or mob: it's pulled in and held floating (items go into your inventory); release to throw it (into a wall, or bowling through other mobs: 10 hearts each at full speed), tap to shove. The visor marks what it can pull. 1 fuel/tick while holding, 80 per throw |
| Mining Drill | Hold right-click on a block: digs it and the 8 around it (a 3x3 face of a wall, floor or ceiling) like a diamond pickaxe + shovel. 20 fuel per block. **Melee:** aimed at a mob within 4 blocks, it grinds it instead: 1.5 damage every 3 ticks (~10 a second, no hit immunity), no knockback, Slowness I, and every hit tears 4 durability off each armour piece the mob wears (or each piece of a suit), on top of the normal wear; 3 fuel a tick |
| Chainsaw | Hold right-click on wood or leaves to cut it; cutting a tree's trunk fells everything above the cut. 15 fuel per log. **Melee:** aimed at a mob within 4 blocks, it shreds it: 2.5 damage every 2 ticks (~25 a second, no hit immunity), no knockback, Slowness II; 4 fuel a tick (config `chainsaw`, `drill`) |
| Flamethrower | Hold right-click: a stream of fire about 7 blocks toward your crosshair. Sets mobs and blocks alight, melts ice and snow, lights campfires and candles, sets off TNT, cooks food lying on the ground. Dead under water. 6 fuel per tick |
| TNT Launcher | Right-click: lobs a block of primed TNT toward your crosshair that blows up the moment it hits something (real TNT: it breaks blocks). A 4-round drum: hold to fire it empty, a round every half second; it then loads its chambers back one a second with TNT from **your inventory** (the HUD shows the drum and counts what you carry); free in creative. No fuel |
| Rail Cannon | Hold right-click to charge (1.5 s, the core between its prongs glows brighter, the HUD shows a charge bar), let go at full charge: an instant beam along your crosshair, 20 hearts to every mob on the line (it goes through them all), breaking glass, panes, leaves and ice on the way; it stops at anything solid. Let go early and nothing fires. Each shot is an amethyst shard from your inventory; charging (and holding the charge) burns 3 fuel a tick |
| Fire | Right-click while piloting (Chaingun): tap for heavy single shots, hold to spin up to a 10-a-second barrage toward your crosshair; one fire charge per bullet from your inventory |
| Repair | Anvil + iron ingots (the item's durability bar is the suit's health) |
| Sealed suit | While powered and wearing its helmet and all five armour pieces: fire, frost, magma, cactus/berry bushes and harmful effects (poison, wither, slowness...) don't reach you or the hull; keeping them out costs fuel. You breathe under water (0.5 fuel/tick extra). A running suit never catches fire (lava excepted: it burns while in it, the flames die as it steps out). Lava still eats the hull (wade through at a third of your speed). No power, no seal: an empty or knocked-out suit burns like anything else. What's already inside you stays yours: poison or wither you had when you climbed in (food poisoning) hurts you, not the suit |
| Strength | Every melee hit from inside (bare hand, sword, axe...) does +4 damage |
| Stomp | Landing from 3.5+ blocks hurts everything around you (not you): 2 damage per block fallen, up to 30, half at the edge of the shock wave (2-3.5 blocks); things get thrown. A normal jump doesn't stomp |
| Smashing through | Walking breaks leaves, glass panes, cobwebs, snow layers, berry bushes, bamboo...; sprinting also breaks glass and ice. Nothing drops. Block tags `power_suits:suit_smashes_walking` / `_sprinting`; can be switched off in the config |
| Companion (machine mind) | A powered suit with nobody inside is driven by its own mind (green visor) **only while a Robot Helmet with a soul sits on it** (see *Helmet styles*): any other helmet, or a Robot Helmet with no soul, leaves the suit standing there; if the soul helmet breaks the companion shuts down until it is mended with gold. The mind works for its owner (whoever last piloted it, or deployed it) from its home (the block where the pilot got out, or where it was deployed). The socket tool picks one of two routes. **Follow route** (chaingun, chainsaw, flamethrower, no tool): it follows its owner like a tamed wolf (walks over 7 blocks away, sprints past 16, stops at 4, no teleporting) and defends them against whatever attacks the owner or the suit, whatever the owner attacks and monsters within 16 blocks of the owner: the **chaingun** shoots (never with the owner, a villager, a pet or another suit in the line of fire), the **chainsaw** runs at the target and shreds it (the melee: slow, no knockback), the **flamethrower** and an empty socket only punch. **Guard route** (EM projector, rail cannon, drill, TNT launcher): it keeps to home, looks at people nearby, walks back if pushed away, and deals with monsters near home: the **EM projector** catches monsters within 12 blocks (config), lifts them overhead and flings them ~30 blocks up (44 blocks/s, config) so the fall kills them (creepers up and away from home; never animals, villagers, players or pets); the **rail cannon** charges and shoots monsters it can see within 40 blocks of home (config), and whatever attacks it or its owner, never with a friend anywhere on the beam; the **drill** charges monsters within 12 blocks of home (config `melee_guard_radius`) and grinds them (slow, no knockback, wrecks their armour); the **TNT launcher** only punches. A mind never mines, fells, burns or blows anything up: the flamethrower and TNT launcher are carried, never fired, and the drill and chainsaw only ever grind their target. The mind's tools never run out of ammo. It burns fuel like a piloted suit (idle 0.25/tick; its tools too): **to park a suit, switch it off**. Design sec. 8 |
| Soul chat | The soul of the Robot Helmet comments on what happens, in the chat, as `<Veteran> Contact.`, to the suit's owner (if within 48 blocks) and to whoever is piloting it. It only speaks while the suit is a companion or piloted with the soul helmet unbroken (the helmet breaking is its last words), and never about gameplay: nothing it says changes anything. Five souls: **Veteran** (gruff, terse), **Optimist** (cheerful, delighted by everything), **Butler** (dry, formal, politely sarcastic), **Nervous** (anxious, brave anyway), **Poet** (wistful, philosophical about blocks and the night; speaks only in haikus, 5-7-5 with the lines divided by slashes). Events (each with two lines per soul, a chance to fire and a cooldown of its own): first words when the soul is given, waking up, the helmet breaking and being mended, low fuel, spotting a monster (a creeper has its own), a kill, being hit, its owner low on health or dying, nightfall, dawn, a storm, a little idle chatter while it walks beside you, you climbing in or out. At most one remark every 30 seconds (the helmet breaking and the owner dying always get through). Config (`mind`): `soul_chat` (on/off), `soul_chat_frequency` (a multiplier on each chance, 0 = silent) and `soul_chat_cooldown_seconds`; each player can also mute it for themselves in the client config (`mute_soul_chat`). The lines are in the language file (`soul.power_suits.<soul>.<event>.<n>`) |
| Helmet styles | Easter eggs: four smithing templates hide in structure chests (ocean ruins and shipwrecks, trial chamber vaults, end cities, desert pyramids and jungle temples). At a smithing table, template + Power Suit Helmet + the object the template names gives that helmet its new look (name, icon and model change; it works the same). Helmet + iron block with no template gives the standard helmet back; 7 diamonds round a template and its object copy it. Rogues sometimes wear one. Design sec. 4c. On the frame the hunter (Samus, 2026-11-14), the protector (Subject Delta, 2026-11-15: its cheek lamps light up with the engine), the spartan (Master Chief, 2026-11-15) have their own helmets; the noble shows the standard helmet until theirs are drawn. The **Robot Helmet** (Guy-Manuel, 2026-11-15) is not a style but an item of its own, no template: it is found **broken** in piglin strongholds (bastion remnants: about one treasure chest in three, one in twenty of the others) and mended with **gold ingots** at an anvil. It is solid gold: paint doesn't change it. At an **enchanting table** it can be given a **soul** (Veteran, Optimist, Butler, Nervous or Poet: the table offers them in its three slots, one at a time, a grindstone takes it off): a personality for the companion robot, flavour only (see *Soul chat* below). Its visor doesn't light up: it shows simple eyes in the visor's colour as reactions, dark when nothing happens: `> <` hit, `^^` a pilot climbs in, heart eyes when refuelled or its helmet is repaired, angry when the suit lands a blow (and on a rogue, always), half-closed eyes while a socket tool works, `@ @` knocked out by lightning or held in an EM field, `x x` while the helmet is broken |
| Paint | Right-click the suit with any dye: its armour pieces (breastplate, waist, hip block, arm pieces with their pauldrons, leg pieces) and the helmet's shell take the colour and the dye is used up (the bare frame stays steel: a dye on a bare part shows once its piece goes on); the cockpit's arms show it too; another dye paints over it, a wet sponge washes it back to bare steel (the sponge stays wet). Only the look changes. A packed suit keeps its paint |
| Ammo | The tools take their ammo from **your inventory**, like a bow's arrows (off hand first): fire charges for the chaingun, TNT for the TNT launcher, amethyst shards for the rail cannon; free in creative. The suit carries none: the machine mind's tools never run out. (Suits from before 1.1 drop what their old ammo slot and nugget store held, as items, the first time they load) |
| Rogue suits | Extremely rare (2% chance per in-game day, config): a rogue suit with a red visor turns up 48-64 blocks from a player. It needs no fuel or ammo, attacks any player or mob it sees and can't be boarded. They come in **three kits**, each a painted frame, a styled helmet and one tool: the **Digger** (brown, the Protector's diver helmet, a drill: 2 in 5) runs at you and grinds you (slow, no knockback, and it wrecks your armour), the **Hunter** (red, the Hunter helmet, a rail cannon: 1 in 5) charges its beam (the core glows first, a second and a half) and shoots you from up to 26 blocks for 10 hearts (config `rogue_rail_damage`), the **Line** (green, the Spartan helmet, a chaingun: 2 in 5) shoots you. (The EM projector and flamethrower rogues no longer turn up by themselves: `/summon` only.) Each rogue wears its own mix of iron armour, from the bare frame to the full set (each piece 50%, config `rogue_armour_chance`, rolled once: a piece knocked off doesn't grow back). **Defeated, it drops its tool and its helmet's smithing template** (Protector, Hunter or Spartan). **Struck by lightning** (a storm, a Channeling trident, a lightning rod) it is stunned for a few seconds (it switches off, convulses and slumps, config `lightning_stun_ticks`), then wakes up still hostile. It leaves after an in-game day once nobody is near. Your chaingun suits shoot rogues on sight. Test one: `/summon power_suits:power_suit ~ ~ ~5 {Mind:"ROGUE",Inventory:{Items:[{Slot:1b,id:"power_suits:chaingun",count:1}]}}` (or `power_suits:drill`, `power_suits:rail_cannon`, `power_suits:em_projector`) |
| Lightning | A strike knocks a fuelled suit out: it convulses, slumps (you're stuck, the seal is off, so the fire the bolt leaves at your feet usually catches it) and restarts by itself after 5 s; the flames die as it powers up |

### Crafting the suit

Each part is crafted on its own, then torso, arms and legs are assembled like a body (at a crafting table):

| Item | Recipe |
|---|---|
| Power Suit Helmet | top row: iron block, redstone block, iron block; middle row: compass, glass, clock (they become the visor's compass and clock) |
| Power Suit Torso | iron blocks in the corners, copper blocks on the edges, a redstone block in the middle |
| Power Suit Arm (x2) | a row: copper block, piston, iron block (either way round) |
| Power Suit Leg (x2) | a column: copper block, piston, iron block (top to bottom) |
| Power Suit | arm, torso, arm across the top row; legs in the corners below |

The helmet isn't part of the assembly: put it on the finished suit (see *Helmet* above). A whole suit with its helmet
takes 12 iron blocks, 8 copper blocks, 2 redstone blocks, 4 pistons and glass (no lapis or furnaces since 2026-10-23). It comes out bare polished steel; paint it with dyes
(blue gives back the suit's old lapis blue).

The frame's armour (one piece per part: craft one torso, two arm and two leg pieces for the full set), iron ingots
round an iron block, shaped like vanilla's armour (the block keeps them apart from vanilla's iron armour):

| Item | Recipe |
|---|---|
| Iron Torso Armour | like a chestplate (ingots), with an iron block in the middle |
| Iron Arm Armour (x2) | like a helmet (ingots), with an iron block in the middle of the top row |
| Iron Leg Armour (x2) | like leggings (ingots), with an iron block in the middle of the top row |
| Copper Torso / Arm / Leg Armour | same shapes as iron armour, using copper ingots round a copper block |
| AR Glasses | top row: copper ingot, redstone dust, copper ingot; middle row: three glass panes |

The engines (swapped in the menu's engine slot; a new suit has none, so craft one before you fuel it):

| Engine | Recipe |
|---|---|
| Firebox | iron blocks in the corners, iron ingots on the edges, a blast furnace in the middle |
| Tidal Engine | iron blocks in the corners, dark prismarine on the edges, a Heart of the Sea in the middle |
| Star Reactor | netherite ingots in the corners, diamonds on the edges, a Nether Star in the middle (another Nether Star goes in the fuel slot) |

### Balance and config
Everything that costs fuel, plus damage, ranges and speeds, is in `config/power_suits-common.toml` (in the
game folder, `run/config/` when developing) and in game under **Mods > Power Suits > Config**. Changes apply
at once. Your own visor colour is a separate file, `config/power_suits-client.toml` (see *The visor and its HUD*). Fuel is counted in energy: walking burns 1 per tick, so 20 energy = 1 s of walking. Defaults (Phase 6
balance pass), with what one piece of coal (1600) buys:

| Use | Cost | Per coal |
|---|---|---|
| Walking / standing / sprinting (piloted or the machine mind) | 1 / 0.25 / 2 per tick | 80 s / 5:20 / 40 s |
| Jump | 20 | 80 jumps |
| Chaingun | 1 per tick with the barrels just turning up to 3 at full spin, while the trigger is held; 1 fire charge per bullet (4 hearts heavy, 1.5 barrage) | ~25 s of barrage (~250 bullets) |
| EM Projector | 1 per tick holding, 80 per throw | 80 s of holding, or 20 throws |
| Mining Drill | 20 per block (180 per 3x3); melee 3 per tick | ~9 faces (80 blocks) |
| Chainsaw | 15 per log; melee 4 per tick | ~20 oaks (5 logs each) |
| Flamethrower | 6 per tick of flame (1.5 hearts per hit, then 5 s of burning) | ~13 s of flame |
| TNT Launcher | no fuel (config `energy_per_shot`): one TNT per round | - |
| Rail Cannon | 3 per tick while the trigger is held (90 per 1.5 s charge) + 1 amethyst shard per shot (20 hearts to everything on the beam) | ~17 shots |
| Sealing | 20 per point of fire/frost damage kept out, 100 per harmful effect, +0.5 per tick of air under water | 80 s of burning |

The firebox burns what a furnace burns, as long as a furnace burns it: coal and charcoal 1600, blaze rod 2400, lava bucket 20000, coal block 16000, planks 300. Hover over any fuel for its walking time.

### Sounds
A powered suit is quiet: no engine loop. Now and then its backpack makes a soft sound (the firebox crackles, the tidal
pump bubbles under water, the star reactor hums), a little more often and louder as it works harder (walking, sprinting,
a tool running). The drill whirs, the chainsaw buzzes, the chaingun's motor whines, the flamethrower roars and the rail cannon hums while charging (subtitles included).
They are vanilla sounds re-pitched in `assets/power_suits/sounds.json`: swap in your own `.ogg` files there.

### The visor and its HUD
With the helmet on you see the inside of the helmet from the cockpit (first person): black pieces in the four
corners and the visor band in the middle of the top edge, like the pumpkin's view but only at the edges. While the suit
has power the visor shows the view through them (only a faint outline of their edges is left) and a HUD floating on the
glass (no helmet, no HUD: then vanilla's vehicle hearts show the hull); without power they're solid again and close the
view in. When the power comes on (fuel is back, or you climb into a running suit) the visor scans itself on: a line
appears across the middle of the screen, widens, and splits into two lines that sweep up and down to the edges; what
they pass is on (the metal turns see-through, the readouts appear). When the power goes, two lines sweep in from the
top and bottom, switching everything off behind them, meet in the middle and shrink away, leaving the glass completely
dark. It's terminal green by default: pick another under **Mods > Power Suits > Config > Visor > Visor colour** (green,
amber, blue, white, red, or Custom for any `#RRGGBB` in *Custom colour*; `visor_preset` / `visor_colour` in
`config/power_suits-client.toml`; only you see it).
- **Top left, the suit:** a blocky figure of the suit (one block per armour piece, each showing its own wear in the visor's one colour: whole above half durability, with texels missing from half, with many missing and blinking in its last 15%; a bare part is faint; the helmet counts too, broken = cracked), **HULL** (its health, % and a bar)
  with a **shield** that's lit while the suit is sealed (running with the helmet and all five armour pieces on) and faded when not, and **FUEL**: how long it lasts at walking pace (∞ on a wet
  tidal engine or a star reactor), a bar for how full the fuel slot is, and three
  **embers** for how fast it burns, about one per walking's worth: one idling or walking, two sprinting, three with a
  hungry tool at work (a charging rail cannon, the chaingun at full spin, the flamethrower; the chaingun's climb from one
  to three as its barrels spin up), none when nothing burns.
- **The socket tool's own readout**, where that tool needs it (tools with nothing to say show nothing: the drill, the
  chainsaw, the flamethrower):
  - **Chaingun**, top right: a big 3-digit counter (006; 999 means 999 or more; ∞ in creative) with **AMMO** beside
    it, and under it the barrels' heat bar with **HEAT** beside it: inverted from half, blinking in its last 15%. Overheated,
    it reads **OVERHEAT** (reaching further left) and keeps blinking all the way down while the barrels cool: the
    gun won't fire again until the bar is empty.
  - **Rail cannon**, round the crosshair: four corner brackets that wait wide and faint, close in as it charges (the
    charge in % under them) and lock with a second, inner set over **READY** at full charge; one pip per ingot left.
  - **TNT launcher**: the **arc** the round will fly, dotted from the launcher's muzzle (where you see the round come
    out) to a diamond where it will go off, with the distance (`22m`); it moves with your aim and is worked out with the
    round's own physics, so it's where the round really goes; it starts just clear of the launcher so it doesn't run
    over the gun (a round that hits nothing goes off in the air at the end of
    its fuse: a small x). Aim the diamond, not the crosshair: the round drops. When it would go off close enough for its
    blast to reach you (twice its strength: 8 blocks by default) the distance blinks inverted (an airburst's x blinks). Top right, where
    the chaingun's ammo is: the revolver **drum**, a filled chamber per round loaded (the next empty one fills while
    it's being loaded), AMMO and the TNT you carry, LOAD while it loads.
  - **EM projector**: it scans on its own: everything within its range (16 blocks) you can see that it could pull
    (mobs, dropped items) gets small faint corner brackets, and so does every other player (whether PvP lets you grab
    them or not); the nearest 10. What a click would grab now (under the crosshair) gets bright brackets, its name
    and its health. While it holds something: brackets round it with its name over them (**HEAVY** first for something
    too heavy to lift, which it only drags and shoves) and its health, and the **arc** it would be thrown along if you
    let go now, to a diamond where it would land (moves with your aim); the marked mobs in its way light up.
- **Top centre, compass and clock** (the helmet is crafted with both), as terminal text: a compass tape that slides a
  character (5°) at a time with a `^` under where you face, the suit's coordinates to its left (the block it stands
  on, like F3's `Block:`; `--- --- ---` in a world with reduced debug info) and the time to its right (`18:40`). Like
  the vanilla items the compass and clock only work in the overworld: elsewhere the tape spins and the time reads
  `--:--`; the coordinates work everywhere. At the right end of that row, under the end of the tape, **NV** while the
  night vision is switched on (N): in the visor colour while it lifts the dark, faint while it waits for the dark (in
  daylight or torchlight).
- The whole visor is one colour, warnings too: a readout in trouble shows its label in **inverse video**, like an old
  terminal (a solid block of the visor colour with the word cut into it). A **warning** (half gone) holds the block
  steady, **critical** (the last 15%, or something you can't use yet) blinks it. Only the label in trouble changes:
  HULL under half (steady) and in its last 15% (blinking), FUEL when low, a tool's own: the last rounds (AMMO: 16
  bullets, the last TNT; the rail cannon's last ingot pip), a hot or overheated chaingun (HEAT, OVERHEAT). With **no
  power** the glass goes completely dark: only the helmet's edge is left. Why it went dark is in the suit menu (E):
  its Fuel panel reads **No fuel**, **No engine** or **Flooded**, or its Power key is out.
- While the HUD is up, vanilla's boss bars move down under the compass and the effect icons under the top right corner.
- **Night vision**: when the light around you falls (light level 7 and under, full at 4: caves, any night outside) the
  visor lifts the dark, tinted in the visor colour, over a second; it goes off with the visor's power or the **N** key
  in a third of one, and fades away by itself when it's light again. It works like vanilla's night-vision potion, part
  of the way (the potion makes everything bright; the visor about half as much, so a cave stays a cave). Settings in
  the same config: `visor_night_vision_on` (what N flips), `visor_night_vision` (strength, 0.3; the potion is 0.6),
  `visor_vision_tint` (`VISOR` or `WHITE`). Only on your screen; shader packs (Iris) draw their own light and don't
  show it.

Fuel works like a furnace: the suit burns one item from the fuel slot at a time. It burns whenever
the suit is powered, piloted or not (the machine mind runs it): standing still uses a quarter of the walking rate, sprinting double, and each
jump a little extra. Under 30 seconds left the suit beeps and the exhaust coughs dark smoke. At zero the suit powers down and slumps; climb out, refuel it in the menu
and it stands back up (1.4 s). Fuel is needed in creative mode too. Suits from before this version
start empty: give them some coal.

**Chaingun** (crafted: iron ingots top and bottom rows; piston, iron block and dispenser in the middle). A cluster of
four barrels driven by the engine. **Tap** right-click for heavy single shots (4 hearts); **hold** it and the barrels
spin up over 2.5 s, firing faster and faster up to a barrage of 10 bullets a second (1.5 hearts each). Let go and they
coast down over 1.5 s; grab the trigger again before they stop and it picks up where it was. While you hold the trigger it burns
fuel with the spin: a walking's worth a tick with the barrels just turning, up to three times that at full spin (the
HUD's burn embers climb from one to three; config `slow_spin_energy_per_tick`, `full_spin_energy_per_tick`). Each
bullet uses **one fire charge** from your inventory (off hand first, like a bow's arrows; free in creative); the HUD shows how many
you carry and the barrels' heat. Bullets are hot tracers at 80 blocks/s that fly along your line of sight (whatever is in the crosshair is what gets hit;
they're drawn coming out of the gun and meet that line at the target). They ignore the half-second of immunity mobs
get after a hit (so every bullet of a barrage counts), push lightly instead of vanilla's knockback, and spark off
blocks without breaking them. **Overheat** (on by default, `overheat` in the config): 80 bullets without letting go and
the barrels glow white-hot and lock until they're cold again (about 4 s: the heat bar empty); the tips glow from a third of the way there. Kills
credit you ("shredded by"). It does nothing on foot. Old Plasma Cannons and Rivet Guns in your world become Chainguns.
With an empty socket or no fuel the trigger just clicks.

**EM Projector** (crafted: iron ingots in the corners, copper ingots top and bottom middle, redstone either
side of a lodestone). Grabs dropped items, mobs and players (players only where PvP is on) within 16 blocks; a rider is caught with their
mount. Other suits and the heavyweights in the entity tag `power_suits:em_heavy` (bosses, iron golems, ravagers, wardens; a
datapack can add more) are too heavy to lift:
they fight the field, held in place and slowed to a crawl (a piloted suit moves at a quarter speed), dragged a little,
and letting go only shoves them. Never spectators, creative players or no-AI "statue" mobs.
Thrown mobs that hit a wall take damage ("slammed into a wall"), and they bowl through any mob in their way: each one
they hit takes the impact ("bowled over", credited to you) and is knocked along, and so does the thrown mob, which flies
on to the next. A full-speed impact does 10 hearts (config `slam_damage`: enough to kill a zombie, a skeleton or a
creeper), a slower one less. Socket only. A redstone electromagnet: four
copper-wound prongs round a redstone lens; the lens glows faintly while it's mounted in a powered suit and the prong
tips light up and spark while it holds something; the beam is redstone dust.

**Mining Drill** (crafted: a diamond on top, iron ingots + a diamond in the middle row, iron ingots + a
piston at the bottom). Diamond-tipped: it digs pickaxe and shovel blocks a diamond tool can harvest
(stone, ores, obsidian, dirt, sand, gravel, snow...), never bedrock/barriers, never wood (that's the
chainsaw's). Aim at a block within your reach (6 blocks inside the suit): the 3x3 around it in the plane of
the face you hit cracks together and breaks together, as slowly as its hardest block (stone 0.3 s, deepslate
0.6 s, obsidian 9.4 s), then a short pause before the next. Drops land where the blocks were (ores drop XP);
like vanilla, creative mode breaks without drops.

**Chainsaw** (crafted: iron ingots around shears and a piston). Cuts axe blocks (logs, planks, wooden
things) and leaves one at a time at diamond-axe speed. A cut log that belongs to a natural tree (logs
touching leaves that grew, not placed ones) brings down every connected log at or above the cut, top first,
3 logs per tick, 15 fuel each; leaves are left to decay as usual. Log cabins and other builds only lose the
block you cut. Both mining tools post Minecraft's block-break event for every block, so land-claim mods can
protect blocks from them.

**Flamethrower** (crafted: iron ingots, a bucket for the tank, copper, flint and steel, a blaze rod). Hold right-click
and it throws a stream of burning fuel, one gob a tick, about 7 blocks out: it arcs a little and takes a moment to get
there, so sweeping the nozzle sweeps the flame. Everything it washes over takes 1.5 hearts (about twice a second) and
burns for 5 s; fire-proof mobs (blazes, magma cubes, a fire resistance potion) don't care. Where it lands it melts ice
and snow, burns cobwebs away, lights campfires and candles, sets off TNT and now and then sets the block on fire (config
`ignites_blocks`; you must be allowed to build there, and claim mods see a block-place event). Raw food lying in the
stream cooks after about a second, the whole stack at once (what a smoker would make of it), and the stream sets no fire
next to dropped items. Under water it only bubbles. Runs on fuel alone: 6 per tick (a coal lasts about 13 s of flame).
Its pilot light glows blue whenever the suit is powered. With the machine mind it does the chaingun's job from close up
(follows and defends its owner, fires from 5.5 blocks, keeps a wider berth round friends) and never sets blocks on fire;
rogue suits sometimes carry one (and set fires if mobs may grief).

**TNT Launcher** (crafted: iron ingots, a dispenser, an iron block, gunpowder, copper). A revolver drum of TNT under a
fat barrel. Right-click lobs a block of primed TNT toward your crosshair (it arcs like an arrow) that blows up the moment it
hits a block or a mob, as real TNT: strength 4, breaking blocks unless the config says not to (`breaks_blocks`), and it
obeys the `tnt_explodes` game rule and land-claim mods. The drum holds 4 rounds: a tap fires one, holding fires them a
half second apart (config `shot_interval_ticks`), so a full drum empties in under two seconds. Reloading is filling the
chambers back up, one a second (`reload_ticks`) with TNT from your inventory (free in creative), starting half a
second after your last shot (`reload_delay_ticks`); a shot restarts the chamber being loaded, so you can fire whatever
is loaded at any time, and holding the trigger on an empty drum fires each round as it's loaded. With an empty drum
and no TNT the trigger only clicks. The rounds in the drum stay in the launcher when you take it out (or pack the
suit); nobody inside, nothing loads. After each shot the drum turns a quarter turn to the
next round. With the helmet on, the visor shows where the
round will land (the arc and a diamond with the distance: aim the diamond). It's yours to fire only: the machine mind never
uses it and rogue suits never carry one.

**Rail Cannon** (crafted: iron ingots, copper ingots, an amethyst shard, an iron block). The chaingun's opposite: one
slow, critical shot instead of a barrage. Two steel prongs with a blue core between them, after DOOM's gauss cannon.
Hold right-click and it charges (1.5 s, config): the core glows brighter, a hum rises and a chime says it's full (the
HUD's brackets lock); it holds the charge as long as you hold the button. Let go at full charge and it fires an
instant beam along your crosshair, up to 64 blocks: every mob on the line takes 20 hearts (it goes through them all,
and through any hit immunity), and on the way it breaks what a sprinting suit smashes through (glass, panes, leaves,
ice, cobwebs; config `breaks_blocks`, claims can veto) until it meets anything solid. Let go early and it just winds
down without firing (no ingot spent, but the fuel it burnt charging is gone). Charging burns 3 fuel a tick (three
times walking, config `charge_energy_per_tick`), and so does holding a full charge; a shot costs an iron ingot from your
inventory (free in creative) and no more fuel, then it cools for a second. With the machine mind it's a long-range guard: from home it shoots monsters it can see within 40
blocks of home (config `rail_guard_radius`) and whatever attacks it or its owner, never with a friend anywhere on the
beam (it goes on past the target), and its beam never breaks blocks. Rogue suits never carry one.

**Right hand**: shows your selected hotbar item and carries it forward (`hold_item`), reaching out each time
you use it (`use_item`). It's the suit's main hand, like yours: until a tool replaces it (a power tool on the right arm takes the hand's place and the attack button; the left arm's tool takes the off hand's). In first person
the suit's gauntlet holds it at the lower right (cockpit viewmodel). It's a normal hand: left click attacks and mines
(at normal speed: riding doesn't count as "in the air" while the suit stands), right click uses the item. When the hand
has nothing to do, right click goes to the left arm's tool instead, exactly like vanilla tries your main hand and then a
shield in your off hand (with no tool on the left arm it is a plain hand: your off-hand item works as in vanilla). A powered-down suit's hand can't do anything.

**Lights**: the firebox on the backpack (under the fuel hatch) glows through its grate while the engine runs (brighter under load,
dimmer when fuel runs low, embers dying out after shutdown), and the visor shows who is in control:
**amber** = a pilot (whatever they do), **green** = the friendly machine mind, **red** = a rogue mind (only rogues,
so red always means danger), **dark** = powered off; it stutters while starting up or shutting down and drops out
now and then on low fuel. Hits don't change it.
The chaingun's barrels glow with heat, the EM projector's redstone with its field and the rail cannon's core with its charge.

While inside: the suit takes hits instead of you, it has no fall damage, steps up full blocks,
and the camera pulls back in third person (F5).

Water (Fallout-style): the suit sinks and walks along the bottom at half speed. It never runs out
of air, but you do: once your head is under, your air bar drains and you drown in survival. Walk out
up a slope or stairs, or jump (weaker underwater).

## Developing

Minecraft 26.3 needs Java 25. It's installed with Homebrew (`brew install openjdk@25`) but not on the PATH by default.
Every terminal needs:

```sh
export JAVA_HOME=$(brew --prefix openjdk@25)/libexec/openjdk.jdk/Contents/Home
```

(add that line to `~/.zshrc` to make it permanent)

Worlds saved by the 1.21.1 version of the mod open in 26.3 (suits keep their fuel, tools, owner and home), but Minecraft
upgrades a world the first time it's opened and there's no way back: let it make the backup it offers.

| Command | What it does |
|---|---|
| `./gradlew runClient` | Starts Minecraft with the mod (offline dev account) |
| `./gradlew runGameTestServer` | Runs the automated in-game tests headless, prints pass/fail |
| `./gradlew build` | Builds the mod jar into `build/libs/` (put it in a real `mods/` folder, plus GeckoLib) |
| `node tools/export-model.mjs` | Re-exports model, animations and texture from the open Blockbench project (the big suit) |
| `uv run --with pillow python3 tools/make-frame-paint.py` | Rebuilds the frame's painted textures (`textures/entity/paint/power_frame(_slim)_<dye>.png`, one per dye and build) from the frame's texture: the armour pieces' and the helmet shell's steel shades swapped for the dye's ramp (run after `export-frame.py`) |
| `python3 tools/export-frame.py` | Exports the frame (`model/power_frame.bbmodel` + `_slim`, built by `model/art/frame_model.py` with the helmet) into the mod without Blockbench: `geckolib/models/entity/power_frame(_slim).geo.json`, their textures (split: opaque, the visor glass `power_frame_glass`, its glowmask `power_frame_glow_visor`, the engine's fire `power_frame_glow_fire` and the same texels in grey for the other engines `power_frame_glow_core`), `power_frame.animation.json` (every animation name, empty: the frame is posed in code) and the cockpit's arm `geckolib/models/view/frame_arm(_slim).geo.json` |
| `./gradlew runAutopilot` | Dev tool: scripted test drive in a fresh flat world (pool, running out of fuel, chaingun range, right hand, EM projector, drill + chainsaw, tool items on foot), saves `run/screenshots/ap_*.png`, `run/autopilot_{water,fuel,cannon,em,mine}.csv`, quits |
| `./gradlew runAutopilotFrame` | Dev tool (~25 s): the frame with the player inside from the front, back and side, the third-person and cockpit views, a walk and a sprint, the head following the view, an empty frame slumped beside it; `run/screenshots/ap_frame_*.png`, `run/autopilot_frame.csv` (hitbox, the pilot's eye height, the walk animation) |
| `./gradlew runAutopilotPose` | Dev tool (~30 s): the code-driven pose from fixed cameras (torso lean with the view pitch, tool raise, torso twist with the view yaw toward marker blocks); `run/screenshots/ap_pose_*.png`, `run/autopilot_pose.csv` |
| `./gradlew runAutopilotGait` | Dev tool (~45 s): foot slip and leg turning while walking, backing up, strafing, turning, sprinting; `run/autopilot_gait.csv`, `python3 tools/gait-report.py` |
| `./gradlew runAutopilotMech` | Dev tool: only the autopilot's last scene (~25 s): smashing through panes/leaves/glass/ice, a 9-block stomp on mobs, lightning, a punch, wading through lava + poison; `run/screenshots/ap_mech_*.png`, `run/autopilot_mech.csv`. A file `run/cleanzap` keeps the bolt's fire away (to see the knock-out animation) |
| `./gradlew runAutopilotTerrain` | Dev tool: drives a suit over real terrain in a **copy** of `run/saves/New World`, logs `run/autopilot_terrain.csv` (speed, height, ground contact, animation, camera) |
| `uv run --with pillow python3 tools/contact-sheet.py fp out.png` | Tiles autopilot screenshots (prefix `fp`, `tp`, `side`, `water`, `fuel`, `menu`) |
| `uv run --with pillow python3 tools/make-gui.py` | Rebuilds the suit menu background from vanilla's inventory screen, and the keys' symbols |
| `uv run --with pillow python3 model/art/item_icons_art.py [--sheet out.png]` | Draws every item icon: hand-made 16 px pixel art (vanilla style), not rendered from the model; `--sheet` writes a review sheet |
| `python3 tools/extract-view-geo.py` | Rebuilds the cockpit viewmodel (`geckolib/models/view`) from the suit model (run after `export-model.mjs`) |
| `uv run --with pillow python3 tools/make-visor-textures.py` | Rebuilds the helmet edge pieces the pilot sees (`textures/gui/visor/`: corners, brow, and their lips alone, all that shows while powered) |
| `uv run --with pillow python3 tools/make-glowmasks.py` | Rebuilds the glowmasks (`power_suit_glow_{fire,visor,heat,heat_barrel,em_core,em_arc}.png`) from the texture's reserved colours (run after `export-model.mjs`) |
| `uv run --with pillow python3 tools/make-paint-textures.py` | Rebuilds the painted textures (`textures/entity/paint/power_suit_<dye>.png`, one per dye) from the steel texture (run after `export-model.mjs`) |
| `./gradlew runAutopilotPaint` | Dev tool (~30 s): a suit right-clicked with dyes and a wet sponge; `run/screenshots/ap_paint_*.png` (in-game back view + front), `run/autopilot_paint.csv` (server/client paint, dyes left) |
| `./gradlew runAutopilotStyles` | Dev tool (~30 s): the helmet styles side by side (in-game back view + front, painted), the smithing table making one; `run/screenshots/ap_style_*.png`, `ap_menu_smithing.png`, `run/autopilot_style.csv` |
| `tools/view-tuner.sh start\|shoot\|stop` | Live-tunes the cockpit viewmodel's placement (`run/view/tuning.json`, shots `run/screenshots/ap_view_*.png`) |
| `python3 tools/terrain-report.py` | Summarizes `run/autopilot_terrain.csv` per leg (speed, air time, drops, step-ups, animations) |

## Where things live

```
src/main/java/dev/ajaczero/powersuits/
  PowerSuits.java            entry point: registers everything
  registry/ModEntities.java  the entity type (hitbox size, pilot seat height)
  registry/ModItems.java     the item
  registry/ModMenus.java     the suit menu type; ModDataComponents.java: the loadout stored on a packed item
  entity/PowerSuitEntity.java  the suit as Minecraft sees it: vanilla hooks (riding, movement, water, jumping, damage,
                             death, saving), the synced data table, the slots, the tick that runs its parts:
    entity/SuitDriving.java  how it moves: the pilot's keys, walk/sprint speeds, stepping down ledges, sinking and walking
                             in water and lava, the charged jump, crawling in an EM field, the legs turning under the torso
    entity/SuitPower.java    the engine and its energy: burning fuel, flooding, free power, the lightning knock-out
    entity/SuitSocket.java   one arm's socket tool as the suit works it (ToolArm LEFT / RIGHT): trigger (pilot / mind), cooldown, synced spin/shots;
                             suit.socket() = the arm being ticked or drawn (onArm), else the primary one (the first tool)
    entity/SuitBrain.java    the machine mind's state: owner, home, aim, the job its tool gives it, rogues' gear and lifetime
  entity/SuitArmour.java   the frame's armour: one piece per part (slots 5-9), protection modifiers, the synced worn tiers, the full set
    entity/SocketVisuals.java   client: the tool arm's raise and recoil, the installed tool's ToolEffects
    entity/SuitAnimator.java    client: measured speed, jumps/landings, step easing, which animation plays and how fast
    entity/SuitLights.java      client: fire, visor, engine glass, lightning sparks
    entity/SuitFace.java        client: the robot helmet's visor faces (what shows when; SuitBlows.java: the server's "landed a blow")
  entity/SuitFuel.java       which items burn and for how long, per engine
  entity/FireboxFuel.java    asks a never-placed furnace how long it burns an item (the firebox's table)
  entity/SuitEngine.java     the engines (firebox / tidal / reactor); item/EngineItem.java: their items
  entity/ExhaustSmoke.java   client-side smoke from the back pipes
  menu/PowerSuitMenu.java   menu logic: socket, fuel, helmet + engine slots, shift-click, F swaps with the
                             socket, Power + Pack keys; opened by E inside (PowerSuitEntity.openCustomInventoryScreen)
  item/SuitLoadout.java      fuel/tool/helmet/engine/armour/half-burnt item carried by a packed suit item
  item/SuitArmourItem.java   a frame armour piece (ArmourPiece: torso/arm/leg; ArmourTier: iron, copper planned)
  item/HelmetStyle.java      the helmet styles (design sec. 4c); SuitHelmetItem: name + flavour line, HelmetTemplateItem: the templates
  item/PowerTool.java        what a socket tool is: fuel per use, cooldown, model bone, use(); worked by an operator
                             (the pilot, or the suit itself while its mind drives: aim, ammo, credit); its mind job
                             (mindUse: entity/ai/ToolUse, and its own goals: mindGoals) and its looks (createEffects)
  item/ToolEffects.java      client: one suit's looks for its tool (moving parts, lights = ToolLight, shot effects);
                             one per tool: ChaingunEffects, TntLauncherEffects, EmProjectorEffects (+ the EM beam),
                             FlamethrowerEffects, RailCannonEffects (+ the rail beam, drawn by client/RailBeamRenderer)
  entity/SuitMind.java       friendly / rogue (synced: the visor colour)
  entity/ai/SuitGoals.java   the goals every machine mind has (vanilla goal system): walk home, look around, follow
                             the owner, pick a target; a rogue wanders
  entity/ai/ (tool jobs)     each tool's own goals, learned when it goes into the socket (PowerTool.mindGoals):
                             GunAttack (chaingun, flamethrower: shoot / punch, base AttackGoal), EmGuard + RogueEmAttack,
                             RailGuard; every mind: MeleeAttack (follow route: chainsaw / punches), HomeGuard (guard route:
                             drill / punches)
  entity/ai/SuitTargets.java who the mind may shoot, what to shoot first, line-of-fire check
  item/ToolMelee.java        the drill's and chainsaw's melee (pilots under the crosshair, a mind only its chosen target)
  entity/RogueSpawner.java   rogue suits turning up once in a while (saved day countdown, like the wandering trader)
  item/ChaingunItem.java     the first tool: spin-up, fire charge ammo, overheat (continuous tool; also a GeckoLib item)
  item/SuitAmmo.java         the tools' ammo: from the pilot's inventory (off hand first), endless for the machine mind
  item/EmProjectorItem.java  the second tool: grab / hold / collect / throw, slam and bowling damage (per-suit state in Beam)
  item/SocketAim.java        muzzle position, crosshair aim point, entity under the crosshair
  item/DrillItem.java        the third tool: 3x3 digging at diamond pickaxe/shovel speed
  item/ChainsawItem.java     the fourth tool: cuts wood, fells natural trees top-down
  item/RailCannonItem.java   charge, fire on release, the piercing beam (blocks it breaks, mobs it hits); the mind's job is
                             entity/ai/RailGuard; item/RailCannonEffects + client/RailBeamRenderer draw the beam
  item/ToolMining.java       shared block breaking for both (BreakEvent, drops, crack overlay, progress)
  entity/Bullet.java         the tracer bullet (flight, hit without immunity, sparks off blocks)
  network/ToolTriggerPayload.java  client -> server "tool button pressed/released"
  network/PowerSwitchPayload.java  client -> server "the pilot pressed the power switch key"
  item/PowerSuitItem.java   deploying / packing / repairing
  PilotProtection.java       redirects damage from the pilot to the suit (not "suffocating" against a wall)
  SuitSeal.java              sealed suit: fire/frost/effects kept out for fuel, air under water (tag damage_type/sealed_out)
  entity/SuitStomp.java      landing dust, stomp shock wave (damage type power_suits:stomp)
  entity/SuitSmash.java      breaking leaves/panes/glass/ice while walking/sprinting (block tags suit_smashes_*)
  PilotHands.java            hand needs power, +1.5 reach, +4 melee damage, F swaps the hand with the socket tool
  PowerSuitsConfig.java      balance knobs (config/power_suits-common.toml)
  registry/ModSounds.java    engine + tool sound events (audio picked in assets/power_suits/sounds.json)
  client/                    rendering only (never loaded on servers)
    PowerSuitModel.java     points GeckoLib at the frame's files (power_frame, or power_frame_slim for an Alex skin)
    PowerSuitRenderer.java  copies the suit's state for the frame (SuitRenderData), poses it in code (vanilla's limb
                             swing, the head following the view, the slump without power); draws only the legs in
                             first person (cockpit)
    PilotLayer.java          the pilot inside the frame: vanilla's player parts in his own skin at the pilot_* bones
    HelmetGlassLayer.java    the helmet's visor glass (a translucent pass over his face)
    SuitRenderData.java      what the renderer and its layers read from the suit each frame (GeckoLib DataTickets)
    PilotView.java           hides vanilla's pilot (PilotLayer draws him) and hands, pulls the camera back
    CockpitHands.java        first-person viewmodel: his left arm in the frame's with the socket tool on its end
                             (geckolib/models/view/frame_tool); on the right the held item (vanilla's) or, empty, his
                             skin arm in the frame's arm (geckolib/models/view/frame_arm; both from export-frame.py)
    CockpitView*.java        its GeckoLib animatable/renderer (geckolib/models/view, cut from the suit by tools/extract-view-geo.py)
    PowerSuitScreen.java    draws the suit menu (vanilla's inventory screen with the suit: preview, keys) and the status
                             panels beside it (Hull, Fuel, Sealed, the pilot's effects, like potion effects)
    SuitKey.java             the menu's slot-sized keys (Power latches pushed in while on; Pack)
    SuitKeys.java            the suit's own key bindings (the power switch, night vision)
    SuitHud.java             the pilot's HUD (suit readout, compass + clock, the tool's own HUD) + low-fuel beep; moves boss bars
    hud/                     each socket tool's own visor HUD: ToolHud, ToolHuds (item -> HUD, filled in by ClientSetup),
                             HudView (colours, crosshair, world-to-screen, the top right ammo block, dotted flight lines),
                             ChaingunHud, RailCannonHud, TntLauncherHud (drum + the round's arc), EmProjectorHud (box + throw arc)
                             and effect icons out of its way
    SuitVisor.java           the helmet's edge around the first-person view (solid pieces unpowered, only their outline powered)
    VisorConfig.java         the player's own visor colour and night vision (CLIENT config, power_suits-client.toml)
    VisorVision.java         the visor's night vision (raises the lightmap's floor); the lamp (a post effect, parked for an upgrade)
    VisorPower.java          the visor's warm-up and shutdown scan (lines sweeping from the screen's middle)
    ToolInput.java           the right arm's tool on left click, the left arm's on the right click the hand passes on (vanilla's off-hand turn)
    HeldItemLayer.java       draws the pilot's selected item in the suit's right hand (third person)
    SuitGlowLayer.java       the suit's lights + the tool's ToolLights (the frame's glowmasks, tinted per frame): the
                             engine's fire, the visor, the status lamp, the chaingun's lights, the pilot light
    BulletRenderer.java      the glowing tracer streak
    ToolRotors.java          turns the chaingun's barrels / the TNT drum, shakes the rail cannon (suit + cockpit viewmodel)
    ClientSetup.java         registers the renderer
    PowerSuitsClient.java    client-only @Mod entry: the visor config + the in-game config screen
    SuitSounds.java          engine sounds now and then + tool loops (tickable sounds that follow the suit)
src/dev/java/dev/ajaczero/powersuits/   development tools: compiled against the mod, NOT in the jar players get
  dev/PowerSuitsDev.java     their @Mod entry point (dev runs load src/main + src/dev as one mod, see build.gradle)
  test/PowerSuitTests.java  GameTests (@SuitTest methods, registered by test/SuitTests.java)
  client/dev/AutoPilot.java  scripted screenshot test drive (only with -Dpower_suits.autopilot); *Scene.java: its scenes,
                             TerrainPilot (real terrain), ShowcaseScene (the mod page's pictures)
  dev/MultiplayerScript.java + client/dev/MultiplayerScene.java   the scripted multiplayer check
src/dev/resources/data/power_suits/structure/test_pad.nbt   floor used by the GameTests (9x11x9, floor on its second layer)
src/main/resources/
  assets/power_suits/geckolib/models|animations/entity/, textures/entity/   exported from Blockbench
  assets/power_suits/textures/gui/power_suit.png      suit menu background (tools/make-gui.py)
  assets/power_suits/post_effect/visor_lamp.json, shaders/post/visor_lamp.fsh   the visor lamp (parked: no setting turns it on)
  assets/power_suits/geckolib/models/view/power_suit_view.geo.json  cockpit viewmodel: tools + gauntlet cut out of the suit model (tools/extract-view-geo.py)
  assets/power_suits/models/item/chaingun.json         a flat hand-held item, like a vanilla tool (item/handheld)
  assets/power_suits/items/<item>.json                 which model each item shows (needed since 1.21.4)
  assets/power_suits/textures/item/*.png               every item icon, 16 px pixel art drawn by model/art/item_icons_art.py
  data/power_suits/damage_type/bullet.json             "shredded" damage type (+ minecraft is_projectile, no_knockback, bypasses_cooldown tags)
  data/power_suits/damage_type/em_slam.json            "slammed into a wall" (EM throws)
  data/power_suits/damage_type/em_struck.json          "bowled over" (a thrown mob hitting another)
  data/power_suits/recipe/*.json                       crafting recipes (suit parts, suit + 4 tools)
```

## Notes

### The frame (branch experimental/frame-concept, going in game step by step)

The frame replaces the big suit's looks inside the same `power_suit` entity (same items, save data, mechanics): an
exosuit the player stands in, drawn in his own skin. Step 1 (2026-11-14) is in: the frame's model (`tools/export-frame.py`),
the pilot (`PilotLayer`: Steve's wide arms or Alex's slim ones, the frame's slim build with them), the code pose
(vanilla's walk swing, the head turning up to 50 deg off the torso and the torso the next 40, a 25 deg slump without
power), a 0.9 x 2.3 hitbox (fits 1-wide and 3-high gaps; the big suit was 1.4 x 2.95) and the pilot's eyes at his
own, 1.98 up. Step 2: the cockpit shows nothing of his body looking down (like vanilla), an empty right hand is his
own arm in the frame's arm (its cage and fist), and the third-person camera sits 5 blocks back. Step 3: the helmet (style C: wraparound visor, radio and camera on
its outer layer) when the suit has one, his face behind its smoked glass, the glass lit in the visor's colour at part
strength (amber: a pilot; green: the mind; red: a rogue; dark without power), his hat layer hidden under it; without a
helmet his own head with its hat layer. The frame's left hand is the socket (the arm ends at his hand). Step 4: the engine (the heart: a
porthole core and copper hoses painted on the front, the hot-rod blower on the back with its fire window, supercharger
and exhaust caps) with the firebox, smoke from the caps. The
tidal engine has a body of its own (2026-11-16, the diver, picked from three drafts: the engines shouldn't follow the
firebox's shape, so the back is 3D and the front and sides are flat decals): two dark iron diving tanks with teal
level windows and a valve each (the bubbles come out of them), a manifold between them with the Heart of the Sea in a
porthole, a dive gauge on the chest (in a steel ring under the breastplate) and glass water lines with bubbles over the
shoulders and down the waist into the tanks; the glass is painted in dark reserved teals and lit by
`power_frame_glow_sea` with the tidal shimmer (`model/art/frame_sea_art.py`, groups `engine_sea` / `sea_open` /
`sea_armored`). The star reactor has its own too (2026-11-16, built like the firebox and the tidal engine after a Sandevistan chain
was dropped; rounds 20-26 of drafts): a beacon case on the back (a pane of violet glass round the star, wrapping onto
its sides as slits, a rim with the beam's hole on top), two pylons of charge cells standing 1 px off the back either
side of it on glass links, a lens on the chest (in a ring under the breastplate) and four violet glass lines over the
shoulders and round the waist, under the pylons into the case's sides; its metal is netherite (a late-game engine).
The cells light one after another up the pylons into the star and out of the rim, faster the harder the engine works
(`SuitLights.getStarSegments`, the masks `power_frame_glow_star` and `_star_0..5` from
`frame_star_art.segment_of`, `model/art/frame_star_art.py`, groups `engine_star` / `star_open` / `star_armored`); ender
motes are drawn into the pylons. The helmet clips into the
blower looking far up (user: fine, it rarely happens). Step 5a: the tools (split into standalone models under `model/tools/` and `geckolib/models/tool/` on 2026-11-21, exported by `tools/export-tools.py` and attached onto `left_socket` / `right_socket` by `ToolLayer` and `CockpitViewRenderer` via `ToolModelRenderer` with independent per-arm glowmasks) in either arm's socket (the drill, the
chainsaw, the chaingun, the flamethrower, the rail cannon, the TNT launcher (a turning fluted dark-slate octagonal drum with four recessed red TNT chamber ends over a light-steel barrel, dark-slate muzzle ring and two-prong fork sight; reworked 2026-11-20 after the big suit's round 5 launcher) and the EM projector (compact 3 px vented housing over a spinning 3 x 1 x 3 redstone core and four flush cardinal copper-wound prongs with aligned redstone tips, 7 px overall, spun by `ToolRotors` while active; reworked 2026-11-20), each in the fist's place; the rail cannon (reworked 2026-11-21 for the 6 x 6 sleeve, `RAIL=gauss`): a two-tone dark-slate and bolted steel receiver with glowing blue capacitor windows, recessed copper induction pockets and a central glowing breech nozzle, feeding 3-step sculpted twin rails (copper breech clamps, vented mid rails with glowing side windows, tapered dark-slate muzzle tips) across a 1.5 px open gap, lit in three bands that surge from the capacitor and breech down the rails as it charges (`ToolLight.RAIL_FLOW_*`, `power_frame_glow_rail_flow_<n>`), the forks straining apart as it shakes); the drill's bit spins and the chain runs (their run animations, kept
from the big suit's file: the frame names those bones the same), the chaingun's barrels turn (ToolRotors). Step 5b: using a tool raises the left arm
until the tool points along the view (pitch and head yaw; a player's one-armed aiming pose), and the muzzle
(SocketAim) is the shoulder plus 17.5 px along the view (shortened 3 px on 2026-11-20 when all seven tools were lifted
+3 px up the forearm to built y 19 with 6 x 6 sleeved bases 0.5 px proud of the arm); in the cockpit his left arm in the frame's, the tool at its
end, where vanilla draws a left hand, turned about the shoulder toward a point low left of the crosshair at rest and
at the crosshair 10 blocks out when raised, with vanilla's bare-arm sideways roll removed so every tool stays top-side up (CockpitHands.toolArmTransform / levelRoll; the hand pass's pose isn't identity in 26.3, so the turn is worked out under it). No exhaust smoke in the pilot's own first-person view (it drifted past the
camera). Step 5c: the tools' lights: a status lamp on the drill's and chainsaw's base (red ready, green running,
dark without power: ToolLight.LAMP_IDLE / LAMP_RUN, painted in reserved dark colours, LAMP=dark), the chaingun's emerald
base vents (moved off the muzzle 2026-11-20, on with the power), its two-stage uniform barrel/muzzle heat glow (`ToolLight.HEAT`
from 30% on the barrel tips, bores and muzzle underside/bottom rim; `ToolLight.HEAT_BARREL` creeping uniformly back from 55%
along the solid muzzle, collar and exposed barrels via per-texel alpha), and the flamethrower's blue pilot light, on the suit and the cockpit
viewmodel (plus the EM projector's redstone core/tips and rail cannon's flowing core). Step 6a
(2026-11-14, design sec. 10): the frame's armour as items and slots, no looks yet: Iron Torso / Arm / Leg Armour (one item
per piece, either side, a tier each), five slots after the old ones (torso, left/right arm, left/right leg: 5-9), each
piece's armour points as an attribute modifier (transient: rebuilt from the slots on load and following config edits),
the bare frame at 0 armour (the big suit had 12), the worn tiers synced in one int (SuitArmour), sealed = powered + helmet +
all five pieces, the pieces packed with the suit. Step 6b (user's pick G1 of five mockup rounds): the suit menu is vanilla's inventory
screen slot for slot (the armour round the preview like a body, the socket in the off-hand slot, fuel -> arrow -> the
Power key in the crafting corner, Pack small at the recipe book's place), the terminal status screen and the burn flame
gone; Hull, Fuel and Sealed as potion-effect panels beside it (Sealed only while sealed), the pilot's effects under them.
Step 6c: the pieces on the frame. The saved files carry the bare frame and the iron pieces both (frame_model.py
ARMOR=game: each part's frame cubes in `frame_<bone>`, its piece in `armor_<bone>`; the engine's front both ways,
`engine_open` and `engine_armored`), and the renderer shows each part's piece while it's worn, its frame otherwise
(client/ArmourBones): the breastplate and waist for the torso (with the engine's armoured front: the lower hoses and the
radiator grille glowing with the fire), the arm pieces with their pauldron decals, the leg pieces; the belt gives way to
the hip block when either leg piece is on. The cockpit's arms follow (their view geo holds both). The model's checks
skip only pairs that are never drawn together, so every mix of worn and bare parts is checked. Then wear (user,
2026-11-14): vanilla's `LivingEntity.hurtArmor` hook (empty on mobs) is where the suit's pieces wear (`SuitArmour.wear`,
vanilla's max(1, damage / 4) per hit), so whatever vanilla's armour formula skips skips the wear too; a piece breaks
with vanilla's sound and particles sent from the server (vanilla's are a client entity event for equipment slots,
which the pieces aren't in). The helmet stops at its max damage instead of breaking (set directly, not hurtAndBreak,
which would use it up) and is "broken" there (`ItemStack.isBroken`; synced as HELMET_BROKEN for the seal). Rogues roll their pieces once (`SuitBrain`'s saved `RogueArmour` flag: `equipRogue` runs
every tick and only fills empty slots). Step 7, paint (user's pick B from in-game mockups, 2026-11-14): the armour pieces and the
helmet's shell take the dye, as on the big suit, the bare frame stays steel (painting its members too speckled their
grain); `tools/make-frame-paint.py` reuses the big suit's dye ramps. Step 7b, the helmet styles, one by one with the
user from a reference picture each (`frame_helmet_art.py`, `HELMET_STYLE=<style>` drafts): the saved files carry each
picked style's helmet beside the standard one under `armor_head` (`helm_standard`, `helm_<style>`; `HELMET_VARIANTS`
in `frame_model.py`), the renderer shows the worn style's or the standard (a style without art yet). The visor glass
and its light come with it (any glass texel is in the glass texture and the visor mask; a hidden bone isn't drawn).
Done: the hunter, the protector (its cheek lamps are painted in the fire's reserved coal colours, so the fire mask lights
them with the engine), the robot: gold in its own fixed shades (never painted), its visor glass over the front, half the
top and the sides' front, stepping round the ear plates; instead of the visor's light it shows eyes-only faces
(`frame_helmet_art.py ROBOT_FACES` -> `power_frame_glow_robot_<face>` by `export-frame.py`; `entity/SuitFace` picks one,
`SuitGlowLayer` draws it opaque in the visor's colour). `runAutopilotStyles` ends with `RobotFaceScene`. The notes below are the big suit's.

### The big suit

- Animation playback rates follow the real speed along the legs so the feet don't slide (backing up plays the walk in
  reverse, `walk_back`). The authored ground speeds were measured in Blockbench: walk 2.218, run 6.249 blocks/s; the game
  walks at 3.0 (the walk steps 1.35x faster) and sprints at 6.25. Tap sprint once: it keeps going while W is held.
- The walk and run keep the tool arm stabilized (IK on the arm), so it stays steady in the cockpit view.
- Cockpit feel: the view stays level (no camera bob); the FOV widens a little with speed, and the viewmodel sways with the
  gait under vanilla's View Bobbing option.
- Terrain: walking off ledges up to 2 blocks steps down instead of falling (keeps speed, no fall
  pose), and step-ups/downs are eased for the camera and the model over ~6 ticks.
- Saved suits: Minecraft stores attribute base values with each entity. `readAdditionalSaveData`
  resets them to the current tuning (`BASE_STATS`), so suits placed with older versions get new speeds.
  If you change `SuitDriving.WALK_BLOCKS_PER_SECOND` / `SPRINT_MULTIPLIER`, the rates follow automatically.
- Jumping: holding Space plays `jump_charge` (crouch); release plays `jump` (push-off) and the suit
  launches 2 ticks later, then `fall` loops; `land` plays after ~0.5 s in the air. Other players
  see the jump via a synced counter bumped by the server.
- Turning: legs (`yBodyRot`) follow the direction of travel; the torso (with arms and tool) twists
  up to 90 degrees and leans to face where the pilot looks (`PowerSuitRenderer.adjustModelBonesForRender`).
- First person: the eye sits at the visor (0.55 forward), the head/torso/hip shell is hidden and the
  suit is drawn with back-face culling, so no insides of cubes show.
- Animation sources (procedural specs) live in `model/anim/`.
- Power: `shutdown` (slump, hold) when the fuel runs out, `powered_off` (its last frame) for suits that were
  already off when they came into view, `startup` (1.4 s, movement blocked meanwhile) when fuel returns.
  The torso stops following the view while powered down. Spec: `model/anim/a_power.js`.
- Socket: the left arm ends in an elbow socket and the installed tool is the forearm, carried at the hip (rest pose:
  upper arm 18 deg forward, elbow 62 deg); `socket` (coupling plate) shows when empty, the installed
  tool's bone (`chaingun`, `em_projector`, `drill`, `chainsaw`) otherwise (`PowerSuitRenderer`). The EM push plays `tool_recoil` (0.5 s overlay, `a_tool_recoil.js`); the chaingun's barrels spin and its shots kick in code (`ToolRotors`, `PowerSuitRenderer`), and `tool_recoil`
  is triggered per shot; it must stay shorter than the cooldown because GeckoLib won't restart a running one.
- Mining tools: while a continuous tool runs, the suit syncs `TOOL_RUNNING` and a fourth controller (`tool`)
  loops the tool's own animation: `drill_run` spins the `drill_bit` 4 turns/s and buzzes the head,
  `chainsaw_run` shimmers the chain (`a_tools.js`). They key only the tool bones, so the arm keeps following
  walk/run and the aim.
- Right hand: `right_hand` grip bone (replaced the grenade prop) and a GeckoLib controller (`right_hand`) that owns the
  right arm while you hold something; `use_item` is triggered on every swing of the pilot's arm (`a_hand.js`).
- Arms swapped (2026-10-13): the hand used to be on the left and the tools on the right. The swap mirrored the
  whole model across x = 0 in Blockbench (geometry, rest poses, every keyframe, left/right names), so every
  animation stayed consistent (the gait now leads with the other foot). The specs in `model/anim/` are
  still written for the old rig; its `kit.json` makes the bake tools mirror them onto the new one.
- Unused animations so far: attack (3-round burst), idle_fidget (throw, stim and sneakwalk were removed 2026-10-18).
