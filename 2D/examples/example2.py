import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from System import System

if __name__ == "__main__":
    system = System()
    # points
    system.newPoint("A", 0, 0)
    system.newPoint("B", 2, 3)
    system.newPoint("C", 4, 6)
    system.newPoint("D", 6, 3)
    system.newPoint("E", 8, 0)

    system.newPoint("F", 4, 3)
    # parts
    system.newPart("ABC", ["A", "B", "C"])
    system.newPart("CDE", ["C", "D", "E"])
    system.newPart("BD", ["B", "D", "F"])
    # constraints
    system.newConstraint("A", "hinge")
    system.newConstraint("B", "intHinge")
    system.newConstraint("C", "intHinge")
    system.newConstraint("D", "intHinge")
    system.newConstraint("E", "wheel", 90)
    # forces
    system.newForce("F", -5, 90)

    system.getUnknownVars()
    system.getKnownVars()
    system.updateMatrix()

    #system.printMatrix(10)

    system.solve()

    #system.printMatrix(10)

    system.printResults()