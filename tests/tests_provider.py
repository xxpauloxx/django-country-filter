"""Test cases related to the django country filter provider, which is a factory."""

import pytest

from django_country_filter.provider import DjangoCountryFilterProvider
from django.conf import settings
from django.test import override_settings

from mock import patch

settings.configure(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
)


def test_provider_settings_not_found(get_request_mock):
    """Must return an exception because there is no provider configuration."""
    with pytest.raises(Exception):
        DjangoCountryFilterProvider(get_request_mock)


@override_settings(DJANGO_COUNTRY_FILTER_PROVIDER='not_exists')
def test_provider_not_found(get_request_mock):
    """Must return an exception because there is no provider that is configured."""
    with pytest.raises(Exception):
        DjangoCountryFilterProvider(get_request_mock)


@override_settings(DJANGO_COUNTRY_FILTER_PROVIDER='provider_mock')
def test_provider_success(get_request_mock, get_provider_mock):
    """Must return a correct answer because the configuration and the provider are correct."""
    with patch.object(DjangoCountryFilterProvider,
                      '_get_imported_provider', 
                      return_value=get_provider_mock(get_request_mock)):
        middleware = DjangoCountryFilterProvider(get_request_mock)
        response = middleware.get()
        assert response['country'] == 'AU'
        assert response['ip'] == '1.1.1.1'
