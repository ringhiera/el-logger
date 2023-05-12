from enum import Enum


class ElLogLevel(Enum):
    """
        Here we are matching default python log-levels for simplicity
    """
    ERROR = 40
    WARN = 30
    INFO = 20
    DEBUG = 10
