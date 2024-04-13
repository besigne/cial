import socket
from urllib.parse import urlparse
from geoip2fast import GeoIP2Fast


class UrlHandler:

    def __init__(self, url: str):
        self.url = url

    def url(self):
        return self.url

    def base_url(self):
        return '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.url))

    def find_country_code_from_url(self):
        url = ('{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.url))
               .replace('http://', '').replace('https://', ''))
        ip = socket.gethostbyname(url)
        geoip = GeoIP2Fast(geoip2fast_data_file="database/geoip2fast.dat.gz")
        if geoip:
            return geoip.lookup(ip).country_code
        return ""
