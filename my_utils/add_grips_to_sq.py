from my_utils.bulk_fillet import bulk_fillet
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.edges_in_plane import edges_in_plane
import FreeCAD as App

def add_grips_to_sq(doc, box):    
    gripFilletConvex = min(STGS.fltRadConvex, 0.45 * STGS.gripW)
    gripEdges = [2, 3, 4, 6, 7, 8, 11, 12]
    for i in range(4):
        signX = 1 if i % 2 == 0 else -1
        signY = 1 if i < 2 else -1
        gripDTaper = STGS.gripH * 2 * STGS.gripDraftSlope
        grip = make_wedge_cen_z_up(
            STGS.gripW + gripDTaper, STGS.gripL + gripDTaper, STGS.gripH,
            STGS.gripW, STGS.gripL
        )
        grip = bulk_fillet(doc, grip, gripFilletConvex, gripEdges)
        gripY = 0.5 * STGS.gripL + STGS.gripDEdge + 0.5 * STGS.innerSqDim
        grip.translate(App.Vector(signX * 0.5 * STGS.gripGap, signY * gripY, 0))
        box = box.fuse(grip)

        grip2 = make_wedge_cen_z_up(
            STGS.gripL + gripDTaper, STGS.gripW + gripDTaper, STGS.gripH,
            STGS.gripL, STGS.gripW
        )
        gripX = 0.5 * STGS.gripL + STGS.gripDEdge + 0.5 * STGS.innerSqDim
        grip2 = bulk_fillet(doc, grip2, gripFilletConvex, gripEdges)
        grip2.translate(App.Vector(signX * gripX, signY * 0.5 * STGS.gripGap, 0))
        box = box.fuse(grip2)

    edge_from_center_L = 0.5 * STGS.innerSqDim + STGS.gripDEdge - 0.1
    edge_from_center_W = 0.5 * STGS.gripGap + 0.5 * STGS.gripW + 0.1

    exclude = []
    for i in range(4):
        signX = 1 if i < 2 else -1
        signY = 1 if i == 0 or i == 3 else -1
        exclude.append((signX * edge_from_center_L, signY * edge_from_center_L))
    includeA = []
    includeB = []
    for i in range(4):
        signX = 1 if i < 2 else -1
        signY = 1 if i == 0 or i == 3 else -1
        includeA.append((2 * signX * edge_from_center_L, signY * edge_from_center_W))
        includeB.append((signX * edge_from_center_W, 2 * signY * edge_from_center_L))
    
    edgesToFil = edges_in_plane(box, STGS.baseThickness, (includeA, includeB), (exclude, ))
    box = bulk_fillet(doc, box, STGS.gripFilRadConcave, edgesToFil)

    return box
