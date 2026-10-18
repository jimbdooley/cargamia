import math

class CargamiaSettings:
    def __init__(self):
        self.marbleDiam = 11
        self.marbleDiamMax = 13
        self.minThickness = 1.6
        self.defaultDraftAngle = 3
            
        self.defaultDraftRad = self.defaultDraftAngle * math.pi / 180
        self.defaultSlope = math.tan(self.defaultDraftRad)
        self.unitSquareDim = 50 * self.marbleDiam / 11
        self.baseDimInwards = 4 
        self.innerSqDim = self.unitSquareDim - 2 * self.baseDimInwards
        self.baseDimOutwards = 6
        self.baseCornerRad = 8 * self.marbleDiam / 11
        
        self.wallThickness = self.minThickness
        self.baseThickness = self.wallThickness
        self.fltRadConcave = 0.5 * self.wallThickness
        self.fltRadConvex = 1.5 * self.wallThickness
        self.fltRadTrack = 1.0
        self.wallSpan = self.wallThickness / math.cos(self.defaultDraftRad)
        self.baseDim = self.unitSquareDim + 2 * self.baseDimOutwards
        self.baseDimPlusTaper = self.baseDim +2 * self.minThickness * self.defaultSlope
        
        self.defaultTrackH = 5 * self.marbleDiam / 11
        self.trackBotZ = self.baseThickness + 3
        self.trackRad = (0.6 + self.marbleDiam) / 2
        self.dz = self.trackBotZ + self.marbleDiamMax + 1.5

        self.plrThickness = self.minThickness
        self.plrDZ = 0.5
        self.plrMidLen = 6
        self.plrEdgeLen = 6
        self.plrMidSocketLen = 4
        self.plrEdgeSocketLen = 3
        self.plrSocketDepth = 4.5
        self.plrFoldAngle = 40
        self.plrSocketDraftAngle = 3

        self.portDraftAngle = self.plrSocketDraftAngle
        self.portDraftSlope = math.tan(math.radians(self.portDraftAngle))
        self.portFoldAngle = self.plrFoldAngle - 2.5
        self.portExpand = 0.25
        self.portH = 2 * self.plrSocketDepth + self.plrDZ
        self.portMidThickness = self.baseThickness
        self.portMidThickness += 0.5 * self.portH * self.portDraftSlope
        self.portMidThickness -= 0.5 * self.portH * self.defaultSlope
        self.portTopThickness = self.portMidThickness
        self.portTopThickness -= 0.5 * self.portH * (self.defaultSlope + self.portDraftSlope)
        self.portTopWidth = 2 * self.portTopThickness + self.plrThickness + self.portExpand
        self.portBotWidth = self.portTopWidth + self.portH * 2 * self.defaultSlope
        self.portLocRad = 2 + 0.7071 * self.innerSqDim + 0.5 * self.portBotWidth
        self.portSideChamferRad = 0.45 * self.portTopWidth
        self.portTopChamferRad = 0.49 * self.portTopThickness


STGS = CargamiaSettings()