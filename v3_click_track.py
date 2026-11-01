from my_utils.v2_center_track_utils import get_base_wedge
from my_utils.v2_make_claw import uncover_claw
from my_utils.v2_settings import STGS
from my_utils.simple_cache import get_cached, store_cached
from my_utils.make_s_tube import make_s_tube
from my_utils.v2_get_octo import getOcto_v2
from my_utils.v2_make_claw import make_claw_v2
import FreeCAD as App
import Part
import math
V = App.Vector

for3DPrint = globals().get("__for3DPrint__", False)
docName = "click_track_v3"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    if obj.Name.startswith("ctcache_"):
        continue
    doc.removeObject(obj.Name)

def get_click_track(for3DPrint):
    baseWedge, h, botW, topW = get_base_wedge(1.0)
    return baseWedge

if True:
    baseOcto = get_cached(doc, "ctcache_baseOcto")
    if baseOcto is None:
        print("Generating base octo...")
        baseOcto = getOcto_v2(doc, False, True, True)
        store_cached(doc, "ctcache_baseOcto", baseOcto)
    octoA = baseOcto.Shape.copy()
    octoB = baseOcto.Shape.copy()
    dist = 0.5 * (STGS.gap + STGS.trackSquareTopDim)
    octoA.translate(V(-dist, 0, 0))
    octoB.translate(V(dist, 0, 0.5 * STGS.dz))
rtnPart = get_click_track(for3DPrint)