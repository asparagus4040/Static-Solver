class Unknown:
    def __init__(self, pointName, name, vector, unknownType):
        self.point = pointName
        self.name = name
        self.vector = vector
        self.unknownType = unknownType
    
    def printInfo(self):
        print("VARIABLE :", self.name)
        print("    POINT NAME :", self.point)
        print("    DIRECTION :", self.vector.string())
        print("    TYPE :", self.unknownType.name)
        print("")