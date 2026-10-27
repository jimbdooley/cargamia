from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.bulk_fillet import bulk_fillet
from my_utils.v2_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
import FreeCAD as App
import Part
V = App.Vector
import math

def cut_track_io_slots_v2(doc, baseOcto, pathSlotY, plrP1, plrP2):
    slotBotWidth = STGS.trackSlotTopWidth + 2 * STGS.baseThickness * STGS.trackSlotSlope
    slotBotDepth = STGS.trackSlotTopDepth + 2 * STGS.baseThickness * STGS.defaultSlope
    slotTopWidth = slotBotWidth - 1.5 * STGS.octoH * STGS.trackSlotSlope
    slotTopDepth = slotBotDepth - 1.5 * STGS.octoH * STGS.defaultSlope
    slotCut = make_wedge_cen_z_up(
        slotBotWidth, slotBotDepth, 0.75*STGS.octoH,
        slotTopWidth, slotTopDepth
    )
    trackSlotPeakZ = STGS.trackSlotPeakZ
    if math.isclose(STGS.trackSlotSlope, 0.0, abs_tol=1e-9):
        raise ValueError("trackSlotSlope must be nonzero to calculate the line intercept.")
    trackSlotLineSlope = 1 / STGS.trackSlotSlope
    plrDz = plrP2[1] - plrP1[1]
    if math.isclose(plrDz, 0.0, abs_tol=1e-9):
        if not math.isclose(plrP1[1], trackSlotPeakZ, abs_tol=1e-9):
            raise ValueError("The PLR line does not intersect trackSlotPeakZ.")
        raise ValueError("The PLR line overlaps trackSlotPeakZ; interceptB is not unique.")

    plrXAtPeakZ = plrP1[0] + (trackSlotPeakZ - plrP1[1]) * (
        (plrP2[0] - plrP1[0]) / plrDz
    )
    interceptB = trackSlotPeakZ + trackSlotLineSlope * plrXAtPeakZ
    yForXDist = trackSlotLineSlope * 0.5 * slotBotWidth
    xDist = (yForXDist - interceptB) / (-trackSlotLineSlope)
    for _rot in range(2):
        baseOcto.rotate(V(0, 0, 0), V(0, 0, 1), 90)
        for xSign, ySign in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            slotCut.Placement.Base = V(xSign * xDist, ySign * pathSlotY, 0)
            baseOcto = baseOcto.cut(slotCut)

    return baseOcto