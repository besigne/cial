import time
import unittest
import requests
import validators
import tests.cases
from utils import UrlHandler
from bs4 import BeautifulSoup
from scrapper import Scrapper
from logger import LoggerHandler
from requests.exceptions import RequestException
from scrapper.handlers import LogoHandler, PhoneHandler


class TestScrapper(unittest.TestCase):

    def setUp(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                      'AppleWebKit/537.36 (KHTML, like Gecko)'
                                      'Chrome/58.0.3029.110 Safari/537.3'
                        }
        self.url = "https://www.cmsenergy.com/contact-us/default.aspx"
        with open('tests/cases/mock.html', 'rb') as mock:
            self.page_content = mock.read()

    def test_urls_validation(self):
        try:
            for url in tests.cases.url_test_cases:
                if validators.url(url):
                    self.assertTrue(validators.url(url))
                else:
                    self.assertFalse(validators.url(url))
        except RequestException:
            raise RequestException

    def test_url_handler(self):
        url_handler = UrlHandler(self.url)
        self.assertEqual(url_handler.url, tests.cases.results_url_handler["url"])
        self.assertEqual(url_handler.base_url(), tests.cases.results_url_handler["base_url"])
        self.assertEqual(url_handler.find_country_code_from_url(),
                         tests.cases.results_url_handler["find_country_code_from_url"])

    def test_logo_handler(self):
        url_handler = UrlHandler(self.url)
        logo_handler = LogoHandler(BeautifulSoup(self.page_content, 'html.parser'), url_handler)
        logo = logo_handler.run()
        self.assertEqual(logo, tests.cases.result_logo_handler)

    def test_phone_handler(self):
        url_handler = UrlHandler(self.url)
        page = requests.get(self.url, headers=self.headers)
        phone_handler = PhoneHandler(BeautifulSoup(self.page_content, 'html.parser'),
                                     url_handler.find_country_code_from_url())
        phones = phone_handler.run()
        self.assertEqual(phones, tests.cases.result_phone_handler)

    def test_full_scrapper_lifecycle(self):
        log_handler = LoggerHandler(running_test=True)
        threads = []

        start_time = time.time()
        log_handler.start(start_time)
        for line in tests.cases.url_test_cases:
            url = line.strip()
            if validators.url(url):
                thread = Scrapper(url=url, log_handler=log_handler, output=False)
                thread.start()
                threads.append(thread)
            else:
                log_handler.url_fail(url)

        for thread in threads:
            thread.join()
        elapsed_time = time.time() - start_time
        log_handler.stop(time.time(), elapsed_time)


if __name__ == "__main__":
    unittest.main()
