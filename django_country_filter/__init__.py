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

    configuration = None

    def __init__(self, get_response):
        """Middleware initializer."""
        self.get_response = get_response

    def check_countries_in_settings(self):
        """Check countries configuration."""
        countries = self.configuration.get('countries')
        if not isinstance(countries, list):
            (DjangoCountryFilterMiddleware
                .logging_check_countries_in_settings())
            return False
        return True

    def __call__(self, request: HttpRequest):
        """Check the middleware settings and calls the provider."""
        if hasattr(settings, 'DJANGO_COUNTRY_FILTER'):
            self.configuration = settings.DJANGO_COUNTRY_FILTER
            request_ip = request.META.get('REMOTE_ADDR')

            if self.check_countries_in_settings():
                cache_provider = CacheProviderFactory(request)
                cache_country = cache_provider.get().get('country')

                if (self.country_is_blocked(cache_country) 
                        and cache_country is not None):
                    (DjangoCountryFilterMiddleware
                        .logging_country_is_blocked(cache_country, request_ip))
                    return HttpResponseForbidden()

                geoip_response = GeoipProviderFactory(request).get()
                geoip_country = geoip_response.get('country')
                cache_provider.provider.persist(geoip_response, datetime.now())

                if self.country_is_blocked(geoip_country):
                    (DjangoCountryFilterMiddleware
                        .logging_country_is_blocked(geoip_country, request_ip))
                    return HttpResponseForbidden()

        return self.get_response(request)

    def country_is_blocked(self, country):
        """Check if the country is blocked."""
        return country not in self.configuration.get('countries')

    @staticmethod
    def logging_country_is_blocked(country, ip):
        """Log information of the block request."""
        log.warning("""
            DJANGO_COUNTRY_FILTER:
            {} is blocked with ip address {}. 
        """.format(country, ip))

    @staticmethod
    def logging_check_countries_in_settings():
        """Log information when countries is not a list or not configured."""
        log.warning("""
            DJANGO_COUNTRY_FILTER:
            countries in settings is not a list or not exist.
        """)
