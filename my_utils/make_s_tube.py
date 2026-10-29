import FreeCAD as App
import Part
import math
V = App.Vector
def make_s_tube(dx, dz, dStraights, r_out, r_in, bottomToKeep, toFuse):
    """
    bottomToKeep  if given (and < outer diameter), everything more than this
                  distance above the bottom of the outer radius is cut away,
                  following the S-curve. None (or >= 2*r_out) = no cut.
    """
    if min(dx, dStraights, r_out) <= 0:
        raise ValueError("dx, dStraights and r_out must be positive")
    if not 0 <= r_in < r_out:
        raise ValueError("Need 0 <= r_in < r_out")
    if bottomToKeep is not None and bottomToKeep <= 0:
        raise ValueError("bottomToKeep must be positive (or None)")

    # --- path points (XZ plane) ---
    p0 = V(0, 0, 0)
    p1 = V(dStraights, 0, 0)
    p2 = V(dStraights + dx, 0, dz)
    p3 = V(2 * dStraights + dx, 0, dz)

    # --- edges ---
    line1 = Part.LineSegment(p0, p1).toShape()

    h = dx / 2.0   # handle length; gives a smooth symmetric S, tangent to the lines
    bez = Part.BezierCurve()
    bez.setPoles([p1, p1 + V(h, 0, 0), p2 - V(h, 0, 0), p2])
    s_edge = bez.toShape()

    line2 = Part.LineSegment(p2, p3).toShape()
    path = Part.Wire([line1, s_edge, line2])

    # --- sanity check: tightest bend vs tube radius ---
    max_curv = max(bez.curvature(i / 100.0) for i in range(101))
    if max_curv > 0 and 1.0 / max_curv < r_out * 1.2:
        App.Console.PrintWarning(
            f"S-curve minimum bend radius is {1.0 / max_curv:.2f} mm, "
            f"close to or below the tube outer radius ({r_out} mm). "
            f"Increase dx or reduce dz/r_out to avoid pinching.\n")

    # --- sweep helper: profile locked to the Y axis (normal of the XZ plane) ---
    def sweep(profile):
        ps = Part.BRepOffsetAPI.MakePipeShell(path)
        ps.setBiNormalMode(V(0, 1, 0))
        ps.add(profile)
        ps.build()
        ps.makeSolid()
        return ps.shape()

    def circle_profile(radius):
        return Part.Wire(Part.makeCircle(radius, p0, V(1, 0, 0)))

    tube = sweep(circle_profile(r_out))
    for obj in toFuse:
        tube = tube.fuse(obj)
    if r_in > 0:
        tube = tube.cut(sweep(circle_profile(r_in)))

    # --- optional: keep only the bottom slice, following the S-curve ---
    if bottomToKeep is not None and bottomToKeep < 2 * r_out:
        margin = 0.5 * r_out                 # cutter overhang past the tube
        w = r_out + margin                   # half-width of cutter (Y)
        z0 = -r_out + bottomToKeep           # cut line, relative to path centre
        z1 = r_out + margin                  # top of cutter
        cutter_profile = Part.makePolygon([
            V(0, -w, z0), V(0, w, z0), V(0, w, z1), V(0, -w, z1), V(0, -w, z0)
        ])
        tube = tube.cut(sweep(cutter_profile))


    tube = tube.removeSplitter()

    if not tube.isValid():
        App.Console.PrintWarning("Resulting tube is not a valid solid.\n")


    return tube