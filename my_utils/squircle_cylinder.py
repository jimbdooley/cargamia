import math
import FreeCAD as App
import Part
from FreeCAD import Vector


def make_squircle_cylinder(radius, height, n=4.0,
                           pnt=Vector(0, 0, 0), dir=Vector(0, 0, 1),
                           samples=360):
    """
    Like Part.makeCylinder, but the cross-section is a squircle |x/r|^n + |y/r|^n = 1.

    radius  : half-side of the bounding square (the squircle touches it at the
              axis points, same as a circle of this radius would)
    height  : length along dir
    n       : squircle exponent (2 = true cylinder, larger = boxier, any real > 0)
    pnt     : center of the base face
    dir     : axis direction
    samples : points used to fit the cross-section spline

    Returns a Part.Solid (not a document object).
    """
    if radius <= 0 or height <= 0:
        raise ValueError("radius and height must be positive.")
    if n <= 0:
        raise ValueError("n must be positive.")

    pnt = Vector(pnt)
    dir = Vector(dir)
    if dir.Length == 0:
        raise ValueError("dir must be a non-zero vector.")

    # Squircle profile in the XY plane, polar form: rho = (|cos|^n + |sin|^n)^(-1/n)
    pts = []
    for i in range(samples):
        th = 2 * math.pi * i / samples
        c, s = math.cos(th), math.sin(th)
        rho = (abs(c) ** n + abs(s) ** n) ** (-1.0 / n)
        pts.append(Vector(radius * rho * c, radius * rho * s, 0))

    spline = Part.BSplineCurve()
    spline.interpolate(Points=pts, PeriodicFlag=True)

    face = Part.Face(Part.Wire(spline.toShape()))
    solid = face.extrude(Vector(0, 0, height))

    # Orient: rotate +Z onto dir, then move base center to pnt
    rot = App.Rotation(Vector(0, 0, 1), dir)
    solid.Placement = App.Placement(pnt, rot)
    return solid


# Example usage
if __name__ == "__main__":
    doc = App.newDocument("Test")
    s = make_squircle_cylinder(10, 25, n=4, pnt=Vector(5, 0, 0), dir=Vector(0, 1, 1))
    Part.show(s)