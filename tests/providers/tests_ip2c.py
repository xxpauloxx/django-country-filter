"""Test case for ip2c provider."""

import pytest

from django_country_filter.providers.ip2c import Ip2C
from django.test import override_settings

from django_country_filter.provider import DjangoCountryFilterProvider


def test_initialize(get_request_mock):
    """Initialize should be define a attribute request."""
    provider = Ip2C(get_request_mock)
    assert provider.request is get_request_mock


def test_get(requests_mock, get_request_mock):
    """Return a dict with country and ip."""
    requests_mock.get('https://ip2c.org/1.1.1.1', text='1;AU;AUS;Australia')

    provider = Ip2C(get_request_mock)
    response = provider.get()

    assert response['country'] == 'AU'
    assert response['ip'] == '1.1.1.1'


@override_settings(DJANGO_COUNTRY_FILTER_PROVIDER='ip2c')
def test_provider_with_ip2c_provider(get_request_mock, get_provider_mock,
                                     requests_mock):
    """Must return a correct response with ip2c provider."""
    requests_mock.get('https://ip2c.org/1.1.1.1', text='1;AU;AUS;Australia')

    middleware = DjangoCountryFilterProvider(get_request_mock)
    response = middleware.get()

    assert response['country'] == 'AU'
    assert response['ip'] == '1.1.1.1'


@override_settings(DJANGO_COUNTRY_FILTER_PROVIDER='ip2c')
def test_ip2c_exception(get_request_mock, get_provider_mock,
                                     requests_mock):
    """Must return an exception with ip2c provider."""
    requests_mock.get('https://ip2c.org/1.1.1.1', text='1;AU;AUS;Australia',
                      status_code=500)

    with pytest.raises(Exception):
        provider = Ip2C(get_request_mock)
        response = provider.get()
