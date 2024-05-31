import math

def cos(x):
    return math.cos(math.radians(x))

def sin(x):
    return math.sin(math.radians(x))

def spacedStr(string, spacingMax):
    return string + (spacingMax - len(string)) * " "