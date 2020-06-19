"""Test case for the implementation of the django country filter middleware\
which calls the django country filter provider factory."""

import pytest

from django_country_filter import DjangoCountryFilterMiddleware
from django_country_filter.geoip_provider_factory import (
    GeoipProviderFactory
)
from django.test import override_settings
from mock import patch


def test_initialize(get_response_mock, get_request_mock):
    """Must return the function that has been injected into the\
    middleware initializer."""
    middleware = DjangoCountryFilterMiddleware(get_response_mock)
    assert middleware.get_response(
        get_request_mock) == 'hello from get_response'


def test_has_no_country_settings(get_response_mock, get_request_mock):
    """Must return the response if the DJANGO_COUNTRY_FILTER_COUNTRIES\
    has not been set."""
    middleware = DjangoCountryFilterMiddleware(get_response_mock)
    assert middleware(get_request_mock) == 'hello from get_response'


@override_settings(
    DJANGO_COUNTRY_FILTER={
        'countries': 'BR'
    }
)
def test_countries_is_not_a_list(get_response_mock, get_request_mock):
    """Must return an exception when DJANGO_COUNTRY_FILTER.get('countries')\
    not a type list."""
    middleware = DjangoCountryFilterMiddleware(get_response_mock)
    assert middleware(get_response_mock) == 'hello from get_response'


@override_settings(
    DJANGO_COUNTRY_FILTER={
        'countries': ['BR']
    }
)
def test_forbidden_when_country_not_set(
    get_response_mock, get_request_mock, get_provider_mock
):
    """Must return an unauthorized response when the request is from\
    a country that is not in DJANGO_COUNTRY_FILTER_COUNTRIES."""
    with patch.object(GeoipProviderFactory,
                      'get_custom_provider',
                      return_value=get_provider_mock(get_request_mock)):
        middleware = DjangoCountryFilterMiddleware(get_response_mock)
        response = middleware(get_request_mock)
        assert response.status_code == 403
