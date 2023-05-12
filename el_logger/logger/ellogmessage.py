import datetime

from el_logger.logger.elloglevel import ElLogLevel


class ElLogMessage:
    def __init__(self, ts: datetime, log_level: ElLogLevel, message: str):
        self.ts = ts
        self.log_level = log_level
        self.message = message

    def __str__(self):
        return f'{ElLogLevel(self.log_level).name} - {self.ts.strftime("%Y-%m-%dT%H:%M:%S.%f%z")}: {self.message}'
