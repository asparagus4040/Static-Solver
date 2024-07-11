from src.Vector3 import Vector3

class Constraint:
    def __init__(self, translation, rotation):
        self.name = translation.name+" "+rotation.name
        
        self.translation = translation
        self.rotation = rotation
        
        self.translationVec1 = Vector3(1,0,0)
        self.translationVec2 = Vector3(0,1,0)
        self.rotationVec1 = Vector3(1,0,0)
        self.rotationVec2 = Vector3(0,1,0)