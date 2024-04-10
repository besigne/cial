import re
import json
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


class Scrapper:

    def __init__(self, url: str):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              'AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/58.0.3029.110 Safari/537.3'
            }
            session = requests.Session()
            session.headers.update(headers)
            page = session.get(url)
            if page.status_code == 200:
                self.result = {
                    "logo": "",
                    "phones": [],
                    "website": f"{url}",
                }
                self.soup = BeautifulSoup(page.content, 'html.parser')
                self.find_logos()
            else:
                self.result = {"Dead Page"}
        except RequestException:
            print("Error: ", RequestException)

    def find_logos(self):
        logos = self.soup.find_all('img')
        for logo in logos:
            print(logo)

    def find_phones(self):
        pass
