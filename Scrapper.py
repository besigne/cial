import re
import os
import json
import threading
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


class Scrapper(threading.Thread):

    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self.base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
        aux = re.search(r'www\.(.*?)\.com', self.base_url)
        self.name = aux.group(1)
        self.soup = None
        self.result = None

    def run(self):
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
                self.result = {
                    "logo": self.find_logos(),
                    "phones": self.find_phones(),
                    "website": f"{self.url}",
                }
                print(json.dumps(self.result))
            else:
                self.result = "Dead Page"
                print(self.result)
        except RequestException:
            print("Error: ", RequestException)

    def find_logos(self):
        header = self.soup.find('header')
        svgs = self.soup.find_all('svg')
        result = None
        if header:
            logos = header.find_all('img')
            if logos:
                result = self.treat_logos(logos)
        else:
            logos = self.soup.find_all('img')
            if logos:
                result = self.treat_logos(logos)

        if svgs:
            self.save_svgs(svgs)

        return result

    def find_phones(self):
        pass

    def treat_logo_path(self, path):
        if path.startswith('//'):
            path = f'https:{path}'
        if path.startswith('/local'):
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
        return result

    def save_svgs(self, svgs):
        path = f"svgs/{self.name}/"
        if not os.path.exists(path):
            os.mkdir(path)
        for index, svg in enumerate(svgs):
            if index == 19:
                print(svg)
            with open(f"{path}{index}.svg", "w") as f:
                f.write(str(svg))
