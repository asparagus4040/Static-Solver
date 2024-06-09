from enum import Enum

Constraint = Enum(
    "Constraint",
    [
        "Hinge", "Wheel",
        "Fixed", ""
    ]
)