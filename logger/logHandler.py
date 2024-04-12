import logging
from threading import Thread


class Logger:

    def __init__(self,log_file):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def start_log(self, msg: str, thread: Thread):
        pass
