import re
import phonenumbers
from bs4 import BeautifulSoup


def format_us_phone_number(phone_number) -> str:
    match = re.match(r'^\+(\d)(\d{3})(\d{3})(\d{4})$', phone_number)
    if match:
        country_code = match.group(1)
        area_code = match.group(2)
        first_part = match.group(3)
        second_part = match.group(4)
        return f'+{country_code} ({area_code}) {first_part} {second_part}'
    return ""


def format_br_phone_number(phone_number) -> str:
    match = re.match(r'^\+(\d{2})(\d{2})(\d{4})(\d{4})$', phone_number)
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

    def run(self) -> list:
        phones = []
        possible_phones = str(self.soup)

        for match in phonenumbers.PhoneNumberMatcher(possible_phones, "US"):
            not_valid_phone_yet = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
            validated = format_us_phone_number(not_valid_phone_yet)
            if validated != "":
                phones.append(validated)

        for match in phonenumbers.PhoneNumberMatcher(possible_phones, "BR"):
            not_valid_phone_yet = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
            validated = format_br_phone_number(not_valid_phone_yet)
            if validated != "":
                phones.append(validated)

        return phones


