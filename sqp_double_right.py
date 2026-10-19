from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.bulk_fillet import bulk_fillet
import FreeCAD as App
import Part

docName = "base_square"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)

sq, botCut, midFuse = get_base_square(doc)

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

__fillets__ = []
__fillets__.append((1111,1.00,1.00))
__fillets__.append((1119,1.00,1.00))
__fillets__.append((1123,1.00,1.00))
__fillets__.append((1131,1.00,1.00))
__fillets__.append((1547,1.00,1.00))
__fillets__.append((1548,1.00,1.00))
__fillets__.append((1549,1.00,1.00))
__fillets__.append((1550,1.00,1.00))
__fillets__.append((1551,1.00,1.00))
__fillets__.append((1552,1.00,1.00))
__fillets__.append((1560,1.00,1.00))
__fillets__.append((1561,1.00,1.00))
__fillets__.append((1562,1.00,1.00))
__fillets__.append((1563,1.00,1.00))
__fillets__.append((1564,1.00,1.00))
__fillets__.append((1565,1.00,1.00))
sq =  bulk_fillet(doc, sq, STGS.fltRadTrack, [e[0] for e in __fillets__])

__fillets__ = []
__fillets__.append((1324,0.60,0.60))
__fillets__.append((1332,0.60,0.60))
__fillets__.append((1538,0.60,0.60))
__fillets__.append((1540,0.60,0.60))
__fillets__.append((1541,0.60,0.60))
__fillets__.append((1542,0.60,0.60))
__fillets__.append((1543,0.60,0.60))
__fillets__.append((1544,0.60,0.60))
#sq =  bulk_fillet(doc, sq, STGS.fltRadTrack, [e[0] for e in __fillets__])
del __fillets__

rtnPart = sq.cut(botCut)
rtnPart = trim_cut_bot_base_square(doc, rtnPart)