from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.bulk_fillet import bulk_fillet
import FreeCAD as App
import Part

useCache = globals().get("__useCache__", False)
docName = "double_right"
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
    torus.Placement.move(App.Vector(shift,shift, STGS.trackBotZ + STGS.trackRad))
    torus = torus.common(midFuse)

    torus2 = Part.makeTorus(torusBigRad, STGS.trackRad + STGS.minThickness, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
    torus2 = torus2.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 180 - 180 * i)
    torus2.Placement.move(App.Vector(shift,shift, STGS.trackBotZ + STGS.trackRad))
    torus2 = torus2.common(midFuse)

    sq = sq.cut(torus)
    botCut = botCut.cut(torus2)


sq = sq.cut(botCut)
sq = trim_cut_bot_base_square(doc, sq)

doc.recompute()

try:
    fltR1 = [1111, 1123, 1547, 1548, 1549, 1550, 1551, 1552]
    sq =  bulk_fillet(doc, sq, STGS.fltRadTrack, fltR1)
    fltR2 = [50, 204, 219, 222, 223, 224, 225, 226]
    sq =  bulk_fillet(doc, sq, STGS.fltRadTrack, fltR2)
    __fillets__ = []
    __fillets__.append((1324,0.80,0.80))
    __fillets__.append((1332,0.80,0.80))
    __fillets__.append((1336,0.80,0.80))
    __fillets__.append((1343,0.80,0.80))
    __fillets__.append((1538,0.80,0.80))
    __fillets__.append((1540,0.80,0.80))
    __fillets__.append((1541,0.80,0.80))
    __fillets__.append((1542,0.80,0.80))
    __fillets__.append((1543,0.80,0.80))
    __fillets__.append((1544,0.80,0.80))
    __fillets__.append((1555,0.80,0.80))
    __fillets__.append((1556,0.80,0.80))
    __fillets__.append((1557,0.80,0.80))
    __fillets__.append((1558,0.80,0.80))
    __fillets__.append((1559,0.80,0.80))
    __fillets__.append((1560,0.80,0.80))
    sq =  bulk_fillet(doc, sq, STGS.fltRadConcave, [e[0] for e in __fillets__])
    del __fillets__
except Exception as e:
    print(f"Error applying bulk fillet: {e}")



rtnPart = sq