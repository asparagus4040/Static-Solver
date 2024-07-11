from src.Util import cos, sin

class UnknownVar:
    def __init__(self, name, partName, pointName, varType, X=0, Y=0, angle=0, sign=0):
        self.name = name
        self.part = partName
        self.point = pointName
        self.varType = varType
        self.X = X
        self.Y = Y
        self.angle = angle
        self.sign = sign

    def getVectorX(self):
        return cos(self.angle)
    
    def getVectorY(self):
        return sin(self.angle)
    
    def getVectorMoment(self):
        return self.X * self.getVectorY() - self.Y * self.getVectorX()