from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.bulk_fillet import bulk_fillet
from my_utils.v2_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
import FreeCAD as App
import Part
V = App.Vector
import math

def get_base_wedge(hScale=1.0):
    h = hScale * (STGS.trackBotZ + STGS.squareTrackH)
    botW = STGS.trackSquareDim
    topW = botW - 2 * STGS.defaultSlope * h
    base = make_wedge_cen_z_up( botW, botW, h, topW, topW )
    return base, h, botW, topW

def make_main_shell(doc):
    base, h, botW, topW = get_base_wedge(1.0)
    cutDiff = STGS.minThickness / math.cos(math.radians(STGS.defaultDraftAngle))
    cBotW = botW - 2 * cutDiff
    cTopW = topW - 2 * cutDiff + 2 * STGS.minThickness * STGS.defaultSlope
    baseCut = make_wedge_cen_z_up(cBotW, cBotW, h - STGS.minThickness, cTopW, cTopW)

    cornerTopDist = 0.5 * STGS.inOctDim + STGS.inOctSlotDepth
    cornerBotDist = cornerTopDist + STGS.octoCenterCutSlope * STGS.centerSlotH
    topR = 0.75
    cornerDist = topR * cornerTopDist + (1 - topR) * cornerBotDist
    cornerCutterBotDim = 100
    cornerCutterTopDim = cornerCutterBotDim + 2 * STGS.octoCenterCutSlope * h
    cornerCutter = make_wedge_cen_z_up(
        cornerCutterBotDim, cornerCutterBotDim, h,
        cornerCutterTopDim, cornerCutterTopDim
    )
    cornerCutter.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    cornerCutDiff = STGS.minThickness / math.cos(math.radians(STGS.octoCenterCutAngle))
    cutRad = math.sqrt(0.5) * (cornerDist + 0.5 * cornerCutterBotDim)
    for xSign in [-1, 1]:
        for ySign in [-1, 1]:
            xLoc = xSign * cutRad
            yLoc = ySign * cutRad
            cornerCutter.Placement.Base = V(xLoc, yLoc, 0)
            base = base.cut(cornerCutter)
            xLoc = xSign * (cutRad - math.sqrt(0.5) * cornerCutDiff)
            yLoc = ySign * (cutRad - math.sqrt(0.5) * cornerCutDiff)
            cornerCutter.Placement.Base = V(xLoc, yLoc, 0)
            baseCut = baseCut.cut(cornerCutter)
            
    
    return base, baseCut