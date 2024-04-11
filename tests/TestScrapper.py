import unittest
import requests
from unittest.mock import patch
from io import StringIO
from scrapper import Scrapper


class TestScrapper(unittest.TestCase):
    def setUp(self):
        self.url_list = [
            "https://www.cmsenergy.com/contact-us/default.aspx",
            "https://www.illion.com.au",
            "https://www.phosagro.com/contacts",
            "https://www.powerlinx.com/contact",
            "https://www.cialdnb.com/en",
            "https://www.illion.com.au/contact-us/"
        ]

    def test_internet_connection(self):
        print("Verifying for internet connection")
        response = requests.get("http://www.google.com", timeout=5)
        self.assertTrue(response.status_code == 200)

    def test_scrapper_default(self):
        print("Using the default list to determine if the scrapper is working")
        threads = []
        for line in self.url_list:
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                thread = Scrapper(url=line.strip())
                thread.start()
                threads.append(thread)
                self.assertEqual(fake_stdout.getvalue().strip(), '')


if __name__ == "__main__":
    unittest.main()
