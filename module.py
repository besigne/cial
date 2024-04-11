import sys
from scrapper import Scrapper

threads = []

for line in sys.stdin:
    thread = Scrapper(url=line.strip())
    thread.start()
    threads.append(thread)

