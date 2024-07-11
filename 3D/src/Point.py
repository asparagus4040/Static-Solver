from src.Vector3 import Vector3
from src.Constraint import Constraint
import src.Enum as Enum

class Point:
    def __init__(self, name, X, Y, Z):
        self.name = name
        self.position = Vector3(X, Y, Z)
        self.force = Vector3()
        self.moment = Vector3()
        self.constraint = Constraint(Enum.Translation.Free, Enum.Rotation.Ball)
    
    def printInfo(self):
        print("POINT :", self.name)
        print("    POSITION :", self.position.string())
        print("    FORCE :", self.force.string())
        print("    MOMENT :", self.moment.string())
        print("    CONSTRAINT :", self.constraint.name)