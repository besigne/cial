import sys
import time
import validators
from scrapper import Scrapper


def init():
    threads = []

    start_time = time.time()
    for line in sys.stdin:
        url = line.strip()
        if validators.url(url):
            thread = Scrapper(url=url)
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()
    elapsed_time = time.time() - start_time
    print("Running time: ", elapsed_time)


if __name__ == "__main__":
    init()
