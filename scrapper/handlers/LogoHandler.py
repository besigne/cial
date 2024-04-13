from bs4 import BeautifulSoup
from bs4.element import Tag
from utils import UrlHandler
from utils import logo_required_tags, possible_logo_tags


def determine_search_string(logo: Tag) -> str:
    search = ''
    for tag in logo_required_tags:
        if logo.has_attr(tag):
            if tag == 'class':
                search += ''.join([x.lower() for x in logo.get('class', '')])
            search += str(logo.get(tag, '')).lower()
    return search


class LogoHandler:

    def __init__(self, soup: BeautifulSoup, url_handler: UrlHandler):
        self.url_handler = url_handler
        self.soup = soup
        self.path_to_logo = ""

    def run(self) -> str:
        logos = self.soup.find_all(possible_logo_tags)
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
            self.path_to_logo = result[0]
            return result[0]
        return ""

    def __treat_path(self, path) -> str:
        if not path.startswith('https://'):
            if path.startswith('//'):
                path = f'https:{path}'
            elif path.startswith('/'):
                path = f'{self.url_handler.base_url()}{path}'
            else:
                path = f'{self.url_handler.base_url()}/{path}'
        return path

    def logo_url(self) -> str:
        return self.path_to_logo
