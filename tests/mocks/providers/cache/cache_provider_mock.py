"""Cache provider mock."""

from django.http.request import HttpRequest
from datetime import datetime


class CacheProviderMock:
    """Cache provider mock implementation."""

    def __init__(self, request: HttpRequest):
        """Initialize."""
        self.db = {}
        self.request = request

    def get(self):
        """Get data in cache database."""
        ip = self.request.META.get('REMOTE_ADDR')
        if ip == '1.1.1.1':
            return {
                'country': 'BR',
                'ip': ip,
                'created_at': datetime.now()
            }
        return {}

    def persist(self, data, created_at):
        """Persist the data on shelve database."""
        data_cache = {
            'country': data['country'],
            'created_at': created_at,
            'ip': data['ip']
        }
        self.db.update({'countries': [data_cache]})
