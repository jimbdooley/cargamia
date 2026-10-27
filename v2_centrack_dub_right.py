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

main_shell = make_main_shell(doc)
cut = Part.makeTorus(STGS.trackSquareDim / 2, STGS.trackRad)
cutZ = STGS.trackRad + STGS.trackBotZ
cut.Placement.Base = V(-STGS.trackSquareDim / 2, -STGS.trackSquareDim / 2, cutZ)
main_shell = main_shell.cut(cut)
cut.Placement.Base = V(STGS.trackSquareDim / 2, STGS.trackSquareDim / 2, cutZ)
main_shell = main_shell.cut(cut)

rtnPart = main_shell