from enum import Enum


# Emum for project types
class TypeOfProject(Enum):
    REPLACE = 0
    NEW_ADDITION = 1
    REPAIR = 2
    NEW_HOME = 3
    NOT_SURE = 4


# Emum for siding types
class TypeOfSiding(Enum):
    VINYL = 0
    CEMENT = 1
    WOOD = 2
    OTHER = 3
    NOT_SURE = 4


# Emum for expected results
class Expected(Enum):
    CORRECT = 0
    WRONG_ZIP_CODE = 1
    INVALID = 2
    EMPTY = 3
    STARTS_WITH_ZERO = 4
    INCOMPLETE = 5
    ALREADY_EXISTS = 6
