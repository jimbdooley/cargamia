from my_utils.v2_dub_right_maker import make_dub_right
from my_utils.simple_cache import get_cached, store_cached
from my_utils.v2_get_octo import getOcto_v2
import FreeCAD as App
import Part
V = App.Vector
import math

useCache = globals().get("__useCache__", False)
for3DPrint = globals().get("__for3DPrint__", False)
docName = "centrack_dub_right_v2"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    if obj.Name.startswith("ctcache_"):
        continue
    doc.removeObject(obj.Name)

dr = make_dub_right(doc)

if False:
    baseOcto = get_cached(doc, "ctcache_baseOcto")
    if baseOcto is None:
        baseOcto = getOcto_v2(doc, False, True, False)
        store_cached(doc, "ctcache_baseOcto", baseOcto)
    octoA = baseOcto.Shape.copy()
    dr = dr.fuse(octoA)

rtnPart = dr