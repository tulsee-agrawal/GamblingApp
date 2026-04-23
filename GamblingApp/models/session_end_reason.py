from enum import Enum

class SessionEndReason(Enum):
    UPPER_LIMIT = "UPPER_LIMIT"
    LOWER_LIMIT = "LOWER_LIMIT"
    MANUAL = "MANUAL"
    TIMEOUT = "TIMEOUT"