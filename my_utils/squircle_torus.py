import math
import FreeCAD as App
import Part
from FreeCAD import Vector


def make_squircle_torus(major_radius, minor_radius, n=4.0,
                        minor_height=None, samples=360,
                        name="SquircleTorus", doc=None):
    """
    Torus whose swept cross-section is a squircle |x/a|^n + |z/b|^n = 1.

    major_radius : distance from the torus axis (Z) to the center of the cross-section
    minor_radius : half-width of the cross-section (the 'a' semi-axis, radial direction)
    n            : squircle exponent (2 = normal torus, larger = squarer, any real > 0)
    minor_height : half-height of the cross-section ('b' semi-axis); defaults to minor_radius
    samples      : points used to fit the cross-section spline
    """
    if major_radius <= minor_radius:
        raise ValueError("major_radius must be larger than minor_radius, "
                         "otherwise the profile crosses the axis.")
    if n <= 0:
        raise ValueError("n must be positive.")

    a = minor_radius
    b = minor_height if minor_height is not None else minor_radius
    doc = doc or App.ActiveDocument or App.newDocument(name)

    # Sample the squircle in polar form: rho(theta) = 1 / (|cos|^n + |sin|^n)^(1/n)
    # This gives well-behaved, evenly angled points (no sign tricks needed, abs handles it).
    pts = []
    for i in range(samples):
        th = 2 * math.pi * i / samples
        c, s = math.cos(th), math.sin(th)
        rho = (abs(c) ** n + abs(s) ** n) ** (-1.0 / n)
        x = major_radius + a * rho * c   # radial direction
        z = b * rho * s                  # axial direction
        pts.append(Vector(x, 0, z))

    # Closed, periodic spline through the points (don't repeat the first point)
    spline = Part.BSplineCurve()
    spline.interpolate(Points=pts, PeriodicFlag=True)

    wire = Part.Wire(spline.toShape())
    face = Part.Face(wire)

    # Revolve the profile 360 degrees about the global Z axis
    solid = face.revolve(Vector(0, 0, 0), Vector(0, 0, 1), 360)

    return solid


# Example usage
if __name__ == "__main__":
    make_squircle_torus(major_radius=30, minor_radius=8, n=4)