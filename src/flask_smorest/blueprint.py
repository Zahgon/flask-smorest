"""API Blueprint

This is a subclass of Flask's Blueprint

It provides added features:

- Decorators to specify Marshmallow schema for view functions I/O

- API documentation registration

Documentation process works in several steps:

- At import time

  - When a MethodView or a view function is decorated, relevant information
    is automatically added to the object's ``_apidoc`` attribute.

  - The ``Blueprint.doc`` decorator stores additional information in there that
    flask-smorest can not - or does not yet - infer from the code.

  - The ``Blueprint.route`` decorator registers the endpoint in the Blueprint
    and gathers all documentation information about the endpoint in
    ``Blueprint._docs[endpoint]``.

- At initialization time

  - Schema instances are replaced by their reference in the `schemas` section
    of the spec components.

  - The ``Blueprint.register_blueprint`` method merges nested blueprint
    documentation into the parent blueprint documentation.

  - Documentation is finalized using the information stored in
    ``Blueprint._docs``, with adaptations to parameters only known at init
    time, such as OAS version.

  - Manual documentation is deep-merged with automatic documentation.

  - Endpoints documentation is registered in the APISpec object.
"""
from copy import deepcopy
from functools import wraps
from flask import Blueprint as FlaskBlueprint
from flask import current_app
from flask.views import MethodView
from .arguments import ArgumentsMixin
from .etag import EtagMixin
from .pagination import PaginationMixin
from .response import ResponseMixin
from .utils import deepupdate, load_info_from_docstring

class Blueprint(FlaskBlueprint, ArgumentsMixin, ResponseMixin, PaginationMixin, EtagMixin):
    """Blueprint that registers info in API documentation"""
    HTTP_METHODS = ['OPTIONS', 'HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    DEFAULT_LOCATION_CONTENT_TYPE_MAPPING = {'json': 'application/json', 'form': 'application/x-www-form-urlencoded', 'files': 'multipart/form-data'}
    DOCSTRING_INFO_DELIMITER = '---'

    def __init__(self, *args, **kwargs):
        self.description = kwargs.pop('description', '')
        super().__init__(*args, **kwargs)
        self._docs = {}
        self._endpoints = []
        self._prepare_doc_cbks = [self._prepare_arguments_doc, self._prepare_response_doc, self._prepare_pagination_doc, self._prepare_etag_doc]

    def add_url_rule(self, rule, endpoint=None, view_func=None, provide_automatic_options=None, *, parameters=None, tags=None, **options):
        """Register url rule in application

        Also stores doc info for later registration

        Use this to register a :class:`MethodView <flask.views.MethodView>` or
        a resource function.

        :param str rule: URL rule as string.
        :param str endpoint: Endpoint for the registered URL rule (defaults
            to function name).
        :param callable|MethodView view_func: View function or MethodView class
        :param list parameters: List of parameter descriptions relevant to all
            operations in this path. Only used to document the resource.
        :param list tags: List of tags for the resource.
            If None, ``Blueprint`` name is used.
        :param options: Options to be forwarded to the underlying
            :class:`werkzeug.routing.Rule <Rule>` object.
        """
        pass

    def route(self, rule, *, parameters=None, tags=None, **options):
        """Decorator to register view function in application and documentation

        Calls :meth:`add_url_rule <Blueprint.add_url_rule>`.
        """
        pass

    def register_blueprint(self, blueprint, **options):
        """Register a nested blueprint in application

        Also stores doc info from the nested bluepint for later registration.

        Use this to register a nested :class:`Blueprint <Blueprint>`.

        :param Blueprint blueprint: Blueprint to register under this blueprint.
        :param options: Options to be forwarded to the underlying
            :meth:`flask.Blueprint.register_blueprint` method.

        See :ref:`register-nested-blueprints`.
        """
        pass

    def _store_endpoint_docs(self, endpoint, obj, parameters, tags, **options):
        """Store view or function doc info"""
        pass

    def register_views_in_doc(self, api, app, spec, *, name, parameters):
        """Register views information in documentation

        If a schema in a parameter or a response appears in the spec
        `schemas` section, it is replaced by a reference in the parameter or
        response documentation:

        "schema":{"$ref": "#/components/schemas/MySchema"}
        """
        pass

    @staticmethod
    def doc(**kwargs):
        """Decorator adding description attributes to a view function

        Values passed as kwargs are copied verbatim in the docs

            Example: ::

                @blp.doc(description="Return pets based on ID",
                         summary="Find pets by ID"
                )
                def get(...):
                    ...
        """
        pass

    def _decorate_view_func_or_method_view(self, decorator, obj):
        """Apply decorator to view func or MethodView HTTP methods"""
        pass
