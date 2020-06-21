"""Test cases related to the django country filter provider."""

from django_country_filter.cache_provider_factory import (
    CacheProviderFactory
)
from django.test import override_settings


def test_provider_with_default_provider(
        get_request_mock, get_geoip_provider_mock
):
    """Must return a correct provider with default cache provider."""
    factory = CacheProviderFactory(get_request_mock)
    assert 'DefaultCacheProvider' in factory.provider.__str__()


@override_settings(DJANGO_COUNTRY_FILTER={
    'cache_provider': 'CacheProviderMock',
    'cache_provider_path': 'tests.mocks.providers.cache.cache_provider_mock'
})
def test_provider_get_custom_provider(
    get_request_mock, get_geoip_provider_mock
):
    """Must return a correct provider with custom cache provider."""
    factory = CacheProviderFactory(get_request_mock)
    assert 'CacheProviderMock' in factory.provider.__str__()


