import re
import phonenumbers
from bs4 import BeautifulSoup
from utils.tags import possible_phone_tags


def watering_soup(soup) -> str:
    search = ''
    [data.extract() for data in soup(['script', 'style'])]
    tags = soup.find_all(possible_phone_tags)
    search += ''.join(str(tag.get_text()) for tag in tags)
    return search


class PhoneHandler:

    def __init__(self, soup: BeautifulSoup, country_code: str):
        self.soup = watering_soup(soup)
        self.country_code = country_code
        self.phones_count = 0

    def run(self) -> list:
        phones = []
        all_possible_phones = phonenumbers.PhoneNumberMatcher(self.soup, self.country_code)

        for unvalidated_number in all_possible_phones:

            if not phonenumbers.is_valid_number(unvalidated_number.number):
                continue

            carrier = "+" + str(
                phonenumbers.country_code_for_region(phonenumbers.region_code_for_number(unvalidated_number.number)))

            number = phonenumbers.format_in_original_format(unvalidated_number.number, self.country_code)

            combined = re.sub('[^0-9()+]+', ' ', f'{carrier} {number}')

            if combined not in phones:
                phones.append(combined)
                self.phones_count += 1

        return phones

    def how_many_phones(self) -> int:
        return self.phones_count
