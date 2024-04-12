import re
import phonenumbers
from bs4 import BeautifulSoup

regions = {
    "US": r'^\+(\d)(\d{3})(\d{3})(\d{4})$',
    "BR": r'^\+(\d{2})(\d{2})(\d{4})(\d{4})$'
}


def format_phone_number(phone_number: str, regex: str) -> str:
    match = re.match(f'{regex}', phone_number)
    if match:
        country_code = match.group(1)
        area_code = match.group(2)
        first_part = match.group(3)
        second_part = match.group(4)
        return f'+{country_code} ({area_code}) {first_part} {second_part}'
    else:
        return ""


class PhoneHandler:

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
        self.phones_count = 0

    def run(self) -> list:
        phones = []
        possible_phones = str(self.soup)

        for region, regex in regions.items():
            for match in phonenumbers.PhoneNumberMatcher(possible_phones, region):
                not_valid_phone_yet = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
                validated = format_phone_number(not_valid_phone_yet, regex)
                if validated != "":
                    self.phones_count += 1
                    phones.append(validated)

        return phones

    def how_many_phones(self) -> int:
        return self.phones_count
