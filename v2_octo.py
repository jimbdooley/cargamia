from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.v2_settings import STGS
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

def getOcto_v2(for3DPrint):
    octoTopW = STGS.octoDim - STGS.octoH * 2 * STGS.defaultSlope
    octoSlabDim = STGS.octoDim + 4
    baseOcto = Part.makeBox(octoSlabDim, octoSlabDim, STGS.octoH)
    baseOcto.translate(V(-0.5 * octoSlabDim, -0.5 * octoSlabDim, 0))

    draftCutterDim = STGS.octoDim + 10
    draftCutterTopDim = draftCutterDim - 2 * STGS.defaultSlope * STGS.baseThickness
    draftCutter0 = make_wedge_cen_z_up(
        draftCutterDim, draftCutterDim, STGS.baseThickness, 
        draftCutterTopDim, draftCutterTopDim)
    for i in range(4):
        xSign = [-1, 1, 0, 0][i]
        ySign = [0, 0, -1, 1][i]
        xLoc = xSign * 0.5 * (STGS.octoDim + draftCutterTopDim)
        yLoc = ySign * 0.5 * (STGS.octoDim + draftCutterTopDim)
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
    cornerFlattenDimBot = cornerFlattenDim - 2 * STGS.crnFlttnSlope * (STGS.octoH - STGS.baseThickness)
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
    

    cenCut = make_octo_wedge_cen_z_up(STGS.inOctDim, STGS.inOctDim2, 
                                      STGS.baseThickness, -STGS.defaultSlope)
    baseOcto = baseOcto.cut(cenCut)
    cenWedgeBotW = STGS.inOctSlotLen + 2 * STGS.defaultSlope * STGS.baseThickness
    cenWedgeBotL = STGS.inOctDim + 2 * STGS.inOctSlotDepth
    cenWedgeBotL += 2 * STGS.defaultSlope * STGS.baseThickness
    cenWedgeCut = make_wedge_cen_z_up(
        cenWedgeBotW, cenWedgeBotL, STGS.baseThickness,
        STGS.inOctSlotLen, STGS.inOctDim + 2 * STGS.inOctSlotDepth
    )
    baseOcto = baseOcto.cut(cenWedgeCut)
    cenWedgeCut.rotate(V(0, 0, 0), V(0, 0, 1), 90)
    baseOcto = baseOcto.cut(cenWedgeCut)
    for i in range(2):
        if i == 1:
            baseOcto.rotate(V(0, 0, 0), V(0, 0, 1), 90)
        for xSign in [-1, 1]:
            for ySign in [-1, 1]:
                trackSlotCutBotL = STGS.trackSlotTopL + 2 * STGS.defaultSlope * STGS.baseThickness
                trackSlotCutBotW = STGS.trackSlotTopW + 2 * STGS.defaultSlope * STGS.baseThickness
                trackSlotCut = make_wedge_cen_z_up(
                    trackSlotCutBotW, trackSlotCutBotL, STGS.baseThickness,
                    STGS.trackSlotTopW, STGS.trackSlotTopL
                )
                xLoc = xSign * 0.5 * STGS.trackSlotTopGap
                yLoc = ySign * STGS.trackSlotTopDist
                trackSlotCut.translate(V(xLoc, yLoc, 0))
                baseOcto = baseOcto.cut(trackSlotCut)
    
    #cut slot holes in pillar port
    for i in range(2):
        baseOcto.rotate(V(0, 0, 0.5 * STGS.octoH), V(0, 1, 0), 180)
        slotCutBotW = STGS.plrSlotTopWidth - 2 * STGS.plrSlotSlope * STGS.plrPortDepth
        slotCutBotL = STGS.plrSlotTopDepth - 2 * STGS.plrSlotSlope * STGS.plrPortDepth
        pinsCutW = STGS.plrSlotTopWidth - 2 * STGS.plrSlotPinsarLen
        pinsCutBotW = pinsCutW - 2 * STGS.plrSlotSlope * STGS.plrPortDepth
        slotCut = make_wedge_cen_z_up(
            STGS.plrSlotTopWidth, STGS.plrSlotTopDepth, STGS.plrPortDepth,
            slotCutBotW, slotCutBotL)
        pinsCut = make_wedge_cen_z_up(
            pinsCutW, STGS.plrSlotTopDepth, STGS.plrPortDepth,
            pinsCutBotW, slotCutBotL)
        rad = 0.25 * (STGS.octoDim + STGS.octoDim2) - math.sqrt(0.5) * 0.5 * STGS.plrPlatformDepth
        rad -= math.sqrt(0.5) * STGS.octoH * STGS.defaultSlope
        pinsRad = rad + slotCutBotL * math.sqrt(0.5)
        slotCut.rotate(V(0, 0, 0), V(0, 0, 1), 45)
        pinsCut.rotate(V(0, 0, 0), V(0, 0, 1), 45)
        for j in range(4):
            slotCut.rotate(V(0, 0, 0), V(0, 0, 1), 90)
            pinsCut.rotate(V(0, 0, 0), V(0, 0, 1), 90)
            xSign = 1 if j < 2 else -1
            ySign = 1 if j == 0 or j == 3 else -1
            slotCut.Placement.Base = V(xSign * rad, ySign * rad, 0)
            pinsCut.Placement.Base = V(xSign * pinsRad, ySign * pinsRad, 0)
            baseOcto = baseOcto.cut(slotCut)
            baseOcto = baseOcto.cut(pinsCut)

        indentDepth = slotCutBotL - STGS.plrThickness
        indentTopDepth = indentDepth
        indentBotDepth = indentDepth - 2 * STGS.plrSlotSlope * STGS.plrPortDepth
        indentTopW = STGS.minThickness + 2 * STGS.defaultSlope * STGS.plrPortDepth
        indent = make_wedge_cen_z_up(
            STGS.minThickness, indentBotDepth, STGS.plrPortDepth,
            indentTopW, indentTopDepth
        )
        indent.rotate(V(0, 0, 0), V(0, 0, 1), 45)
        indentRad = rad - math.sqrt(0.5) * 0.5 * (STGS.plrSlotTopDepth - indentBotDepth)
        for j in range(4):
            indent.rotate(V(0, 0, 0), V(0, 0, 1), 90)
            xSign = 1 if j < 2 else -1
            ySign = 1 if j == 0 or j == 3 else -1
            indent.Placement.Base = V(xSign * indentRad, ySign * indentRad, 0)
            baseOcto = baseOcto.fuse(indent.copy())
    
    baseOcto = baseOcto.removeSplitter()
    return baseOcto

rtnPart = getOcto_v2(for3DPrint)