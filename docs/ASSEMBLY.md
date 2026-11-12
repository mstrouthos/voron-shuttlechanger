# Assembly, Klipper and audit notes (v32.1)

For the illustrated, step-by-step build (inserts, opener, dock shafts and set-up), see [ASSEMBLY_GUIDE.md](ASSEMBLY_GUIDE.md).

Stock CW2 + LDO-36 · pull rod and spring set the idler tension · a Ø5 shaft at each dock opens the idler (no servo) · tool on 2 Ø3 pins + magnets · dock: 2 Ø3 pins enter 2 holes in the tool at the end of a 14 mm X shift · 63 mm dock pitch.

All parts are in print orientation as single watertight bodies and need no supports (`print_audit.json`). `layer_audit.json` checks this layer by layer, the way a slicer would: nothing starts in mid-air, bridges stay under 10 mm and one-sided lips under 3 mm. `fits.json` lists every pin, pivot, press and screw fit with its clearance. The body is stock Voron geometry and keeps Voron's own bridges.

## Setup
1. Guidler A + mast: prints flat like the stock part, mast and ring included, no supports. The mast rises on the left of the CW2 body-to-plate screw to a block with a slot for the pull rod, and ends in a ring (6.6 × 12.6 mm inside) whose top is 17 mm above the motor plate. The v29 Ø4.4 arm hole and the stock spring pocket are not used.
2. Motor plate: press the 5 M3×5×4 inserts in (see the guide), the stock CW2 ones. Leave out the two upper-left CW2 rear screws (as in v29). The block that stands up from the front face near the top is the spring anchor.
3. Pull rod, from the left: M3x60 + washer through the mast slot, then through the slot in the plate's anchor. Then a washer, the 0.7 × 6 × 40 spring, a washer and the tension nyloc. The spring's free end stops 2 mm short of the rod end, so the washer and nut start with almost no squeeze.
4. Tension: turn the tension nyloc. Tighter = more grip. The reference is about **28.5 mm** of spring between the washers, about 13.6 N at the rod with a 1.2 N/mm spring. That is the same idler force as before. Spring rates vary between makers, so treat 28.5 mm as a start and set it by grip.
5. Check by hand: push the ring to the left. The idler must swing open about 11° (the ring moves about 13 mm) and snap back when you let go. The rod swings down about 12° in the anchor slot as it opens.
6. Head onto the Tap: the whole head (CW2, motor, pull rod) is built on the bench. The 2 **M3x10** plate-to-Tap screws must be dropped into the plate's lower counterbores before the CW2 body goes on, tips flush with the back of the plate. With the head against the Tap front, push them home and tighten them with a 2.5 mm hex key through the round holes low in the body front.
7. Receiver: press the Ø3x30 dowels through until 23 mm stick out at the front. Put 2 magnets in each pocket. Screw it to the receiver frame with 2x **M3x6** (they self-tap into Ø2.5 holes).
8. Tool magnets: **1 per pocket**. Orient them so the pairs attract.
9. Tool: put the shroud under the tool top and bolt the heatsink up through both with 4x **M2.5x10**. Press the Ø3x12 pivot pin through the tool top's front into the guide lever (the lever must swing freely). Push the spool's 4x2 PTFE 6 mm into the socket at the lever top.
10. Receiver frame: bolt it to the CNC Tap with 2x M3x20 and the posts to the CW2 front with 2x **M3x10**. Those two screws go through the holes in the body's front face into M3 inserts pressed in from the back of the body, as on a stock CW2. Put inserts in the duct legs and bolt them under the frame wings with 2x M3x10.
11. Dock: press 2x **Ø3x15 dowels** into the holes in the dock face so 7 mm stick out, then bolt it on with 2x **M5x10 SHCS** into drop-in T-nuts. Set the toolchange Z in your macro so the pins line up with the two Ø3.2 holes in the tool's front-left block (the hole lead-ins catch ±0.8 mm).
12. Shaft post: bolt one to the **top slot** of the rail beside each dock with 2x **M5x10 SHCS** into drop-in T-nuts, foot flush with the rail's front and back faces. Push the **Ø5x100 shaft** through its bore from the front until the tip is **80 mm behind the rail**, and pinch it with the **M3x16** in the top (it self-taps below the slit). Slide the post until the gap between the shaft and the dock's left face (the face the two pins stick out of) is **37.3 mm**. Sliding it right opens the idler less, left opens it more. The shaft's underside is 2.3 mm above the motor plate, and the ring gives 0.9 mm of height either way: jog the head in slowly the first time.
13. Wires: run the heater, thermistor and fan wires up the outside of the shroud's left side to the left edge of the tool top. Lay them on the outer face of the wire column at the front-left. Thread 2 zip ties (≤3.6 mm wide) front-to-back through its slots and around the bundle. Put the tie heads on the front or outer face, never at the back: the back of the column is only 1.5 mm from the receiver frame.

