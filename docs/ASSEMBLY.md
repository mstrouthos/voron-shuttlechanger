# Assembly, Klipper and audit notes (v30.9)

For the illustrated, step-by-step build (inserts, opener, SB2209 wiring and Klipper setup), see [ASSEMBLY_GUIDE.md](ASSEMBLY_GUIDE.md).

Stock CW2 + LDO-36 · servo crank and pull rod (sets the idler tension and opens it) · tool on 2 Ø3 pins + magnets · dock: 2 Ø3 pins enter 2 holes in the tool during a 9 mm X shift · 63 mm dock pitch.

All parts are in print orientation as single watertight bodies and need no supports (`print_audit.json`). The body is stock Voron geometry and keeps Voron's own bridges.

## Setup
1. Guidler A + mast: prints flat like the stock part, mast included, no supports. The mast rises on the left of the CW2 body-to-plate screw and ends in a block with a slot for the pull rod. The v29 Ø4.4 arm hole and the stock spring pocket are not used.
2. Motor plate: press the 7 M3×5×4 inserts in (see the guide): 2 in the back face at the top for the servo bracket, plus the 5 stock CW2 ones. Leave out the two upper-left CW2 rear screws (as in v29).
3. Servo: fit it into the bracket with its own 2 M2 tab screws, from the back. Bolt the bracket to the plate back with 2x **M3x12** into the inserts. The spline now sits inside the plate bore.
4. Trunnion (bayonet, no screw): with the crank's arm pointing right, hold the trunnion with its rod hole nearly upright (106° counterclockwise from level, seen from the front) so its 2 lugs line up with the 2 notches in the crank web. Push it in from the front, then turn it clockwise 106° until the rod hole is level. The lugs lock behind the web. In use the trunnion turns 0 to 148° clockwise relative to the crank, so it never comes back to the insert angle (the model shows it only comes free between +102° and +110°).
5. Crank: power the servo (plug it into the SB2209 with the head beside the printer, or use a servo tester) and send it to the closed angle (see Klipper). From the front, put the crank's hub into the plate bore with the stop tab in its pocket and resting on the pocket's closed end. In that position the trunnion points right, 6° below horizontal. Push it onto the spline with firm hand pressure. The socket is Ø4.75 with three relief slits; if it is still too tight, open it with a 4.8 mm drill by hand. There is no horn screw: the trunnion and the rod trap the crank, and its stop tab keeps it in the plate. Turn the trunnion so its flats face left and right.
6. Pull rod, from the left: M3x55 + washer through the mast slot. Then the push nyloc: run it up to the mast's right face and back it off to about 0.2 mm of play. Then the stop nyloc, the trunnion's cross hole, the stock spring, a washer and the tension nyloc.
7. Stop nut: with the crank closed, set a **2.5 mm gap** between the stop nyloc and the trunnion's left flat. That is how far the spring unloads before the idler starts to open.
8. Tension: turn the tension nyloc. Tighter = more grip. The reference is about 10.8 mm of spring between the trunnion and the washer, about 13.5 N at the rod. That gives the same idler force as v29's 20 N at the old screw, because the rod pulls 52 mm from the guidler pivot instead of 35.
9. Head onto the Tap: the whole head (CW2, motor, servo, crank, pull rod) is built on the bench. The 2 **M3x10** plate-to-Tap screws must be dropped into the plate's lower counterbores before the CW2 body goes on, tips flush with the back of the plate. With the head against the Tap front, push them home and tighten them with a 2.5 mm hex key through the round holes low in the body front.
10. Receiver: press the Ø3x30 dowels through until 23 mm stick out at the front. Put 2 magnets in each pocket. Screw it to the receiver frame with 2x **M3x6** (they self-tap into Ø2.5 holes).
11. Tool magnets: **1 per pocket**. Orient them so the pairs attract.
12. Tool: put the shroud under the tool top and bolt the heatsink up through both with 4x **M2.5x10**. Press the Ø3x12 pivot pin through the tool top's front into the guide lever (the lever must swing freely). Push the spool's 4x2 PTFE 6 mm into the socket at the lever top.
13. Receiver frame: bolt it to the CNC Tap with 2x M3x20 and the posts to the CW2 front with 2x **M3x10**. Those two screws go through the holes in the body's front face into M3 inserts pressed in from the back of the body, as on a stock CW2. Put inserts in the duct legs and bolt them under the frame wings with 2x M3x10.
14. Dock: press 2x **Ø3x15 dowels** into the holes in the dock face so 7 mm stick out, then bolt it on with 2x **M5x10 SHCS** into drop-in T-nuts. Set the toolchange Z in your macro so the pins line up with the two Ø3.2 holes in the tool's front-left block (the hole lead-ins catch ±0.8 mm).
15. Wires: run the heater, thermistor and fan wires up the outside of the shroud's left side to the left edge of the tool top. Lay them on the outer face of the wire column at the front-left. Thread 2 zip ties (≤3.6 mm wide) front-to-back through its slots and around the bundle. Put the tie heads on the front or outer face, never at the back: the back of the column is only 1.5 mm from the receiver frame.

