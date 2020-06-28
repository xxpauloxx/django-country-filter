"""Django country filter middleware implementation."""

import logging

from datetime import datetime
from django.http.request import HttpRequest
from django.http import HttpResponseForbidden
from django.conf import settings

from .geoip_provider_factory import GeoipProviderFactory
from .cache_provider_factory import CacheProviderFactory

log = logging.getLogger(__name__)


class DjangoCountryFilterMiddleware:
    """Django middleware to call the classes factories or default providers."""

    __TAG = 'DjangoCountryFilterMiddleware'

    __CONFIGURATION = None
    __CACHE_PROVIDER = None
    __GEOIP_PROVIDER = None

    def __init__(self, get_response):
        """Middleware initializer."""
        self.get_response = get_response

    def check_countries_in_settings(self):
        """Check countries configuration."""
        countries = self.configuration.get('countries')
        if not isinstance(countries, list):
            self.logging_check_countries_in_settings()
            return False
        return True

    def is_blocked_from_cache(self, request):
        """Check ip on cache and block if not exist countries settings."""
        ip = request.META.get('REMOTE_ADDR')
        self.__CACHE_PROVIDER = CacheProviderFactory(request)
        country = self.__CACHE_PROVIDER.get().get('country')
        if country is None:
            return {'cache': 'NONE'}
        if self.country_is_blocked(country) and country is not None:
            self.logging_country_is_blocked(country, ip)
            return {'cache': 'BLOCK'}
        return {'cache': 'RELEASE'}

    def is_blocked_from_geoip(self, request):
        """Check ip and block if country not exist countries settings."""
        ip = request.META.get('REMOTE_ADDR')
        response = GeoipProviderFactory(request).get()
        country = response.get('country')
        self.__CACHE_PROVIDER.provider.persist(response, datetime.now())
        if self.country_is_blocked(country):
            self.logging_country_is_blocked(country, ip)
            return True
        return False

    def __call__(self, request: HttpRequest):
        """Check the middleware settings and calls the provider."""
        if hasattr(settings, 'DJANGO_COUNTRY_FILTER'):
            self.configuration = settings.DJANGO_COUNTRY_FILTER
            if self.check_countries_in_settings():
                cache_result = self.is_blocked_from_cache(request)
                if cache_result.get('cache') == 'BLOCK':
                    return HttpResponseForbidden()
                elif cache_result.get('cache') == 'RELEASE':
                    return self.get_response(request)
                elif cache_result.get('cache') == 'NONE':
                    if self.is_blocked_from_geoip(request):
                        return HttpResponseForbidden()
        return self.get_response(request)

    def country_is_blocked(self, country):
        """Check if the country is blocked."""
        return country not in self.configuration.get('countries')

    def logging_country_is_blocked(self, country, ip):
        """Log information of the block request."""
        log.warning(f'{self.__TAG}: {country} is blocked with ip address {ip}.')

    def logging_check_countries_in_settings(self):
        """Log information when countries is not a list or not configured."""
        log.warning(f'{self.__TAG}: Countries is not a list or not exist.')
