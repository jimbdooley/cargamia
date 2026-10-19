
CACHE_NAMES = ("cache_sq", "cache_botCut", "cache_midFuse")

def get_cached_shapes(doc):
    objs = [doc.getObject(n) for n in CACHE_NAMES]
    if any(o is None for o in objs):
        return None
    return tuple(o.Shape.copy() for o in objs)

def store_cached_shapes(doc, shapes):
    for name, shape in zip(CACHE_NAMES, shapes):
        obj = doc.getObject(name)
        if obj is None:
            obj = doc.addObject("Part::Feature", name)
        obj.Shape = shape
        if obj.ViewObject:
            obj.ViewObject.Visibility = False
    doc.recompute()

