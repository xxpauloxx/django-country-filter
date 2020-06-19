"""Test cases related to the django country filter provider."""

import pytest

from django_country_filter.geoip_provider_factory import (
    GeoipProviderFactory
)
from django.conf import settings
from django.test import override_settings

from mock import patch

settings.configure(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
)


@override_settings(DJANGO_COUNTRY_FILTER_PROVIDER='provider_mock')
def test_provider_with_provider_mock(get_request_mock, get_provider_mock):
    """Must return a correct response because the configuration and\
    the provider are correct."""
    with patch.object(GeoipProviderFactory,
                      'get_custom_provider',
                      return_value=get_provider_mock(get_request_mock)):

        middleware = GeoipProviderFactory(get_request_mock)
        response = middleware.get()

        assert response['country'] == 'AU'
        assert response['ip'] == '1.1.1.1'
