"""
Implementation of the middleware.

Responsible for filtering released countries to access the application.

"""
import logging

from datetime import datetime
from django.http.request import HttpRequest
from django.http import HttpResponseForbidden
from django.conf import settings

from .geoip_provider_factory import GeoipProviderFactory
from .cache_provider_factory import CacheProviderFactory

log = logging.getLogger(__name__)


class DjangoCountryFilterMiddleware:
    """Django middleware to call the class GeoipProviderFactory."""

    configuration = None

    def __init__(self, get_response):
        """Middleware initializer."""
        self.get_response = get_response

    def check_countries_in_settings(self):
        """Check countries configuration."""
        countries = self.configuration.get('countries')
        if not isinstance(countries, list):
            log.warning('''
                DJANGO_COUNTRY_FILTER:
                countries field on settings must be list.
            ''')
            return False
        return True

    def __call__(self, request: HttpRequest):
        """Check the middleware settings and calls the provider."""
        if hasattr(settings, 'DJANGO_COUNTRY_FILTER'):
            self.configuration = settings.DJANGO_COUNTRY_FILTER
            if self.check_countries_in_settings():
                cache_provider = CacheProviderFactory(request)
                if self.blocked_country(cache_provider.get().get('country')):
                    return HttpResponseForbidden()
                geoip_provider = GeoipProviderFactory(request).get()
                cache_provider.provider.persist(geoip_provider, datetime.now())
                if self.blocked_country(geoip_provider['country']):
                    return HttpResponseForbidden()
        return self.get_response(request)

    def blocked_country(self, country):
        """Check if the country is blocked."""
        return country not in self.configuration.get('countries')
