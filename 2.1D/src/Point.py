from src.Force import Force

class Point:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.forces = []
        self.moment = 0
        self.constraint = "none"
        self.constraintAngle = 0
    
    def addMoment(self, value):
        self.moment += value
    
    def addForce(self, value, angle):
        force = Force(value, angle)
        self.forces.append(force)
    
    def setConstraint(self, constraintType, angle=0):
        self.constraint = constraintType
        self.constraintAngle = angle