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
docName = "s_curve_v2"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    if obj.Name.startswith("ctcache_"):
        continue
    doc.removeObject(obj.Name)

def get_s_bridge(for3DPrint):
    flatDim = 0.5 # portion of s curve that is straight
    cutBuf = 5
    sBridgeDZ = STGS.trackRad + STGS.trackBotZInc
    
    clawA, clawB = make_claw_v2(cutBuf, sBridgeDZ)
    
    bridgeDH = (STGS.trackBotZInc - STGS.trackBotZOut)
    bridgeH = STGS.dz - bridgeDH
    sBridge = make_s_tube(STGS.gap - 2 * flatDim, 
                          bridgeH, 
                          flatDim + cutBuf, 
                        STGS.trackRad + STGS.trackThickness, 
                        STGS.trackRad,
                        STGS.defaultTrackH + STGS.trackThickness,
                        [clawA, clawB])
    sBridge.translate(V(-0.5 * STGS.gap - cutBuf, 0, sBridgeDZ))


    dist = 0.5 * (STGS.gap + STGS.trackSquareTopDim)
    base, _, _, _ = get_base_wedge(2)
    base.scale(1.020)
    base.translate(V(-dist, 0, 0))
    sBridge = sBridge.cut(base)
    base.translate(V(dist * 2, 0, STGS.dz))
    sBridge = sBridge.cut(base)

    sBridge = uncover_claw(doc, sBridge)
    sBridge = sBridge.removeSplitter()
    return sBridge

if False:
    baseOcto = get_cached(doc, "ctcache_baseOcto")
    if baseOcto is None:
        baseOcto = getOcto_v2(doc, False, True)
        store_cached(doc, "ctcache_baseOcto", baseOcto)
    octoA = baseOcto.Shape.copy()
    octoB = baseOcto.Shape.copy()
    dist = 0.5 * (STGS.gap + STGS.trackSquareTopDim)
    octoA.translate(V(-dist, 0, 0))
    octoB.translate(V(dist, 0, STGS.dz))
rtnPart = get_s_bridge(for3DPrint)
