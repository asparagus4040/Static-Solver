from src.Point import Point
from src.Part import Part
from src.Vector3 import Vector3
from src.Constraint import Constraint
from src.Unknown import Unknown
import src.Enum as Enum

class System:
    def __init__(self):
        self.mat = []
        self.points = {}
        self.parts = {}
        self.unknowns = []
    
    # preferable to declare the constraint on
    def addPoint(self, name, posX, posY, posZ):
        self.points[name] = Point(name, posX, posY, posZ)
    
    def addPart(self, name, pointList):
        self.parts[name] = Part(name, pointList)
        # check if the points exist
        for pointName in pointList:
            if not pointName in self.points:
                print("ERROR : point", pointName, "doesnt exist")
    
    def addConstraint(self, pointName, translation, rotation,
                     translationVec1=Vector3(), translationVec2=Vector3(),
                     rotationVec1=Vector3(), rotationVec2=Vector3()):
        self.points[pointName].constraint = Constraint(translation, rotation)
        self.points[pointName].constraint.translationVec1 = translationVec1
        self.points[pointName].constraint.translationVec2 = translationVec2
        self.points[pointName].constraint.rotationVec1 = rotationVec1
        self.points[pointName].constraint.rotationVec2 = rotationVec2

    def addUnknown(self, pointName, name, vector, unknownType):
        self.unknowns.append(Unknown(pointName, name, vector, unknownType))
    
    # adding and removing forces/moments from points
    def addForce(self, pointName, X, Y, Z):
        self.points[pointName].force += Vector3(X, Y, Z)
    
    def addMoment(self, pointName, X, Y, Z):
        self.points[pointName].moment += Vector3(X, Y, Z)

    def updateUnknowns(self):
        for partName, part in self.parts.items():
            for pointName in part.pointList:
                point = self.points[pointName]
                constraint = point.constraint
                # intersection variables on ball
                if constraint.rotation == Enum.Rotation.Intersection:
                    self.addUnknown(pointName, partName+"_"+pointName+"_x", Vector3(1, 0, 0), Enum.UnknownType.Force)
                    self.addUnknown(pointName, partName+"_"+pointName+"_y", Vector3(0, 1, 0), Enum.UnknownType.Force)
                    self.addUnknown(pointName, partName+"_"+pointName+"_z", Vector3(0, 0, 1), Enum.UnknownType.Force)
                    continue
                # translations
                if constraint.translation == Enum.Translation.Fixed:
                    self.addUnknown(pointName, partName+"_"+pointName+"_x", Vector3(1, 0, 0), Enum.UnknownType.Force)
                    self.addUnknown(pointName, partName+"_"+pointName+"_y", Vector3(0, 1, 0), Enum.UnknownType.Force)
                    self.addUnknown(pointName, partName+"_"+pointName+"_z", Vector3(0, 0, 1), Enum.UnknownType.Force)
                elif constraint.translation == Enum.Translation.Linear:
                    self.addUnknown(pointName, partName+"_"+pointName+"_1", constraint.translationVec1, Enum.UnknownType.Force)
                    self.addUnknown(pointName, partName+"_"+pointName+"_2", constraint.translationVec2, Enum.UnknownType.Force)
                elif constraint.translation == Enum.Translation.Planar:
                    self.addUnknown(pointName, partName+"_"+pointName, constraint.translationVec1, Enum.UnknownType.Force)
                # rotations
                if constraint.rotation == Enum.Rotation.Weld:
                    self.addUnknown(pointName, partName+"_"+pointName+"_Mx", Vector3(1, 0, 0), Enum.UnknownType.Moment)
                    self.addUnknown(pointName, partName+"_"+pointName+"_My", Vector3(0, 1, 0), Enum.UnknownType.Moment)
                    self.addUnknown(pointName, partName+"_"+pointName+"_Mz", Vector3(0, 0, 1), Enum.UnknownType.Moment)
                elif constraint.rotation == Enum.Rotation.Hinge:
                    self.addUnknown(pointName, partName+"_"+pointName+"_M1", constraint.rotationVec1, Enum.UnknownType.Moment)
                    self.addUnknown(pointName, partName+"_"+pointName+"_M2", constraint.rotationVec2, Enum.UnknownType.Moment)
                elif constraint.rotation == Enum.Rotation.Swivel:
                    self.addUnknown(pointName, partName+"_"+pointName+"_M", constraint.rotationVec1, Enum.UnknownType.Moment)
        # intersection-only intersection base
        for pointName, point in self.points.items():
            constraint = point.constraint
            if constraint.rotation != Enum.Rotation.Intersection:
                continue
            if constraint.translation == Enum.Translation.Fixed:
                self.addUnknown(pointName, pointName+"_Rx", Vector3(1, 0, 0), Enum.UnknownType.IntersectionForce)
                self.addUnknown(pointName, pointName+"_Ry", Vector3(0, 1, 0), Enum.UnknownType.IntersectionForce)
                self.addUnknown(pointName, pointName+"_Rz", Vector3(0, 0, 1), Enum.UnknownType.IntersectionForce)
            elif constraint.translation == Enum.Translation.Linear:
                self.addUnknown(pointName, pointName+"_R1", constraint.translationVec1, Enum.UnknownType.IntersectionForce)
                self.addUnknown(pointName, pointName+"_R2", constraint.translationVec2, Enum.UnknownType.IntersectionForce)
            elif constraint.translation == Enum.Translation.Planar:
                self.addUnknown(pointName, pointName+"_R", constraint.translationVec1, Enum.UnknownType.IntersectionForce)
    
    def updateMatrix(self):
        # equations from parts
        for part in self.parts.values():
            # forces in X
            # unknowns
            line = []
            for unk in self.unknowns:
                if unk.point in part.pointList and unk.unknownType == Enum.UnknownType.Force:
                    line.append(unk.vector.X)
                else:
                    line.append(0)
            self.mat.append(line)
            # knowns



    def printPoints(self):
        for point in self.points.values():
            point.printInfo()
    
    def printParts(self):
        for part in self.parts.values():
            part.printInfo()

    def printUnknowns(self):
        print(len(self.unknowns), "unknowns\n")
        for unk in self.unknowns:
            unk.printInfo()