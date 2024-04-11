import re
import json
import threading
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


class Scrapper(threading.Thread):

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url
        self.base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
        self.soup = None

    def run(self) -> None:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              'AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/58.0.3029.110 Safari/537.3'
            }
            session = requests.Session()
            session.headers.update(headers)
            page = session.get(self.url)
            if page.status_code == 200:
                self.soup = BeautifulSoup(page.content, 'html.parser')
                self.output(logo=self.find_logos(), phones=self.find_phones())
            else:
                print("Dead page")
        except RequestException:
            raise RequestException

    def output(self, logo: str, phones: list):
        result = {
            "logo": logo,
            "phones": phones,
            "website": self.url
        }
        print(json.dumps(result))

    def find_logos(self) -> str:
        header = self.soup.find('header')
        result = None
        if header:
            logos = header.find_all('img')
            if logos:
                result = self.treat_logos(logos)
        else:
            logos = self.soup.find_all('img')
            if logos:
                result = self.treat_logos(logos)
        return result

    def treat_logo_path(self, path):
        if path.startswith('//'):
            path = f'https:{path}'
        if path.startswith('/'):
            path = f'{self.base_url}{path}'
        return path

    def treat_logos(self, logos):
        result = []
        for logo in logos:
            search = f'{logo.get('alt', '').lower()}{logo.get('src', '').lower()}'
            if 'logo' in search:
                result.append(self.treat_logo_path(logo['src']))
            if logo.has_attr('class'):
                for class_string in logo.get('class', ''):
                    if 'logo' in class_string:
                        result.append(self.treat_logo_path(logo['src']))
        if len(result) > 0:
            return result[0]
        return ""

    def find_phones(self) -> list:
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
