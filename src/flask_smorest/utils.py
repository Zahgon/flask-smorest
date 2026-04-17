"""Utils"""
from collections import abc
from flask import g
from werkzeug.datastructures import Headers
from apispec.utils import dedent, trim_docstring

def deepupdate(original, update):
    """Recursively update a dict.

    Subdict's won't be overwritten but also updated.
    """
    pass

def remove_none(mapping):
    """Remove None values in a dict"""
    pass

def resolve_schema_instance(schema):
    """Return schema instance for given schema (instance or class).

    :param type|Schema schema: marshmallow.Schema instance or class
    :return: schema instance of given schema
    """
    pass

def get_appcontext():
    """Get extension section in flask g"""
    pass

def load_info_from_docstring(docstring, *, delimiter='---'):
    """Load summary and description from docstring

    :param str delimiter: Summary and description information delimiter.
    If a line starts with this string, this line and the lines after are
    ignored. Defaults to "---".
    """
    pass

def unpack_tuple_response(rv):
    """Unpack a flask Response tuple"""
    pass

def set_status_and_headers_in_response(response, status, headers):
    """Set status and headers in flask Response object"""
    pass

def prepare_response(response, spec, content_type):
    """Rework response according to OAS version"""
    pass

def normalize_config_prefix(config_prefix):
    """Normalize API config prefix

    Sets upper case and appends underscore if missing.

    :param str config_prefix: Raw prefix

    :return: Normalized prefix
    """
    pass

class PrefixedMappingProxy(abc.Mapping):
    """Mapping to proxy another mapping using a prefix

    .. code-block:: python
        some_dict = PrefixedMappingProxy(
            proxied_dict={"foobar_key1": 1, "foobar_key2": 2}, prefix="foobar_"
        )
        assert some_dict["key1"] == 1
        assert some_dict["key2"] == 2
    """

    def __init__(self, proxied_dict, prefix):
        self._dict = proxied_dict
        self.prefix = prefix

    def __getitem__(self, key):
        return self._dict[self.prefix + str(key)]

    def __iter__(self):
        return iter((x for x in self._dict if x.startswith(self.prefix)))

    def __len__(self):
        return sum((1 for _ in iter(self)))
