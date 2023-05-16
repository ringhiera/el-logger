from abc import ABC

from el_logger.logger.elloglevel import ElLogLevel
from el_logger.utils.thread_safe_print import sync_print


class LogHandler(ABC):
    """
    This class defines the abstract template for the log handler of a generic Target.
    """
    log_level = ElLogLevel.INFO

    # Every implementation should provide a specific implementation
    # Therefore, this method should be abstract
    # Given most implementations are mock we provide a default mock-log implementation
    def log(self, message):
        """
        Performs the actual logging delivering the log message to the appropriate (Mock) Target Stream
        :param message: THe log message
        """
        sync_print("Logger: " + self.__class__.__name__ + " - " + str(message))

    # loggers usually use resources that require management e.g. logfiles
    # Here we are defining the entry points of the context management protocol,
    # so that we can have the context manage the resources
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
