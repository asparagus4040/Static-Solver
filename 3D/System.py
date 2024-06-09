from Enums import Constraint

class System:
    def __init__(self):
        self.mat = []
        self.points = []
        self.knownVars = []
        self.unknownVars = []
    
    def newPoint(self, name, posX, posY, posZ):
        self.points[name] = {"X": posX, "Y": posY, "Z": posZ}