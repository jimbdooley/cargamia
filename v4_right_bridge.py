from my_utils.v2_settings import STGS
from my_utils.v4_right_bridge_starter import make_right_bridge_starter_v4
from my_utils.simple_cache import get_cached, store_cached
from my_utils.v2_get_octo import getOcto_v2
from my_utils.warcle_torus import make_warcle_torus
from my_utils.warcle_beam import make_warcle_beam
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
    xferH = 4.5
    iXferWAtTop = 2 * STGS.trackRad - 2 * (STGS.trackRad - xferH) * STGS.warcleSlope
    oXferWAtTop = iXferWAtTop + 2 * STGS.minThickness
    xferLen = 0.5 + 0.5 * (STGS.octoDim - STGS.trackSquareTopDim)
    bridgeDZ = dz + STGS.trackBotZOut - STGS.trackBotZInc
    xferDZTop = 1.2
    xferDZBot = 2.2
    xferDXTop = math.sqrt(xferLen ** 2 - xferDZTop ** 2)
    xferDXBot = math.sqrt(xferLen ** 2 - xferDZBot ** 2)
    dyAfterXY = 0.5 * STGS.gap - xferDXTop
    bridge, distToMid = make_right_bridge_starter_v4(dz, xferLen, bridgeDZ, 
         xferH, xferDZTop, xferDZBot, xferDXTop, xferDXBot)
    torRad = distToMid - xferLen
    tiltAngle = math.degrees(math.asin(bridgeDZ / distToMid))
    cutDim = (STGS.gap - 2 * xferLen)
    midCut = Part.makeBox(cutDim, cutDim, 100)
    midCut.translate(V(-0.5 * cutDim, -0.5 * cutDim, 0))
    bridge = bridge.cut(midCut)

    radL1 = dyAfterXY / 3
    oRadL1 = 90
    wtA = make_warcle_torus(radL1, oXferWAtTop, xferH + STGS.minThickness,
                           STGS.oWarcleRad, STGS.warcleSlope, oRadL1)
    wtAInner = make_warcle_torus(radL1, iXferWAtTop, xferH,
                                STGS.iWarcleRad, STGS.warcleSlope, oRadL1)
    wtAInner.translate(V(0, 0, STGS.minThickness))
    wtA = wtA.cut(wtAInner)
    wtB = wtA.copy()
    wtC = wtA.copy()
    wtA.rotate(V(0, 0, 0), V(0, 0, 1), -oRadL1)
    wtAz = 0.5 * STGS.dz + STGS.trackBotZOut - xferDZTop - STGS.minThickness
    wtA.translate(V(-radL1, 0.5 * STGS.gap - xferDXTop, wtAz))
    wtB.rotate(V(0, 0, 0), V(0, 0, 1), -oRadL1)
    wtB.translate(V(xferDXBot-0.5*STGS.gap, radL1, STGS.trackBotZInc + xferDZBot - STGS.minThickness))
    wtC.rotate(V(0, 0, 0), V(0, 0, 1), oRadL1)
    wtC.translate(V(xferDXBot-0.5*STGS.gap+2*radL1, radL1, STGS.trackBotZInc + xferDZBot - STGS.minThickness))
    bridge = bridge.fuse(wtA.common(midCut))
    sPart = wtB.fuse(wtC)
    sPartBeam = make_warcle_beam(10, oXferWAtTop, xferH + STGS.minThickness,
                                 STGS.oWarcleRad, STGS.warcleSlope)
    sPartIBeam = make_warcle_beam(10, iXferWAtTop, xferH, STGS.iWarcleRad, STGS.warcleSlope)
    sPartIBeam.translate(V(0, 0, STGS.minThickness))
    sPartBeam = sPartBeam.cut(sPartIBeam)
    sPartBeam2 = sPartBeam.copy()
    sPartBeamX = -0.5 * STGS.gap + xferDXBot + 2 * radL1 + 5
    sPartBeam.translate(V(sPartBeamX, 2 * radL1, STGS.trackBotZInc + xferDZBot - STGS.minThickness))
    sPartBeam2.translate(V(sPartBeamX - 2 * radL1 - 10, 0, STGS.trackBotZInc + xferDZBot - STGS.minThickness))
    
    sPart = sPart.fuse(sPartBeam)
    sPart = sPart.fuse(sPartBeam2)
    sPartP1 = (-0.5 * STGS.gap + xferDXBot, STGS.trackBotZInc + xferDZBot)
    sPartP2 = (-radL1, 0.5 * STGS.dz + STGS.trackBotZOut - xferDZTop)
    sPartSlope = (sPartP2[1] - sPartP1[1]) / (sPartP2[0] - sPartP1[0])
    sPartRads = math.atan(sPartSlope)
    sPart.rotate(V(sPartP1[0], 0, sPartP1[1]), V(0, 1, 0), -math.degrees(sPartRads))
    sPartRegion = Part.makeBox(sPartP2[0] - sPartP1[0], 100, 100)
    sPartRegion.translate(V(sPartP1[0], -50, -50))
    sPart = sPart.common(sPartRegion)

    miscSmoother = Part.makeBox(4*radL1, 2*radL1, 2)
    miscSmoother.translate(V(-2*radL1, radL1 - 0.1, xferH + 0.5 * STGS.dz + STGS.trackBotZOut - xferDZTop))
    sPart = sPart.cut(miscSmoother)

    bridge = bridge.fuse(sPart)
    return bridge



if 0>0:
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
