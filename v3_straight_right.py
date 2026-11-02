from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.bulk_fillet import bulk_fillet
from my_utils.v2_center_track_utils import make_main_shell
from my_utils.warcle_torus import make_warcle_torus
from my_utils.warcle_beam import make_warcle_beam
from my_utils.v2_settings import STGS
from my_utils.squircle_torus import make_squircle_torus
from my_utils.squircle_cylinder import make_squircle_cylinder
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
import FreeCAD as App
import Part
V = App.Vector
import math

useCache = globals().get("__useCache__", False)
for3DPrint = globals().get("__for3DPrint__", False)
docName = "straight_right_v3"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    doc.removeObject(obj.Name)

def make_straight_right(doc):
    main_shell, shell_cut = make_main_shell(doc)

    hDif = STGS.trackRad - STGS.squareTrackH
    wAtTop = 2 * STGS.trackRad - 2 * hDif * STGS.warcleSlope

    edgeDist = STGS.trackSquareDim * 0.5 - STGS.defaultSlope * (STGS.trackBotZ - STGS.baseThickness)
    
    
    straight = make_warcle_beam(100, wAtTop, STGS.squareTrackH, STGS.iWarcleRad, STGS.warcleSlope)
    straight2 = make_warcle_beam(100,  wAtTop + 2 * STGS.minThickness, 
                                STGS.squareTrackH + STGS.minThickness, 
                               STGS.oWarcleRad, STGS.warcleSlope)
    straight.translate(V(0, 0, STGS.trackBotZ))
    straight2.translate(V(0, 0, STGS.trackBotZ - STGS.minThickness))
    hscDim = 50
    scDimBot = 2 * hscDim + 2 * STGS.warcleSlope * STGS.squareTrackH
    straightCut = make_wedge_cen_z_up(scDimBot, scDimBot, 
                                      STGS.squareTrackH, 2 * hscDim, 2 * hscDim)
    scRads = math.atan(15) # 15 is just an eyeballed value
    straightCut.rotate(V(0, 0, 0), V(0, 0, 1), scRads * 180 / math.pi)
    straightCut.translate(V( -hscDim * math.cos(scRads), 6+hscDim * math.sin(scRads), STGS.trackBotZ))
    straight = straight.cut(straightCut)
    #return straight
    main_shell = main_shell.cut(straight)
    shell_cut = shell_cut.cut(straight2)

    if True:
        torusRad = 0.60 * edgeDist
        cut = make_warcle_torus(torusRad, 
                                wAtTop, 
                                STGS.squareTrackH, 
                                STGS.iWarcleRad, 
                                STGS.warcleSlope,
                                45)
        cutCut = make_warcle_torus(torusRad, 
                                wAtTop + 2 * STGS.minThickness, 
                                STGS.squareTrackH + STGS.minThickness, 
                                STGS.oWarcleRad, 
                                STGS.warcleSlope,
                                45)
        
        for i in range(2):
            cut.rotate(V(0, 0, 0), V(0, 0, 1), 180)
            cutCut.rotate(V(0, 0, 0), V(0, 0, 1), 180)
            sign = 1 if i == 0 else -1
            cut.Placement.Base = V(sign * torusRad, sign * edgeDist, STGS.trackBotZ)
            if i == 0: main_shell = main_shell.cut(cut)
            cutCut.Placement.Base = V(sign * torusRad, sign * edgeDist, STGS.trackBotZ - STGS.minThickness)
            if i == 0: shell_cut = shell_cut.cut(cutCut)
        cut.Placement.Base = V(0, 0, 0)
        cut.rotate(V(0, 0, 0), V(0, 0, 1), 45)
        cutCut.Placement.Base = V(0, 0, 0)
        cutCut.rotate(V(0, 0, 0), V(0, 0, 1), 45)
        for i in range(2):
            cut.rotate(V(0, 0, 0), V(0, 0, 1), 180)
            cutCut.rotate(V(0, 0, 0), V(0, 0, 1), 180)
            sign = 1 if i == 0 else -1
            cut.Placement.Base = V(sign * edgeDist, sign * torusRad, STGS.trackBotZ)
            if i == 0: main_shell = main_shell.cut(cut)
            cutCut.Placement.Base = V(sign * edgeDist, sign * torusRad, STGS.trackBotZ - STGS.minThickness)
            if i == 0: shell_cut = shell_cut.cut(cutCut)

        cx0 = edgeDist - torusRad * math.cos(math.radians(45))
        cy0 = torusRad - torusRad * math.sin(math.radians(45))
        cx1 = cy0
        cy1 = cx0
        cenDist = math.sqrt((cx0-cx1)**2 + (cy0-cy1)**2)
        cenBeam = make_warcle_beam(cenDist, wAtTop, 
                                STGS.squareTrackH, 
                                STGS.iWarcleRad, STGS.warcleSlope)
        cenBeam2 = make_warcle_beam(cenDist,  wAtTop + 2 * STGS.minThickness, 
                                    STGS.squareTrackH + STGS.minThickness, 
                                STGS.oWarcleRad, STGS.warcleSlope)
        cenBeam.translate(V(0, 0, STGS.trackBotZ))
        cenBeam.rotate(V(0, 0, 0), V(0, 0, 1), -45)
        cenBeam.translate(V(0.5 * (cx0 + cx1), 0.5 * (cy0 + cy1), 0))
        main_shell = main_shell.cut(cenBeam)
        cenBeam.translate(V(-(cx0 + cx1), -(cy0 + cy1), 0))
        #main_shell = main_shell.cut(cenBeam)
        cenBeam2.translate(V(0, 0, STGS.trackBotZ - STGS.minThickness))
        cenBeam2.rotate(V(0, 0, 0), V(0, 0, 1), -45)
        cenBeam2.translate(V(0.5 * (cx0 + cx1), 0.5 * (cy0 + cy1), 0))
        shell_cut = shell_cut.cut(cenBeam2)
        cenBeam2.translate(V(-(cx0 + cx1), -(cy0 + cy1), 0))
        #shell_cut = shell_cut.cut(cenBeam2)
        

    main_shell = main_shell.cut(shell_cut)

    main_shell.rotate(V(0, 0, 0), V(0, 0, 1), 45)
    slotCutDY = 50
    slotCutDX = 150
    slotCutTopDY = slotCutDY - 2 * STGS.baseThickness * STGS.defaultSlope
    slotCutTopDX = slotCutDX - 2 * STGS.baseThickness * STGS.defaultSlope
    slotCut = make_wedge_cen_z_up(slotCutDX, slotCutDY, 
                                STGS.baseThickness, slotCutTopDX, slotCutTopDY)


    for i in range(2):
        yLoc = 0.5 * STGS.inOctSlotLen - 1 + 0.5 * slotCutDY
        yLoc *= (-1 if i == 0 else 1)
        slotCut.Placement.Base = V(0, yLoc, 0)
        main_shell = main_shell.cut(slotCut)
    main_shell.rotate(V(0, 0, 0), V(0, 0, 1), 45)


    randDim = 100
    squareH = STGS.trackBotZ + STGS.squareTrackH
    randDimTop = randDim + 2 * squareH * STGS.defaultSlope
    randCut = make_wedge_cen_z_up(randDim, randDim, squareH, randDimTop, randDimTop)
    randDist = 0.5 * STGS.trackSquareTopDim + STGS.baseThickness * STGS.defaultSlope
    randCut.Placement.Base = V(0, randDist + 0.5 * randDim, 0)
    main_shell = main_shell.cut(randCut)

    topCutDim = 100
    topCut = Part.makeBox(topCutDim, topCutDim, topCutDim)
    h = STGS.trackBotZ + STGS.squareTrackH
    topCut.translate(V(-topCutDim, 3, h-2))
    main_shell = main_shell.cut(topCut)

    return main_shell


rtnPart = make_straight_right(doc)