"""Class factory for providers."""

from django.conf import settings
from importlib import import_module

PACKAGE_GEOIP_PROVIDERS = 'django_country_filter.providers.geoip.'


class ProviderFactory:
    """Class factory for providers."""

    @staticmethod
    def get_provider_module(request):
        """Return a provider according to the provider creation conventions."""
        provider_name = settings.DJANGO_COUNTRY_FILTER_PROVIDER
        class_name = provider_name.title().replace('_', '')
        provider = import_module(f'{PACKAGE_GEOIP_PROVIDERS}{provider_name}')
        return getattr(provider, class_name)(request)

    def __init__(self, request):
        """Class initializer."""
        if not hasattr(settings, 'DJANGO_COUNTRY_FILTER_PROVIDER'):
            raise Exception('DJANGO_COUNTRY_FILTER_PROVIDER is not defined.')
        try:
            self.provider = self.get_provider_module(request)
        except Exception:
            raise Exception('Error on provider building: Provider not found.')

    def get(self):
        """Call the get method of the built provider."""
        return self.provider.get()
