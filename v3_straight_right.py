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

    torusRad = STGS.trackSquareDim * 0.5
    cut = make_warcle_torus(torusRad, 2*STGS.trackRad, STGS.squareTrackH, STGS.iWarcleRad, STGS.warcleSlope)
    cutCut = make_warcle_torus(torusRad, 2*(STGS.trackRad + STGS.minThickness), STGS.squareTrackH + STGS.minThickness, STGS.oWarcleRad, STGS.warcleSlope)

    cut.Placement.Base = V(torusRad, torusRad, STGS.trackBotZ)
    main_shell = main_shell.cut(cut)
    cutCut.Placement.Base = V(torusRad, torusRad, STGS.trackBotZ - STGS.minThickness)
    shell_cut = shell_cut.cut(cutCut)

    beam = make_warcle_beam(100, 2 * STGS.trackRad, STGS.squareTrackH, STGS.iWarcleRad, STGS.warcleSlope)
    beam.translate(V(0, 0, STGS.trackBotZ))
    main_shell = main_shell.cut(beam)

    outerW = 2 * (STGS.trackRad + STGS.minThickness)
    beam2 = make_warcle_beam(100, outerW, STGS.squareTrackH, STGS.oWarcleRad, STGS.warcleSlope)
    beam2.translate(V(0, 0, STGS.trackBotZ - STGS.minThickness))
    shell_cut = shell_cut.cut(beam2)

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
    return main_shell


rtnPart = make_straight_right(doc)