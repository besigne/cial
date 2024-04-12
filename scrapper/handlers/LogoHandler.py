from bs4 import BeautifulSoup
from bs4.element import Tag


def determine_search_string(logo: Tag) -> str:
    search = ''
    if logo.has_attr('src'):
        search += logo.get('src', '').lower()
    if logo.has_attr('alt'):
        search += logo.get('alt', '').lower()
    if logo.has_attr('class'):
        search += ''.join([x.lower() for x in logo.get('class', '')])
    return search


class LogoHandler:

    def __init__(self, soup: BeautifulSoup, url: str, base_url: str):
        self.soup = soup
        self.url = url
        self.base_url = base_url
        self.found_logo = False

    def run(self) -> str:
        logos = self.soup.find_all(['header', 'img'])
        if logos:
            return self.__treat(logos)

    def __treat(self, logos: [Tag]) -> str:
        result = []
        for logo in logos:
            if not logo.has_attr('src'):
                continue
            search = determine_search_string(logo)
            if 'logo' in search:
                result.append(self.__treat_path(logo['src']))

        if len(result) > 0 and result[0]:
            self.found_logo = True
            return result[0]
        return ""

    def __treat_path(self, path) -> str:
        if not path.startswith('https://'):
            if path.startswith('//'):
                path = f'https:{path}'
            elif path.startswith('/'):
                path = f'{self.base_url}{path}'
            else:
                path = f'{self.base_url}/{path}'
        return path

    def is_logo_found(self):
        return self.found_logo
