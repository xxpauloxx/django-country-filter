"""Ip2c provider."""

import requests
from django.http.request import HttpRequest


class DefaultGeoipProvider:
    """Implementation of the provider based on the ip2c.org service."""

    __TAG = 'DefaultGeoipProvider'
    __URI = 'https://ip2c.org/{}'

    def __init__(self, request: HttpRequest):
        """Initialize class."""
        self.request = request

    def get(self):
        """Must return the country and the IP address that made the\
        request in the application."""
        ip = self.request.META.get('REMOTE_ADDR')
        response = requests.get(self.__URI.format(ip))
        if response.status_code != 200:
            status_code = response.status_code
            content = response.content
            raise Exception(f'{self.__TAG}: {status_code}\n{content}')
        country = response.content.decode().split(';')[1]
        return {'country': country, 'ip': ip}
