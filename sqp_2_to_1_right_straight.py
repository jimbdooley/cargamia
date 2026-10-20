from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.bulk_fillet import bulk_fillet
import FreeCAD as App
import Part

useCache = globals().get("__useCache__", False)
for3DPrint = globals().get("__for3DPrint__", False)
docName = "two_to_one_right_straight"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)

sq, botCut, midFuse = get_base_square(doc, useCache)

torusBigRad = 0.5 * STGS.innerSqDim
trackCut = Part.makeCylinder(STGS.trackRad, 100)
trackCut.rotate(App.Vector(0, 0, 50), App.Vector(1, 0, 0), 90)
trackCut.translate(App.Vector(0, 0, -50 + STGS.trackRad + STGS.trackBotZ))
sq = sq.cut(trackCut)
trackCut2 = Part.makeCylinder(STGS.trackRad + STGS.minThickness, 100)
trackCut2.rotate(App.Vector(0, 0, 50), App.Vector(1, 0, 0), 90)
trackCut2.translate(App.Vector(0, 0, -50 + STGS.trackRad + STGS.trackBotZ))
botCut = botCut.cut(trackCut2)
for i in range(1):
    sign = 1 if i == 0 else -1
    shift = -sign * torusBigRad
    torus = Part.makeTorus(torusBigRad, STGS.trackRad, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
    torus.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 180 - 180 * i)
    torus.Placement.move(App.Vector(shift,-torusBigRad, STGS.trackBotZ + STGS.trackRad))
    torus = torus.common(midFuse)

    torus2 = Part.makeTorus(torusBigRad, STGS.trackRad + STGS.minThickness, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
    torus2 = torus2.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 180 - 180 * i)
    torus2.Placement.move(App.Vector(shift,-torusBigRad, STGS.trackBotZ + STGS.trackRad))
    torus2 = torus2.common(midFuse)

    trackCut = trackCut.fuse(torus)
    trackCut2 = trackCut2.fuse(torus2)

sq = sq.cut(trackCut)
botCut = botCut.cut(trackCut2)


if True:
    __fillets__ = []
    __fillets__.append((1063,1.00,1.00))
    __fillets__.append((1071,1.00,1.00))
    __fillets__.append((1075,1.00,1.00))
    __fillets__.append((1076,1.00,1.00))
    __fillets__.append((1466,1.00,1.00))
    __fillets__.append((1468,1.00,1.00))
    __fillets__.append((1469,1.00,1.00))
    __fillets__.append((1470,1.00,1.00))
    __fillets__.append((1471,1.00,1.00))
    __fillets__.append((1472,1.00,1.00))
    __fillets__.append((1482,1.00,1.00))
    __fillets__.append((1483,1.00,1.00))
    __fillets__.append((1484,1.00,1.00))
    __fillets__.append((1485,1.00,1.00))
    __fillets__.append((1486,1.00,1.00))
    sq =  bulk_fillet(doc, sq, STGS.fltRadTrack, [e[0] for e in __fillets__])
    del __fillets__

if not for3DPrint:
    sq = sq.cut(botCut)
    sq = trim_cut_bot_base_square(doc, sq)



rtnPart = sq