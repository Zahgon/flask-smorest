"""API specification using OpenAPI"""

import http

import click
import flask

import apispec
from apispec.ext.marshmallow import MarshmallowPlugin
from webargs.fields import DelimitedList

try:  # pragma: no cover
    import yaml

    HAS_PYYAML = True
except ImportError:  # pragma: no cover
    HAS_PYYAML = False

from flask_smorest import etag as fs_etag
from flask_smorest import pagination as fs_pagination
from flask_smorest.exceptions import MissingAPIParameterError
from flask_smorest.utils import normalize_config_prefix, prepare_response

from .field_converters import uploadfield2properties
from .plugins import FlaskPlugin


def _add_leading_slash(string):
    """Add leading slash to a string if there is None"""
    pass


def delimited_list2param(self, field, **kwargs):
    """apispec parameter attribute function documenting DelimitedList field"""
    pass


class DocBlueprintMixin:
    """Extend Api to serve the spec in a dedicated blueprint."""

    def _make_doc_blueprint_name(self):
        pass

    def _register_doc_blueprint(self):
        """Register a blueprint in the application to expose the spec

        Doc Blueprint contains routes to
        - json spec file
        - spec UI (ReDoc, Swagger UI).
        """
        pass

    def _register_redoc_rule(self, blueprint):
        """Register ReDoc rule

        The ReDoc script URL should be specified as OPENAPI_REDOC_URL.
        """
        pass

    def _register_swagger_ui_rule(self, blueprint):
        """Register Swagger UI rule

        The Swagger UI scripts base URL should be specified as
        OPENAPI_SWAGGER_UI_URL.
        """
        pass

    def _register_rapidoc_rule(self, blueprint):
        """Register RapiDoc rule

        The RapiDoc script URL should be specified as OPENAPI_RAPIDOC_URL.
        """
        pass

    def _openapi_json(self):
        """Serve JSON spec file"""
        pass

    def _openapi_redoc(self):
        """Expose OpenAPI spec with ReDoc"""
        pass

    def _openapi_swagger_ui(self):
        """Expose OpenAPI spec with Swagger UI"""
        pass

    def _openapi_rapidoc(self):
        """Expose OpenAPI spec with RapiDoc"""
        pass


class APISpecMixin(DocBlueprintMixin):
    """Add APISpec related features to Api class"""

    DEFAULT_ERROR_RESPONSE_NAME = "DEFAULT_ERROR"

    DEFAULT_REQUEST_BODY_CONTENT_TYPE = "application/json"
    DEFAULT_RESPONSE_CONTENT_TYPE = "application/json"

    def _init_spec(
        self,
        *,
        flask_plugin=None,
        marshmallow_plugin=None,
        extra_plugins=None,
        title=None,
        version=None,
        openapi_version=None,
        **options,
    ):
        # Plugins
        pass

    def register_converter(self, converter, func):
        """Register custom path parameter converter

        :param BaseConverter converter: Converter
            Subclass of werkzeug's BaseConverter
        :param callable func: Function returning a parameter schema from
            a converter intance

        Example: ::

            # Register MongoDB's ObjectId converter in Flask application
            app.url_map.converters['objectid'] = ObjectIdConverter

            # Define custom converter to schema function
            def objectidconverter2paramschema(converter):
                return {'type': 'string', 'format': 'ObjectID'}

            # Register converter in Api
            api.register_converter(
                ObjectIdConverter,
                objectidconverter2paramschema
            )

            @blp.route('/pets/{objectid:pet_id}')
                ...

            api.register_blueprint(blp)

        Once the converter is registered, all paths using it will have
        corresponding path parameter documented with the right schema.

        Should be called before registering paths with
        :meth:`Blueprint.route <Blueprint.route>`.
        """
        pass

    def _register_converter(self, converter, func):
        pass

    def register_field(self, field, *args):
        """Register custom Marshmallow field

        Registering the Field class allows the Schema parser to set the proper
        type and format when documenting parameters from Schema fields.

        :param Field field: Marshmallow Field class

        ``*args`` can be:

        - a pair of the form ``(type, format)`` to map to
        - a core marshmallow field type (then that type's mapping is used)

        Examples: ::

            # Map to ('string', 'ObjectId') passing type and format
            api.register_field(ObjectId, "string", "ObjectId")

            # Map to ('string', ) passing type
            api.register_field(CustomString, "string", None)

            # Map to ('string, 'date-time') passing a marshmallow Field
            api.register_field(CustomDateTime, ma.fields.DateTime)

        Should be called before registering schemas with
        :meth:`schema <Api.schema>`.
        """
        pass

    def _register_field(self, field, *args):
        pass

    def _register_responses(self):
        """Lazyly register default responses for all status codes"""
        pass

    def _register_etag_headers(self):
        pass

    def _register_pagination_header(self):
        pass


openapi_cli = flask.cli.AppGroup("openapi", help="OpenAPI commands.")


def _get_spec_dict(config_prefix):
    pass


@openapi_cli.command("print")
@click.option("-f", "--format", type=click.Choice(["json", "yaml"]), default="json")
@click.option("--config-prefix", type=click.STRING, metavar="", default="")
def print_openapi_doc(format, config_prefix):
    """Print OpenAPI JSON document."""
    pass


@openapi_cli.command("write")
@click.option("-f", "--format", type=click.Choice(["json", "yaml"]), default="json")
@click.option("--config-prefix", type=click.STRING, metavar="", default="")
@click.argument("output_file", type=click.File(mode="w"))
def write_openapi_doc(format, output_file, config_prefix):
    """Write OpenAPI JSON document to a file."""
    pass


@openapi_cli.command("list-config-prefixes")
def list_config_prefixes():
    """List available API config prefixes."""
    pass
