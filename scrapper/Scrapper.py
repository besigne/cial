import json
import threading
import requests
from utils import UrlHandler
from bs4 import BeautifulSoup
from logger import LoggerHandler
from requests.exceptions import RequestException
from scrapper.handlers import LogoHandler, PhoneHandler


class Scrapper(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      'AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/58.0.3029.110 Safari/537.3'
    }

    def __init__(self, url: str, log_handler: LoggerHandler, output=True) -> None:
        super(Scrapper, self).__init__()
        self.url_handler = UrlHandler(url)
        self.url = url
        self.log_handler = log_handler
        self.output = output

    def run(self) -> None:
        try:

            page = requests.get(self.url, headers=self.headers)
            will_scrapper_run = page.status_code == requests.codes.ok
            if will_scrapper_run:
                soup = BeautifulSoup(page.content, 'html.parser')

                logo_handler = LogoHandler(soup, self.url_handler)
                phone_handler = PhoneHandler(soup, self.url_handler.find_country_code_from_url())
                logo_scrapper = logo_handler.run()
                phone_scrapper = phone_handler.run()
                self.__output(logo_scrapper, phone_scrapper, will_scrapper_run)

                self.log_handler.log(self.url_handler.base_url(), page.status_code,
                                     logo_handler.logo_url(), phone_handler.phones_count)

            else:
                self.__output("", [], will_scrapper_run)
                self.log_handler.fail(self.url_handler.base_url(), page.status_code)

        except RequestException:
            raise RequestException

    def __output(self, logo: str, phones: list, success: bool) -> json:
        if self.output:
            if success:
                result = {
                    "logo": logo,
                    "phones": phones,
                    "website": self.url
                }
            else:
                result = "Dead Page"
            print(json.dumps(result))
        else:
            pass
