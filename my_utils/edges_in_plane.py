import math

def _locate(x, y, poly, tol):
    """Return 1 if (x, y) is strictly inside poly, 0 if on its boundary
    (within tol), -1 if outside. poly is a list of (x, y); a repeated
    closing point is harmless."""
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        # distance from point to segment
        dx, dy = x2 - x1, y2 - y1
        seg_len2 = dx * dx + dy * dy
        if seg_len2 == 0.0:
            d = math.hypot(x - x1, y - y1)
        else:
            t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / seg_len2))
            d = math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))
        if d <= tol:
            return 0

        # ray casting (ray toward +x)
        if (y1 > y) != (y2 > y):
            x_cross = x1 + (y - y1) * dx / dy
            if x < x_cross:
                inside = not inside
    return 1 if inside else -1


def edges_in_plane(shape, z, include, exclude=(), tol=1e-7, steps=25,
                   return_indices=False):
    """
    Return edges of `shape` that lie fully in the plane Z=z (within tol),
    are fully enclosed by ONE include perimeter, and are fully outside
    ALL exclude perimeters.

    include / exclude: lists of perimeters, each a list of (x, y) points.
    Points exactly on a perimeter (within tol) count as enclosed for
    include, and as outside for exclude, so edges lying along a perimeter
    are kept.
    steps: sample points per edge (endpoints included).
    return_indices: return 1-based edge numbers (GUI style, ready for
    bulk_fillet / bulk_chamfer) instead of edge objects.
    """
    result = []
    for idx, e in enumerate(shape.Edges, start=1):
        # cheap prefilter on the endpoints
        if any(abs(v.Point.z - z) > tol for v in e.Vertexes):
            continue

        pts = e.discretize(Number=steps)
        if any(abs(p.z - z) > tol for p in pts):
            continue

        # fully outside every exclude perimeter
        if any(_locate(p.x, p.y, ex, tol) > 0 for p in pts for ex in exclude):
            continue

        # fully inside at least one single include perimeter
        if include and not any(all(_locate(p.x, p.y, inc, tol) >= 0 for p in pts)
                   for inc in include):
            continue

        result.append(idx if return_indices else e)
    return result