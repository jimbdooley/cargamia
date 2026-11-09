from my_utils.v2_settings import STGS
from my_utils.warcle_beam import make_warcle_beam
from my_utils.simple_cache import get_cached, store_cached
from my_utils.v2_get_octo import getOcto_v2
from my_utils.v2_center_track_utils import fit_track_ends_right
from my_utils.v2_make_claw import make_claw_v2, make_base_claw, uncover_claw
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
import FreeCAD as App
import Part
import math
V = App.Vector


def make_right_bridge_starter_v4(dz, xferLen, bridgeDZ, xferH, 
                                 xferDZTop, xferDZBot, xferDXTop, xferDXBot):
    distToMid = math.sqrt(0.25 * bridgeDZ ** 2 + 0.25 * STGS.gap ** 2)
    bDistA = 0.5 * STGS.gap - 0.5 * xferDXBot
    bDistB = 0.5 * STGS.gap - 0.5 * xferDXTop
    xferAngleTop = math.degrees(math.asin(xferDZTop / xferLen))
    xferAngleBot = math.degrees(math.asin(xferDZBot / xferLen))
    xferPad = 1
    xferLenPadded = xferLen + 2 * xferPad
    xferH2 = xferH + STGS.minThickness
    xferWAtTop = 2 * STGS.trackRad - 2 * (STGS.trackRad - xferH) * STGS.warcleSlope
    xferWAtTop2 = xferWAtTop + 2 * STGS.minThickness
    xferBeamA = make_warcle_beam(xferLenPadded, xferWAtTop, xferH, STGS.iWarcleRad, STGS.warcleSlope)
    xferBeamA2 = make_warcle_beam(xferLenPadded, xferWAtTop2, xferH2, STGS.oWarcleRad, STGS.warcleSlope)
    xferBeamA2.translate(V(0, 0, -STGS.minThickness))
    xferBeamB = xferBeamA.copy()
    xferBeamB2 = xferBeamA2.copy()

    softenerH = 2.2
    softenerW = 30
    sDimBot = softenerW - 2 * softenerH
    softener = make_wedge_cen_z_up(sDimBot, sDimBot, softenerH, softenerW, softenerW)
    softDistA = 0.5 * xferLen + 0.5 * softenerW - softenerH - 0.1
    softDistB = 0.5 * xferLen + 0.5 * softenerW - softenerH + 0.75
    softener.Placement.Base = V(-softDistA, 0, xferH - softenerH)
    xferBeamA2 = xferBeamA2.cut(softener)
    softener.Placement.Base = V(softDistB, 0, xferH - softenerH)
    xferBeamB2 = xferBeamB2.cut(softener)

    
    xferBeamA.rotate(V(0, 0, 0), V(0, 1, 0), -xferAngleBot)
    xferBeamA2.rotate(V(0, 0, 0), V(0, 1, 0), -xferAngleBot)
    xferBeamB.rotate(V(0, 0, 0), V(0, 1, 0), -xferAngleTop)
    xferBeamB2.rotate(V(0, 0, 0), V(0, 1, 0), -xferAngleTop)
    xferBeamB.rotate(V(0, 0, 0), V(0, 0, 1), 90)
    xferBeamB2.rotate(V(0, 0, 0), V(0, 0, 1), 90)
    xferBeamA.translate(V(-bDistA, 0, STGS.trackBotZInc + 0.5 * xferDZBot))
    xferBeamB.translate(V(0, bDistB, dz + STGS.trackBotZOut - 0.5 * xferDZTop))
    xferBeamA2.translate(V(-bDistA, 0, STGS.trackBotZInc + 0.5 * xferDZBot))
    xferBeamB2.translate(V(0, bDistB, dz + STGS.trackBotZOut - 0.5 * xferDZTop))
    clawA = make_base_claw()
    clawB = clawA.copy()
    clawCut = Part.makeBox(100, 100, 100)
    clawCut.translate(V(-50, -50, 7.5))
    clawA = clawA.cut(clawCut)
    clawCut.translate(V(0, 0, -1.5))
    clawB = clawB.cut(clawCut)
    clawB.rotate(V(0, 0, 0), V(0, 0, 1), 270)
    clawDist = 0.5 * (STGS.trackSquareTopDim + STGS.gap) - STGS.getPathSlotDist()
    clawDist -= (0.5 * STGS.clawBotExtra - STGS.clawOverhang) 
    clawA.translate(V(-clawDist, 0, 0))
    clawB.translate(V(0, clawDist, dz))
    xferBeamA2 = xferBeamA2.fuse(clawA)
    xferBeamB2 = xferBeamB2.fuse(clawB)
    xferBeamA2 = xferBeamA2.cut(xferBeamA)
    xferBeamB2 = xferBeamB2.cut(xferBeamB)
    bridge = xferBeamA2.fuse(xferBeamB2)
    bridge.rotate(V(0, 0, 0), V(0, 0, 1), -90)
    bridge = uncover_claw(bridge, dz)
    bridge.rotate(V(0, 0, 0), V(0, 0, 1), 90)
    bridge = uncover_claw(bridge, dz)
    bridge = fit_track_ends_right(bridge, dz)
    bridge = bridge.removeSplitter()
    return bridge, distToMid, 

