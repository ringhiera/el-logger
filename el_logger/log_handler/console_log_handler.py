from el_logger.log_handler.log_handler import LogHandler
from el_logger.logger.elloglevel import ElLogLevel


class ConsoleLogHandler(LogHandler):
    """
    A mock Console Log Handler.
    """
    def __init__(self, log_level: ElLogLevel):
        self.log_level = log_level
