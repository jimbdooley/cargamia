def _edge_numbers(shape, edges_or_numbers):
    """Convert a mix of 1-based edge numbers and Part.Edge objects
    into a list of 1-based edge numbers for `shape`."""
    nums = []
    for item in edges_or_numbers:
        if isinstance(item, int):
            nums.append(item)
            continue
        for i, e in enumerate(shape.Edges, start=1):
            if e.isSame(item):
                nums.append(i)
                break
        else:
            raise ValueError("Edge is not part of the given shape")
    return sorted(set(nums))   # drop duplicates


def bulk_fillet(doc, shape, radius, edges, radius2=None):
    """
    Fillet several edges of `shape` in one operation using Part::Fillet.

    `edges` is a list of 1-based edge numbers (GUI "Edge29" naming,
    i.e. shape.Edges[28]), Part.Edge objects belonging to `shape`,
    or a mix of both.
    Returns a new, document-independent Part.Shape.
    """
    if radius2 is None:
        radius2 = radius

    edge_numbers = _edge_numbers(shape, edges)
    if not edge_numbers:
        print(f"bulk_fillet: no edges given (radius {radius}), shape unchanged")
        return shape.copy()

    src = doc.addObject("Part::Feature", "_bf_src")
    src.Shape = shape
    fil = doc.addObject("Part::Fillet", "_bf_fillet")
    try:
        fil.Base = src
        fil.Edges = [(n, radius, radius2) for n in edge_numbers]
        doc.recompute()
        if not fil.isValid() or fil.Shape.isNull():
            msg = "invalid fillet" if not fil.isValid() else "null fillet"
            raise RuntimeError(
                f"bulk_fillet failed for edges {edge_numbers} (radius {radius}): {msg}"
            )
        return fil.Shape.copy()
    finally:
        doc.removeObject(fil.Name)   # fillet first, then its base
        doc.removeObject(src.Name)