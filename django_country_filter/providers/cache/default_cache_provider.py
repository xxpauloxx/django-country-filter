"""Default cache provider package."""

import shelve

from django.http.request import HttpRequest


class DefaultCacheProvider:
    """Default cache provider implementation."""

    def __init__(self):
        """Initialize."""
        self.db = shelve.open('cache.db')

    def get(self, request: HttpRequest):
        """Get data in cache database."""
        ip = request.META.get('REMOTE_ADDR')
        for req in self.db.get('countries'):
            if req['ip'] == ip:
                return req
        return {}

    def save_on_database(self, data_cache):
        """Save data cache on database."""
        if self.db.get('countries') is None:
            self.db['countries'] = [data_cache]
        else:
            for i in range(len(self.db.get('countries'))):
                country = self.db.get('countries')[i]
                if country.get('ip') == data_cache.get('ip'):
                    self.db.get('countries')[i]['country'] = (
                        data_cache.get('country'))
                else:
                    self.db['countries'].append(data_cache)

    def persist(self, data, created_at):
        """Persist the data on shelve database."""
        data_cache = {
            'country': data['country'],
            'created_at': created_at,
            'ip': data['ip']
        }
        self.save_on_database(data_cache)



