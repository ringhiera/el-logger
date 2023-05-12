from el_logger.logger.elloglevel import ElLogLevel
from el_logger.log_handler.log_handler import LogHandler


class ConsoleLogHandler(LogHandler):

    def __init__(self, log_level: ElLogLevel):
        self.log_level = log_level