## Klipper
The opener needs no config: there is no servo. It is worked by the tool-change moves. "X−14" is 14.1 mm left of the dock position.

- **Drop:** Y safe at X−14 → Y dock → X dock (slow; the last 7 mm slide the tool onto the dock pins, the last 1.7 mm tilt the guide lever) → Y out 36 mm → X−14 → Y safe.
- **Pickup:** Y safe at X−14 → Y in to 36 mm out → X dock → Y dock (slow) → X−14 (slow) → Y safe.

Y safe must be at least **50 mm** behind the dock position: the ring leaves the shaft tip 42 mm out.

What the shaft does during those moves:
- **Y in, at X−14:** the ring slides onto the shaft with 0.8 mm of room each side. The idler stays closed.
- **X shift to the dock:** after 0.8 mm the shaft meets the ring's left wall and holds it back. At the dock the ring is 13.3 mm back and the idler 11.4° open. At 1.7 mm before the end, where the dock starts to tilt the guide lever, it is already 10.1° open (2.3 mm at the idler).
- **Y moves at X dock:** the ring slides along the shaft and the idler stays fully open, so the gears pass the filament freely.
- **X shift back to X−14:** the spring closes the idler as the head moves. With the tool left in the dock this is done 36 mm out; with a new tool on the head it is done at the dock, and the same move slides the tool off the dock pins.

Always shift back to X−14 before moving out past 42 mm. If the ring leaves the shaft while the idler is open, it snaps shut from fully open. The empty head runs with the idler closed.

## Structural audit
- `screw_audit.json`: every screw's path through the printed parts, with the smallest clear radius in each part. Each part comes out as clearance, tapped/self-tapping, or blocked; none is blocked.
- `struct_audit.json`: wall-thickness scan of every STL by inward ray casting. It flags regions under 1.2 mm.
- `load_cases.json`: hand load cases. Allowables are 20 MPa along layers and 8 MPa across layers. All cases pass. The closest to its limit is the Guidler A mast root with a jammed guidler (18.6 of 20 MPa).

v32 opener (parts 02, 05 and 14):
- **Opener sweep:** Guidler A, the idler and the pull-rod hardware from closed to 11.4° open, against the body, the plate, all hardware, the LDO-36, the tool, the lever and the PTFE. What remains is the stock guidler and idler hardware, which the model holds still, and the 0.1 mm the stock guidler touches the plate's pivot boss.
- **Tool-change sweep:** the full drop sequence in 0.5 to 1 mm steps (in at X−14, shift to the dock, out 36 mm, shift back, leave), with the idler angle the shaft gives at each step, the shaft and post in place, and the shafts, posts and docked tools of both neighbouring docks. Pickup is the same path in reverse. Clean, apart from the dock pushing the guide lever and the shaft touching the ring wall, which is how it works.
- **Loads:** the shaft pushes the ring with 11 N at first contact and 20.9 N fully open; the rod force goes from 13.6 to 25.8 N. A jammed guidler with the gantry stalling at an assumed 60 N puts 18.6 MPa in the mast root (limit 20 along the layers). The shaft bends 0.09 mm with the head docked and 0.52 mm with the head 36 mm out, where the idler is opened for a pickup.
- **Wall thickness and gaps:** the new geometry adds no regions under 1.2 mm. The flagged regions left in 02 and 05 are stock geometry already in the earlier reports. The 02, 05 and 14 entries are marked `"scan": "v32"`.

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
- the 1.7 mm strip of the plate's spring anchor in front of the rod slot (11 mm tall, backed by the ridge; the washer bears on it and on the 4.7 mm strip behind the slot)

