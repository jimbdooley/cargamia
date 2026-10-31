import math
import FreeCAD as App
import Part
from FreeCAD import Vector as V
from my_utils.line_circle_bottom_intersect import line_circle_bottom_intersections


def make_warcle_beam(length, w, h, botRad, slope):
    """
    Warcle beam: round bottom (radius botRad, touching z=0), sloped sides, flat top
    of width w at height h. Centered on x=0, runs along +Y from y=0 to y=length.
    """
    ps = line_circle_bottom_intersections(botRad, (0.5 * w, h), 1 / slope)
    if len(ps) == 2 and math.hypot(ps[0][0] - ps[1][0], ps[0][1] - ps[1][1]) < 1e-6:
        ps = ps[:1]
    if len(ps) != 1:
        raise ValueError("Expected exactly one intersection point, got {}".format(len(ps)))
    px, pz = ps[0]

    # Cylinder along Y, center at z = botRad so the bottom touches z = 0
    beam = Part.makeCylinder(botRad, length, V(0, 0, botRad), V(0, 1, 0))

    # Cut off everything above the tangent height
    cutDim = 3 * (w + botRad + length)
    cutter = Part.makeBox(cutDim, cutDim, cutDim)
    cutter.translate(V(-0.5 * cutDim, -0.5 * cutDim, pz))
    beam = beam.cut(cutter)

    # Wedge: FreeCAD wedges have their "height" along Y, so build it with
    # x = width, y = height, z = length, then rotate Y->Z.
    # makeWedge(xmin, ymin, zmin, z2min, x2min, xmax, ymax, zmax, z2max, x2max)
    wedge = Part.makeWedge(-px, 0, 0, 0, -0.5 * w,
                           px, h - pz, length, length, 0.5 * w)
    wedge.rotate(V(0, 0, 0), V(1, 0, 0), 90)     # y -> z, z -> -y
    wedge.translate(V(0, length, pz))            # put length back on 0..+length, lift to pz
    beam = beam.fuse(wedge)
    beam.Placement.Base = V(0, -0.5 * length, 0)
    return beam


if __name__ == "__main__":
    doc = App.ActiveDocument or App.newDocument("Beam")
    beam = make_warcle_beam(length=100, w=30, h=20, botRad=8, slope=2)
    print(beam.BoundBox, beam.isValid())
    Part.show(beam)