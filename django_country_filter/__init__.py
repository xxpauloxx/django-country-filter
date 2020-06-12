"""
Implementation of the middleware.

Responsible for filtering released countries to access the application.

"""

from django.http.request import HttpRequest
from django.http import HttpResponseForbidden
from django.conf import settings

from .provider import DjangoCountryFilterProvider


class DjangoCountryFilterMiddleware:
    """Django middleware to call the class DjangoCountryFilterProvider."""

    def __init__(self, get_response):
        """Middleware initializer."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        """Check the middleware settings and calls the provider."""
        response = self.get_response(request)
        if hasattr(settings, 'DJANGO_COUNTRY_FILTER_COUNTRIES'):
            if not isinstance(settings.DJANGO_COUNTRY_FILTER_COUNTRIES, list):
                raise Exception(
                    'DJANGO_COUNTRY_FILTER_COUNTRIES is not a list type.')
            else:
                response_provider = DjangoCountryFilterProvider(request).get()
                if not (response_provider['country'] in
                        settings.DJANGO_COUNTRY_FILTER_COUNTRIES):
                    return HttpResponseForbidden()
        return response
