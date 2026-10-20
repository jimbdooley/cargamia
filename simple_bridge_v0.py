from my_utils.make_base_square import get_base_square, trim_cut_bot_base_square
from my_utils.cargamia_settings import STGS
from my_utils.wedge_centered_zup import make_wedge_cen_z_up
from my_utils.bulk_fillet import bulk_fillet
import FreeCAD as App
import Part
import math

useCache = globals().get("__useCache__", False)
for3DPrint = globals().get("__for3DPrint__", False)
docName = "simple_bridge"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    doc.removeObject(obj.Name)

def get_simple_bridge(slotDelta=0):
    bridge = Part.makeCylinder(STGS.trackRadOld + STGS.minThickness, STGS.gap)
    bridge.translate(App.Vector(0, 0, -0.5 * STGS.gap))
    bridge.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
    bridge.Placement.Base = App.Vector(-0.5 * STGS.gap, 0, STGS.trackBotZ + STGS.trackRadOld)

    supportLen = STGS.gap - 2.8
    bridgeSupport = Part.makeBox(supportLen, 2*(STGS.trackRadOld + STGS.minThickness), 20)
    bridgeSupport.Placement.Base = App.Vector(-0.5 * supportLen, - (STGS.trackRadOld + STGS.minThickness), STGS.baseThickness)
    bridge = bridge.fuse(bridgeSupport)

    bridgeInner = Part.makeCylinder(STGS.trackRadOld, STGS.gap)
    bridgeInner.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
    bridgeInner.Placement.Base = App.Vector(-0.5 * STGS.gap, 0, STGS.trackBotZ + STGS.trackRadOld)
    bridge = bridge.cut(bridgeInner)

    bridgeLatchWidth = STGS.gripGap + 5
    bridgeLatchLength = STGS.brdgPastGrip * 2 + STGS.gripL
    bridgeLatch = Part.makeBox(bridgeLatchLength, bridgeLatchWidth, STGS.minThickness)
    bridgeLatchX = 0.5 * STGS.gap - bridgeLatchLength + STGS.brdgPastGrip - STGS.gripDEdge
    bridgeLatch.Placement.Base = App.Vector(bridgeLatchX, -0.5 * bridgeLatchWidth, STGS.baseThickness)
    bridge = bridge.fuse(bridgeLatch)
    bridgeLatch2 = bridgeLatch.copy()
    bridgeLatch2.Placement.Base = App.Vector(-bridgeLatchX - bridgeLatchLength, -0.5 * bridgeLatchWidth, STGS.baseThickness)
    bridge = bridge.fuse(bridgeLatch2)
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
                0
            )
            bridge = bridge.cut(latchSlotCutterCopy)
    

    topCut = Part.makeBox(2*STGS.gap, 2*STGS.gap, STGS.gap)
    topCut.Placement.Base = App.Vector(-STGS.gap, -STGS.gap, STGS.trackBotZ + STGS.defaultTrackH)
    bridge = bridge.cut(topCut)
    sideCutH = STGS.trackBotZ + STGS.defaultTrackH
    sideCutDX = sideCutH * math.tan(STGS.defaultDraftRad)
    sideCutter = make_wedge_cen_z_up(
        10 + 2 * sideCutDX, 4 * STGS.trackRadOld, sideCutH,
        10, 4 * STGS.trackRadOld
    )
    sideCutter.translate(App.Vector(-5 - 0.5 * STGS.gap, 0, 0))
    bridge = bridge.cut(sideCutter.copy())
    sideCutter.translate(App.Vector(10 + STGS.gap, 0, 0))
    bridge = bridge.cut(sideCutter)
                                   
    return bridge


rtnPart = get_simple_bridge(0.5)
