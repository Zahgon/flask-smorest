"""apispec plugins"""

import re
from collections.abc import Mapping

import werkzeug.routing

from apispec import BasePlugin

# from flask-restplus
RE_URL = re.compile(r"<(?:[^:<>]+:)?([^<>]+)>")


def baseconverter2paramschema(converter):
    pass


def unicodeconverter2paramschema(converter):
    pass


def integerconverter2paramschema(converter):
    pass


def floatconverter2paramschema(converter):
    pass


def anyconverter2paramschema(converter):
    pass


def uuidconverter2paramschema(converter):
    pass


DEFAULT_CONVERTER_MAPPING = {
    werkzeug.routing.BaseConverter: baseconverter2paramschema,
    werkzeug.routing.AnyConverter: anyconverter2paramschema,
    werkzeug.routing.UnicodeConverter: unicodeconverter2paramschema,
    werkzeug.routing.IntegerConverter: integerconverter2paramschema,
    werkzeug.routing.FloatConverter: floatconverter2paramschema,
    werkzeug.routing.UUIDConverter: uuidconverter2paramschema,
}


class FlaskPlugin(BasePlugin):
    """Plugin to create OpenAPI paths from Flask rules

    Heavily copied from apispec.
    """

    def __init__(self):
        super().__init__()
        self.converter_mapping = dict(DEFAULT_CONVERTER_MAPPING)
        self.openapi_version = None

    def init_spec(self, spec):
        pass

    # From apispec
    @staticmethod
    def flaskpath2openapi(path):
        """Convert a Flask URL rule to an OpenAPI-compliant path.

        :param str path: Flask path template.
        """
        pass

    def register_converter(self, converter, func):
        """Register custom path parameter converter

        :param BaseConverter converter: Converter.
            Subclass of werkzeug's BaseConverter
        :param callable func: Function returning a parameter schema from
            a converter intance
        """
        pass

    def rule_to_params(self, rule):
        """Get parameters from flask Rule"""
        pass

    def path_helper(self, rule, operations, parameters, **kwargs):
        """Get path from flask Rule and set path parameters in operations"""
        pass
