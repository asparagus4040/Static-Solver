from src.Util import cos, sin

class KnownVar:
    def __init__(self, part, point, varType, X=0, Y=0, value=0, angle=0):
        self.part = part
        self.point = point
        self.varType = varType
        self.X = X
        self.Y = Y
        self.value = value
        self.angle = angle

    def getForceX(self):
        return self.value * cos(self.angle)

    def getForceY(self):
        return self.value * sin(self.angle)

    def getForceMoment(self):
        # inverted for the equation
        return self.Y * self.getForceX() - self.X * self.getForceY()