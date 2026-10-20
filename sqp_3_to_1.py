from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.bulk_fillet import bulk_fillet
import FreeCAD as App
import Part

useCache = globals().get("__useCache__", False)
docName = "three_to_one"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)

sq, botCut, midFuse = get_base_square(doc, useCache)
torusBigRad = 0.5 * STGS.innerSqDim
for i in range(2):
    sign = 1 if i == 0 else -1
    shift = - sign * torusBigRad
    torus = Part.makeTorus(torusBigRad, STGS.trackRad, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
    torus = torus.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 180 - 180 * i)
    torus.Placement.move(App.Vector(shift,torusBigRad, STGS.trackBotZ + STGS.trackRad))
    torus = torus.common(midFuse)

    torus2 = Part.makeTorus(torusBigRad, STGS.trackRad + STGS.minThickness, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
    torus2 = torus2.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 180 - 180 * i)
    torus2.Placement.move(App.Vector(shift,torusBigRad, STGS.trackBotZ + STGS.trackRad))
    torus2 = torus2.common(midFuse)

    sq = sq.cut(torus)
    botCut = botCut.cut(torus2)


sq = sq.cut(botCut)
sq = trim_cut_bot_base_square(doc, sq)



rtnPart = sq