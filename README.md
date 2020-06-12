# DJANGO COUNTRY FILTER  
  
Django middleware is an application access filter from the country of the request. The idea that you can do an access control directly in the application, without the need for a firewall or other resource, because often the applications are for country-specific use without many complexities.  
  
  
## Installation and use

The use of middleware is very simple, just install the middleware via pip and configure it in the application.

```bash
$ pip install django_country_filter
```

In the `settings.py` file of the Django application, just insert the following line in the `MIDDLEWARE` configuration.  

Need to `DJANGO_COUNTRY_FILTER_PROVIDER` and `DJANGO_COUNTRY_FILTER_COUNTRIES` configurations.
```
MIDDLEWARE = {
    'django_country_filter.DjangoCountryFilterMiddleware',
    ...
}

DJANGO_COUNTRY_FILTER_PROVIDER = 'ip2c' # But you can create your provider.
DJANGO_COUNTRY_FILTER_COUNTRIES = ['BR'] # Only Brazil access application.
```

## How to help in development?

You can help improve the code, improve the documentation and also implement new providers. To help, just keep the tests integral.

### Environment

```bash
$ python -m venv .env
$ source .env/bin/activate
$ pip install -r requirements/development.txt
$ pytest
```
