from my_utils.v2_center_track_utils import fit_track_ends
from my_utils.v2_make_claw import uncover_claw, uncover_claw_short
from my_utils.v2_settings import STGS
from my_utils.simple_cache import get_cached, store_cached
from my_utils.make_s_tube import make_s_tube
from my_utils.v2_get_octo import getOcto_v2
from my_utils.v2_make_claw import make_claw_v2, make_base_claw
from my_utils.warcle_beam import make_warcle_beam
import FreeCAD as App
import Part
import math
V = App.Vector



def make_bridge_v4(bridgeLen):
    buf = 2
    bDist = bridgeLen + 2 * buf
    innerH = 4.5
    outerH = innerH + STGS.minThickness
    wAtTop = 2 * STGS.trackRad - 2 * (STGS.trackRad - innerH) * STGS.warcleSlope
    oWAtTop = wAtTop + 2 * STGS.minThickness
    beam = make_warcle_beam(bDist, wAtTop, innerH, STGS.iWarcleRad, STGS.warcleSlope)
    oRad = STGS.oWarcleRad - (1.21 if bridgeLen < 0.5 * STGS.gap else 0)
    oBeam = make_warcle_beam(bDist, oWAtTop, outerH, oRad, STGS.warcleSlope)
    beam.translate(V(0, 0, STGS.trackBotZ))
    oBeam.translate(V(0, 0, STGS.trackBotZ - STGS.minThickness))

    clawA = make_base_claw()
    clawCut = Part.makeBox(100, 100, 100)
    clawCut.translate(V(-50, -50, 6))
    clawA = clawA.cut(clawCut)
    clawB = clawA.copy()
    clawB.rotate(V(0, 0, 0), V(0, 0, 1), 180)
    clawDist = 0.5 * (bridgeLen + STGS.trackSquareTopDim) - STGS.getPathSlotDist()
    clawDist -= (0.5 * STGS.clawBotExtra - STGS.clawOverhang) 
    clawA.translate(V(-clawDist, 0, 0))
    clawB.translate(V(clawDist, 0, 0))
    oBeam = oBeam.fuse(clawA)
    oBeam = oBeam.fuse(clawB)

    beam = oBeam.cut(beam)

    beam = fit_track_ends(beam, 0, bridgeLen)
    beam = uncover_claw_short(beam, bridgeLen, innerH)
    beam = beam.removeSplitter()
    return beam
        