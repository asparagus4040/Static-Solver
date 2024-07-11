from src.Util import sin, cos, spacedStr
from src.Matrix import rowMult, rowSwap, rowScale
from src.Point import Point
from src.Part import Part
from src.UnknownVar import UnknownVar
from src.KnownVar import KnownVar

class System:
    def __init__(self):
        self.points = {}
        self.parts = {}
        self.knownVars = []
        self.unknownVars = []
        self.mat = []

    # functions for declaring new objects
    def newPoint(self, name, posX, posY):
        self.points[name] = Point(posX, posY)
    
    def newPart(self, name, pointList):
        self.parts[name] = Part(pointList)
    
    def newForce(self, pointName, value, angle):
        self.points[pointName].addForce(value, angle)
    
    def newMoment(self, pointName, value):
        self.points[pointName].addMoment(value)
    
    def newConstraint(self, pointName, constraintType, angle=0):
        self.points[pointName].setConstraint(constraintType, angle)

    def newUnknownForce(self, name, posX, posY, angle, partName, pointName):
        self.unknownVars.append(UnknownVar(name, partName, pointName, "force", X=posX, Y=posY, angle=angle))
    
    def newUnknownMoment(self, name, sign, partName, pointName):
        self.unknownVars.append(UnknownVar(name, partName, pointName, "moment", sign=sign))
    
    def newKnownForce(self, posX, posY, value, angle, partName, pointName):
        self.knownVars.append(KnownVar(partName, pointName, "force", X=posX, Y=posY, value=value, angle=angle))
    
    def newKnownMoment(self, value, partName, pointName):
        self.knownVars.append(KnownVar(partName, pointName, "moment", value=value))

    # other functions    
    def getUnknownVars(self):
        # clear unknown vars
        self.unknownVars = []
        # get variable order
        for partName, part in self.parts.items():
            for pointName in part.pointList:
                point: Point = self.points[pointName]
                posX = point.X
                posY = point.Y
                ct = point.constraint
                # register variables from constraints
                # and variables from intersections
                if ct == "fixed":
                    self.newUnknownForce(partName+"_"+pointName+"_X", posX, posY, 0, partName, pointName)
                    self.newUnknownForce(partName+"_"+pointName+"_Y", posX, posY, 90, partName, pointName)
                    self.newUnknownMoment(partName+"_"+pointName+"_M", 1, partName, pointName)
                elif ct == "hinge" or ct == "intHinge":
                    self.newUnknownForce(partName+"_"+pointName+"_X", posX, posY, 0, partName, pointName)
                    self.newUnknownForce(partName+"_"+pointName+"_Y", posX, posY, 90, partName, pointName)
                elif ct == "roller":
                    self.newUnknownForce(partName+"_"+pointName, posX, posY, point.constraintAngle, partName, pointName)
                    self.newUnknownMoment(partName+"_"+pointName+"M", 1, partName, pointName)
                elif ct == "wheel":
                    self.newUnknownForce(partName+"_"+pointName, posX, posY, point.constraintAngle, partName, pointName)
        print(f"{len(self.unknownVars)} unknown variables")
    
    def getKnownVars(self):
        # clear known vars
        self.knownVars = []
        # attention: forces and moments on an intersection will get registered twice
        for partName, part in self.parts.items():                    
            for pointName in part.pointList:
                point: Point = self.points[pointName]
                posX = point.X
                posY = point.Y
                # forces
                for f in point.forces:
                    self.newKnownForce(posX, posY, f.value, f.angle, partName, pointName)
                # moment
                if point.moment != 0:
                    self.newKnownMoment(point.moment, partName, pointName)
        print(f"{len(self.knownVars)} known variables")
    
    def lineX(self, partName: str):
        line = []
        # unknown
        for var in self.unknownVars:
            if var.part == partName and var.varType == "force":
                line.append(var.getVectorX())
            else:
                line.append(0)
        # known
        forceSum = 0
        for var in self.knownVars:
            if var.part == partName and var.varType == "force":
                forceSum -= var.getForceX()
        line.append(forceSum)
        self.mat.append(line)

    def lineY(self, partName: str):
        line = []
        # unknown
        for var in self.unknownVars:
            if var.part == partName and var.varType == "force":
                line.append(var.getVectorY())
            else:
                line.append(0)
        # known
        forceSum = 0
        for var in self.knownVars:
            if var.part == partName and var.varType == "force":
                forceSum -= var.getForceY()
        line.append(forceSum)
        self.mat.append(line)

    def lineM(self, partName: str):
        line = []
        # unknown
        for var in self.unknownVars:
            if var.part == partName:
                if var.varType == "force":
                    line.append(var.getVectorMoment())
                else:
                    line.append(var.sign)
            else:
                line.append(0)
        # known
        momentSum = 0
        for var in self.knownVars:
            if var.part == partName:
                if var.varType == "force":
                    momentSum += var.getForceMoment()
                else:
                    momentSum -= var.value
        line.append(momentSum)
        self.mat.append(line)

    def lineIntX(self, pointName, point):
        line = []
        for var in self.unknownVars:
            if var.point == pointName and var.varType == "force":
                line.append(var.getVectorX())
            else:
                line.append(0)
        forceSum = 0
        for f in point.forces:
            forceSum -= f.getForceX()
        line.append(forceSum)
        self.mat.append(line)
    
    def lineIntY(self, pointName, point):
        line = []
        for var in self.unknownVars:
            if var.point == pointName and var.varType == "force":
                line.append(var.getVectorY())
            else:
                line.append(0)
        forceSum = 0
        for f in point.forces:
            forceSum -= f.getForceY()
        line.append(forceSum)
        self.mat.append(line)

    def updateMatrix(self):
        # clear matrix
        self.mat = []
        # lines from parts
        for partName in self.parts.keys():
            # sum of forces in X
            self.lineX(partName)

            # sum of forces in Y
            self.lineY(partName)

            # sum of moments at (0,0)
            self.lineM(partName)

        # lines from intersections
        for pointName, point in self.points.items():
            ct = point.constraint
            if ct == "intHinge":
                # sum of forces in X
                self.lineIntX(pointName, point)
                # sum of forces in Y
                self.lineIntY(pointName, point)

    def printMatrix(self, spacing=12):
        for var in self.unknownVars:
            print(spacedStr(var.name, spacing), end="")
        for l in self.mat:
            print("")
            for n in l:
                if abs(n) < 0.00001:
                    print(spacedStr("", spacing), end="")
                else:
                    print(spacedStr(str(round(n, 4)), spacing), end="")
        print("\n")
    
    def printPointResult(self, pointName, spacing=12):
        for i in range(len(self.unknownVars)):
            var = self.unknownVars[i]
            value = self.mat[i][-1]
            if var.point != pointName:
                continue
            print(spacedStr(var.name, spacing), end="")
            print(spacedStr(str(round(value, 4)), spacing))
        print("\n")

    def printResults(self, spacing=12):
        print(spacedStr("Variable:", spacing), end="")
        print(spacedStr("Value:", spacing))
        for i in range(len(self.unknownVars)):
            var = self.unknownVars[i]
            value = self.mat[i][-1]
            print(spacedStr(var.name, spacing), end="")
            print(spacedStr(str(round(value, 4)), spacing))
        print("\n")

    def solve(self):
        n = len(self.mat)
        i = 0 # column index
        while i != n:
            j = i
            permutated = False
            while self.mat[j][i] == 0:
                j += 1
                permutated = True
                if j == n:
                    print("empty column error")
                    return
            if permutated == True:
                rowSwap(self.mat, j, i)
            # transform every row except current row
            for k in range(n):
                if k != i:
                    rowMult(self.mat, k, i, -self.mat[k][i]/self.mat[i][i])
            i += 1
        # scale rows
        for k in range(n):
            rowScale(self.mat, k, 1/self.mat[k][k])