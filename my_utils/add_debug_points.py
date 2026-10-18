import FreeCAD as App
import Part


def add_debug_points(doc, part, points, radius=0.5, name="DebugPart"):
    """
    Fuse small spheres at `points` (list of (x, y, z)) onto `part` and
    show the result in `doc` with the sphere faces colored red.

    `part` can be a Part.Shape or a document object with a .Shape.
    Returns the fused Part.Shape (geometry only, color lives on the
    document object).
    """
    shape = part.Shape if hasattr(part, "Shape") else part
    if not points:
        print("add_debug_points: no points given, shape unchanged")
        return shape.copy()

    centers = [App.Vector(*p) for p in points]
    spheres = [Part.makeSphere(radius, c) for c in centers]
    fused = shape.fuse(spheres)

    obj = doc.addObject("Part::Feature", name)
    obj.Shape = fused


    doc.recompute()
    rtn = fused.copy()
    doc.removeObject(obj.Name)
    return rtn