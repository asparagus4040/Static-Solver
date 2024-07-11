from src.Util import cos, sin

class Force:
    def __init__(self, value, angle):
        self.value = value
        self.angle = angle
    
    def getForceX(self):
        return self.value * cos(self.angle)

    def getForceY(self):
        return self.value * sin(self.angle)