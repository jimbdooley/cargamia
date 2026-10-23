from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.v2_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.bulk_fillet import bulk_fillet
import FreeCAD as App
import Part
V = App.Vector
import math

useCache = globals().get("__useCache__", False)
for3DPrint = globals().get("__for3DPrint__", False)
docName = "pillar_v2"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    doc.removeObject(obj.Name)

def getPillar_v2(for3DPrint, n):
    thickness = STGS.plrThickness * (0.6 if for3DPrint else 1)
    plrHeight = n * STGS.dz - STGS.plrZGap
    rtn = Part.makeBox(STGS.plrWidth, thickness, plrHeight)  # Example placeholder for the pillar part
    return rtn

rtnPart = getPillar_v2(for3DPrint, 1)