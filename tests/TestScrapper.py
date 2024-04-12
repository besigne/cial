import unittest
from validators import url as validator
from .cases import valid_urls, invalid_urls
from requests.exceptions import RequestException


class TestScrapper(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_urls(self):
        try:
            for url in valid_urls:
                self.assertTrue(validator(url))
        except RequestException:
            raise RequestException

    def test_invalid_urls(self):
        try:
            for url in invalid_urls:
                self.assertFalse(validator(url))
        except RequestException:
            raise RequestException


if __name__ == "__main__":
    unittest.main()
