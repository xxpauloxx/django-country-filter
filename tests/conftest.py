"""Configurations for tests."""

import pytest

from django.http.request import HttpRequest
from django.test.client import RequestFactory

from .mocks.providers.geoip.geoip_provider_mock import GeoipProviderMock
from .mocks.providers.cache.cache_provider_mock import CacheProviderMock

from django.conf import settings
settings.configure(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
)


@pytest.fixture
def get_response_mock():
    """Mock for get_response method on middleware."""
    def get_response_closure(request: HttpRequest):
        return 'hello from get_response'
    return get_response_closure


@pytest.fixture
def get_request_mock():
    """Mock request."""
    request = RequestFactory()
    request.META = {'REMOTE_ADDR': '1.1.1.1'}
    return request


@pytest.fixture
def get_geoip_provider_mock():
    """Return the GeoipProviderMock class."""
    return GeoipProviderMock


@pytest.fixture
def get_cache_provider_mock():
    """Return the CacheProviderMock class."""
    return CacheProviderMock
