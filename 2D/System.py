from Util import sin, cos, spacedStr
from Matrix import rowMult, rowSwap, rowScale

class System:
    def __init__(self):
        self.points = {}
        self.parts = {}
        self.knownVars = []
        self.unknownVars = []
        self.mat = []

    # functions for declaring new objects
    def newPoint(self, name, posX, posY):
        self.points[name] = {"X": posX, "Y": posY, "forces": [], "moment": 0, "constraint": "none"}
    
    def newPart(self, name, pointList):
        self.parts[name] = {"pointList": pointList}
    
    def newForce(self, pointName, value, angle):
        self.points[pointName]["forces"].append(
            {"value": value, "angle": angle}
        )
    
    def newMoment(self, pointName, value):
        self.points[pointName]["moment"] += value
    
    def newConstraint(self, pointName, constraintType, angle=0):
        self.points[pointName]["constraint"] = constraintType
        if constraintType == "roller" or constraintType == "wheel":
            self.points[pointName]["constraintAngle"] = angle

    def newUnknownForce(self, name, posX, posY, angle, partName, pointName):
        self.unknownVars.append(
            {"name": name, "part": partName, "point": pointName, "X": posX, "Y": posY, "angle": angle, "varType": "force"}
        )
    
    def newUnknownMoment(self, name, sign, partName, pointName):
        self.unknownVars.append(
            {"name": name, "part": partName, "point": pointName, "sign": sign, "varType": "moment"}
        )
    
    def newKnownForce(self, posX, posY, value, angle, partName, pointName):
        self.knownVars.append(
            {"part": partName, "point": pointName, "X": posX, "Y": posY, "value": value, "angle": angle, "varType": "force"}
        )
    
    def newKnownMoment(self, value, partName, pointName):
        self.knownVars.append(
            {"part": partName, "point": pointName, "value": value, "varType": "moment"}
        )

    # other functions    
    def getUnknownVars(self):
        # clear unknown vars
        self.unknownVars = []
        # get variable order
        for partName, partData in self.parts.items():
            for pointName in partData["pointList"]:
                pointData = self.points[pointName]
                posX = pointData["X"]
                posY = pointData["Y"]
                ct = pointData["constraint"]
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
                    self.newUnknownForce(partName+"_"+pointName, posX, posY, pointData["constraintAngle"], partName, pointName)
                    self.newUnknownMoment(partName+"_"+pointName+"M", 1, partName, pointName)
                elif ct == "wheel":
                    self.newUnknownForce(partName+"_"+pointName, posX, posY, pointData["constraintAngle"], partName, pointName)
        print(f"{len(self.unknownVars)} unknown variables")
    
    def getKnownVars(self):
        # clear known vars
        self.knownVars = []
        # attention: forces and moments on an intersection will get registered twice
        for partName, partData in self.parts.items():                    
            for pointName in partData["pointList"]:
                pointData = self.points[pointName]
                posX = pointData["X"]
                posY = pointData["Y"]
                # forces
                for f in pointData["forces"]:
                    self.newKnownForce(posX, posY, f["value"], f["angle"], partName, pointName)
                # moment
                if pointData["moment"] != 0:
                    self.newKnownMoment(pointData["moment"], partName, pointName)
        print(f"{len(self.knownVars)} known variables")
    
    def updateMatrix(self):
        # clear matrix
        self.mat = []
        # lines from parts
        for partName in self.parts.keys():
            # sum of forces in X
            line = []
            for var in self.unknownVars:
                if var["part"] != partName or var["varType"] != "force":
                    line.append(0)
                else:
                    line.append(cos(var["angle"]))
            forceSum = 0
            for var in self.knownVars:
                if var["part"] == partName and var["varType"] == "force":
                    forceSum -= var["value"] * cos(var["angle"])
            line.append(forceSum)
            self.mat.append(line)
            # sum of forces in Y
            line = []
            for var in self.unknownVars:
                if var["part"] != partName or var["varType"] != "force":
                    line.append(0)
                else:
                    line.append(sin(var["angle"]))
            forceSum = 0
            for var in self.knownVars:
                if var["part"] == partName and var["varType"] == "force":
                    forceSum -= var["value"] * sin(var["angle"])
            line.append(forceSum)
            self.mat.append(line)
            # sum of moments at (0,0)
            line = []
            for var in self.unknownVars:
                if var["part"] != partName:
                    line.append(0)
                else:
                    if var["varType"] == "force":
                        line.append(var["X"] * sin(var["angle"]) - var["Y"] * cos(var["angle"]))
                    else:
                        line.append(var["sign"])
            momentSum = 0
            for var in self.knownVars:
                if var["part"] == partName:
                    if var["varType"] == "force":
                        momentX = var["Y"] * var["value"] * cos(var["angle"])
                        momentY = var["X"] * var["value"] * sin(var["angle"])
                        momentSum += momentX - momentY
                    else:
                        momentSum -= var["value"]
            line.append(momentSum)
            self.mat.append(line)

        # lines from intersections
        for pointName, pointData in self.points.items():
            ct = pointData["constraint"]
            if ct == "intHinge":
                # sum of forces in X
                line = []
                for var in self.unknownVars:
                    if var["point"] != pointName or var["varType"] != "force":
                        line.append(0)
                    else:
                        line.append(cos(var["angle"]))
                forceSum = 0
                for var in pointData["forces"]:
                    forceSum -= var["value"] * cos(var["angle"])
                line.append(forceSum)
                self.mat.append(line)
                # sum of forces in Y
                line = []
                for var in self.unknownVars:
                    if var["point"] != pointName or var["varType"] != "force":
                        line.append(0)
                    else:
                        line.append(sin(var["angle"]))
                forceSum = 0
                for var in pointData["forces"]:
                    forceSum -= var["value"] * sin(var["angle"])
                line.append(forceSum)
                self.mat.append(line)

    def printMatrix(self, spacing=12):
        for var in self.unknownVars:
            print(spacedStr(var["name"], spacing), end="")
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
            if var["point"] != pointName:
                continue
            print(spacedStr(var["name"], spacing), end="")
            print(spacedStr(str(round(value, 4)), spacing))
        print("\n")

    def printResults(self, spacing=12):
        print(spacedStr("Variable:", spacing), end="")
        print(spacedStr("Value:", spacing))
        for i in range(len(self.unknownVars)):
            var = self.unknownVars[i]
            value = self.mat[i][-1]
            print(spacedStr(var["name"], spacing), end="")
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