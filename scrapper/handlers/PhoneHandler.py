import re
from bs4 import BeautifulSoup


class PhoneHandler:

    def __init__(self, soup: BeautifulSoup, url: str):
        self.soup = soup
        self.url = url

    def run(self):
        return self.find()

    def find(self):
        phones = []
        possible_phones = str(self.soup)
        patterns = [
            r'\(\d{3}\) \d{3}-\d{4}',
            r'\b\d{2} \d{2} \d{2}\b',
            r'\+\d+ \d{1,3} \d{4} \d{4,}',
            r'\b\d{4} \d{3} \d{3}\b',
            r'\+\d+ \(\d{3}\) \d{3}-\d{2}-\d{2}',
            r'\d{4} \d{6}'
        ]
        for pattern in patterns:
            phones_found = re.findall(pattern, possible_phones)
            for phone in phones_found:
                phones.append(phone)

        phones = list(set(phones))
        phones = [number.replace('-', ' ').replace('/', ' ') for number in phones]
        return phones
