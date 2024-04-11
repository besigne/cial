from bs4 import BeautifulSoup


class LogoHandler:

    def __init__(self, soup: BeautifulSoup, url: str):
        self.soup = soup
        self.url = url

    def run(self):
        return self.find()

    def find(self) -> str:
        header = self.soup.find('header')
        result = None
        if header:
            logos = header.find_all('img')
            if logos:
                result = self.treat(logos)
        else:
            logos = self.soup.find_all('img')
            if logos:
                result = self.treat(logos)
        return result

    def treat(self, logos) -> str:
        result = []
        for logo in logos:
            search = f'{logo.get('alt', '').lower()}{logo.get('src', '').lower()}'
            if 'logo' in search:
                result.append(self.treat_path(logo['src']))
            if logo.has_attr('class'):
                for class_string in logo.get('class', ''):
                    if 'logo' in class_string:
                        result.append(self.treat_path(logo['src']))
        if len(result) > 0:
            return result[0]
        return ""

    def treat_path(self, path) -> str:
        if path.startswith('//'):
            path = f'https:{path}'
        if path.startswith('/'):
            path = f'{self.url}{path}'
        return path
