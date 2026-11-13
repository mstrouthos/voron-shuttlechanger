# Model scripts

Working scripts, kept as they were used. They need numpy, trimesh, manifold3d, shapely and vtk.

1. `python extract_old.py` writes `old_parts.pkl`: the meshes reused from v32 (Tap, hotends, shrouds, duct, fans), read from branch `redesign-v31`.
2. `build35.py` builds the parts (arm on the right); `build36.py` mirrors them into the final layout. `build34.py` only supplies helper functions.
3. `sweep36.py` runs the collision checks. `export36.py`, `struct36.py` and `loads36.py` write the STLs and audit files into a `v36/` folder here.
4. `apply36.py` writes the viewer page; `render36.py` renders the pictures.

`export36.py` has an absolute path to `audit/tools`; change it to yours.
