"""Class factory for providers."""

import logging

from importlib import import_module
from django.conf import settings

log = logging.getLogger(__name__)


class GenericProviderFactory:
    """Generic class factory for providers."""

    __TAG = 'GenericProviderFactory'

    _PROVIDER_PATH = ''
    _PROVIDER = ''
    _DEFAULT_CLASS_PROVIDER = None

    def get_custom_provider(self, request):
        """Return a provider according to the provider creation conventions."""
        configuration = settings.DJANGO_COUNTRY_FILTER
        package = import_module('{}'.format(
            configuration.get(self._PROVIDER_PATH)))
        return getattr(package, configuration.get(self._PROVIDER))(request)

    def __init__(self, request):
        """Class initializer."""
        try:
            self.provider = self.get_custom_provider(request)
        except Exception as e:
            log.info(f'{self.__TAG} error: {e}')
            self.provider = self._DEFAULT_CLASS_PROVIDER(request)

    def get(self):
        """Call the get method of the built provider."""
        return self.provider.get()
