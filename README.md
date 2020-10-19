# Minitower

Kræver pip pakker:
- django == 3.1.1
- jsonpath-ng
- ansible
- django-extensions https://django-extensions.readthedocs.io/en/latest/
- django-environg https://django-environ.readthedocs.io/en/latest/
- pytest
- pytest-django
- pytest-cov
- unittest

## Environmental file .env
Denne fil indholder env variabler til bruge i django installationen.
False if not in os.environ
- DEBUG = env('DEBUG')

Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
- SECRET_KEY = env('SECRET_KEY')

I .env file vil det derfor have input som:
- DEBUG=TRUE
- SECRET_KEY=2F3fkdfu3e9fe>JJF........fFJEFEF



## Pytest 

Python test binary

I pytest.ini er der defineret settings til brug for test. En lokal settings file.

```python
[pytest]
DJANGO_SETTINGS_MODULE = minitower.local_settings

python_files = tests.py test_*.py *_test.py
```