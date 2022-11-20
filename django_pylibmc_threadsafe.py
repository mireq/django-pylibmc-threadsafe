# -*- coding: utf-8 -*-
import contextvars as cv
import types
from functools import wraps

from django.core.cache.backends import memcached
from django.utils.functional import cached_property


# Save connection per context
current_connection = cv.ContextVar("current_connection", default=None)


# Default return values if method throws exception
DEFAULTS = {
	'set_multi': [],
	'set_many': [],
}


def wrap_safe(meth, name):
	"""
	Prevent throwing exceptions from method
	"""
	@wraps(meth)
	def wrapped(*args, **kwargs):
		try:
			return meth(*args, **kwargs)
		except Exception:
			return DEFAULTS.get(name)
	return wrapped


class SafeCache(object):
	"""
	Wraps all methods of object to wrap_safe
	"""
	def __init__(self, cache):
		self._cache = cache

	def __getattribute__(self, name):
		cache = super(SafeCache, self).__getattribute__('_cache')
		attr = cache.__getattribute__(name)
		if type(attr) == types.MethodType or type(attr) == types.BuiltinMethodType:
			attr = wrap_safe(attr, name)
		return attr


class PyLibMCCache(memcached.PyLibMCCache):
	"""
	Thread safe implementation of PyLibMCCache
	"""

	def __init__(self, *args, **kwargs):
		"""
		Use ignore_exc option to prevent raising exceptions.
		"""
		super().__init__(*args, **kwargs)
		self._ignore_exc = self._options.pop('ignore_exc', False)

	@cached_property
	def _base_cache(self):
		return self._class(self.client_servers, **self._options)

	@property
	def _cache(self):
		# Get connection for context
		instance = current_connection.get()
		if instance is None: # Or create new for new context
			instance = self._base_cache.clone()
			if self._ignore_exc: # Wrap connection to SafeCache
				instance = SafeCache(instance)
			current_connection.set(instance)
		return instance
