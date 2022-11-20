============================================
Thread safe pylibmc cache backend for django
============================================

|version| |downloads| |license|

Default django pylibmc cache backend don't work correctly using multithread
uWSGI or celery worker.

This package uses separate connection for each context (thread or async context)
and can be used as direct replacement of
``django.core.cache.backends.memcached.PyLibMCCache``.

Install
-------

.. code:: bash

	pip install django_pylibmc_threadsafe

Configuration
-------------

This package has only one additional option - ``ignore_exc`` used to suppress all
exceptions (behavior used in old
``django.core.cache.backends.memcached.MemcachedCache`` backend). All other
options are identical to ``django.core.cache.backends.memcached.PyLibMCCache``.

Example configuration:

.. code-block:: python

	CACHES = {
		'default': {
			'BACKEND': 'django_pylibmc_threadsafe.PyLibMCCache',
			'LOCATION': '127.0.0.1:11211',
			'KEY_PREFIX': '',
			'OPTIONS': {
				'binary': True,
				'ignore_exc': True,
				'behaviors': {
					'ketama': True,
				}
			}
		},

.. |version| image:: https://badge.fury.io/py/django-pylibmc-threadsafe.svg
	:target: https://pypi.python.org/pypi/django-pylibmc-threadsafe/

.. |downloads| image:: https://img.shields.io/pypi/dw/django-pylibmc-threadsafe.svg
	:target: https://pypi.python.org/pypi/django-pylibmc-threadsafe/

.. |license| image:: https://img.shields.io/pypi/l/django-pylibmc-threadsafe.svg
	:target: https://pypi.python.org/pypi/django-pylibmc-threadsafe/
