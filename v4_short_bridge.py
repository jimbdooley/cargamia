from my_utils.v4_make_bridge import make_bridge_v4
from my_utils.v2_settings import STGS
from my_utils.simple_cache import get_cached, store_cached
from my_utils.v2_get_octo import getOcto_v2
import FreeCAD as App
import Part
import math
V = App.Vector

for3DPrint = globals().get("__for3DPrint__", False)
docName = "short_bridge_v4"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    if not obj.Name.startswith("ctcache_"):
        doc.removeObject(obj.Name)

shortBridgeLen = 0.5 * (STGS.gap - STGS.trackSquareTopDim)
shortBridge = make_bridge_v4(shortBridgeLen)

if False:
    baseOcto = get_cached(doc, "ctcache_baseOcto")
    if baseOcto is None:
        print("Generating base octo...")
        baseOcto = getOcto_v2(doc, False, True, True)
        store_cached(doc, "ctcache_baseOcto", baseOcto)
    octoA = baseOcto.Shape.copy()
    octoB = baseOcto.Shape.copy()
    dist = 0.5 * (STGS.trackSquareTopDim + shortBridgeLen)
    octoA.translate(V(-dist, 0, 0))
    octoB.translate(V(dist, 0, 0))
rtnPart = shortBridge
