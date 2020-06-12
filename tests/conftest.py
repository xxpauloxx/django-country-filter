"""Configurations for tests."""

import pytest

from django.http.request import HttpRequest
from django.test.client import RequestFactory

from .mocks.provider_mock import ProviderMock


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
def get_provider_mock():
    """Return the ProviderMock class."""
    return ProviderMock
