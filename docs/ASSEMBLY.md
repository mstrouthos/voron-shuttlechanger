# Design notes (v36)

For the build steps see [ASSEMBLY_GUIDE.md](ASSEMBLY_GUIDE.md). This page records how the head is laid out, what the tool change does, what was checked, and how the design got here.

Left and right are as you face the printer. Positions are in millimetres from the filament line (x right, y back, z up), with the Tap's front face 22.5 mm behind the filament.

## Layout
- **Back plate:** three prints. The body bolts to the Tap with its four M3 holes and carries the lower coupling grooves and the duct ears. The front slab carries the motor (which passes through a window in the body), the dual-gear pocket, the arm pivot and the spring boss. The coupling plate covers the dual gear and carries the top groove and magnets.
- **Gears:** the two HGX gears are 18.8 mm apart, 74 mm above the hotend's mounting face. The fixed gear is on the right, its axle held by the gear housing in front and the coupling plate and slab behind. The idler is on the swing arm on the left, between two webs.
- **Reduction:** motor pinion 10 → dual gear 44/17 → fixed gear 37, about 9.6 : 1.
- **Swing arm:** pivots on a Ø3 pin 18 mm above the idler. The spring pushes its top 19.5 mm above the pivot; the dock pin pushes a screw at its foot 32 mm below.
- **Coupling:** balls at the top centre and at the two lower corners of the tool. Top groove vertical, lower grooves aimed at the centre of the triangle. Magnets leave a 0.3 mm gap.
- **Motor:** above the Tap, where the CW2 motor sits, turned so its upper screw clears the spring boss.
- **SB2209:** right side, upright, 17 mm further out than on a CW2 and 3 mm lower, on two spacers.

## Tool change
The dock position is where both hook screws pass through the large holes.

1. In from 30 mm behind the dock.
2. Shift 3 mm right. The hooks slide into the slots. The dock pin pushes the arm's foot: the idler opens 1.5 mm.
3. Out 30 mm, still shifted. The magnets let go, the gears slide off the filament along their axles, and the arm closes once its foot has passed the pin's tip.
4. Shift back.

Pickup is the same in reverse. The pin's rounded tip opens the arm as the head comes in.

The head must stay shifted until it is 30 mm out. If it shifts back sooner, the cooling duct catches the heater block of a parked Dragon.

## Forces
With the grip set to 40 N: spring 37 N closed and 47 N open; push on the dock pin 22 N to 29 N. The forces scale with the grip.

## Checks
All on the model.
- **Collisions** (`model/sweep36.py`): tool on the head, the full arm swing, and a release and pickup with a parked tool and dock on each side.
- **Printability** (`audit/layer_audit.json`): layer by layer, as a slicer sees it. No islands; largest bridge 2.1 mm; largest one-sided lip 1.8 mm.
- **Walls** (`audit/struct_audit.json`): ray scan for walls under 1.2 mm. Left thin on purpose: the 0.8 to 1.0 mm floors behind the top magnets and groove in the coupling plate, and 45° chamfer edges.
- **Loads** (`audit/load_cases.json`): hand calculations against 20 MPa along the layers, 8 MPa across and 10 MPa bearing. Closest: the dock's pin block at 7.5 of 8 MPa if the gantry stalls against a jammed arm.

## History
- **v36:** v35 mirrored. Swing arm on the left like a CW2 idler arm; SB2209 on the right side in its CW2 orientation; the bracket over the motor removed.
- **v35:** HGX gears again, reshaped to print without supports. Back plate split in three; cover turned into a gear housing; swing arm thickened; one-piece dock with a nozzle wiper; dock pitch 54 mm; the exit move changed so the duct clears a parked Dragon.
- **v34 (dropped):** the same concept with the stock CW2 gears. The hobbed gear had to hang 12 mm in front of its bearings to leave the filament free, so it was abandoned.
- **v33:** first model of the CxChanger mechanism on the Tap, with HGX gears. Branch `v33-hgx`.
- **v32.4 and earlier:** a stock CW2 with a dock-tripped opener on Guidler A, and before that a servo opener. Branch `redesign-v31` and `main`.
