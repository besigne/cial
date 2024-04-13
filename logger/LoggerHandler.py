import logging
import time
from datetime import datetime, timedelta


class LoggerHandler:

    def __init__(self, running_test=False):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(message)s')

        if running_test:
            file_handler = logging.FileHandler('tests/tests_log')
        else:
            file_handler = logging.FileHandler('log')

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def start(self, start: time) -> None:
        self.logger.info(f'Process started at {datetime.fromtimestamp(start).strftime('%d/%m/%Y %H:%M:%S')}')

    def stop(self, stop: time, elapsed: float) -> None:
        self.logger.info(f'Process finished at {datetime.fromtimestamp(stop).strftime('%d/%m/%Y %H:%M:%S')}'
                         f' - Runtime: {timedelta(seconds=round(elapsed, 2))}')

    def log(self, url: str, status_code: int, logo_path: str, phones_count: int) -> None:
        msg = f'{url} - Status {status_code}'
        msg += f' - logo: {logo_path} - {phones_count} phones found'\
            if logo_path != "" else f' - no logo found - {phones_count} phones found'
        self.logger.info(msg)

    def fail(self, url: str, status: int) -> None:
        self.logger.warning(f'{url} - Status Code {status} - Dead Page')

    def url_fail(self, url: str) -> None:
        self.logger.warning(f'{url} - Malformed URL')
