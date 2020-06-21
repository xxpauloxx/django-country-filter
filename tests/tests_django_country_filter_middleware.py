"""Test case for the implementation of the django country filter middleware\
which calls the django country filter provider factory."""

from datetime import datetime
from django_country_filter import DjangoCountryFilterMiddleware
from django_country_filter.geoip_provider_factory import (
    GeoipProviderFactory
)
from django.test import override_settings
from mock import patch
from django_country_filter.providers.cache.default_cache_provider import (
    DefaultCacheProvider
)


def test_initialize(get_response_mock, get_request_mock):
    """Must return the function that has been injected into the\
    middleware initializer."""
    factory = DjangoCountryFilterMiddleware(get_response_mock)
    assert factory.get_response(
        get_request_mock) == 'hello from get_response'


def test_has_no_country_settings(get_response_mock, get_request_mock):
    """Must return the response if the DJANGO_COUNTRY_FILTER_COUNTRIES\
    has not been set."""
    factory = DjangoCountryFilterMiddleware(get_response_mock)
    assert factory(get_request_mock) == 'hello from get_response'


@override_settings(
    DJANGO_COUNTRY_FILTER={
        'countries': 'BR'
    }
)
def test_countries_is_not_a_list(get_response_mock, get_request_mock):
    """Must return an exception when DJANGO_COUNTRY_FILTER.get('countries')\
    not a type list."""
    factory = DjangoCountryFilterMiddleware(get_response_mock)
    assert factory(get_response_mock) == 'hello from get_response'


@override_settings(
    DJANGO_COUNTRY_FILTER={
        'countries': ['BR']
    }
)
@patch('shelve.open', return_value={})
def test_forbidden_when_country_not_set(
    get_response_mock, get_request_mock, get_geoip_provider_mock
):
    """Must return an unauthorized response when the request is from\
    a country that is not in DJANGO_COUNTRY_FILTER_COUNTRIES."""
    with patch.object(GeoipProviderFactory,
                      'get_custom_provider',
                      return_value=get_geoip_provider_mock(get_request_mock)):
        factory = DjangoCountryFilterMiddleware(get_response_mock)
        response = factory(get_request_mock)
        assert response.status_code == 403


@override_settings(
    DJANGO_COUNTRY_FILTER={
        'countries': ['BR']
    }
)
@patch('shelve.open', return_value={})
def test_forbidden_ip_cached(
        get_response_mock, get_request_mock, get_geoip_provider_mock):
    data = {'country': 'AU', 'ip': '1.1.1.1'}

    cache_provider = DefaultCacheProvider(get_request_mock)
    cache_provider.persist(data, datetime.now())

    factory = DjangoCountryFilterMiddleware(get_response_mock)
    response = factory(get_request_mock)
    assert response.status_code == 403


@override_settings(
    DJANGO_COUNTRY_FILTER={
        'countries': ['BR']
    }
)
@patch('shelve.open', return_value={})
def test_ip_cached_persist(
        get_response_mock, get_request_mock, get_geoip_provider_mock):
    with patch.object(GeoipProviderFactory,
                      'get_custom_provider',
                      return_value=get_geoip_provider_mock(get_request_mock)):
        data = {'country': 'BR', 'ip': '1.1.1.1'}

        cache_provider = DefaultCacheProvider(get_request_mock)
        cache_provider.persist(data, datetime.now())

        factory = DjangoCountryFilterMiddleware(get_response_mock)
        response = factory(get_request_mock)
        assert response.status_code == 403


@override_settings(
    DJANGO_COUNTRY_FILTER={
        'countries': ['BR'],
        'cache_provider': 'CacheProviderMock',
        'cache_provider_path': 'tests.mocks.providers.cache.cache_provider_mock'
    }
)
@patch('shelve.open', return_value={})
def test_ip_cached_persist(
        get_response_mock, get_request_mock, get_geoip_provider_mock):
    with patch.object(GeoipProviderFactory,
                      'get_custom_provider',
                      return_value=get_geoip_provider_mock(get_request_mock)):
        data = {'country': 'BR', 'ip': '1.1.1.1'}

        cache_provider = DefaultCacheProvider(get_request_mock)
        cache_provider.persist(data, datetime.now())

        factory = DjangoCountryFilterMiddleware(get_response_mock)
        response = factory(get_request_mock)
        assert response.status_code == 403
