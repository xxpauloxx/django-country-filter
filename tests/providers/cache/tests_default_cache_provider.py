"""Test case for default cache provider."""

import mock

from datetime import datetime
from django_country_filter.providers.cache.default_cache_provider import (
    DefaultCacheProvider
)


@mock.patch('shelve.open', return_value={})
def test_persist_cache_on_database_not_exist(shelve_mock, get_request_mock):
    """Must be return country if address is cached on non-existent database."""
    data = {'country': 'AU', 'ip': '1.1.1.1'}

    cache_provider = DefaultCacheProvider(get_request_mock)
    cache_provider.persist(data, datetime.now())
    data_cached = cache_provider.db.get('countries')

    assert isinstance(data_cached, list)
    assert data_cached[0]['country'] == 'AU'
    assert data_cached[0]['ip'] == '1.1.1.1'


@mock.patch('shelve.open', return_value={})
def test_persist_cache_on_database_exist(shelve_mock, get_request_mock):
    """Must be return country if address is cached on existing database."""
    first_data = {'country': 'AU', 'ip': '1.1.1.1'}
    second_data = {'country': 'BR', 'ip': '2.2.2.2'}

    cache_provider = DefaultCacheProvider(get_request_mock)
    cache_provider.persist(first_data, datetime.now())
    cache_provider.persist(second_data, datetime.now())
    data_cached = cache_provider.db.get('countries')

    assert isinstance(data_cached, list)
    assert data_cached[1]['country'] == 'BR'
    assert data_cached[1]['ip'] == '2.2.2.2'


@mock.patch('shelve.open', return_value={})
def test_persist_not_duplicate_ip_address(shelve_mock, get_request_mock):
    """Must be return country if address is cached on existing database."""
    first_data = {'country': 'AU', 'ip': '1.1.1.1'}
    second_data = {'country': 'BR', 'ip': '1.1.1.1'}
    third_data = {'country': 'BR', 'ip': '2.2.2.2'}

    cache_provider = DefaultCacheProvider(get_request_mock)
    cache_provider.persist(first_data, datetime.now())
    cache_provider.persist(second_data, datetime.now())
    cache_provider.persist(third_data, datetime.now())
    data_cached = cache_provider.db.get('countries')

    assert isinstance(data_cached, list)
    assert data_cached[0]['country'] == 'BR'
    assert data_cached[0]['ip'] == '1.1.1.1'
    assert data_cached[1]['country'] == 'BR'
    assert data_cached[1]['ip'] == '2.2.2.2'


@mock.patch('shelve.open', return_value={})
def test_persist_get_address(shelve_mock, get_request_mock):
    """Must be return country if address is cached on existing database."""
    first_data = {'country': 'AU', 'ip': '1.1.1.1'}
    now = datetime.now()

    cache_provider = DefaultCacheProvider(get_request_mock)
    cache_provider.persist(first_data, now)
    req = cache_provider.get()

    assert req['ip'] == '1.1.1.1'
    assert req['country'] == 'AU'
    assert req['created_at'] == now


@mock.patch('shelve.open', return_value={})
def test_persist_get_address_not_found(shelve_mock, get_request_mock):
    """Must be return country if address is cached on existing database."""
    first_data = {'country': 'BR', 'ip': '2.2.2.2'}

    cache_provider = DefaultCacheProvider(get_request_mock)
    cache_provider.persist(first_data, datetime.now())
    req = cache_provider.get()

    assert req == {}
