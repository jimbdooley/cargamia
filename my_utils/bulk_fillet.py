def bulk_fillet(doc, shape, radius, edge_numbers, radius2=None):
    """
    Fillet several edges of `shape` in one operation using Part::Fillet.

    edge_numbers are 1-based, matching the GUI's "Edge29" naming
    (i.e. shape.Edges[28]).
    Returns a new, document-independent Part.Shape.
    """
    if radius2 is None:
        radius2 = radius

    src = doc.addObject("Part::Feature", "_bf_src")
    src.Shape = shape
    fil = doc.addObject("Part::Fillet", "_bf_fillet")
    try:
        fil.Base = src
        fil.Edges = [(n, radius, radius2) for n in edge_numbers]
        doc.recompute()
        if not fil.isValid() or fil.Shape.isNull():
            raise RuntimeError(
                f"bulk_fillet failed for edges {list(edge_numbers)} (radius {radius})"
            )
        return fil.Shape.copy()
    finally:
        doc.removeObject(fil.Name)   # fillet first, then its base
        doc.removeObject(src.Name)