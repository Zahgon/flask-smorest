"""Arguments parsing"""
import http
from collections import abc
from copy import deepcopy
from functools import wraps
from flask import current_app
from webargs.flaskparser import FlaskParser
from .utils import deepupdate

class ArgumentsMixin:
    """Extend Blueprint to add arguments parsing feature"""
    ARGUMENTS_PARSER = FlaskParser()

    def arguments(self, schema, *, location='json', content_type=None, required=True, description=None, example=None, examples=None, **kwargs):
        """Decorator specifying the schema used to deserialize parameters

        :param type|Schema schema: Marshmallow ``Schema`` class or instance
            used to deserialize and validate the argument.
        :param str location: Location of the argument.
        :param str content_type: Content type of the argument.
            Should only be used in conjunction with ``json``, ``form`` or
            ``files`` location.
            The default value depends on the location and is set in
            ``Blueprint.DEFAULT_LOCATION_CONTENT_TYPE_MAPPING``.
            This is only used for documentation purpose.
        :param bool required: Whether argument is required (default: True).
        :param str description: Argument description.
        :param dict example: Parameter example.
        :param dict examples: Parameter examples.
        :param kwargs: Keyword arguments passed to the webargs
            :meth:`use_args <webargs.core.Parser.use_args>` decorator used
            internally.

        The `required` and `description` only affect `body` arguments
        (OpenAPI 2) or `requestBody` (OpenAPI 3), because the docs expose the
        whole schema. For other locations, the schema is turned into an array
        of parameters and the required/description value of each parameter item
        is taken from the corresponding field in the schema.

        The `example` and `examples` parameters are mutually exclusive and
        should only be used with OpenAPI 3 and when location is ``json``.

        See :doc:`Arguments <arguments>`.
        """
        pass

    def _prepare_arguments_doc(self, doc, doc_info, *, api, spec, **kwargs):
        pass
