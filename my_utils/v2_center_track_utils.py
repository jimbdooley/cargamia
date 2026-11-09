from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.bulk_fillet import bulk_fillet
from my_utils.v2_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
import FreeCAD as App
import Part
V = App.Vector
import math

def get_base_wedge(hScale, slope):
    h = hScale * (STGS.trackBotZ + STGS.squareTrackH)
    botW = STGS.trackSquareDim
    topW = botW - 2 * slope * h
    base = make_wedge_cen_z_up( botW, botW, h, topW, topW )
    return base, h, botW, topW

def _fit_track_ends_helper(part, dz, p1, p2):
    base, _, _, _ = get_base_wedge(2, STGS.defaultSlope)
    base.scale(1.020)
    base.translate(V(p1[0], p1[1], 0))
    part = part.cut(base)
    base.translate(V(p2[0] - p1[0], p2[1] - p1[1], dz))
    part = part.cut(base)
    return part

def fit_track_ends_right(part, dz, _trackLen=None):
    trackLen = _trackLen if _trackLen is not None else STGS.gap
    dist = 0.5 * (trackLen + STGS.trackSquareTopDim)
    return _fit_track_ends_helper(part, dz, (-dist, 0), (0, dist))

def fit_track_ends(part, dz, _trackLen=None):
    trackLen = _trackLen if _trackLen is not None else STGS.gap
    dist = 0.5 * (trackLen + STGS.trackSquareTopDim)
    return _fit_track_ends_helper(part, dz, (-dist, 0), (dist, 0))

def make_main_shell(slope):
    base, h, botW, topW = get_base_wedge(1.0, slope)
    cutDiff = STGS.minThickness / math.cos(math.radians(STGS.defaultDraftAngle))
    cBotW = botW - 2 * cutDiff
    cTopW = topW - 2 * cutDiff + 2 * STGS.minThickness * slope
    if cBotW - cTopW < STGS.defaultSlope * (h - STGS.minThickness):
        cTopW = cBotW - 0.6 * STGS.defaultSlope * (h - STGS.minThickness)
        cBotW = cBotW + 0.4 * STGS.defaultSlope * (h - STGS.minThickness)
    baseCut = make_wedge_cen_z_up(cBotW, cBotW, h - STGS.minThickness, cTopW, cTopW)

    cornerTopDist = 0.5 * STGS.inOctDim + STGS.inOctSlotDepth
    cornerBotDist = cornerTopDist + STGS.octoCenterCutSlope * STGS.centerSlotH
    topR = STGS.squareSqueezeR
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

    cornerSmoothH = 1.1
    cornerSmoothHR = cornerSmoothH / h
    cornerSmootherTopDist = cornerTopDist * cornerSmoothHR
    cornerSmootherTopDist += cornerBotDist * (1 - cornerSmoothHR)
    cornerSmoothSlope = 0.3
    cornerSmoothTopDim = 100
    cornerSmoothBotDim = 100 + 2 * cornerSmoothSlope * cornerSmoothH
    cornerSmoother = make_wedge_cen_z_up(
        cornerSmoothBotDim, cornerSmoothBotDim, cornerSmoothH,
        cornerSmoothTopDim, cornerSmoothTopDim
    )
    cornerSmoother.translate(V(cornerDist + 0.5 * cornerSmoothTopDim, 0, 0))
    base.rotate(V(0, 0, 0), V(0, 0, 1), -45)
    for i in range(4):
        base.rotate(V(0, 0, 0), V(0, 0, 1), 90)
        base = base.cut(cornerSmoother)

    base.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    
    return base, baseCut