import math
import FreeCAD as App
import Part
from FreeCAD import Vector as V
from my_utils.line_circle_bottom_intersect import line_circle_bottom_intersections

def make_warcle_torus(rad, w, h, botRad, slope, angleUsed=360):

    warcleTorus = Part.makeTorus(rad, botRad, V(0, 0, 0), V(0, 0, 1), 0, 360, angleUsed)
    warcleTorus.Placement.Base = V(0, 0, botRad)
    ps = line_circle_bottom_intersections(botRad, (0.5 * w, h), 1/slope)
    if len(ps) != 1:
        raise ValueError("Expected exactly one intersection point, got {}".format(len(ps)))
    p = ps[0]

    cutDim = 3 * (rad + botRad)
    cutter = Part.makeBox(cutDim, cutDim, cutDim)
    cutter.translate(V(-0.5 * cutDim, -0.5 * cutDim, p[1]))
    warcleTorus = warcleTorus.cut(cutter)

    cone = Part.makeCone(rad + p[0], rad + 0.5 * w, h - p[1], V(0, 0, 0), V(0, 0, 1), angleUsed)
    cone.translate(V(0, 0, p[1]))
    warcleTorus = warcleTorus.fuse(cone)

    iCone = Part.makeCone(rad - p[0], rad - 0.5 * w, h - p[1])
    iCone.translate(V(0, 0, p[1]))
    warcleTorus = warcleTorus.cut(iCone)

    return warcleTorus