from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.bulk_fillet import bulk_fillet
from my_utils.v2_center_track_utils import make_main_shell
from my_utils.v2_settings import STGS
from my_utils.v2_octo_center_ops import octo_center_ops_v2
from my_utils.v2_shape_pillar_port import shape_pillar_port_v2
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
import FreeCAD as App
import Part
V = App.Vector
import math

useCache = globals().get("__useCache__", False)
for3DPrint = globals().get("__for3DPrint__", False)
docName = "centrack_dub_right_v2"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    doc.removeObject(obj.Name)

main_shell, shell_cut = make_main_shell(doc)
cut = Part.makeTorus(STGS.trackSquareDim / 2, STGS.trackRad)
cutCut = Part.makeTorus(STGS.trackSquareDim / 2, STGS.trackRad + STGS.minThickness)
cutZ = STGS.trackRad + STGS.trackBotZ

cut.Placement.Base = V(-STGS.trackSquareDim / 2, -STGS.trackSquareDim / 2, cutZ)
main_shell = main_shell.cut(cut)
cut.Placement.Base = V(STGS.trackSquareDim / 2, STGS.trackSquareDim / 2, cutZ)
main_shell = main_shell.cut(cut)

cutCut.Placement.Base = V(-STGS.trackSquareDim / 2, -STGS.trackSquareDim / 2, cutZ)
shell_cut = shell_cut.cut(cutCut)
cutCut.Placement.Base = V(STGS.trackSquareDim / 2, STGS.trackSquareDim / 2, cutZ)
shell_cut = shell_cut.cut(cutCut)

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

rtnPart = main_shell