"""Class factory for providers."""

from importlib import import_module
from django.conf import settings

from django_country_filter.providers.geoip.default_geoip_provider import (
    DefaultGeoipProvider
)


class GeoipProviderFactory:
    """Class factory for geoip providers."""

    def get_custom_provider(self, request):
        """Return a provider according to the provider creation conventions."""
        configuration = settings.DJANGO_COUNTRY_FILTER
        package = import_module('{}'.format(
            configuration.get('geoip_provider_path'))
        )
        return getattr(package, configuration.get('geoip_provider'))(request)

    def __init__(self, request):
        """Class initializer."""
        try:
            self.provider = self.get_custom_provider(request)
        except Exception:
            self.provider = DefaultGeoipProvider(request)

    def get(self):
        """Call the get method of the built provider."""
        return self.provider.get()
