from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.v2_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
import FreeCAD as App
import Part
V = App.Vector
import math

def make_octo_wedge_cen_z_up(majorDim, minorDim, height, slope):
    slopeDif = math.abs(slope * height)
    wedgeTopDim = majorDim if slope >= 0 else majorDim - slopeDif
    wedgeBotDim = majorDim if slope < 0 else majorDim - slopeDif

    octoWedge = make_wedge_cen_z_up(
        wedgeBotDim, wedgeBotDim, height,
        wedgeTopDim, wedgeTopDim
    )
    return octoWedge