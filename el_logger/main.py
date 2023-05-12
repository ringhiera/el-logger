import time

from el_logger.log_handler.async_log_handler import AsyncLogHandler
from el_logger.log_handler.console_log_handler import ConsoleLogHandler
from el_logger.log_handler.email_log_handler import EmailLogHandler
from el_logger.log_handler.file_log_handler import FileLogHandler
from el_logger.logger.elbaselogger import ElBaseLogger
from el_logger.logger.elloglevel import ElLogLevel


def main():
    # Under normal circumstances we should provide the initialization via e.g. configuration files and return only the logger
    # In this example of usage we instantiate the handlers directly and inject them in the logger

    # To note, loggers usually use resource that require to be closed down correctly, ensuring all logs are flushed and
    # all resources are closed down properly
    # Therefore we should define the log handlers in a context so that context is managing safe closure of resources
    # e.g. explicitly using a context
    # with ConsoleLogHandler(ElLogLevel.ERROR) as console_log_handler, \
    #         EmailLogHandler(ElLogLevel.WARN) as email_log_handler, \
    #         FileLogHandler(ElLogLevel.INFO) as file_log_handler, \
    #         AsyncLogHandler(ElLogLevel.DEBUG) as async_log_handler:

    # Given the logger is also expected to live for the full execution,
    # we can instantiate them in main and expect the runtime context to close them down on exit via the context protocol
    # However, abrupt termination of the main context may shut down the async processes and release resources
    # before all logs are flushed
    # e.g. relying on the execution context to terminate the processes
    # console_log_handler = ConsoleLogHandler(ElLogLevel.ERROR)
    # email_log_handler = EmailLogHandler(ElLogLevel.WARN)
    # file_log_handler = FileLogHandler(ElLogLevel.INFO)
    # async_log_handler = AsyncLogHandler(ElLogLevel.DEBUG)

    with ConsoleLogHandler(ElLogLevel.ERROR) as console_log_handler, \
            EmailLogHandler(ElLogLevel.WARN) as email_log_handler, \
            FileLogHandler(ElLogLevel.INFO) as file_log_handler, \
            AsyncLogHandler(ElLogLevel.DEBUG) as async_log_handler:

        # creating the logger
        logger = ElBaseLogger([
            console_log_handler,
            email_log_handler,
            file_log_handler,
            async_log_handler
        ], ElLogLevel.DEBUG)

        # logging with different log-level
        # the first calls with no delay shows the async logger is likely to add some lag before printing the logs
        # the added delay allows for the logs to be generated with some time difference in the timestamp
        logger.error("Error message 1")
        logger.error("Error message 2")
        logger.error("Error message 3")
        time.sleep(1)
        logger.warn("Warning message")
        time.sleep(1)
        logger.info("Info message")
        time.sleep(1)
        logger.debug("Debug message")


if __name__ == '__main__':
    main()
