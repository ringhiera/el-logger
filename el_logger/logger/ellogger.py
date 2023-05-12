from abc import ABC, abstractmethod


class ElLogger(ABC):
    """
    base class for the expert lead logger
    """

    @abstractmethod
    def error(self, message):
        pass

    @abstractmethod
    def warn(self, message):
        pass

    @abstractmethod
    def info(self, message):
        pass

    @abstractmethod
    def debug(self, message):
        pass

