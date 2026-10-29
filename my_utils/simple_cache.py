
def get_cached(doc, key):
    rtn = doc.getObject(key)
    return rtn

def store_cached(doc, key, shape):
    obj = doc.getObject(key)
    if obj is None:
        obj = doc.addObject("Part::Feature", key)
    obj.Shape = shape
    if obj.ViewObject:
        obj.ViewObject.Visibility = False
    doc.recompute()