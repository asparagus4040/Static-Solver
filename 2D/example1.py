from System import System

if __name__ == "__main__":
    system = System()
    # points
    system.newPoint("A", 0, 2)
    system.newPoint("B", 3, 0)
    system.newPoint("C", 6, 2)
    # parts
    system.newPart("ABC", ["A", "B", "C"])
    # constraints
    system.newConstraint("A", "wheel", 0)
    system.newConstraint("B", "hinge")
    # forces
    system.newForce("C", 5, 90)

    system.getUnknownVars()
    system.getKnownVars()
    system.updateMatrix()

    system.printMatrix()

    system.solve()

    system.printMatrix()