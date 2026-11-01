from my_utils.v2_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
import FreeCAD as App
import Part
import math
V = App.Vector

def uncover_claw(doc, part, zDif):
    cutDimBot = 30
    cutH = 20
    clawBotDepth = STGS.trackSlotTopDepth + STGS.clawBotExtra
    clawDist = 0.5 * (STGS.gap + STGS.trackSquareTopDim) - STGS.getPathSlotDist()
    clawDist -= (0.5 * STGS.clawBotExtra - STGS.clawOverhang) 
    cutDimTop = cutDimBot + 2 * cutH * STGS.trackSlotSlope
    cut = make_wedge_cen_z_up(cutDimBot, cutDimBot, cutH, cutDimTop, cutDimTop)
    b = STGS.getPathB()
    bridgeClawGap = 0.2
    bridgeClawW = 2 * b * STGS.trackSlotSlope - 2 * bridgeClawGap
    for xSign, ySign in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
        cutY = ySign * 0.5 * (bridgeClawW + cutDimBot)
        cutX = xSign * (clawDist + 0.5 * cutDimBot - 0.5 * clawBotDepth)
        cut.Placement.Base = V(cutX, cutY, zDif if xSign > 0 else 0)
        part = part.cut(cut.copy())
    return part

def make_claw_v2(cutBuf, dz, zDif):
    clawH = 15
    clawBotDepth = STGS.trackSlotTopDepth + STGS.clawBotExtra
    clawTopDepth = clawBotDepth + 2 * clawH * STGS.trackSlotSlope
    clawMidDepth = clawBotDepth + 2 * STGS.clawBotH * STGS.trackSlotSlope

    b = STGS.getPathB()
    bridgeClawGap = 0.2
    bridgeClawW = 2 * b * STGS.trackSlotSlope - 2 * bridgeClawGap
    topW = bridgeClawW - 2 * clawH * STGS.trackSlotSlope
    botW = bridgeClawW - 2 * STGS.clawBotH * STGS.trackSlotSlope
    clawA = make_wedge_cen_z_up(
        clawMidDepth, botW, clawH - STGS.clawBotH, clawTopDepth, topW
    )
    botBotW = botW + 2 * STGS.defaultSlope * STGS.clawBotH
    clawABot = make_wedge_cen_z_up(
        clawBotDepth, botBotW, STGS.clawBotH, clawMidDepth, botW
    )
    clawA.Placement.Base = V(0, 0, STGS.clawBotH)
    clawA = clawA.fuse(clawABot)

    cutDiff = STGS.minThickness / (1 - STGS.trackSlotSlope)
    cutH = clawH - STGS.minThickness
    cutDepth = 100
    cutBotW = bridgeClawW - 2 * cutDiff
    cutTopW = cutBotW - 2 * cutH * STGS.trackSlotSlope
    clawCut = make_wedge_cen_z_up(
        cutDepth, cutBotW, cutH, cutDepth, cutTopW
    )
    clawA = clawA.cut(clawCut)

    clawNotchH = STGS.baseThickness + 0.05
    topCutDepth = 10
    botCutDepth = topCutDepth + 2 * STGS.trackSlotSlope * clawNotchH
    clawNotchWTop = STGS.trackSlotTopDepth - STGS.trackClawBuffer
    clawNotch = make_wedge_cen_z_up(botCutDepth, 100, clawNotchH, topCutDepth, 100)
    cutTransX = -0.5 * clawNotchWTop - 0.5 * topCutDepth -(0.5 * STGS.clawBotExtra - STGS.clawOverhang) 
    clawNotch.translate(V(cutTransX, 0, 0))
    clawA = clawA.cut(clawNotch)
    clawNotch.translate(V(clawNotchWTop + topCutDepth, 0, 0))
    clawA = clawA.cut(clawNotch)

    clawB = clawA.copy()
    clawB.rotate(V(0, 0, 0), V(0, 0, 1), 180)
    clawDist = 0.5 * (STGS.gap + STGS.trackSquareTopDim) - STGS.getPathSlotDist()
    clawDist -= (0.5 * STGS.clawBotExtra - STGS.clawOverhang) 
    clawA.translate(V(-clawDist + 0.5 * STGS.gap + cutBuf, 0, -dz))
    clawB.translate(V(clawDist + 0.5 * STGS.gap + cutBuf, 0, zDif - dz))

    return clawA, clawB