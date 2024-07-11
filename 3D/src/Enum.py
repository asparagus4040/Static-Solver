from enum import Enum

Translation = Enum(
    "Translation",
    [
        "Free",
        "Planar",
        "Linear",
        "Fixed"        
    ]
)

Rotation = Enum(
    "Rotation",
    [
        "Ball",
        "Swivel",
        "Hinge",
        "Weld",
        "Intersection"
    ]
)

UnknownType = Enum(
    "UnknownType",
    [
        "Force",
        "Moment",
        "IntersectionForce"
    ]
)