## Klipper
```
[servo opener]
pin: <free PWM pin>
maximum_servo_angle: 180
minimum_pulse_width: 0.0005
maximum_pulse_width: 0.0025
```
Opener travel is 166° of crank (closed at 6° past dead centre, open at 160°):
- **0–50°:** the spring unloads.
- **About 50–60°:** slack before the stop nut catches the trunnion.
- **To 166°:** the rod pushes Guidler A open by 11.4°.

The peak load is about 25 N·mm while the spring unloads. An FS90 makes about 150, so an MG90S isn't needed.

Find the closed angle on the printer with `SET_SERVO SERVO=opener ANGLE=..`. It is the angle where the crank tab just rests on its stop. Open is 166° from it. If the crank moves down first, the servo turns the other way: use closed − 166° for open. After each move you can drop the signal (`SET_SERVO SERVO=opener WIDTH=0`). The crank is over centre, so the spring holds it closed, and when open nothing loads it.

Y safe must be at least 30 mm behind the dock position (23 mm of pin engagement).

- **Drop:** Y safe at X−9 → Y dock → servo open → X dock (slow; the last 1.7 mm tilts the guide lever) → Y safe.
- **Pickup:** Y safe at X dock → Y dock (slow, servo open) → X−9 (slow) → servo close → Y safe.

Always open the servo before the X shift into the dock.

## Structural audit
- `screw_audit.json`: every screw's path through the printed parts, with the smallest clear radius in each part. Each part comes out as clearance, tapped/self-tapping, or blocked; none is blocked.
- `struct_audit.json`: wall-thickness scan of every STL by inward ray casting. It flags regions under 1.2 mm.
- `load_cases.json`: hand load cases. Allowables are 20 MPa along layers and 8 MPa across layers. All cases pass. The worst are the dock finger hit sideways (30 N, 6.7 MPa) and the tool-foot root (6.1 MPa).

v30 opener (parts 02–06):
- **Collision sweep:** the whole 166° of crank travel, in 2–4° steps, against the body, the plate, all hardware, the LDO-36, the servo, the tool, the lever and the PTFE. What remains is the servo spline press fit, plus the stock guidler and idler hardware, which the model holds still. v29 shows the same contacts.
- **Pull-rod hardware:** the mast's rod faces are carved to the envelope of the tilting screw head, washer and push nut. The rod tilts up to 21° in mid-stroke.
- **Wall thickness and gaps:** the new geometry adds no regions under 1.2 mm and no slits under 1 mm. The 02–06 entries in the audit JSONs come from a re-implemented scan (marked `"scan": "v30"`), which flags a few more stock regions than the v29 scan did. The flagged regions left in 02 and 05 are stock geometry already in the v29 report. One stock flange at the plate's lower-left corner is now 0.5 mm minimum (was 0.69), because the rail was cut back to the CW2 outline there.

Fixed in v29:
- dock: full-depth tower, front lips 1.95 → 2.95, counterbore walls 0.8 → 2.2 (bolts moved apart), teardrop bolt holes
- tool top:
  - pins moved to x ±11.75. The M2.5 counterbores were 0.13 mm from the pin bores; now 1.5.
  - side walls 2.2
  - rear counterbores open to the front (was a 0.6 skin)
  - the magnet pocket no longer breaks into the counterbore
  - sleeve roof 1.5
  - lug foot 8 → 12 wide
- lever:
  - pivot boss 2.0 walls all round, with the pivot raised 2 mm
  - tube holder 0.57 → 1.6 (1.1 at the very top, where it must lean back to clear the body when tilted)
  - column 0.8 → 1.6 wall on the idler side
- shroud: all duct walls ≥1.6, including the sloped transition (was 0.6)
- receiver: no 0.7 front wall at the inserts (self-tapping holes now), pin holes through
- servo bracket: base 2.0 → 3.9, bosses 1.7 wall, no slivers at the motor flange
- crank: real 1.2 floor in the spline socket
- shuttle: groove, nut pocket and tongue all ≥1.6 walls
- receiver frame: 0.2 mm skin removed
- duct: insert towers 0.3 → 1.5 walls

