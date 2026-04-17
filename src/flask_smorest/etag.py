"""ETag feature"""

import hashlib
import http
import warnings
from copy import deepcopy
from functools import wraps

from flask import current_app, json, request

from .exceptions import NotModified, PreconditionFailed, PreconditionRequired
from .globals import current_api
from .utils import deepupdate, get_appcontext, resolve_schema_instance

IF_NONE_MATCH_HEADER = {
    "name": "If-None-Match",
    "in": "header",
    "description": "Tag to check against",
    "schema": {"type": "string"},
}

IF_MATCH_HEADER = {
    "name": "If-Match",
    "in": "header",
    "required": True,
    "description": "Tag to check against",
    "schema": {"type": "string"},
}

ETAG_HEADER = {
    "description": "Tag for the returned entry",
    "schema": {"type": "string"},
}


def _get_etag_ctx():
    """Get ETag section of AppContext"""
    return get_appcontext().setdefault("etag", {})


class EtagMixin:
    """Extend Blueprint to add ETag handling"""

    METHODS_CHECKING_NOT_MODIFIED = ["GET", "HEAD"]
    METHODS_NEEDING_CHECK_ETAG = ["PUT", "PATCH", "DELETE"]
    METHODS_ALLOWING_SET_ETAG = ["GET", "HEAD", "POST", "PUT", "PATCH"]

    # Headers to include in ETag computation
    ETAG_INCLUDE_HEADERS = ["X-Pagination"]

    def etag(self, obj):
        """Decorator adding ETag management to the endpoint

        The ``etag`` decorator expects the decorated view function to return a
        ``Response`` object. It is the case if it is decorated with the
        ``response`` decorator.

        The ``etag`` decorator may be used to decorate a
        :class:`MethodView <flask.views.MethodView>`. In this case, it applies
        to all HTTP methods in the ``MethodView``.

        See :doc:`ETag <etag>`.
        """
        pass

    @staticmethod
    def _generate_etag(etag_data, extra_data=None):
        """Generate an ETag from data

        etag_data: Data to use to compute ETag
        extra_data: Extra data to add before hashing

        Typically, extra_data is used to add pagination metadata to the hash.
        It is not dumped through the Schema.

        Data is JSON serialized before hashing using the Flask app JSON serializer.
        """
        if extra_data:
            etag_data = (etag_data, extra_data)
        data = json.dumps(etag_data, sort_keys=True)
        return hashlib.sha1(bytes(data, "utf-8")).hexdigest()

    def _check_precondition(self):
        """Check If-Match header is there

        Raise 428 if If-Match header missing

        Called automatically for PUT, PATCH and DELETE methods
        """
        pass

    def check_etag(self, etag_data, etag_schema=None):
        """Compare If-Match header with computed ETag

        Raise 412 if If-Match header does not match.

        Must be called from resource code to check ETag.

        Unfortunately, there is no way to call it automatically. It is the
        developer's responsability to do it. However, a warning is issued at
        runtime if this function was not called.

        Issues a warning if called in a method other than PUT, PATCH, or
        DELETE.
        """
        pass

    def _is_etag_enabled(self):
        """Return True if ETag feature is enabled api-wise"""
        return not current_api.config.get("ETAG_DISABLED", False)

    def _verify_check_etag(self):
        """Verify check_etag was called in resource code

        Issues a warning if ETag is enabled but check_etag was not called in
        resource code in a PUT, PATCH or DELETE method.

        This is called automatically. It is meant to warn the developer about
        an issue in his ETag management.
        """
        pass

    def _check_not_modified(self, etag):
        """Raise NotModified if etag is in If-None-Match header

        Only applies to methods returning a 304 (Not Modified) code
        """
        if (
            request.method in self.METHODS_CHECKING_NOT_MODIFIED
            and etag in request.if_none_match
        ):
            raise NotModified

    def set_etag(self, etag_data, etag_schema=None):
        """Set ETag for this response

        Raise 304 if ETag identical to If-None-Match header

        Must be called from resource code, unless the view function is
        decorated with the ``response`` decorator, in which case the ETag is
        computed by default from response data if ``set_etag`` is not called.

        Issues a warning if called in a method other than GET, HEAD, POST, PUT
        or PATCH.
        """
        if request.method not in self.METHODS_ALLOWING_SET_ETAG:
            warnings.warn(
                f"ETag cannot be set on {request.method} request.",
                stacklevel=2,
            )
        if self._is_etag_enabled():
            if etag_schema is not None:
                etag_data = resolve_schema_instance(etag_schema).dump(etag_data)
            new_etag = self._generate_etag(etag_data)
            self._check_not_modified(new_etag)
            # Store ETag in AppContext to add it to response headers later on
            _get_etag_ctx()["etag"] = new_etag

    def _set_etag_in_response(self, response):
        """Set ETag in response object

        Called automatically.

        If no ETag data was computed using set_etag, it is computed here from
        response data.
        """
        pass

    def _prepare_etag_doc(self, doc, doc_info, *, api, spec, method, **kwargs):
        pass
