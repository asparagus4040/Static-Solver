from src.System import System
import src.Enum as Enum

if __name__ == "__main__":
    system = System()

    system.addPoint("A", 0, 0, 0)
    system.addPoint("B", 0, 1, 0)
    system.addPoint("C", 2, 0, 0)

    system.addConstraint("A", Enum.Translation.Fixed, Enum.Rotation.Ball)
    system.addConstraint("B", Enum.Translation.Free, Enum.Rotation.Intersection)
    system.addConstraint("C", Enum.Translation.Fixed, Enum.Rotation.Weld)

    system.addPart("AB", ["A", "B"])
    system.addPart("BC", ["B", "C"])

    system.addForce("A", 0, 10, 0)

    system.updateUnknowns()

    #system.printUnknowns()