Model hygiene: every new or modified part passes a narrow-gap scan (`gaps_under_1mm` in `struct_audit.json`): no slits, V-notches or crevices. Fixed: chamfered sleeve/block corners that left V-notches where they joined, a 0.04–0.3 slit under the tool block, a 0.2 slit in the lever, the receiver-frame posts (old head pocket had 0.3 walls) and its 1 mm base slits, the 0.4 slit between the side-wall rail and the motor plate, and a knife edge at the shroud's fan inlet. The 3 gaps left in 01/02/05 are stock Voron geometry.

Accepted (not on a load path):
- the tool magnet-pocket floor (1.0)
- the lever bore skin at the guidler pivot (0.8 on one side; the 4 × 13.7 column section carries the load)
- the 1.2 shroud lip, clamped between the heatsink and the tool top
- the receiver frame's 0.8–1.0 webs, squeezed between the motor plate and the Tap
- the stock CW2 body, plate and guidler features (bridging layers, gear-side wedges)

## Version history
- **v30.9** — the trunnion is held by a **bayonet** instead of a screw. The M3×4 didn't grip in the thin spigot, and the trunnion wobbled. Reprint 03 and 04 again. No hardware is needed.
  - Trunnion: the Ø4.8 spigot is now 2.7 mm long, with 2 lugs (50° wide, out to Ø6.0, 1.25 thick) 120° apart. The screw pilot is gone, so the rod hole is solid all round.
  - Crank: the web hole has 2 matching 60° notches, and the counterbore is Ø6.4, so the lugs turn behind the 1.2 mm web. Axial play is 0.15 mm in total (it was set by the screw head before).
  - The insert angle (+106°) sits in the middle of the 212° the opener never uses, so there is about 50° of margin on each side. Nothing sticks out of the back of the crank, so the 0.35 mm head-to-plate gap of v30.8 is gone. The full-sweep collision check is unchanged.
- **v30.8** — the trunnion is held by an **M3×4 button head** instead of an M2×3 and an M2 washer. Reprint 03 and 04 again.
  - Trunnion: spigot Ø4.8 (was Ø4.0), with a Ø2.5 self-tapping pilot that opens into the rod hole. An M3×4 tip ends 0.4 mm above the rod.
  - Crank: web hole Ø4.95 and counterbore Ø6.2. The Ø5.7 head overlaps the web by 0.37 mm per side and sits on the spigot end, which stands 0.1 mm proud, so it never clamps the crank.
  - The head is 1.65 mm tall and clears the plate recess by 0.35 mm over the whole crank travel. There is no room for a socket head.
- **v30.7** — reprint 03 trunnion and 04 crank.
  - Trunnion: now prints standing on its square end instead of on a flat. The Ø4 spigot, the Ø6.9 journal and the M2 pilot now print as vertical circles, so they come out round. The rod cross hole is a truncated teardrop. Bed contact goes from 26 to 48 mm², and steep overhang from 29 to 9 mm². The journal is Ø6.9 (was Ø7.0), for 0.125 mm per side in the crank bore. The flat chamfers no longer leave zero-thickness slivers at the corners.
  - Crank: the hub is Ø8.6 (was Ø9.0), 0.4 mm per side in the Ø9.4 plate bore (was 0.2), so it turns freely. The spline relief slits are 0.2 mm shorter, which keeps a 0.8 mm skin outside them.
