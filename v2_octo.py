from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.bulk_fillet import bulk_fillet
from my_utils.v2_settings import STGS
from my_utils.v2_octo_center_ops import octo_center_ops_v2
from my_utils.v2_shape_pillar_port import shape_pillar_port_v2
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.make_oct_wedge_cen_z_up import make_octo_wedge_cen_z_up
import FreeCAD as App
import Part
V = App.Vector
import math

useCache = globals().get("__useCache__", False)
for3DPrint = globals().get("__for3DPrint__", False)
docName = "octo_v2"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    doc.removeObject(obj.Name)

def getOcto_v2(for3DPrint, slopeFromBot=False):
    octoTopW = STGS.octoDim - STGS.octoH * 2 * STGS.defaultSlope
    octoSlabDim = STGS.octoDim + 4
    baseOcto = Part.makeBox(octoSlabDim, octoSlabDim, STGS.octoH)
    baseOcto.translate(V(-0.5 * octoSlabDim, -0.5 * octoSlabDim, 0))

    draftCutterH = STGS.baseThickness if slopeFromBot else STGS.octoH
    draftCutterDim = STGS.octoDim + 10
    draftCutterTopDim = draftCutterDim - (0 if not slopeFromBot else 2 * draftCutterH * STGS.defaultSlope)
    draftCutterBotDim = draftCutterDim - (0 if slopeFromBot else 2 * draftCutterH * STGS.defaultSlope)
    draftCutter0 = make_wedge_cen_z_up(
        draftCutterBotDim, draftCutterBotDim, draftCutterH, 
        draftCutterTopDim, draftCutterTopDim)
    for i in range(4):
        xSign = [-1, 1, 0, 0][i]
        ySign = [0, 0, -1, 1][i]
        xLoc = xSign * 0.5 * (STGS.octoDim + draftCutterDim - 2 * draftCutterH * STGS.defaultSlope)
        yLoc = ySign * 0.5 * (STGS.octoDim + draftCutterDim - 2 * draftCutterH * STGS.defaultSlope)
        draftCutter0.Placement.Base = V(xLoc, yLoc, 0)
        baseOcto = baseOcto.cut(draftCutter0)

    octoCornerCutter = make_wedge_cen_z_up(
        octoTopW, octoTopW, STGS.octoH, STGS.octoDim, STGS.octoDim)
    octoCornerCutter2 = make_wedge_cen_z_up(
        STGS.octoDim, STGS.octoDim, STGS.octoH, octoTopW, octoTopW)
    octoCornerCutter.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    octoCornerCutter2.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    octoDim2HalfDif = 0.5 * (STGS.octoDim - STGS.octoDim2)
    cutLoc = STGS.octoDim2/2
    cutLoc += 0.5 * octoDim2HalfDif
    cutLoc += octoTopW * math.sqrt(2) / 4
    for xSign in [-1, 1]:
        for ySign in [-1, 1]:
            octoCornerCutter.Placement.Base = V(xSign * cutLoc, ySign * cutLoc, 0)
            baseOcto = baseOcto.cut(octoCornerCutter)
            if slopeFromBot:
                octoCornerCutter2.Placement.Base = V(xSign * cutLoc, ySign * cutLoc, 0)
                baseOcto = baseOcto.cut(octoCornerCutter2)

    octoBotCornerDist = math.sqrt(2) * 0.25 * (STGS.octoDim + STGS.octoDim2)
    octoBotCornerDist -= STGS.octoH * STGS.defaultSlope
    topCutDim = 2 * octoBotCornerDist - 2 * STGS.plrPlatformDepth
    topCutBotDim = topCutDim - 2 * STGS.defaultSlope * (STGS.octoH - STGS.baseThickness)
    topCut = make_wedge_cen_z_up(
        topCutBotDim, topCutBotDim, STGS.octoH - STGS.baseThickness,
        topCutDim, topCutDim
    )
    topCut.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    topCut.Placement.Base = V(0, 0, STGS.baseThickness)
    baseOcto = baseOcto.cut(topCut)

    edgeCutDim = 2 * STGS.edgeCutTopDiag * math.sqrt(0.5)
    edgeCutDimBot = edgeCutDim - 2 * STGS.defaultSlope * (STGS.octoH - STGS.baseThickness)
    edgeCut = make_wedge_cen_z_up(
        edgeCutDimBot, edgeCutDimBot, STGS.octoH - STGS.baseThickness,
        edgeCutDim, edgeCutDim
    )
    edgeCut.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    for i in range(4):
        xSign = [-1, 1, 0, 0][i]
        ySign = [0, 0, -1, 1][i]
        cutX = xSign * (0.5 * STGS.octoDimTop + math.sqrt(0.125) * edgeCutDim)
        cutY = ySign * (0.5 * STGS.octoDimTop + math.sqrt(0.125) * edgeCutDim)
        edgeCut.Placement.Base = V(cutX, cutY, STGS.baseThickness)
        baseOcto = baseOcto.cut(edgeCut)

    cornerFlattenDim = edgeCutDim * math.sqrt(0.5)
    cornerFlattenDim -= math.sqrt(2) * STGS.plrPlatformEdgeB4Corner
    cornerFlattenDimBot = cornerFlattenDim - 2 * STGS.octoEnterSlope * (STGS.octoH - STGS.baseThickness)
    platformCornerCutA = make_wedge_cen_z_up(
        cornerFlattenDimBot, 2 * STGS.octoDim, STGS.octoH - STGS.baseThickness,
        cornerFlattenDim, 2 * STGS.octoDim
    )
    platformCornerCutA.translate(V(0, 0, STGS.baseThickness))
    platformCornerCutB = make_wedge_cen_z_up(
        2 * STGS.octoDim, cornerFlattenDimBot, STGS.octoH - STGS.baseThickness,
        2 * STGS.octoDim, cornerFlattenDim
    )
    platformCornerCutB.translate(V(0, 0, STGS.baseThickness))
    baseOcto = baseOcto.cut(platformCornerCutA)
    baseOcto = baseOcto.cut(platformCornerCutB)
    

    
    baseOcto = shape_pillar_port_v2(doc, baseOcto)


    baseOcto = octo_center_ops_v2(doc, baseOcto)

    # misc final things
    baseOcto = baseOcto.removeSplitter()
    marbleCheck = Part.makeCylinder(8.4, 100)
    marbleCheck.rotate(V(0, 0, 0), V(0, 1, 0), 90)
    marbleCheck.Placement.Base = V(-50, 0, 11)
    #baseOcto = baseOcto.fuse(marbleCheck)
    return baseOcto

rtnPart = getOcto_v2(for3DPrint, True)