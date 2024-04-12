import sys
import time
import validators
from scrapper import Scrapper
from logger import LoggerHandler


def init():

    log_handler = LoggerHandler()
    threads = []

    start_time = time.time()
    log_handler.start(start_time)
    for line in sys.stdin:
        url = line.strip()
        if validators.url(url):
            thread = Scrapper(url=url, log_handler=log_handler)
            thread.start()
            threads.append(thread)
        else:
            log_handler.url_fail(url)

    for thread in threads:
        thread.join()
    elapsed_time = time.time() - start_time
    log_handler.stop(time.time(), elapsed_time)


if __name__ == "__main__":
    init()
