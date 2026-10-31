from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.bulk_fillet import bulk_fillet
from my_utils.v2_center_track_utils import make_main_shell
from my_utils.v2_settings import STGS
from my_utils.v2_octo_center_ops import octo_center_ops_v2
from my_utils.v2_shape_pillar_port import shape_pillar_port_v2
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.make_oct_wedge_cen_z_up import make_octo_wedge_cen_z_up
from my_utils.v2_cut_track_io_slots import cut_track_io_slots_v2
import FreeCAD as App
import Part
V = App.Vector
import math

def getOcto_v2(doc, for3DPrint, slopeFromBot=False):
    octoTopW = STGS.octoDim - STGS.octoH * 2 * STGS.defaultSlope
    octoSlabDim = STGS.octoDim + 4
    baseOcto = Part.makeBox(octoSlabDim, octoSlabDim, STGS.octoH)
    baseOcto.translate(V(-0.5 * octoSlabDim, -0.5 * octoSlabDim, 0))

    draftCutterH = STGS.baseThickness if slopeFromBot else STGS.octoH
    draftCutterDim = STGS.octoDim + 10
    draftCutterTopDim = draftCutterDim - (0 if not slopeFromBot else 2 * draftCutterH * STGS.defaultSlope)
    draftCutterBotDim = draftCutterDim - (0 if slopeFromBot else 2 * draftCutterH * STGS.defaultSlope)
    draftCutter0 = make_wedge_cen_z_up(
        draftCutterBotDim, draftCutterBotDim, draftCutterH, 
        draftCutterTopDim, draftCutterTopDim)
    for xSign, ySign in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        xLoc = xSign * 0.5 * (STGS.octoDim + draftCutterDim - 2 * draftCutterH * STGS.defaultSlope)
        yLoc = ySign * 0.5 * (STGS.octoDim + draftCutterDim - 2 * draftCutterH * STGS.defaultSlope)
        draftCutter0.Placement.Base = V(xLoc, yLoc, 0)
        baseOcto = baseOcto.cut(draftCutter0)

    octoCornerCutter = make_wedge_cen_z_up(
        octoTopW, octoTopW, STGS.octoH, STGS.octoDim, STGS.octoDim)
    octoCornerCutter2 = make_wedge_cen_z_up(
        STGS.octoDim, STGS.octoDim, STGS.octoH, octoTopW, octoTopW)
    octoCornerCutter.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    octoCornerCutter2.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    octoDim2HalfDif = 0.5 * (STGS.octoDim - STGS.octoDim2)
    cutLoc = STGS.octoDim2/2
    cutLoc += 0.5 * octoDim2HalfDif
    cutLoc += octoTopW * math.sqrt(2) / 4
    for xSign, ySign in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            octoCornerCutter.Placement.Base = V(xSign * cutLoc, ySign * cutLoc, 0)
            baseOcto = baseOcto.cut(octoCornerCutter)
            if slopeFromBot:
                octoCornerCutter2.Placement.Base = V(xSign * cutLoc, ySign * cutLoc, 0)
                baseOcto = baseOcto.cut(octoCornerCutter2)

    
    topCut = make_wedge_cen_z_up(
        STGS.topCutBotDim, STGS.topCutBotDim, 
        STGS.octoH - STGS.baseThickness,
        STGS.topCutDim, STGS.topCutDim
    )
    topCut.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    topCut.Placement.Base = V(0, 0, STGS.baseThickness)
    baseOcto = baseOcto.cut(topCut)

    edgeCutDim = 2 * STGS.edgeCutTopDiag * math.sqrt(0.5)
    edgeCutDimBot = edgeCutDim - 2 * STGS.defaultSlope * (STGS.octoH - STGS.baseThickness)
    edgeCut = make_wedge_cen_z_up(
        edgeCutDimBot, edgeCutDimBot, STGS.octoH - STGS.baseThickness,
        edgeCutDim, edgeCutDim
    )
    edgeCut.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    edgeCutDist = 0.5 * STGS.octoDimTop + math.sqrt(0.125) * edgeCutDim
    for xSign, ySign in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        cutX = xSign * edgeCutDist
        cutY = ySign * edgeCutDist
        edgeCut.Placement.Base = V(cutX, cutY, STGS.baseThickness)
        baseOcto = baseOcto.cut(edgeCut)

    cornerFlattenDim = edgeCutDim * math.sqrt(0.5)
    cornerFlattenDim -= math.sqrt(2) * STGS.plrPlatformEdgeB4Corner
    cornerFlattenDimBot = cornerFlattenDim - 2 * STGS.octoEnterSlope * (STGS.octoH - STGS.baseThickness)
    platformCornerCutA = make_wedge_cen_z_up(
        cornerFlattenDimBot, 2 * STGS.octoDim, STGS.octoH - STGS.baseThickness,
        cornerFlattenDim, 2 * STGS.octoDim
    )
    platformCornerCutA.translate(V(0, 0, STGS.baseThickness))
    platformCornerCutB = make_wedge_cen_z_up(
        2 * STGS.octoDim, cornerFlattenDimBot, STGS.octoH - STGS.baseThickness,
        2 * STGS.octoDim, cornerFlattenDim
    )
    platformCornerCutB.translate(V(0, 0, STGS.baseThickness))
    baseOcto = baseOcto.cut(platformCornerCutA)
    baseOcto = baseOcto.cut(platformCornerCutB)
    
    baseOcto = shape_pillar_port_v2(doc, baseOcto)
    
    baseOcto = octo_center_ops_v2(doc, baseOcto)

    pathSlotY = STGS.getPathSlotDist()
    baseOcto = cut_track_io_slots_v2(doc, baseOcto, pathSlotY)

    edgeTrim = make_wedge_cen_z_up(
        STGS.octoDim, 
        STGS.octoDim, 
        STGS.octoH,
        STGS.octoDim - 2 * STGS.defaultSlope * STGS.octoH, 
        STGS.octoDim - 2 * STGS.defaultSlope * STGS.octoH,
    )
    edgeTrimRad = STGS.octoDim - STGS.octoEdgeTrim - STGS.defaultSlope * STGS.baseThickness
    for xySign in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        xLoc = xySign[0] * edgeTrimRad
        yLoc = xySign[1] * edgeTrimRad
        edgeTrim.Placement.Base = V(xLoc, yLoc, 0)
        baseOcto = baseOcto.cut(edgeTrim)

    finalNotchDim = 15
    finalNotch = make_octo_wedge_cen_z_up(
        finalNotchDim, 4, STGS.baseThickness, -STGS.defaultSlope)
    fnDist = 0.5 * (STGS.octoDim + finalNotchDim - STGS.octoEdgeTrim) - 4.5
    for xSign, ySign in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        finalNotch.Placement.Base = V(xSign * fnDist, ySign * fnDist, 0)
        baseOcto = baseOcto.cut(finalNotch)

    # misc final things
    baseOcto = baseOcto.removeSplitter()
    trackOutRad = STGS.trackRad + STGS.trackThickness
    marbleCheck = Part.makeCylinder(trackOutRad, 100)
    marbleCheck.rotate(V(0, 0, 0), V(0, 1, 0), 90)
    marbleCheckCutter = make_wedge_cen_z_up(500, 500, 500, 500, 500)
    marbleCheckCutter.translate(V(0, 0, -trackOutRad + STGS.defaultTrackH + STGS.trackThickness))
    marbleCheck = marbleCheck.cut(marbleCheckCutter)
    marbleCheck.Placement.Base = V(-50, 0, trackOutRad + STGS.trackBotZ - STGS.trackThickness)
    #baseOcto = baseOcto.fuse(marbleCheck)
    #baseOcto.rotate(V(0, 0, 0), V(0, 0, 1), 45)

    if True:
        main_shell, _ = make_main_shell(doc)
        cut = Part.makeTorus(STGS.trackSquareDim / 2, STGS.trackRad)
        cutZ = STGS.trackRad + STGS.trackBotZ
        cut.Placement.Base = V(-STGS.trackSquareDim / 2, -STGS.trackSquareDim / 2, cutZ)
        main_shell = main_shell.cut(cut)
        cut.Placement.Base = V(STGS.trackSquareDim / 2, STGS.trackSquareDim / 2, cutZ)
        main_shell = main_shell.cut(cut)
        baseOcto = baseOcto.fuse(main_shell)

    return baseOcto
