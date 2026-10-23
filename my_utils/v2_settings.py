import math

class CargamiaSettingsV2:
    def __init__(self):
        
        self.gap = 66
        self.marbleDiam = 11
        self.marbleDiamMax = 13
        self.minThickness = 1.6
        self.pillarPortTopEdgeThickness = 1.3
        self.wallThickness = self.minThickness
        self.baseThickness = self.wallThickness
        self.defaultDraftAngle = 6
        self.defaultDraftRad = math.radians(self.defaultDraftAngle)
        self.defaultSlope = math.tan(self.defaultDraftRad)
        self.defaultTrackH = 5 * self.marbleDiam / 11
        self.trackBotZ = self.baseThickness + 2.2
        self.trackBotZInc = self.trackBotZ + 0.8
        self.trackBotZOut = self.trackBotZ - 0.5

        self.trackRad = (2 + self.marbleDiamMax) / 2
        self.dz = self.trackBotZ + self.marbleDiamMax + 1.5

        self.crnFlttnDraftAngle = 4
        self.crnFlttnDraftRad = math.radians(self.crnFlttnDraftAngle)
        self.crnFlttnSlope = math.tan(self.crnFlttnDraftRad)

        self.plrZGap = self.minThickness
        self.plrThickness = 25.4 / 16
        self.plrWidth = 13.5
        self.plrPortDepth = 4.5
        self.plrPlatformWidth = self.plrWidth + 2 * self.pillarPortTopEdgeThickness + 1.25
        self.plrPlatformDepth = 4 * self.minThickness
        self.plrPlatformEdgeB4Corner = 2.25 * self.minThickness
        self.plrSlotDraftAngle = 3
        self.plrSlotDraftRad = math.radians(self.plrSlotDraftAngle)
        self.plrSlotSlope = math.tan(self.plrSlotDraftRad)
        self.plrSlotTopWidth = self.plrPlatformWidth - 2 * self.pillarPortTopEdgeThickness
        self.plrSlotTopDepth = self.plrPlatformDepth - 2 * self.minThickness
        self.plrSlotPinsarLen = 3.5

        self.octoDim = 52
        self.octoH = 2 * self.plrPortDepth + self.plrZGap
        self.octoDimDiff = self.octoH * self.defaultSlope
        self.octoDimTop = self.octoDim - 2 * self.octoDimDiff
        self.octoCornerDim = self.plrPlatformWidth + 2 * self.octoDimDiff * math.tan(math.pi/8)
        self.octoDim2 = self.octoDim - self.octoCornerDim * math.sqrt(2) 

        self.inOctDim = 26
        self.inOctDim2 = 13
        self.inOctSlotLen = 10
        self.inOctSlotDepth = 3

        self.trackSlotTopW = self.minThickness + 0.2
        self.trackSlotTopL = 5
        self.trackSlotTopGap = 16
        self.trackSlotTopDist = 0.5 * self.octoDim - 0.5 * self.trackSlotTopL - 2.5

        self.edgeCutTopDiag = self.octoDimTop - 2 * (0.5 ** 0.5) * self.plrPlatformWidth
        

STGS = CargamiaSettingsV2()