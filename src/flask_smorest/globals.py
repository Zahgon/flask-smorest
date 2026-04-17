"""Globals"""

from flask import current_app, request
from werkzeug.local import LocalProxy

from .exceptions import CurrentApiNotAvailableError


def _find_current_api():
    pass


# Proxy for the current Api. Only available within a request context and only
# if current Blueprint is registered in a flask-smorest Api.
current_api = LocalProxy(_find_current_api)
