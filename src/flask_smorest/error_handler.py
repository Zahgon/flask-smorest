"""Exception handler"""

from werkzeug.exceptions import HTTPException

import marshmallow as ma


class ErrorSchema(ma.Schema):
    """Schema describing the error payload

    Not actually used to dump payload, but only for documentation purposes
    """

    code = ma.fields.Integer(metadata={"description": "Error code"})
    status = ma.fields.String(metadata={"description": "Error name"})
    message = ma.fields.String(metadata={"description": "Error message"})
    errors = ma.fields.Dict(metadata={"description": "Errors"})


class ErrorHandlerMixin:
    """Extend Api to manage error handling."""

    # Should match payload structure in handle_http_exception
    ERROR_SCHEMA = ErrorSchema

    def _register_error_handlers(self):
        """Register error handlers in Flask app

        This method registers a default error handler for ``HTTPException``.
        """
        pass

    def handle_http_exception(self, error):
        """Return a JSON response containing a description of the error

        This method is registered at app init to handle ``HTTPException``.

        - When ``abort`` is called in the code, an ``HTTPException`` is
          triggered and Flask calls this handler.

        - When an exception is not caught in a view, Flask makes it an
          ``InternalServerError`` and calls this handler.

        flask-smorest republishes webargs's
        :func:`abort <webargs.flaskparser.abort>`. This ``abort`` allows the
        caller to pass kwargs and stores them in ``exception.data`` so that the
        error handler can use them to populate the response payload.

        Extra information expected by this handler:

        - `message` (``str``): a comment
        - `errors` (``dict``): errors, typically validation errors in
            parameters and request body
        - `headers` (``dict``): additional headers
        """
        pass
