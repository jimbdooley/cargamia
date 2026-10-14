import math

class CargamiaSettings:
    def __init__(self):
        self.defaultDraftAngle = 3
        self.defaultDraftRad = self.defaultDraftAngle * math.pi / 180
        self.defaultSlope = math.tan(self.defaultDraftRad)
        self.fltRadConcave = 2.0
        self.fltRadSmall = 1.0
        self.unitSquareDim = 50
        self.squareBaseDimInwards = 4
        self.innerSqDim = self.unitSquareDim - 2 * self.squareBaseDimInwards
        self.squareBaseDimOutwards = 4
        self.marbleDiam = 14
        self.marbleDiamMax = 15
        self.minThickness = 1.6
        self.wallThickness = self.minThickness
        self.wallSpan = self.wallThickness / math.cos(self.defaultDraftRad)
        self.sqBaseDim = self.unitSquareDim + 2 * self.squareBaseDimOutwards
        self.sqBaseDimPlusTaper = self.sqBaseDim +2 * self.minThickness * self.defaultSlope
        self.baseThickness = 2
        self.defaultTrackH = 5
        self.trackBotZ = self.baseThickness + 1.2
        self.trackRad = 15.5 / 2
        self.dz = self.trackBotZ + self.marbleDiamMax + 1.5

STGS = CargamiaSettings()