from my_utils.make_base_square import make_base_square
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.bulk_fillet import bulk_fillet
import FreeCAD as App
import Part

makeMold = globals().get("__makeMold__", False)
docName = "base_square"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)

for obj in list(doc.Objects):
    doc.removeObject(obj.Name)

sq, botCut = make_base_square(doc, makeMold)
rtnPart = sq.cut(botCut)


"""
topBotCutters = [getPortCut(i) for i in range(4)]
rtnPart = topBotCutters[0][0]
"""
