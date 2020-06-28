"""Class factory for providers."""

from django_country_filter.generic_provider_factory import GenericProviderFactory
from django_country_filter.providers.geoip.default_geoip_provider import (
    DefaultGeoipProvider
)


class GeoipProviderFactory(GenericProviderFactory):
    """Geoip class provider factory implementation."""

    _PROVIDER_PATH = 'geoip_provider_path'
    _PROVIDER = 'geoip_provider'
    _DEFAULT_CLASS_PROVIDER = DefaultGeoipProvider
