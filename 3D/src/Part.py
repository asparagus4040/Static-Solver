class Part:
    def __init__(self, name, pointList):
        self.name = name
        self.pointList = pointList
    
    def printInfo(self):
        print("PART :", self.name)
        print("    POINTS :", " ".join(self.pointList))