from abc import ABC

from el_logger.utils.thread_safe_print import sync_print
from el_logger.logger.elloglevel import ElLogLevel


class LogHandler(ABC):
    log_level = ElLogLevel.INFO

    def log(self, message):
        sync_print("Logger: " + self.__class__.__name__ + " - " + str(message))

    # loggers usually use resources that require management e.g. logfiles
    # Here we are defining the entry points of the context management protocol,
    # so that we can have the context manage the resources
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
