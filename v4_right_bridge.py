from my_utils.v2_settings import STGS
from my_utils.warcle_beam import make_warcle_beam
from my_utils.simple_cache import get_cached, store_cached
from my_utils.v2_get_octo import getOcto_v2
from my_utils.v2_center_track_utils import fit_track_ends_right
from my_utils.v2_make_claw import make_claw_v2, make_base_claw, uncover_claw
import FreeCAD as App
import Part
import math
V = App.Vector

for3DPrint = globals().get("__for3DPrint__", False)
docName = "right_bridge_v4"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    if not obj.Name.startswith("ctcache_"):
        doc.removeObject(obj.Name)

rbdz = 0.5 * STGS.dz

def make_right_bridge_v4(dz):
    xferLen = 4 + 0.5 * (STGS.octoDim - STGS.trackSquareTopDim)
    xferDZTop = 1.2
    xferDZBot = 2
    xferDXTop = math.sqrt(xferLen ** 2 - xferDZTop ** 2)
    xferDXBot = math.sqrt(xferLen ** 2 - xferDZBot ** 2)
    bDistA = 0.5 * STGS.gap - 0.5 * xferDXBot
    bDistB = 0.5 * STGS.gap - 0.5 * xferDXTop
    xferAngleTop = math.degrees(math.asin(xferDZTop / xferLen))
    xferAngleBot = math.degrees(math.asin(xferDZBot / xferLen))
    xferPad = 1.5
    xferH = 4.5
    xferLenPadded = xferLen + 2 * xferPad
    xferH2 = xferH + STGS.minThickness
    xferWAtTop = 2 * STGS.trackRad - 2 * (STGS.trackRad - xferH) * STGS.warcleSlope
    xferWAtTop2 = xferWAtTop + 2 * STGS.minThickness
    xferBeamA = make_warcle_beam(xferLenPadded, xferWAtTop, xferH, STGS.iWarcleRad, STGS.warcleSlope)
    xferBeamA2 = make_warcle_beam(xferLenPadded, xferWAtTop2, xferH2, STGS.oWarcleRad, STGS.warcleSlope)
    xferBeamA.translate(V(0, 0, STGS.minThickness))
    xferBeamB = xferBeamA.copy()
    xferBeamB2 = xferBeamA2.copy()
    xferBeamA.rotate(V(0, 0, 0), V(0, 1, 0), -xferAngleBot)
    xferBeamA2.rotate(V(0, 0, 0), V(0, 1, 0), -xferAngleBot)
    xferBeamB.rotate(V(0, 0, 0), V(0, 1, 0), -xferAngleTop)
    xferBeamB2.rotate(V(0, 0, 0), V(0, 1, 0), -xferAngleTop)
    xferBeamB.rotate(V(0, 0, 0), V(0, 0, 1), 90)
    xferBeamB2.rotate(V(0, 0, 0), V(0, 0, 1), 90)
    xferBeamA.translate(V(-bDistA, 0, STGS.trackBotZInc - STGS.minThickness + 0.5 * xferDZBot))
    xferBeamB.translate(V(0, bDistB, dz + STGS.trackBotZOut - STGS.minThickness - 0.5 * xferDZTop))
    xferBeamA2.translate(V(-bDistA, 0, STGS.trackBotZInc - STGS.minThickness + 0.5 * xferDZBot))
    xferBeamB2.translate(V(0, bDistB, dz + STGS.trackBotZOut - STGS.minThickness - 0.5 * xferDZTop))
    clawA = make_base_claw()
    clawCut = Part.makeBox(100, 100, 100)
    clawCut.translate(V(-50, -50, 6))
    clawA = clawA.cut(clawCut)
    clawB = clawA.copy()
    clawB.rotate(V(0, 0, 0), V(0, 0, 1), 270)
    clawDist = 0.5 * (STGS.trackSquareTopDim + STGS.gap) - STGS.getPathSlotDist()
    clawDist -= (0.5 * STGS.clawBotExtra - STGS.clawOverhang) 
    clawA.translate(V(-clawDist, 0, 0))
    clawB.translate(V(0, clawDist, dz))
    xferBeamA2 = xferBeamA2.fuse(clawA)
    xferBeamB2 = xferBeamB2.fuse(clawB)
    xferBeamA2 = xferBeamA2.cut(xferBeamA)
    xferBeamB2 = xferBeamB2.cut(xferBeamB)
    bridge = xferBeamA2.fuse(xferBeamB2)
    bridge = fit_track_ends_right(bridge, dz)
    return bridge
    
    '''
    xferBeam.translate(V(0, 0, STGS.minThickness))
    xferBeam2.translate(V(0, 0, 0))
    xferBeam = xferBeam2.cut(xferBeam)
    xferBeam.rotate(V(0, 0, 0), V(0, 1, 0), -xferAngle)
    beam2 = xferBeam.copy()
    xferBeam.translate(V(-bDist, 0, STGS.trackBotZInc - STGS.minThickness + 0.5 * xferDZ))
    beam2.rotate(V(0, 0, 0), V(0, 0, 1), 90)
    beam2.translate(V(0, bDist, dz + STGS.trackBotZOut - STGS.minThickness - 0.5 * xferDZ))

    bridge = beam2.fuse(xferBeam)
    return bridge
    '''



if True:
    baseOcto = get_cached(doc, "ctcache_baseOcto")
    if baseOcto is None:
        print("Generating base octo...")
        baseOcto = getOcto_v2(doc, False, True, True)
        store_cached(doc, "ctcache_baseOcto", baseOcto)
    octoA = baseOcto.Shape.copy()
    octoB = baseOcto.Shape.copy()
    dist = 0.5 * (STGS.trackSquareTopDim + STGS.gap)
    octoA.translate(V(-dist, 0, 0))
    octoB.translate(V(0, dist, rbdz))

rtnPart = make_right_bridge_v4(rbdz)
