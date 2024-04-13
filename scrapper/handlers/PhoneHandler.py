import phonenumbers
from bs4 import BeautifulSoup
from utils.tags import possible_phone_tags


def add_parenthesis_to_phone(phone_number: str) -> str:
    phone_pieces = phone_number.split(' ')
    phone_pieces[1] = f"({phone_pieces[1]})"
    return ' '.join(phone_pieces)


class PhoneHandler:

    def __init__(self, soup: BeautifulSoup, country_code: str):
        self.soup = soup
        self.country_code = country_code
        self.phones_count = 0

    def run(self) -> list:
        phones = []
        numbers = phonenumbers.PhoneNumberMatcher(self.__watering_soup(), self.country_code)
        for unvalidated_number in numbers:
            formated_number = phonenumbers.format_number(
                unvalidated_number.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL).replace('-', ' ')
            if phonenumbers.is_possible_number(
                    phonenumbers.parse(formated_number, self.country_code)) and formated_number not in phones:
                phones.append(formated_number)
                self.phones_count += 1

        return phones

    def how_many_phones(self) -> int:
        return self.phones_count

    def __watering_soup(self) -> str:
        search = ''
        [data.extract() for data in self.soup(['script', 'style'])]
        tags = self.soup.find_all(possible_phone_tags)
        search += ''.join(str(tag.get_text()) for tag in tags)
        return search
