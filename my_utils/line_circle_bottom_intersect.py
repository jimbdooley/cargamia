import math

def line_circle_bottom_intersections(radius, point, slope, eps=1e-9):
    """
    Intersect a line with the BOTTOM half of a circle of given radius,
    centered at (0, radius) so its lowest point touches (0, 0).

    radius : circle radius
    point  : (px, py) a point on the line
    slope  : line slope; use None or math.inf for a vertical line

    Returns a list of (x, y) tuples, sorted by x. It holds 0, 1, or 2 points.
    """
    R = radius
    px, py = point

    # Vertical line: x = px
    if slope is None or math.isinf(slope):
        d = R * R - px * px
        if d < -eps:
            return []
        y = R - math.sqrt(max(d, 0.0))   # bottom half is the smaller-y root
        return [(px, y)]

    m = slope
    c = py - m * px                      # line: y = m*x + c

    # x^2 + (m*x + c - R)^2 = R^2  ->  A x^2 + B x + C = 0
    A = 1 + m * m
    B = 2 * m * (c - R)
    C = (c - R) ** 2 - R * R

    disc = B * B - 4 * A * C
    if disc < -eps:
        return []
    sq = math.sqrt(max(disc, 0.0))

    xs = [(-B - sq) / (2 * A)]
    if sq > eps:
        xs.append((-B + sq) / (2 * A))

    pts = []
    for x in xs:
        y = m * x + c
        if y <= R + eps:                 # keep only the bottom half
            pts.append((x, y))
    return sorted(pts)


# Example
if __name__ == "__main__":
    print(line_circle_bottom_intersections(5, (0, 2), 0))        # horizontal line y=2
    print(line_circle_bottom_intersections(5, (-3, 0), 1))       # diagonal
    print(line_circle_bottom_intersections(5, (1, 10), None))    # vertical at x=1