"""Test cases related to the django country filter provider."""

from django_country_filter.geoip_provider_factory import (
    GeoipProviderFactory
)
from django.test import override_settings


def test_provider_with_default_provider(get_request_mock, get_provider_mock):
    """Must return a correct response because the configuration and\
    the provider are correct."""
    factory = GeoipProviderFactory(get_request_mock)
    assert 'DefaultGeoipProvider' in factory.provider.__str__()


@override_settings(
    DJANGO_COUNTRY_FILTER={
        'geoip_provider': 'GeoipProviderMock',
        'geoip_provider_path': 'tests.mocks.providers.geoip.geoip_provider_mock'
    }
)
def test_provider_with_custom_provider(get_request_mock, get_provider_mock):
    """Must return a correct response because the configuration and\
    the provider are correct."""
    factory = GeoipProviderFactory(get_request_mock)
    response = factory.get()

    assert response['country'] == 'AU'
    assert response['ip'] == '1.1.1.1'
