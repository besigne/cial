import json
import threading
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from scrapper.handlers import LogoHandler, PhoneHandler
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
                logo_handler = LogoHandler(self.soup, self.url)
                phone_handler = PhoneHandler(self.soup, self.url)
                self.output(logo=logo_handler.run(), phones=phone_handler.run())
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
