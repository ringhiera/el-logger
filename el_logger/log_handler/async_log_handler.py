import queue
import threading

from el_logger.log_handler.log_handler import LogHandler
from el_logger.logger.elloglevel import ElLogLevel
from el_logger.utils.thread_safe_print import sync_print


class AsyncLogHandler(LogHandler):
    """
    this class implement an asyncronous producer consumer log handler.
    Given logs are critical to the debug of an application one should take care they are persisted immediately.
    However, under some circumstances one might want to distribute the load to asynchronous threads to dispatch the logs
    """

    def __init__(self, log_level: ElLogLevel):
        self.log_level = log_level
        # set up the synchronized queue between the logger and the worker threads
        self._log_q = queue.Queue()
        # set up the worker thread. In this case we spawn one thread, we can spawn as many as needed.
        self.thread = threading.Thread(target=self.start_thread, daemon=True)
        self.thread.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # tear down resources on context exit. In particular join the queue and terminate the workers
        self.close()

    def start_thread(self):
        # This worker listen to the queue for new logs and prints them until the termination event is set
        while True:
            # get() is synchronized, thread waits on the queue to produce.
            message = self._log_q.get()
            # If the print can fail we might want to protect the execution and ensure task_done is called.
            # In this specific case it is not needed as print does not raise.
            sync_print("Logger: " + self.__class__.__name__ + " - " + str(message))
            self._log_q.task_done()

    def close(self):
        # wait for the queue to join
        self._log_q.join()

    def log(self, message):
        # The message is put in the queue for the worker threads to handle
        self._log_q.put(message)
