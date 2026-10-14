import FreeCAD as App
import Part


def make_wedge_cen_z_up(
    base_x, base_y, height, top_x, top_y, 
    offset_x=0.0, offset_y=0.0
):
    """
    Wedge with Z as the height axis, sitting on Z=0 and centered in X and Y.

    base_x, base_y : base rectangle size (at Z = 0)
    height         : wedge height along +Z
    top_x, top_y   : top rectangle size (at Z = height); use 0 on one for a sharp edge
    offset_x/y     : shift of the top rectangle relative to the base center
    """
    # Build in makeWedge's native frame (height along Y), with the base centered.
    # A +90 deg rotation about X sends native Y -> Z and native Z -> -Y,
    # so the native Z values are negated to make offset_y behave as expected.
    shape = Part.makeWedge(
        -base_x / 2, 0, -base_y / 2,                  # xmin, ymin, zmin
        -offset_y - top_y / 2, offset_x - top_x / 2,  # z2min, x2min
        base_x / 2, height, base_y / 2,               # xmax, ymax, zmax
        -offset_y + top_y / 2, offset_x + top_x / 2,  # z2max, x2max
    )

    shape = shape.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), 90)

    return shape