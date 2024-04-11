import sys
from Scrapper import Scrapper

lines = [
    # "https://www.cmsenergy.com/contact-us/default.aspx",
    # "https://www.illion.com.au",
    # "https://www.phosagro.com/contacts",
    # "https://www.powerlinx.com/contact",
    "https://www.cialdnb.com/en,",
    # "https://www.illion.com.au/contact-us/"
]

threads = []

# for line in sys.stdin:
#     thread = Scrapper(url=line.strip())
#     thread.start()
#     threads.append(thread)

for line in lines:
    thread = Scrapper(url=line.strip())
    thread.start()
    threads.append(thread)
