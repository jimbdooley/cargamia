from matplotlib import use

from my_utils.bulk_fillet import bulk_fillet
from my_utils.bulk_chamfer import bulk_chamfer
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.get_vert_port import getVertPort
from my_utils.get_port_cut import getPortCut
from my_utils.edges_in_plane import edges_in_plane
from my_utils.add_debug_points import add_debug_points
from my_utils.add_grips_to_sq import add_grips_to_sq
from my_utils.cache_sq import get_cached_shapes, store_cached_shapes, CACHE_NAMES
import FreeCAD as App
import Part
import math

def get_base_square(doc, useCache=False):
    for obj in list(doc.Objects):
        if useCache and obj.Name in CACHE_NAMES: continue
        doc.removeObject(obj.Name)

    cached_shapes = None if not useCache else get_cached_shapes(doc)
    if cached_shapes is not None:
        sq, botCut, midFuse = cached_shapes
    else:
        sq, botCut, midFuse = make_base_square(doc)
        if useCache:
            store_cached_shapes(doc, (sq, botCut, midFuse))
    
    return sq, botCut, midFuse

def _get_bot_dims():
    wedgeH = STGS.defaultTrackH + STGS.trackBotZ
    wedgeBaseDxy = wedgeH * STGS.defaultSlope
    botCutTopW = STGS.innerSqDim - 2 * STGS.minThickness / math.cos(math.radians(STGS.defaultDraftAngle))
    botCutBotW = botCutTopW + 2 * wedgeBaseDxy
    return wedgeH, wedgeBaseDxy, botCutTopW, botCutBotW

def trim_cut_bot_base_square(doc, prt):
    wedgeH, wedgeBaseDxy, botCutTopW, botCutBotW = _get_bot_dims()
    perimR = botCutBotW / 2 + 0.1
    perim = []
    for i in range(4):
        signX = 1 if i < 2 else -1
        signY = 1 if i == 0 or i == 3 else -1
        perim.append((signX * perimR, signY * perimR))
    edgesToFil = edges_in_plane(prt, 0, (perim,), ())
    rad = min(0.85 * (STGS.trackBotZ - STGS.minThickness), STGS.fltRadConvex)
    prt = bulk_fillet(doc, prt, rad, edgesToFil)
    return prt

def make_base_square(doc):
        
    wedgeH, wedgeBaseDxy, botCutTopW, botCutBotW = _get_bot_dims()
    wedgeDim = STGS.innerSqDim + 2 * wedgeBaseDxy
    box = make_wedge_cen_z_up(wedgeDim, wedgeDim, wedgeH, STGS.innerSqDim, STGS.innerSqDim)
    box = bulk_fillet(doc, box, STGS.fltRadConvex, [2, 3, 4, 6, 7, 8, 11, 12])
    base = make_wedge_cen_z_up(
        STGS.baseDimPlusTaper, STGS.baseDimPlusTaper, STGS.baseThickness,
        STGS.baseDim, STGS.baseDim
    )
    box = box.fuse(base)
    box = bulk_fillet(doc, box, STGS.fltRadConcave, range(21, 28 + 1))


    box = bulk_chamfer(doc, box, STGS.baseCornerRad, (29, 30, 33, 35))
    box = bulk_fillet(doc, box, 3 * STGS.fltRadConvex, [17, 18, 21, 23, 25, 27, 29, 31])


    for i in range(4):
        vPort = getVertPort(i)
        box = box.fuse(vPort)

    topBotCutters = [getPortCut(i) for i in range(4)]

    for cutters in topBotCutters:
        box = box.cut(cutters[0])

    cpr = STGS.innerSqDim / 2 + 3 # cenPerimRad
    cenPerim = [(cpr, cpr), (cpr, -cpr), (-cpr, cpr), (-cpr, -cpr)]
    edgesToCut = edges_in_plane(box, STGS.portH, None, (cenPerim, ))
    box = bulk_fillet(doc, box, 0.48 * STGS.portTopThickness, edgesToCut)

    baseHRad = - 0.4 + STGS.baseDim / 2 - 0.5 * STGS.baseCornerRad
    baseLenMin = 0.5 * STGS.baseDim - 0.4
    baseDimDiff = baseLenMin - baseHRad
    baseCenPerim = [
        (baseHRad - baseDimDiff, baseLenMin-0.5),
        (baseHRad, baseHRad), 
        (baseLenMin-0.5, baseHRad - baseDimDiff), 
    ]
    for i in range(1, 4):
        xSign = -1 if i >= 2 else 1
        ySign =  -1 if i < 3 else 1
        for j in ([2, 1, 0] if i != 2 else [0, 1, 2]):
            newX = xSign * baseCenPerim[j][0]
            newY = ySign * baseCenPerim[j][1]
            baseCenPerim.append((newX, newY))


    debug_points = [(baseCenPerim[i][0], baseCenPerim[i][1], 0) for i in range(len(baseCenPerim))]
    debug_points2 = [(baseCenPerim[i][0], baseCenPerim[i][1], STGS.baseThickness) for i in range(len(baseCenPerim))]
    #box = add_debug_points(doc, box, debug_points, radius=0.1, name="DebugPoints")
    #box = add_debug_points(doc, box, debug_points2, radius=0.1, name="DebugPoints2")



    edgesToFil2 = edges_in_plane(box, STGS.baseThickness, (baseCenPerim, ) , (cenPerim, ))
    box = bulk_fillet(doc, box, 1 * STGS.fltRadConcave, edgesToFil2)

    box = add_grips_to_sq(doc, box)


    for cutters in topBotCutters:
        box = box.cut(cutters[1])
    box = box.removeSplitter()
    edgesToFil3 = edges_in_plane(box, 0, (baseCenPerim,  ) , (cenPerim,))
    box = bulk_fillet(doc, box, 0.25 * STGS.fltRadConvex, edgesToFil3)

    botCut = make_wedge_cen_z_up(
        botCutBotW, botCutBotW, wedgeH,
        botCutTopW, botCutTopW
    )
    botCut = bulk_fillet(doc, botCut, STGS.fltRadConcave, [2, 3, 4, 6, 7, 8, 11, 12])
    botCut.translate(App.Vector(0, 0, -STGS.minThickness))
    midFuse = Part.makeBox(wedgeDim, wedgeDim, wedgeH)
    midFuse.translate(App.Vector(-0.5 * wedgeDim, -0.5 * wedgeDim, 0))
    return box, botCut, midFuse