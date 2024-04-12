import json
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from logger import LoggerHandler
from scrapper.handlers import LogoHandler, PhoneHandler
from requests.exceptions import RequestException


class Scrapper(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      'AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/58.0.3029.110 Safari/537.3'
    }

    def __init__(self, url: str, log_handler: LoggerHandler) -> None:
        super(Scrapper, self).__init__()
        self.url = url
        self.base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
        self.log_handler = log_handler

    def run(self) -> None:
        try:

            session = requests.Session()
            session.headers.update(self.headers)
            page = session.get(self.url)

            if page.status_code == requests.codes.ok:
                soup = BeautifulSoup(page.content, 'html.parser')
                logo_handler = LogoHandler(soup, self.url, self.base_url)
                phone_handler = PhoneHandler(soup)
                self.__output(logo=logo_handler.run(), phones=phone_handler.run())
                self.log_handler.log(self.base_url, page.status_code,
                                     logo_handler.found_logo, phone_handler.phones_count)
            else:
                self.log_handler.fail(self.base_url, page.status_code)
                print("Dead page")

        except RequestException:
            raise RequestException

    def __output(self, logo: str, phones: list) -> json:
        result = {
            "logo": logo,
            "phones": phones,
            "website": self.url
        }
        print(json.dumps(result))
