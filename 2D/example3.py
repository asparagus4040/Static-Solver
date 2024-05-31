from System import System

if __name__ == "__main__":
    system = System()
    # points
    system.newPoint("A", 0, 0)
    system.newPoint("B", 1, 0)
    system.newPoint("C", 3, 3)
    system.newPoint("D", 5, 0)
    system.newPoint("E", 7, 3)
    system.newPoint("F", 9, 0)
    system.newPoint("G", 10, 0)

    system.newPoint("m", 5, 3)
    # parts
    system.newPart("ABD", ["A", "B", "D"])
    system.newPart("BC", ["B", "C"])
    system.newPart("CD", ["C", "D"])
    system.newPart("CE", ["C", "E", "m"])
    system.newPart("DE", ["D", "E"])
    system.newPart("EF", ["E", "F"])
    system.newPart("DFG", ["D", "F", "G"])
    # constraints
    system.newConstraint("A", "hinge")
    system.newConstraint("B", "intHinge")
    system.newConstraint("C", "intHinge")
    system.newConstraint("D", "intHinge")
    system.newConstraint("E", "intHinge")
    system.newConstraint("F", "intHinge")
    system.newConstraint("G", "wheel", 90)
    # forces
    system.newForce("D", -5, 90)

    system.getUnknownVars()
    
    for i in range(5):
        # change moment
        system.points["m"]["moment"] = -i
        system.getKnownVars()
        system.updateMatrix()

        system.solve()

        #system.printResults()
        system.printPointResult("C")