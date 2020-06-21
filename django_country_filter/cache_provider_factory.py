"""Cache provider factory."""

from importlib import import_module
from django.conf import settings
from django_country_filter.providers.cache.default_cache_provider import (
    DefaultCacheProvider
)


class CacheProviderFactory:
    """Cache provider factory implementation."""

    @staticmethod
    def get_custom_provider(request):
        """Return a provider according to the provider creation conventions."""
        configuration = settings.DJANGO_COUNTRY_FILTER
        package = import_module('{}'.format(
            configuration.get('cache_provider_path'))
        )
        return getattr(package, configuration.get('cache_provider'))(request)

    def __init__(self, request):
        """Class initializer."""
        self.request = request
        try:
            self.provider = CacheProviderFactory.get_custom_provider(request)
        except Exception:
            self.provider = DefaultCacheProvider(request)

    def get(self):
        """Call the get method of the built provider."""
        return self.provider.get()
