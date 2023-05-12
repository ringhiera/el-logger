import datetime
from threading import Lock
from typing import List

from el_logger.logger.elloglevel import ElLogLevel
from el_logger.logger.ellogmessage import ElLogMessage
from el_logger.logger.ellogger import ElLogger


class ElBaseLogger(ElLogger):

    def __init__(self, log_handlers: List, min_log_level: ElLogLevel):
        self._log_handlers = log_handlers
        self._min_log_level = min_log_level
        self._min_log_level_lock = Lock()

    def _log(self, log_level: ElLogLevel, message: str):
        # ignore log levels
        if self._min_log_level.value <= log_level.value:
            # Create a log message
            log_message = ElLogMessage(datetime.datetime.now(), log_level, message)
            # Dispatch the log to the handlers
            for handler in self._log_handlers:
                # validation of loglevel might be further delegated to the implementation
                if handler.log_level.value <= log_level.value:
                    handler.log(log_message)

    def set_min_log_level(self, min_log_level: ElLogLevel):
        with self._min_log_level_lock:
            self._min_log_level = min_log_level

    def error(self, message: str):
        self._log(ElLogLevel.ERROR, message)

    def warn(self, message: str):
        self._log(ElLogLevel.WARN, message)

    def info(self, message: str):
        self._log(ElLogLevel.INFO, message)

    def debug(self, message: str):
        self._log(ElLogLevel.DEBUG, message)
