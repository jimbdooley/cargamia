import FreeCAD as App
import Part

V = App.Vector


def make_octagon(majorDim, height, minorDim, center=True, name=None):
    """
    Square of side majorDim with its corners cut at 45 degrees, extruded
    by height along +Z.

    majorDim  side length of the starting square (overall width/depth)
    height    extrusion height (Z)
    minorDim  length of each remaining orthogonal (flat) side, 0 < minorDim <= majorDim
              (minorDim == majorDim leaves a plain square)
    center    True: centered on the origin in XY. False: corner at the origin.
    name      if given, the result is added to the active document

    The 45 degree cuts are each (majorDim - minorDim) / 2 long on both legs.
    For a regular octagon, use minorDim = majorDim / (1 + sqrt(2)).
    """
    M, m = float(majorDim), float(minorDim)
    if min(M, m, height) <= 0:
        raise ValueError("majorDim, minorDim and height must be positive")
    if m > M:
        raise ValueError("minorDim must be <= majorDim")

    c = (M - m) / 2.0          # leg of each corner cut
    o = -M / 2.0 if center else 0.0

    if c == 0:
        pts = [(0, 0), (M, 0), (M, M), (0, M)]
    else:
        pts = [(c, 0), (M - c, 0), (M, c), (M, M - c),
               (M - c, M), (c, M), (0, M - c), (0, c)]

    verts = [V(x + o, y + o, 0) for x, y in pts]
    wire = Part.makePolygon(verts + [verts[0]])
    solid = Part.Face(wire).extrude(V(0, 0, height))

    if name:
        doc = App.ActiveDocument or App.newDocument()
        Part.show(solid, name)
        doc.recompute()

    return solid


# Example: 20 mm square, 5 mm tall, 8 mm flats
oct_shape = make_octagon(majorDim=20, height=5, minorDim=8, name="Octagon")