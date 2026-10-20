from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.bulk_fillet import bulk_fillet
import FreeCAD as App
import Part
import math

useCache = globals().get("__useCache__", False)
for3DPrint = globals().get("__for3DPrint__", False)
docName = "double_right"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    doc.removeObject(obj.Name)

def getPillar_v0(thickness):
    portTopThickness = thickness - 2 * STGS.plrSocketDepth * STGS.plrSocketDraftSlope
    plrFltRad = 0.45 * portTopThickness
    pad = 0.5 * thickness * math.tan(0.5 * STGS.plrFoldRads)
    pillarBodyH = STGS.dz - STGS.plrDZ - 2 * STGS.plrSocketDepth
    rtn = Part.makeBox(STGS.plrMidLen + 2 * pad, thickness, pillarBodyH)
    rtn.translate(App.Vector(-0.5 * (STGS.plrMidLen + 2 * pad), -0.5 * thickness, 0))

    for i in range(2):
        sign = 1 if i == 0 else -1
        wing = Part.makeBox(STGS.plrEdgeLen + pad, thickness, pillarBodyH)
        wing.translate(App.Vector(-0.5 * (STGS.plrEdgeLen + pad), -0.5 * thickness, 0))
        wing.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), sign * STGS.plrFoldAngle)
        wingDx = sign * (0.5 * STGS.plrMidLen + math.cos(STGS.plrFoldRads) * 0.5 * (STGS.plrEdgeLen - pad))
        wingDy = math.sin(STGS.plrFoldRads) * 0.5 * (STGS.plrEdgeLen - pad)
        wing.translate(App.Vector(wingDx, wingDy, 0))
        rtn = rtn.fuse(wing)
    rtn = rtn.removeSplitter()
    rtn = bulk_fillet(doc, rtn, plrFltRad, [2, 4, 6, 9, 12, 15, 18, 21])

    topMid = make_wedge_cen_z_up(
        STGS.plrMidLen, thickness, STGS.plrSocketDepth,
        STGS.plrMidLen, portTopThickness
    )
    topMidCut = make_wedge_cen_z_up(
        STGS.plrMidLen + 4, portTopThickness, STGS.plrSocketDepth,
        STGS.plrMidLen + 4, thickness
    )
    topMid.translate(App.Vector(0, 0, pillarBodyH))
    topMidCut.translate(App.Vector(0, -0.5 * (portTopThickness + thickness), pillarBodyH))
    preCutPad = 0.52
    preCutWingLen = STGS.plrEdgeSocketLen + preCutPad
    for i in range(2):
        sign = 1 if i == 0 else -1
        wing = make_wedge_cen_z_up(
            preCutWingLen, thickness, STGS.plrSocketDepth,
            preCutWingLen - 2 * STGS.plrSocketDepth * STGS.plrSocketDraftSlope, portTopThickness
        )
        wing.translate(App.Vector(0, 0, pillarBodyH))
        wing.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), sign * STGS.plrFoldAngle)
        wingDx = sign * (0.5 * STGS.plrMidLen + math.cos(STGS.plrFoldRads) * 0.5 * (STGS.plrEdgeSocketLen - preCutPad))
        wingDy = math.sin(STGS.plrFoldRads) * 0.5 * (STGS.plrEdgeSocketLen - preCutPad)
        wing.translate(App.Vector(wingDx, wingDy, 0))
        topMid = topMid.fuse(wing)
    topMid = topMid.cut(topMidCut)

    topMid = topMid.removeSplitter()
    topMid = bulk_fillet(doc, topMid, plrFltRad, [
        1, 2, 4, 6, 7, 8, 9, 11, 12, 14, 15, 18, 19, 20, 21, 24
    ])
    botMirror = topMid.mirror(App.Vector(0, 0, 0), App.Vector(0, 0, 1))
    botMirror.translate(App.Vector(0, 0, pillarBodyH))
    rtn = rtn.fuse(topMid)
    rtn = rtn.fuse(botMirror)

    return rtn

rtnPart = getPillar_v0(STGS.plrThickness * 0.6)