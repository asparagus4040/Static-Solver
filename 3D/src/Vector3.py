from math import sqrt

class Vector3:
    def __init__(self, X=0, Y=0, Z=0):
        self.X = X
        self.Y = Y
        self.Z = Z
    
    def magnitude(self):
        return sqrt(self.X**2 + self.Y**2 + self.Z**2)
    
    def __add__(self, other):
        return Vector3(self.X + other.X, self.Y + other.Y, self.Z + other.Z)
    
    def __sub__(self, other):
        return Vector3(self.X - other.X, self.Y - other.Y, self.Z - other.Z)
    
    def __mul__(self, other):
        return Vector3(other * self.X, other * self.Y, other * self.Z)
    
    def __div__(self, other):
        return Vector3(self.X / other, self.Y / other, self.Z / other)
        
    def unit(self):
        return Vector3(self.X, self.X, self.X) / self.magnitude()
    
    def string(self):
        return str(self.X)+" "+str(self.Y)+" "+str(self.Z)