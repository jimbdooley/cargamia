from my_utils.v2_center_track_utils import fit_track_ends
from my_utils.v2_make_claw import uncover_claw
from my_utils.v2_settings import STGS
from my_utils.simple_cache import get_cached, store_cached
from my_utils.make_s_tube import make_s_tube
from my_utils.v2_get_octo import getOcto_v2
from my_utils.v2_make_claw import make_claw_v2, make_base_claw
from my_utils.warcle_beam import make_warcle_beam
import FreeCAD as App
import Part
import math
V = App.Vector

for3DPrint = globals().get("__for3DPrint__", False)
docName = "click_track_v3"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    if obj.Name.startswith("ctcache_"):
        continue
    doc.removeObject(obj.Name)

def get_click_track(for3DPrint, n):
    overlap = STGS.minThickness
    innerH = 5.5
    outerH = innerH + STGS.minThickness
    wAtTop = 2 * STGS.trackRad - 2 * (STGS.trackRad - innerH) * STGS.warcleSlope
    clawA = make_base_claw()
    clawCut = Part.makeBox(100, 100, 100)
    clawCut.translate(V(-50, -50, 6))
    clawA = clawA.cut(clawCut)
    clawB = clawA.copy()
    clawB.rotate(V(0, 0, 0), V(0, 0, 1), 180)
    clawDist = 0.5 * (STGS.gap + STGS.trackSquareTopDim) - STGS.getPathSlotDist()
    clawDist -= (0.5 * STGS.clawBotExtra - STGS.clawOverhang) 
    clawA.translate(V(-clawDist, 0, 0))
    clawB.translate(V(clawDist, 0, 0.5*STGS.dz))

    
    drop = 1
    netDZ = 0.5 * STGS.dz + STGS.trackBotZOut - STGS.trackBotZInc
    dzPerUnit = (netDZ - (n-1) * drop) / n
    dxPerUnit = STGS.gap / n + overlap * (n - 1) / n
    unitDist = math.sqrt(dzPerUnit**2 + dxPerUnit**2)
    oWAtTop = wAtTop + 2 * STGS.minThickness
    clickTrackAngle = math.atan(dzPerUnit / dxPerUnit)
    x0 = -0.5*STGS.gap + 0.5 * dxPerUnit * math.cos(clickTrackAngle)
    z0 = STGS.trackBotZInc + 0.5 * dxPerUnit * math.sin(clickTrackAngle)

    clickTrack = clawA.fuse(clawB)
    finalBuf = 2
    for i in range(n):
        beamDist = unitDist + float(i + 1 == n) * finalBuf
        beam = make_warcle_beam(beamDist, wAtTop, innerH, STGS.iWarcleRad, STGS.warcleSlope)
        oBeam = make_warcle_beam(beamDist, oWAtTop, outerH, STGS.oWarcleRad, STGS.warcleSlope)
        beam.translate(V(0, 0, STGS.minThickness))
        uncut = beam.copy()
        beam = oBeam.cut(beam)
        beam.rotate(V(0, 0, 0), V(0, 1, 0), -clickTrackAngle * 180 / math.pi)
        uncut.rotate(V(0, 0, 0), V(0, 1, 0), -clickTrackAngle * 180 / math.pi)
        x = x0 + i * (dxPerUnit * math.cos(clickTrackAngle) - overlap)
        z = z0 + i * (dxPerUnit * math.sin(clickTrackAngle) + drop) - STGS.minThickness
        if i + 1 == n:
            x += 0.5 * finalBuf * math.cos(clickTrackAngle)
            z += 0.5 * finalBuf * math.sin(clickTrackAngle)
        beam.translate(V(x, 0, z))
        uncut.translate(V(x, 0, z))
        if clickTrack is None:
            clickTrack = beam
        else:
            clickTrack = clickTrack.cut(uncut)
            clickTrack = clickTrack.fuse(beam)

    clickTrack = fit_track_ends(clickTrack, 0.5 * STGS.dz)
    
    clickTrack = uncover_claw(doc, clickTrack, 0.5 * STGS.dz)
    clickTrack = clickTrack.removeSplitter()
    return clickTrack


track = get_click_track(for3DPrint, 6)

if True:
    baseOcto = get_cached(doc, "ctcache_baseOcto")
    if baseOcto is None:
        print("Generating base octo...")
        baseOcto = getOcto_v2(doc, False, True, True)
        store_cached(doc, "ctcache_baseOcto", baseOcto)
    octoA = baseOcto.Shape.copy()
    octoB = baseOcto.Shape.copy()
    dist = 0.5 * (STGS.gap + STGS.trackSquareTopDim)
    octoA.translate(V(-dist, 0, 0))
    octoB.translate(V(dist, 0, 0.5 * STGS.dz))

rtnPart = track