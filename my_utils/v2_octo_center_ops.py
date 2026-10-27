from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.bulk_fillet import bulk_fillet
from my_utils.v2_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.make_oct_wedge_cen_z_up import make_octo_wedge_cen_z_up
import FreeCAD as App
import Part
V = App.Vector
import math

def octo_center_ops_v2(doc, baseOcto):
    cenCut = make_octo_wedge_cen_z_up(STGS.inOctDim, STGS.inOctDim2, 
                                      STGS.baseThickness, -STGS.octoCenterCutSlope)
    baseOcto.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    baseOcto = baseOcto.cut(cenCut)
    centerSlotBotDepth = STGS.centerSlotDepth + 2 * STGS.octoCenterCutSlope * STGS.centerSlotH
    centerSlotTopWidth = STGS.inOctSlotLen
    centerSlotBotWidth = centerSlotTopWidth + 2 * STGS.octoCenterCutSlope * STGS.centerSlotH
    centerSlotWedge = make_wedge_cen_z_up(
        centerSlotBotWidth, centerSlotBotDepth, STGS.centerSlotH,
        centerSlotTopWidth, STGS.centerSlotDepth
    )
    centerSlotWedge = bulk_fillet(doc, centerSlotWedge, 0.5 * STGS.minThickness, [4, 8])
    centerSlotDist = 0.5 * (STGS.inOctDim + STGS.centerSlotDepth) + STGS.inOctSlotDepth

    centerSlotLen = STGS.inOctSlotLen - STGS.minThickness
    centerSlotGuide = Part.makeCylinder(0.5 * STGS.minThickness, centerSlotLen)
    centerSlotGuide.rotate(V(0, 0, 0), V(0, 1, 0), 90)
    guideSphere = Part.makeSphere(0.5 * STGS.minThickness)
    for i in range(2):
        baseOcto.rotate(V(0, 0, 0), V(0, 0, 1), 90)
        centerSlotWedge.Placement.Base = V(0, centerSlotDist, 0)
        baseOcto = baseOcto.fuse(centerSlotWedge.copy())
        centerSlotWedge.Placement.Base = V(0, -centerSlotDist, 0)
        centerSlotWedge.rotate(V(0, -centerSlotDist, 0), V(0, 0, 1), 180)
        baseOcto = baseOcto.fuse(centerSlotWedge.copy())
        centerSlotWedge.rotate(V(0, -centerSlotDist, 0), V(0, 0, 1), 180)
        for xSign in [-1, 1]:
            for ySign in [-1, 1]:
                xLoc = xSign * 0.5 * centerSlotLen
                guideSphere.Placement.Base = V(xLoc, ySign * centerSlotDist, STGS.centerSlotH)
                baseOcto = baseOcto.fuse(guideSphere.copy())
        centerSlotGuide.Placement.Base = V(-0.5 * centerSlotLen, centerSlotDist, STGS.centerSlotH)
        baseOcto = baseOcto.fuse(centerSlotGuide.copy())
        centerSlotGuide.Placement.Base = V(-0.5 * centerSlotLen, -centerSlotDist, STGS.centerSlotH)
        baseOcto = baseOcto.fuse(centerSlotGuide.copy())
    cenWedgeBotW = STGS.inOctSlotLen + 2 * STGS.octoCenterCutSlope * STGS.centerSlotH
    cenWedgeBotL = STGS.inOctDim + 2 * STGS.inOctSlotDepth
    cenWedgeBotL += 2 * STGS.octoCenterCutSlope * STGS.centerSlotH
    cenWedgeCut = make_wedge_cen_z_up(
        cenWedgeBotW, cenWedgeBotL, STGS.centerSlotH,
        STGS.inOctSlotLen, STGS.inOctDim + 2 * STGS.inOctSlotDepth
    )
    baseOcto = baseOcto.cut(cenWedgeCut)
    cenWedgeCut.rotate(V(0, 0, 0), V(0, 0, 1), 90)
    baseOcto = baseOcto.cut(cenWedgeCut)
    baseOcto.rotate(V(0, 0, 0), V(0, 0, 1), -45)

    return baseOcto