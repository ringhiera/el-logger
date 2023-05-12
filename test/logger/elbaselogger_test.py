import unittest
from unittest.mock import MagicMock

from el_logger.logger.elbaselogger import ElBaseLogger
from el_logger.logger.elloglevel import ElLogLevel

class ElBaseLoggerTestCase(unittest.TestCase):

    def test_baselogger_log_on_high_loglevel(self):
        mock_log_handler = MagicMock()
        mock_log_handler.log_level = ElLogLevel.INFO
        logger = ElBaseLogger([mock_log_handler])
        logger.error("some message")
        mock_log_handler.log.assert_called()

    def test_baselogger_log_on_same_loglevel(self):
        mock_log_handler = MagicMock()
        mock_log_handler.log_level = ElLogLevel.INFO
        logger = ElBaseLogger([mock_log_handler])
        logger.info("some message")
        mock_log_handler.log.assert_called()

    def test_baselogger_log_on_low_loglevel(self):
        mock_log_handler = MagicMock()
        mock_log_handler.log_level = ElLogLevel.INFO
        logger = ElBaseLogger([mock_log_handler])
        logger.debug("some message")
        assert not mock_log_handler.log.called

    # Unit tests on trivial methods are skipped for brevity. In prod code we might want to have them implemented
