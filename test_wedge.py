import FreeCAD as App
import FreeCADGui as Gui
import Part
import math
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up

makeMold = globals().get("__makeMold__", False)
docName = "wedge_test23"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)

for obj in list(doc.Objects):
    doc.removeObject(obj.Name)

wedgeH = STGS.defaultTrackH + STGS.trackBotZ
wedgeBaseDxy = wedgeH * STGS.defaultSlope
wedgeDim = STGS.innerSqDim + 2 * wedgeBaseDxy
box = make_wedge_cen_z_up(wedgeDim, wedgeDim, wedgeH, STGS.innerSqDim, STGS.innerSqDim)
box = box.makeFillet(STGS.fltRadConvex, [box.Edges[i] for i in [1, 2, 3, 5, 6, 7, 10, 11]])
base = make_wedge_cen_z_up(
    STGS.baseDimPlusTaper, STGS.baseDimPlusTaper, STGS.baseThickness,
    STGS.baseDim, STGS.baseDim
)
box = box.fuse(base)

torusBigRad = 0.5 * STGS.innerSqDim
torus = Part.makeTorus(torusBigRad, STGS.trackRad, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
torus = torus.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 180)
torus.Placement.move(App.Vector(-torusBigRad,-torusBigRad, STGS.trackBotZ + STGS.trackRad))
torus2 = Part.makeTorus(torusBigRad, STGS.trackRad + STGS.minThickness, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
torus2 = torus2.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 180)
torus2.Placement.move(App.Vector(-torusBigRad,-torusBigRad, STGS.trackBotZ + STGS.trackRad))
box = box.cut(torus)

__fillets__ = [49, 55, 69, 70, 71, 72, 73, 74, 75]
#box = box.makeFillet(STGS.fltRadTrack, [box.Edges[i] for i in __fillets__])

if not makeMold:
    cutInnerLen = STGS.innerSqDim + 2 * (STGS.defaultSlope - 1) * STGS.minThickness
    cutOuterLen = cutInnerLen + 2 * STGS.defaultSlope * wedgeH
    cutWedge = make_wedge_cen_z_up(
        cutOuterLen, cutOuterLen, wedgeH,
        cutInnerLen, cutInnerLen
    )
    cutWedge.translate(App.Vector(0, 0, -STGS.baseThickness))
    cutWedge = cutWedge.cut(torus2)

    box = box.cut(cutWedge)


if makeMold:
    mold = Part.makeBox(2 * STGS.baseDim, 2 * STGS.baseDim, 3 * STGS.marbleDiamMax)
    mold.Placement.move(App.Vector(-STGS.baseDim, -STGS.baseDim, 0.05))
    box = mold.cut(box)

rtnPart = box

