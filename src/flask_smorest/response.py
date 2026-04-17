"""Response processor"""
import http
from collections import abc
from copy import deepcopy
from functools import wraps
from flask import current_app, jsonify
from werkzeug import Response
from .utils import deepupdate, get_appcontext, prepare_response, remove_none, resolve_schema_instance, set_status_and_headers_in_response, unpack_tuple_response

class ResponseMixin:
    """Extend Blueprint to add response handling"""

    def response(self, status_code, schema=None, *, content_type=None, description=None, example=None, examples=None, headers=None):
        """Decorator generating an endpoint response

        :param int|str|HTTPStatus status_code: HTTP status code.
            Used if none is returned from the view function.
        :param schema schema|str|dict: :class:`Schema <marshmallow.Schema>`
            class or instance or reference or dict.
            If not None, will be used to serialize response data.
        :param str content_type: Content type of the response.
        :param str description: Description of the response (default: None).
        :param dict example: Example of response message.
        :param dict examples: Examples of response message.
        :param dict headers: Headers returned by the response.

        The decorated function is expected to return the same types of value
        than a typical flask view function, except the body part may be an
        object or a list of objects to serialize with the schema, rather than
        a ``string``.

        If the decorated function returns a ``Response`` object, the ``schema``
        and ``status_code`` parameters are only used to document the resource.
        Only in this case, ``schema`` may be a reference as string or a schema
        definition as dict.

        The `example` and `examples` parameters are mutually exclusive. The
        latter should only be used with OpenAPI 3.

        The `example`, `examples` and `headers` parameters are only used to
        document the resource.

        See :doc:`Response <response>`.
        """
        pass

    def alt_response(self, status_code, response=None, *, schema=None, content_type=None, description=None, example=None, examples=None, headers=None, success=False):
        """Decorator documenting an alternative response

        :param int|str|HTTPStatus status_code: HTTP status code.
        :param str response: Response reference.
        :param schema schema|str|dict: :class:`Schema <marshmallow.Schema>`
            class or instance or reference or dict.
        :param str description: Description of the response (default: None).
        :param dict example: Example of response message.
        :param dict examples: Examples of response message.
        :param dict headers: Headers returned by the response.
        :param bool success: ``True`` if this response is part of the normal
            flow of the function. Default: ``False``.

        This decorator allows the user to document an alternative response.
        This can be an error managed with :func:`abort <abort>` or any response
        that is not the primary flow of the function documented by
        :meth:`Blueprint.response <Blueprint.response>`.

        When a response reference is passed as ``response``, it is used as
        description and the keyword arguments are ignored. Otherwise, a
        description is built from the keyword arguments.

        See :ref:`document-alternative-responses`.
        """
        pass

    @staticmethod
    def _make_doc_response_schema(schema):
        """Override this to modify response schema in docs

        This can be used to document a wrapping structure.

            Example: ::

                @staticmethod
                def _make_doc_response_schema(schema):
                    if schema:
                        return type(
                            "Wrap" + schema.__class__.__name__,
                            (ma.Schema,),
                            {"data": ma.fields.Nested(schema)},
                        )
                    return None
        """
        pass

    @staticmethod
    def _prepare_response_content(data):
        """Override this to modify the data structure

        This allows to insert the data in a wrapping structure.

            Example: ::

                @staticmethod
                def _prepare_response_content(data):
                    if data is not None:
                        return {"data": data}
                    return None
        """
        pass

    @staticmethod
    def _prepare_response_doc(doc, doc_info, *, api, spec, **kwargs):
        pass
