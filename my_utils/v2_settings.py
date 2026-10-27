import math

class CargamiaSettingsV2:
    def __init__(self):
        
        self.gap = 66
        self.marbleDiam = 11
        self.marbleDiamMax = 13
        self.minThickness = 1.6
        self.trackThickness = 1.4
        self.pillarPortTopEdgeThickness = 1.3
        self.wallThickness = self.minThickness
        self.baseThickness = self.wallThickness
        self.defaultDraftAngle = 6
        self.defaultSlope = math.tan(math.radians(self.defaultDraftAngle))
        self.octoEnterAngle = 6
        self.octoEnterSlope = math.tan(math.radians(self.octoEnterAngle))
        self.octoCenterCutAngle = 12
        self.octoCenterCutSlope = math.tan(math.radians(self.octoCenterCutAngle))
        self.defaultTrackH = 5
        self.squareTrackH = 5
        self.trackBotZ = self.baseThickness + 1.4 + self.minThickness
        self.trackBotZInc = self.trackBotZ + 0.7
        self.trackBotZOut = self.trackBotZ - 0.4

        self.trackRad = (1 + self.marbleDiamMax) / 2
        self.dz = self.trackBotZ + self.marbleDiamMax + 1.5

        self.plrZGap = self.minThickness
        self.plrThickness = 25.4 / 16
        self.plrWidth = 13.5
        self.plrPortDepth = 4.5
        self.plrPlatformWidth = self.plrWidth + 2 * self.pillarPortTopEdgeThickness + 1.25
        self.plrPlatformDepth = 4 * self.minThickness
        self.plrPlatformEdgeB4Corner = 3 * self.minThickness
        self.plrSlotDraftAngle = 3
        self.plrSlotDraftRad = math.radians(self.plrSlotDraftAngle)
        self.plrSlotSlope = math.tan(self.plrSlotDraftRad)
        self.plrSlotTopWidth = self.plrPlatformWidth - 2 * self.pillarPortTopEdgeThickness
        self.plrSlotTopDepth = self.plrPlatformDepth - 2 * self.minThickness
        self.plrSlotPinsarLen = 3.1

        self.octoDim = 52
        self.octoH = 2 * self.plrPortDepth + self.plrZGap
        self.octoDimDiff = self.octoH * self.defaultSlope
        self.octoDimTop = self.octoDim - 2 * self.octoDimDiff
        self.octoCornerDim = self.plrPlatformWidth + 2 * self.octoDimDiff * math.tan(math.pi/8)
        self.octoDim2 = self.octoDim - self.octoCornerDim * math.sqrt(2) 
        self.centerSlotH = 2 * self.baseThickness
        self.centerSlotDepth = 1 * self.baseThickness
        self.centerGuideH = 0.6 * self.minThickness
        self.centerGuideAngle = 15
        self.octoEdgeTrim = 0.5

        self.inOctDim = 29
        self.inOctDim2 = 9
        self.inOctSlotLen = 9
        self.inOctSlotDepth = 2

        self.trackSquareTopDim = 32
        self.trackSquareDim = self.trackSquareTopDim
        self.trackSquareDim += 2 * self.baseThickness * self.defaultSlope

        self.trackSlotAngle = 8
        self.trackSlotSlope = math.tan(math.radians(self.trackSlotAngle))
        self.trackSlotTopDepth = 5
        self.trackSlotTopWidth = 2.9
        self.trackSlotDistFromEdge = 3
        self.trackSlotPeakZ = 5

        self.edgeCutTopDiag = self.octoDimTop - 2 * (0.5 ** 0.5) * self.plrPlatformWidth
        

STGS = CargamiaSettingsV2()