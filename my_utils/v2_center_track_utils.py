from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.bulk_fillet import bulk_fillet
from my_utils.v2_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
import FreeCAD as App
import Part
V = App.Vector
import math

def make_main_shell(doc):
    h = STGS.trackBotZ + STGS.squareTrackH
    botW = STGS.trackSquareDim
    topW = botW - 2 * STGS.defaultSlope * h
    base = make_wedge_cen_z_up( botW, botW, h, topW, topW )

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
    for xSign in [-1, 1]:
        for ySign in [-1, 1]:
            xLoc = xSign * math.sqrt(0.5) * (cornerDist + 0.5 * cornerCutterBotDim)
            yLoc = ySign * math.sqrt(0.5) * (cornerDist + 0.5 * cornerCutterBotDim)
            cornerCutter.Placement.Base = V(xLoc, yLoc, 0)
            base = base.cut(cornerCutter)

    return base