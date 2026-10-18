from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.bulk_fillet import bulk_fillet
import FreeCAD as App
import Part
import math

def getVertPort(i):
    pad = 2
    midPad = 0
    edgeLen = STGS.plrEdgeLen - 1 + STGS.portTopThickness
    center = make_wedge_cen_z_up(
        STGS.portBotWidth, 2 * midPad + STGS.plrMidLen,
        STGS.portH,
        STGS.portTopWidth, 2 * midPad + STGS.plrMidLen
    )
    cutter = make_wedge_cen_z_up(
        STGS.portTopWidth, 10 * (2 * midPad + STGS.plrMidLen),
        STGS.portH,
        STGS.portBotWidth, 10 * (2 * midPad + STGS.plrMidLen)
    )
    dx = STGS.portLocRad * math.cos(math.pi/4 + i * math.pi/2)
    dy = STGS.portLocRad * math.sin(math.pi/4 + i * math.pi/2)
    center.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 45 + i * 90)
    center.translate(App.Vector(dx, dy, 0))
    cutterDRad = -0.001 + 0.5 * (STGS.portTopWidth + STGS.portBotWidth)
    cutterDx = (STGS.portLocRad + cutterDRad) * math.cos(math.pi/4 + i * math.pi/2)
    cutterDy = (STGS.portLocRad + cutterDRad) * math.sin(math.pi/4 + i * math.pi/2)
    cutter.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 45 + i * 90)
    cutter.translate(App.Vector(cutterDx, cutterDy, 0))
    for j in range(2):
        sign = 1 if j == 0 else -1
        edgeA = make_wedge_cen_z_up(
            STGS.portBotWidth, pad + edgeLen + STGS.portBotWidth - STGS.portTopWidth,
            STGS.portH,
            STGS.portTopWidth, pad + edgeLen
        )
        edgeA.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 45 + i * 90 - sign * STGS.plrFoldAngle)
        travelRad = i * math.pi/2 + math.pi/4 - sign * math.pi / 2
        edgeADx = dx + 0.5 * STGS.plrMidLen * math.cos(travelRad)
        edgeADy = dy + 0.5 * STGS.plrMidLen * math.sin(travelRad)
        travelRad -= sign * math.radians(STGS.plrFoldAngle)
        edgeADx += 0.5 * (edgeLen - pad) * math.cos(travelRad)
        edgeADy += 0.5 * (edgeLen - pad) * math.sin(travelRad)
        edgeA.translate(App.Vector(edgeADx, edgeADy, 0))
        center = center.fuse(edgeA)

    center = center.cut(cutter)
    sideEdges = [12, 18, 32, 48, 49, 50, 51, 52]
    center = bulk_fillet(App.ActiveDocument, center, STGS.portSideChamferRad, sideEdges)
    topEdges = [
        6, 8, 10, 23, 29, 
        30, 31, 32, 34, 36, 
        46, 61, 62, 63, 64,
        65, 66, 67
    ]
    #center = bulk_fillet(App.ActiveDocument, center, STGS.portTopChamferRad, topEdges)
    return center