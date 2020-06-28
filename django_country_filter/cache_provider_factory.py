"""Cache provider factory."""

from django_country_filter.generic_provider_factory import GenericProviderFactory
from django_country_filter.providers.cache.default_cache_provider import (
    DefaultCacheProvider
)


class CacheProviderFactory(GenericProviderFactory):
    """Cache class provider factory implementation."""

    _PROVIDER_PATH = 'cache_provider_path'
    _PROVIDER = 'cache_provider'
    _DEFAULT_CLASS_PROVIDER = DefaultCacheProvider
