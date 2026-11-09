# Assembly, Klipper and audit notes (v29)

Stock CW2 + LDO-36 · servo-driven spring shuttle (sets the idler tension and opens it) · tool on 2 Ø4 pins + magnets · dock: 2 Ø3 pins enter 2 holes in the tool during a 9 mm X shift · 63 mm dock pitch.

All parts are in print orientation as single watertight bodies and need no supports (`print_audit.json`). The body is stock Voron geometry and keeps Voron's own bridges.

## Setup
1. Guidler A: stock print plus a Ø4.4 hole along the arm for the tension screw. No insert, no dowel.
2. Motor plate: put inserts in the 2 guide bosses and the bracket hole in the back. Put the shuttle on the rail and hold it with 2x **M3x8 SHCS + DIN 9021 washers** in the bosses.
3. Tension stack, from the left: drop the M3 hex nut into the shuttle's pocket, then thread in the **M3x40 button head** from the left. Add the seat nyloc + washer, the stock spring, the Guidler A arm, then washer + end nyloc. Leave a 3.5 mm gap between the end washer and the arm when it is closed.
4. Tension: turn the M3x40 head. Clockwise adds tension (about 3.8 mm of range). Then reset the end nyloc to a 3.5 mm gap.
5. Crank: press the Ø3x8 dowel in. Centre the servo, then push the crank onto the spline with the pin in the shuttle groove at the closed end. **No horn screw**: the shuttle traps the crank.
6. Fit the servo into the bracket with its own M2 screws. Fix the bracket to the plate back with 2x **M3x6**. Leave out the two upper-left CW2 rear screws.
7. Receiver: press the Ø4x30 dowels through until 23 mm stick out at the front. Put 2 magnets in each pocket. Screw it to the receiver frame with 2x **M3x6** (they self-tap into Ø2.5 holes).
8. Tool magnets: **1 per pocket**. Orient them so the pairs attract.
9. Tool: put the shroud under the tool top and bolt the heatsink up through both with 4x **M2.5x10**. Press the Ø3x12 pivot pin through the tool top's front into the guide lever (the lever must swing freely). Push the spool's 4x2 PTFE 6 mm into the socket at the lever top.
10. Receiver frame: bolt it to the CNC Tap with 2x M3x20 and the posts to the CW2 front with 2x **M3x10**. Put inserts in the duct legs and bolt them under the frame wings with 2x M3x10.
11. Dock: press 2x **Ø3x15 dowels** into the holes in the dock face so 7 mm stick out, then bolt it on with 2x **M5x10 SHCS** into drop-in T-nuts. Set the toolchange Z in your macro so the pins line up with the two Ø3.2 holes in the tool's front-left block (the hole lead-ins catch ±0.8 mm).
12. Wires: run the heater, thermistor and fan wires up the outside of the shroud's left side to the left edge of the tool top. Lay them on the outer face of the wire column at the front-left. Thread 2 zip ties (≤3.6 mm wide) front-to-back through its slots and around the bundle. Put the tie heads on the front or outer face, never at the back: the back of the column is only 1.5 mm from the receiver frame.

## Klipper
```
[servo opener]
pin: <free PWM pin>
maximum_servo_angle: 180
minimum_pulse_width: 0.0005
maximum_pulse_width: 0.0025
```
Opener travel is 102° (dwell, unload the spring, pull the idler open, dwell). It opens the idler about 10–11°. FS90 torque margin is about 1.3–1.5×; an MG90S fits the same bracket if it stalls. Set the closed and open angles on the printer with `SET_SERVO SERVO=opener ANGLE=..`.

Y safe must be at least 30 mm behind the dock position (23 mm of pin engagement).

- **Drop:** Y safe at X−9 → Y dock → servo open → X dock (slow; the last 1.7 mm tilts the guide lever) → Y safe.
- **Pickup:** Y safe at X dock → Y dock (slow, servo open) → X−9 (slow) → servo close → Y safe.

Always open the servo before the X shift into the dock.

## Structural audit
- `struct_audit.json`: wall-thickness scan of every STL by inward ray casting. It flags regions under 1.2 mm.
- `load_cases.json`: hand load cases. Allowables are 20 MPa along layers and 8 MPa across layers. All cases pass. The worst are the dock finger hit sideways (30 N, 6.7 MPa) and the tool-foot root (6.1 MPa).

Fixed in this pass:
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
- **v29** — spring shuttle: the servo now unloads the CW2 spring and pulls the idler open, and closed tension is set with the M3x40. Replaces the cam plate and the old side wall. Guidler A goes back to stock plus one hole. Receiver screws are M3x6 and post screws M3x10 (bolt position matched to the CW2 inserts). The head is about 15 mm wider on the left when closed and about 25 mm when open.
- **v28** — dock: 2 Ø3 steel pins along X into 2 holes in a block on the tool (replaces the T-lug and slot).
- **v27** — filament path Ø3.0 nominal (prints ≈Ø2.7–2.8): lever, tool top and shroud lip; column and body slot widened round it; open U-channel beside the guidler.
- **v26** — gap-free models: no slits, V-notches or crevices; receiver-frame posts rebuilt.
- **v25** — Ø2.4 filament path; printed bore above the gears; 3 mm shroud lip (M2.5x10); thicker receiver-frame posts.
- **v24** — wire column with 2 zip-tie slots on the tool top.
- **v23** — structural pass: dock tower, walls ≥1.6, pin spacing, magnets, load cases.
- **v22** — servo opener, tilting guide lever, 4010 shrouds, dock with X-shift lug.
