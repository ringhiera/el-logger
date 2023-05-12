import datetime
from typing import List

from el_logger.logger.elloglevel import ElLogLevel
from el_logger.logger.ellogmessage import ElLogMessage
from el_logger.logger.ellogger import ElLogger


class ElBaseLogger(ElLogger):

    def __init__(self, log_handlers: List):
        self._log_handlers = log_handlers

    def _log(self, log_level: ElLogLevel, message: str):
        # Create a log message
        log_message = ElLogMessage(datetime.datetime.now(), log_level, message)
        # Dispatch the log to the handlers
        for handler in self._log_handlers:
            if handler.log_level.value <= log_level.value:
                handler.log(log_message)

    def error(self, message):
        self._log(ElLogLevel.ERROR, message)

    def warn(self, message):
        self._log(ElLogLevel.WARN, message)

    def info(self, message):
        self._log(ElLogLevel.INFO, message)

    def debug(self, message):
        self._log(ElLogLevel.DEBUG, message)
