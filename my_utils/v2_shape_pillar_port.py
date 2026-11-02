from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.bulk_fillet import bulk_fillet
from my_utils.v2_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
import FreeCAD as App
import Part
V = App.Vector
import math

def shape_pillar_port_v2(doc, baseOcto):
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

        indentDepth = slotCutBotL - STGS.plrThickness + STGS.plrSqueezeMM
        indentTopDepth = indentDepth + 2 * STGS.plrSlotSlope * STGS.plrPortDepth
        indentBotDepth = indentDepth
        indentTopW = STGS.minThickness + 2 * STGS.plrSlotSlope * STGS.plrPortDepth
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

        slotHelperDepth = 2 * STGS.plrCutGuideDim + STGS.plrThickness - STGS.plrSqueezeMM
        slotHelperDepth += 2 * STGS.plrPortDepth * STGS.plrSlotSlope
        slotHelperWidth = STGS.plrPlatformWidth - 2 * STGS.pillarPortTopEdgeThickness
        slotHelperBotDepth = slotHelperDepth -  2 * STGS.plrCutGuideDim
        slotHelperBotDepth -= 4 * STGS.plrPortDepth * STGS.plrSlotSlope
        slotHelperBotWidth = slotHelperWidth -  2 * STGS.plrCutGuideDim * STGS.plrSlotSlope
        slotHelper = make_wedge_cen_z_up(slotHelperBotWidth, slotHelperBotDepth,
                                         2 * STGS.plrCutGuideDim, 
                                         slotHelperWidth, slotHelperDepth)
        slotHelper.rotate(V(0, 0, 0), V(0, 0, 1), 45)
        slotHelperDist = rad + math.sqrt(0.125) * indentDepth
        for xSign, ySign in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
            slotHelper.Placement.Base = V(0, 0, 0)
            slotHelper.rotate(V(0, 0, 0), V(0, 0, 1), 90)
            xLoc = xSign * slotHelperDist
            yLoc = ySign * slotHelperDist
            slotHelper.Placement.Base = V(xLoc, yLoc, STGS.octoH - 2 * STGS.plrCutGuideDim)
            baseOcto = baseOcto.cut(slotHelper)
    return baseOcto