def bulk_chamfer(doc, shape, size, edge_numbers, size2=None):
    """
    Chamfer several edges of `shape` in one operation using Part::Chamfer.

    edge_numbers are 1-based, matching the GUI's "Edge29" naming
    (i.e. shape.Edges[28]).
    Returns a new, document-independent Part.Shape.
    """
    size2 = size if size2 is None else size2

    if not edge_numbers:
        print(f"bulk_chamfer: no edges given (size {size}), shape unchanged")
        return shape.copy()
    src = doc.addObject("Part::Feature", "_bc_src")
    src.Shape = shape
    cham = doc.addObject("Part::Chamfer", "_bc_chamfer")
    try:
        cham.Base = src
        cham.Edges = [(n, size, size2) for n in edge_numbers]
        doc.recompute()
        if not cham.isValid() or cham.Shape.isNull():
            er = f"bulk_chamfer failed for edges {list(edge_numbers)} (size {size})"
            raise RuntimeError(er)
        return cham.Shape.copy()
    finally:
        doc.removeObject(cham.Name)   # chamfer first, then its base
        doc.removeObject(src.Name)