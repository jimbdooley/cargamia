from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.bulk_fillet import bulk_fillet
import FreeCAD as App
import Part
import math

def getPortCut(i):
    edgePad = 1
    edgeLen = STGS.plrEdgeLen - 1
    topCutW = STGS.plrThickness + STGS.portExpand
    midCutW = STGS.plrThickness + STGS.portExpand - STGS.portH * STGS.portDraftSlope
    topCut = make_wedge_cen_z_up(
        midCutW, STGS.plrMidLen, 0.5 * STGS.portH,
        topCutW, STGS.plrMidLen
    )
    topCutCutter = make_wedge_cen_z_up(
        topCutW, 10 * STGS.plrMidLen, 0.5 * STGS.portH,
        midCutW, 10 * STGS.plrMidLen
    )
    topCut.translate(App.Vector(0, 0, 0.5 * STGS.portH))
    topCutCutter.translate(App.Vector(0, 0, 0.5 * STGS.portH))
    botCut = make_wedge_cen_z_up(
        topCutW, STGS.plrMidLen, 0.5 * STGS.portH,
        midCutW, STGS.plrMidLen
    )
    botCutCutter = make_wedge_cen_z_up(
        midCutW, 10 * STGS.plrMidLen, 0.5 * STGS.portH,
        topCutW, 10 * STGS.plrMidLen
    )
    dx = STGS.portLocRad * math.cos(math.pi/4 + i * math.pi/2)
    dy = STGS.portLocRad * math.sin(math.pi/4 + i * math.pi/2)
    for cut in (topCut, botCut):
        cut.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 45 + i * 90)
        cut.translate(App.Vector(dx, dy, 0))
    wideLen = edgeLen + 0.5 * (STGS.portBotWidth - STGS.portTopWidth)
    for j in range(2):
        sign = 1 if j == 0 else -1
        edgeTop = make_wedge_cen_z_up(
            midCutW, edgeLen, 0.5 * STGS.portH,
            topCutW, wideLen
        )
        edgeTop.translate(App.Vector(0, 0, 0.5 * STGS.portH))
        edgeBot = make_wedge_cen_z_up(
            topCutW, wideLen, 0.5 * STGS.portH,
            midCutW, edgeLen
        )
        for k in range(2):
            edge = edgeTop if k == 0 else edgeBot
            
            edge.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 45 + i * 90 - sign * STGS.plrFoldAngle)
            travelRad = i * math.pi/2 + math.pi/4 - sign * math.pi / 2
            edgeDx = dx + 0.5 * STGS.plrMidLen * math.cos(travelRad)
            edgeDy = dy + 0.5 * STGS.plrMidLen * math.sin(travelRad)
            travelRad -= sign * math.radians(STGS.plrFoldAngle)
            edgeDx += 0.5 * (edgeLen - edgePad) * math.cos(travelRad)
            edgeDy += 0.5 * (edgeLen - edgePad) * math.sin(travelRad)
            edge.translate(App.Vector(edgeDx, edgeDy, 0))
            if k == 0:
                topCut = topCut.fuse(edge)
            else:
                botCut = botCut.fuse(edge)

    cutCutterDRad = -0.001 + 0.5 * (midCutW + topCutW)
    cutCutterDx = dx + cutCutterDRad * math.cos(math.pi/4 + i * math.pi/2)
    cutCutterDy = dy + cutCutterDRad * math.sin(math.pi/4 + i * math.pi/2)
    for cutCutter in (topCutCutter, botCutCutter):
        cutCutter.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 45 + i * 90)
        cutCutter.translate(App.Vector(cutCutterDx, cutCutterDy, 0))

    topCut = topCut.cut(topCutCutter)
    botCut = botCut.cut(botCutCutter)

    filletRad = 0.48 * midCutW
    topEdges = [10, 16, 28, 44, 45, 46, 47, 48]
    botEdges = [10, 16, 28, 44, 45, 46, 47, 48]
    topCut = bulk_fillet(App.ActiveDocument, topCut, filletRad, topEdges)
    botCut = bulk_fillet(App.ActiveDocument, botCut, filletRad, botEdges)
    return topCut, botCut