## Version history
- **v32.1** — the printed trip arm is replaced by a **Ø5 × 100 mm steel shaft**, and the finger on Guidler A by a **ring** that slides onto it. Reprint 02; print the new 14 (shaft post) instead of the trip arm.
  - **Why:** with the head docked the steel shaft bends 0.09 mm, where the printed bar bent about 0.4. It needs no ramp, and the ring can't slip off it sideways.
  - **Guidler A (02):** the mast ends in a ring, 6.6 × 12.6 mm inside, with a 1.2 mm lead-in at the front. The shaft slides 5.8 mm up the ring's left wall as the idler opens, which is why the ring is tall.
  - **Shaft post (14):** a tower on the rail's top slot with a Ø5.1 bore, a slit and an M3×16 pinch screw. Still 2× M5×10 into T-nuts.
  - **Moves:** a straight shaft can't open the idler while the head moves in Y, so the head now makes the whole opening with a sideways shift. It comes in 14.1 mm left of the dock (was 9) and shifts right to open. To close, it shifts back left: 36 mm out after a drop, at the dock after a pickup. Y safe goes from 35 to 50 mm.
  - **Motor plate (05):** the anchor gusset is 1 mm shorter to clear the ring.
  - **Checks:** opener sweep, tool-change sweep with the new sequence and both neighbouring docks, layer check and load cases, all redone. Not printed.
- **v32.0** — the opener no longer has a servo: a trip arm at each dock opens the idler, the way Lineux Hotswap does it. Reprint 02 and 05, print one new 14 per dock. Parts 03, 04 and 06 are gone.
  - **Removed:** servo, crank, trunnion, servo bracket, 2 plate inserts, 2 M3×12, 2 of the 3 nylocs, the servo wiring and the Klipper servo section.
  - **Guidler A (02):** the mast ends in a finger that stands 15.5 mm above the motor plate. The column is 8.1 mm thick (was 5.6). The rod slot is 4.6 mm tall instead of 9.2, because the rod now turns with the mast.
  - **Motor plate (05):** a fixed anchor for the spring stands up from the front face, with a slot for the rod and a rounded ridge for the washer to rock on. The crank bore, recess, stop pocket and the 2 bracket inserts are gone, the unused CW2 latch-insert hole is closed, and the top is back down to z 132.
  - **Trip arm (14, new):** a tower on the top slot of the dock rail with a bar that reaches back over the head. The bar's left face holds the finger back; its tip is ramped at 35° so the idler opens and closes gradually as the head moves in Y.
  - **Spring:** a 0.7 × 6 × 40 mm compression spring (about 1.2 N/mm) replaces the BMG thumbscrew spring. Opening the idler now squeezes the spring a further 10 mm, and the 13 mm BMG spring goes solid long before that. The rod is an M3×60.
  - **Why not the stock spring:** the CW2 idler pivots only 13 mm from the gear, so it has to swing 11° to open 2.6 mm. Lineux's idler lever pivots further away and needs much less travel.
  - **Checks:** opener sweep and tool-change sweep with the arm and both neighbouring docks, both clean; layer check OK for 02 and 14, and for 05 apart from the 5 mm roof of the rod slot; load cases added for the mast, the anchor and the arm.
  - **Layer audit tool:** it now slices with manifold3d. The trimesh slicer dropped loops on some meshes and reported overhangs that aren't there. All 15 earlier results are unchanged.
  - **Not done:** nothing is printed or tried on a printer. The stall force of the gantry (60 N) is an assumption.
