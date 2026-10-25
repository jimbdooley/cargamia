import numpy as np
import trimesh

def generate_mold_halves(input_stl_loc, input_stl_name, margin=10.0):
    """
    Converts a watertight STL part into two matching mold halves.
    
    :param input_stl_loc: Directory containing the source .stl file
    :param input_stl_name: Name of the source .stl file
    :param margin: Padding (in mm) around the part to form the mold walls
    """
    # 1. Load the target mesh and verify it's closed
    part = trimesh.load(input_stl_loc + input_stl_name)
    if not part.is_watertight:
        print("Warning: Input mesh is not watertight. Booleans may fail.")
    
    # Center the part at origin for predictable splitting
    part.vertices -= part.center_mass
    
    # 2. Compute bounding dimensions
    bounds = part.bounds
    extents = part.extents
    
    # 3. Create the outer mold enclosure block
    mold_size = extents + (margin * 2.0)
    mold_block = trimesh.creation.box(extents=mold_size)
    
    # 4. Carve the cavity (Block minus Part)
    # Uses the configured engine (e.g., 'manifold' or 'scad') for manifold evaluation
    print("Carving out the mold cavity...")
    cavity_block = mold_block.difference(part, engine='manifold')
    
    # 5. Define cutting volumes for the Top and Bottom halves at Z = 0
    # Make cutting blocks large enough to guarantee complete clipping
    cut_box_size = mold_size * 2.0 
    
    # Extract only the Z height component for the vertical translations
    z_shift = cut_box_size[2] / 2.0
    
    top_cutting_box = trimesh.creation.box(
        extents=cut_box_size, 
        transform=trimesh.transformations.translation_matrix([0, 0, z_shift])
    )
    bottom_cutting_box = trimesh.creation.box(
        extents=cut_box_size, 
        transform=trimesh.transformations.translation_matrix([0, 0, -z_shift])
    )
    
    # 6. Intersect the carved block with the cutting volumes to get distinct halves
    print("Splitting mold into halves...")
    mold_top = cavity_block.intersection(top_cutting_box, engine='manifold')
    mold_bottom = cavity_block.intersection(bottom_cutting_box, engine='manifold')
    
    # 7. Export files
    mold_top.export(input_stl_loc + input_stl_name[:-4] + "top.stl")
    mold_bottom.export(input_stl_loc + input_stl_name[:-4] + "bottom.stl")
    print(f"Success! '{input_stl_name[:-4]}top.stl' and '{input_stl_name[:-4]}bottom.stl' have been generated.")

# Example Usage:
generate_mold_halves('C:\\Users\\james\\Desktop\\misc_geo\\', "octo_v2_in_prog.stl", margin=15.0)
