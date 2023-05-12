import unittest
from datetime import datetime

from el_logger.logger.elloglevel import ElLogLevel
from el_logger.logger.ellogmessage import ElLogMessage


class ElLogMessageTestCase(unittest.TestCase):

    def test_str(self):
        ts = datetime.strptime('2023-05-11T19:32:09.754070', '%Y-%m-%dT%H:%M:%S.%f')
        expected_message = 'INFO - 2023-05-11T19:32:09.754070: some message'
        actual_message = str(ElLogMessage(ts, ElLogLevel.INFO, "some message"))

        assert actual_message == expected_message
