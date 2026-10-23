from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.v2_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
import FreeCAD as App
import Part
V = App.Vector
import math

def make_octo_wedge_cen_z_up(majorDim, minorDim, height, slope):
    slopeDif = abs(slope * height)
    wedgeTopDim = majorDim if slope >= 0 else majorDim - 2 * slopeDif
    wedgeBotDim = majorDim if slope < 0 else majorDim - 2 * slopeDif

    octoWedge = make_wedge_cen_z_up(
        wedgeBotDim, wedgeBotDim, height,
        wedgeTopDim, wedgeTopDim
    )

    cornerCutDim = wedgeTopDim
    cornerCutDimBot = cornerCutDim - 2 * slopeDif
    cornerCutter = make_wedge_cen_z_up(
        cornerCutDimBot, cornerCutDimBot, height,
        cornerCutDim, cornerCutDim
    )
    cornerCutter.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    for xSign in [-1, 1]:
        for ySign in [-1, 1]:
            xLoc = xSign * 0.5 * (math.sqrt(0.5) * cornerCutDimBot + 0.5 * (STGS.inOctDim + STGS.inOctDim2))
            yLoc = ySign * 0.5 * (math.sqrt(0.5) * cornerCutDimBot + 0.5 * (STGS.inOctDim + STGS.inOctDim2))
            cornerCutter.Placement.Base = V(xLoc, yLoc, 0)
            octoWedge = octoWedge.cut(cornerCutter)

    return octoWedge