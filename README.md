# DJANGO COUNTRY FILTER  

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7979a0e1e3b449ef8e946a2dc8eeb74f)](https://app.codacy.com/manual/paulo-pinda/django-country-filter?utm_source=github.com&utm_medium=referral&utm_content=0p4ul0/django-country-filter&utm_campaign=Badge_Grade_Dashboard)

Django middleware is an application access filter from the country of the request. The idea that you can do an access control directly in the application, without the need for a firewall or other resource, because often the applications are for country-specific use without many complexities.  
  
## BUILD PROJECT

The use of middleware is very simple, just install the middleware via pip and configure it in the application.

```bash
$ pip install django-country-filter
```
In the `settings.py` file of the Django application, just insert the following line in the `MIDDLEWARE` configuration and
`DJANGO_COUNTRY_FILTER` configuration with parameters `countries`, this is sufficient to load the
default geoip provider.

```python
MIDDLEWARE = {
    'django_country_filter.DjangoCountryFilterMiddleware',
    ...
}

DJANGO_COUNTRY_FILTER = {
    'countries': ['BR']
}
```

## CUSTOM GEOIP PROVIDERS

There is a possibility that you can create your plug-in geoip provider in django-country-filter, using the `geoip_provider` and` geoip_provider_path` settings.

```python
DJANGO_COUNTRY_FILTER = {
    'countries': ['BR'],
    'geoip_provider': '{NameClassProvider}',
    'geoip_provider_path': '{package_directory.package_py}'
}
```

## HELP ME

You can help improve the code, improve the documentation and also implement new providers. To help, just keep the tests integral.

### DEVELOPMENT ENVIRONMENT

```bash
$ python -m venv .env
$ source .env/bin/activate
$ pip install -r requirements/development.txt
$ pytest
```

### BUILD CUSTOM GEOIP PROVIDER

To create a geoip provider is very simple, just follow the convention used
by `django-country-filter`, you need a class with a method called` get` and
with an initializer that receives a `HttpRequest` object from Django.

To create a geoip provider is very simple, just follow the convention used
by `django-country-filter`, you need a class with a method called` get` and
with an initializer that receives a `HttpRequest` object from Django.

```python
"""Template for geoip provider."""

from django.http.request import HttpRequest


class TemplateGeoipProvider:
    """Template geoip provider."""

    def __init__(self, request: HttpRequest):
        """Initialize."""
        self.request = request

    def get(self):
        """The method makes a request at the geoip provider and returns a
        dictionary with the country and the ip address of the request object."""

        return {
            'country': 'AU',
            'ip': self.request.META.get('REMOTE_ADDR')
        }
```

