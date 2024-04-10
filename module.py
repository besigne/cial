import sys
import re
import threading
from Scrapper import Scrapper

for line in sys.stdin:
    Scrapper(url=line.strip())

# scrapper = Scrapper(url="https://www.cmsenergy.com/contact-us/default.aspx")

# scrapper.find_logos()