- **v30.6** — assembly order: the whole head is now built on the bench and bolted to the Tap in one piece. The 2 plate-to-Tap M3×10s go into the plate before the CW2 body and are tightened through the body's front holes with a 2.5 mm hex key (checked: Ø3.6 and Ø5.6 clear paths, nothing in the way). The guide now wires the servo first, so the crank can be fitted on the bench, then builds the head, mounts it, adds the tools and docks, and ends with setup. No part geometry changed.
- **v30.5** — tool locating pins changed from Ø4×30 to **Ø3×30** hardened dowels, so the whole build uses one dowel diameter. Receiver (07): press bores Ø3.94 → Ø2.94. Tool top (10): slip bores Ø4.08 → Ø3.08 teardrops, with a new lead-in chamfer at the back face. Ø5 was checked and rejected: the bores sit 3.5 mm from the side walls of both parts, so a Ø5 bore would leave walls under 1 mm. With Ø3 the walls grow to about 2 mm. Reprint 07 and 10 (one 10 per tool); nothing else changes.
- **v30.4** — complete assembly guide. Exploded views of the head and the tool with numbered parts tables, a full hardware list including the stock CW2 drivetrain (BMG gear kit, 2 MR85, LDO-36) and every screw size, and illustrated steps for the CW2 build, the receiver/frame/duct mount, the tools and the docks. The BOM now lists the stock CW2 hardware. No part geometry changed.
- **v30.3** — screw-path audit (`audit/screw_audit.json`). All 34 screws were traced through every printed part they pass. Fixed:
  - Motor plate: v29 had closed three stock holes with 0.4–0.6 mm skins at the back face (the first layers on the bed). These are the right LDO-36 motor screw, the screw clearance behind the lower front-face insert, and the back-face insert pocket for the CW2 body screw, which was sealed. All three are open again, as on the original Voron plate.
  - Motor plate: small reliefs in the bottom edge, because the M3×6 receiver-screw heads hit it by 1 mm. The unused v29 dimple is filled.
  - Both 4010 shrouds (11 and 12): the two upper fan-screw holes were missing. They are now Ø2.7 self-tapping holes, 4.7 mm deep, like the lower ones.
- **v30.2** — one insert size everywhere:
  - All 12 insert holes are now Ø4.7, for the Voron M3×5×4 insert. The plate's 2 servo-bracket holes and the duct's 2 leg holes were Ø4.0.
  - The duct leg towers grew 0.1–0.15 mm so their walls stay at 1.2 mm or more.
  - The unused v29 bracket insert hole in the plate is filled.
  - Illustrated assembly guide added, with SB2209 servo wiring and Klipper setup.
- **v30.1** — fixes from the first look at the parts:
  - CW2 body: the receiver-frame post screws had no way through the front face. A 2 mm skin closed both insert pockets, and the right pocket was only half a hole. Both now have a Ø3.4 front hole, the right one a full Ø4.7 pocket with a small boss.
  - Receiver frame: the left post hole is moved 0.6 mm to line up with its insert, and both Tap-screw holes are opened to Ø3.5.
  - Trunnion: now held in the crank by an M2x3 button head and washer from the back. Before, only the rod kept it in, and the rod could yaw enough to pull it about 1.7 mm out of its 2.6 mm bore.
  - Crank: 1.5 mm thicker and sitting in a shallow recess in the plate, so the trunnion screw fits. The spline socket goes from Ø4.6 to Ø4.75 with three relief slits, because Ø4.6 was too tight.
- **v30** — pull-rod opener. The servo lies flat behind the plate above the LDO-36 and turns a crank in the gap between the CW2 body and the plate. A trunnion on the crank works an M3x55 pull rod that runs from a mast on Guidler A to the stock spring and a tension nyloc. The spring sits inside the head, so nothing slides out to the left any more, and the crank locks over centre when closed. The shuttle, rail, guide screws and servo pocket are gone, and the plate is cut back to the CW2 outline on the left. Left side: 1.9 mm past the CW2 body closed (was 19), 12 mm open (was about 29). The top of the plate is 2.7 mm higher, and the crank reaches 6 mm higher while it passes 90°. Servo travel 166°, idler opening 11.4°.
- **v29** — spring shuttle: the servo now unloads the CW2 spring and pulls the idler open, and closed tension is set with the M3x40. Replaces the cam plate and the old side wall. Guidler A goes back to stock plus one hole. Receiver screws are M3x6 and post screws M3x10 (bolt position matched to the CW2 inserts). The head is about 15 mm wider on the left when closed and about 25 mm when open.
- **v28** — dock: 2 Ø3 steel pins along X into 2 holes in a block on the tool (replaces the T-lug and slot).
- **v27** — filament path Ø3.0 nominal (prints ≈Ø2.7–2.8): lever, tool top and shroud lip; column and body slot widened round it; open U-channel beside the guidler.
- **v26** — gap-free models: no slits, V-notches or crevices; receiver-frame posts rebuilt.
- **v25** — Ø2.4 filament path; printed bore above the gears; 3 mm shroud lip (M2.5x10); thicker receiver-frame posts.
- **v24** — wire column with 2 zip-tie slots on the tool top.
- **v23** — structural pass: dock tower, walls ≥1.6, pin spacing, magnets, load cases.
- **v22** — servo opener, tilting guide lever, 4010 shrouds, dock with X-shift lug.
