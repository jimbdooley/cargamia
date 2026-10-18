import FreeCAD as App
import FreeCADGui as Gui
import Part
import math
from my_utils.bulk_fillet import bulk_fillet
from my_utils.bulk_chamfer import bulk_chamfer
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.get_vert_port import getVertPort
makeMold = globals().get("__makeMold__", False)
docName = "base_square"
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
box = bulk_fillet(doc, box, STGS.fltRadConvex, [2, 3, 4, 6, 7, 8, 11, 12])
base = make_wedge_cen_z_up(
    STGS.baseDimPlusTaper, STGS.baseDimPlusTaper, STGS.baseThickness,
    STGS.baseDim, STGS.baseDim
)
box = box.fuse(base)
box = bulk_fillet(doc, box, STGS.fltRadConcave, range(21, 28 + 1))


box = bulk_chamfer(doc, box, STGS.baseCornerRad, (29, 30, 33, 35))
box = bulk_fillet(doc, box, 3 * STGS.fltRadConvex, [17, 18, 21, 23, 25, 27, 29, 31])


for i in range(1):
    vPort = getVertPort(i)
    box = box.fuse(vPort)



if makeMold:
    mold = Part.makeBox(2 * STGS.baseDim, 2 * STGS.baseDim, 3 * STGS.marbleDiamMax)
    mold.Placement.move(App.Vector(-STGS.baseDim, -STGS.baseDim, 0.05))
    box = mold.cut(box)

"""
if not makeMold:
    cutInnerLen = STGS.innerSqDim + 2 * (STGS.defaultSlope - 1) * STGS.minThickness
    cutOuterLen = cutInnerLen + 2 * STGS.defaultSlope * wedgeH
    cutWedge = make_wedge_cen_z_up(
        cutOuterLen, cutOuterLen, wedgeH,
        cutInnerLen, cutInnerLen
    )
    cutWedge.translate(App.Vector(0, 0, -STGS.baseThickness))

    box = box.cut(cutWedge)


"""
rtnPart = vPort

