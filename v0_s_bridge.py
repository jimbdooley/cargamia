from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.bulk_fillet import bulk_fillet
from my_utils.make_s_tube import make_s_tube
import FreeCAD as App
import Part
import math
V = App.Vector

for3DPrint = globals().get("__for3DPrint__", False)
docName = "simple_bridge"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    doc.removeObject(obj.Name)

def get_s_bridge(for3DPrint):
    slotDelta = 0.35 if for3DPrint else 0
    platformShrink = 0.35 if for3DPrint else 0
    sBridge = make_s_tube(STGS.gap-18, STGS.dz, 9, 
                        STGS.trackRadOld + STGS.minThickness, 
                        STGS.trackRadOld,
                        STGS.defaultTrackH + STGS.minThickness)
    sBridgeDZ = STGS.trackBotZ + STGS.trackRadOld
    sBridge.translate(V(-0.5 * STGS.gap, 0, sBridgeDZ))

    bridgeLatchWidth = STGS.gripGap + 5
    bridgeLatchLength = STGS.brdgPastGrip * 2 + STGS.gripL
    bridgeLatch = Part.makeBox(bridgeLatchLength, bridgeLatchWidth, STGS.minThickness - platformShrink)
    bridgeLatchX = 0.5 * STGS.gap - bridgeLatchLength + STGS.brdgPastGrip - STGS.gripDEdge
    bridgeLatch.Placement.Base = App.Vector(bridgeLatchX, -0.5 * bridgeLatchWidth, STGS.baseThickness + STGS.dz + platformShrink)
    sBridge = sBridge.fuse(bridgeLatch)
    bridgeLatch2 = bridgeLatch.copy()
    bridgeLatch2.Placement.Base = App.Vector(-bridgeLatchX - bridgeLatchLength, -0.5 * bridgeLatchWidth, STGS.baseThickness + platformShrink)
    sBridge = sBridge.fuse(bridgeLatch2)
    latchSlotDX = STGS.gripL + 0.5 * STGS.gripH * STGS.gripDraftSlope + 2 * slotDelta
    latchSlotY0 = 0.5 * STGS.gripGap - 0.5 * STGS.gripW - 0.5 * STGS.gripH * STGS.gripDraftSlope
    latchSlotY0 -= slotDelta
    latchSlotCutter = Part.makeBox(latchSlotDX, 10, 10)
    for xSign in [1, -1]:
        for ySign in [1, -1]:
            latchSlotCutterCopy = latchSlotCutter.copy()
            latchSlotCutterCopy.Placement.Base = App.Vector(
                (bridgeLatchX + 0.5 * bridgeLatchLength) * xSign - 0.5 * latchSlotDX,
                ySign * (latchSlotY0 + 5) - 5,
                STGS.dz if xSign > 0 else 0
            )
            sBridge = sBridge.cut(latchSlotCutterCopy)
    return sBridge

rtnPart = get_s_bridge(for3DPrint)