- **v31.0** — full audit of every part, with two new checks, and the fixes it led to. Reprint 04, 07, 08, 10, 10b, 11 or 12, and 13.
  - **New check, layer by layer** (`audit/layer_audit.json`): the old print audit only failed wide flat ceilings, so it passed features that start in mid-air. The new one slices each STL at 0.2 mm and classifies everything with nothing under it as an island, a bridge or a one-sided lip.
  - **New check, fits** (`audit/fits.json`): every pin, pivot, press and screw fit, measured from the models. Sliding and pivot fits now have at least 0.15 mm per side; several had 0.04 to 0.07, which binds once printed.
  - **Shrouds 11 and 12** failed the layer check: the 40 mm fan wall and the two funnel wings started in mid-air beside the lip, and the floor behind the heatsink was a 22 mm bridge. The wall and wings now start on the bed, and the floor has 45° gussets with an 8 mm flat. The parts fit the same way.
  - **Tool top 10:** head-pin bores Ø3.08 → Ø3.3; dock-pin bores Ø3.14 → Ø3.4 with teardrop roofs and a wider lead-in; lever-pivot press bore Ø2.88 → Ø3.0.
  - **Guide lever 10b:** pivot bore Ø3.14 → Ø3.3; PTFE socket Ø4.03 → Ø4.15; the foot is relieved round two M2.5 screw heads it overlapped by 0.15 mm.
  - **Receiver 07 and dock 13:** dowel press bores Ø2.94 / Ø2.88 → Ø3.0.
  - **Receiver frame 08:** receiver-screw holes Ø3.06 → Ø3.4 with Ø6.0 head recesses; the head pockets for the two M3×20 Tap screws are Ø6.1 (the left one was 0.28 mm narrower than the head).
  - **Crank 04:** trunnion bore Ø7.15 → Ø7.3 (0.2 mm per side).
  - **Tool-change collision sweep** (new): approach, the 9 mm shift onto the dock pins and the back-out, in 0.5 mm steps. Clean, apart from the dock pushing the lever, which is how it works.
  - **Viewer:** a leftover screw head inside the plate beside the crank is removed.
  - **Not changed:** the body's bridges and lips are in every earlier body and are stock CW2 features. Guidler A's rod-slot roof is a 9.2 mm bridge. The duct's outlet lips taper to a feather that lies on the bed. Guidler A touches the plate's pivot boss by 0.1 mm in the model, as the stock part does.
- **v30.11** — the trunnion joint is redesigned for printing. Reprint 03 and 04.
  - The screw (v30.8) and the bayonet (v30.9 and v30.10) both needed tiny features: a thin spigot, 1 mm lugs, notches and stepped counterbores. Those don't print reliably at this size.
  - Trunnion: now just the 7×7 block and a plain **Ø6.9 boss, 4.3 mm long**, printed standing on the block. There is nothing thin, no lugs and no pilot hole.
  - Crank: a plain **Ø7.15 through bore**, 4.1 long, with a lead-in at the front. The web, notches and counterbore are gone.
  - Retention: once the pull rod is fitted, the trunnion can slide forward at most 2.2 mm (the rod tilts up to 3.3° in the 3.4 mm mast slot, plus hole clearance). With 4.0 mm engaged, 1.8 mm always stays in the bore. The bearing is also 3× longer than before, so the trunnion wobbles much less.
  - Spline socket unchanged from v30.10 (Ø4.9 with a lead-in chamfer). Full-sweep collision check unchanged.
- **v30.10** — stronger bayonet and a looser spline. Reprint 03 and 04.
  - Trunnion: the lugs are now 70° wide (was 50°), reach Ø6.9 (was Ø6.0) and are 1.5 mm thick (was 1.25). They overlap the crank web by 1.0 mm instead of 0.5, so normal print tolerance can't let them slip past. Root bending at 10 N is about 2.7 MPa.
  - Crank: notches 80° wide, counterbore Ø7.4. The spline socket goes from Ø4.75 to **Ø4.9**, with a 0.6 mm lead-in chamfer: the Ø4.75 socket was far too tight to push onto the servo.
  - Released only between +102° and +110°, as before; the full-sweep collision check is unchanged.
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
