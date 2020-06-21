"""Test case for ip2c provider."""

import pytest

from django_country_filter.geoip_provider_factory import (
    GeoipProviderFactory
)
from django_country_filter.providers.geoip.default_geoip_provider import (
    DefaultGeoipProvider
)


def test_initialize(get_request_mock):
    """Initialize should be define a attribute request."""
    provider = DefaultGeoipProvider(get_request_mock)
    assert provider.request is get_request_mock


def test_get(requests_mock, get_request_mock):
    """Return a dict with country and ip."""
    requests_mock.get('https://ip2c.org/1.1.1.1', text='1;AU;AUS;Australia')

    provider = DefaultGeoipProvider(get_request_mock)
    response = provider.get()

    assert response['country'] == 'AU'
    assert response['ip'] == '1.1.1.1'


def test_provider_with_ip2c_provider(get_request_mock, requests_mock):
    """Must return a correct response with ip2c provider."""
    requests_mock.get('https://ip2c.org/1.1.1.1', text='1;AU;AUS;Australia')

    middleware = GeoipProviderFactory(get_request_mock)
    response = middleware.get()

    assert response['country'] == 'AU'
    assert response['ip'] == '1.1.1.1'


def test_ip2c_exception(get_request_mock, requests_mock):
    """Must return an exception with ip2c provider."""
    requests_mock.get('https://ip2c.org/1.1.1.1', text='1;AU;AUS;Australia',
                      status_code=500)

    with pytest.raises(Exception):
        provider = DefaultGeoipProvider(get_request_mock)
        provider.get()
