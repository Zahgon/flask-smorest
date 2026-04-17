"""Pagination feature

Two pagination modes are supported:

- Pagination inside the resource: the resource function is responsible for
  selecting requested range of items and setting total number of items.

- Post-pagination: the resource returns an iterator (typically a DB cursor) and
  a pager is provided to paginate the data and get the total number of items.
"""
import http
import json
import warnings
from copy import deepcopy
from functools import wraps
from flask import current_app, request
import marshmallow as ma
from webargs.flaskparser import FlaskParser
from .utils import unpack_tuple_response

class PaginationParameters:
    """Holds pagination arguments

    :param int page: Page number
    :param int page_size: Page size
    """

    def __init__(self, page, page_size):
        self.page = page
        self.page_size = page_size
        self.item_count = None

    @property
    def first_item(self):
        """Return first item number"""
        pass

    @property
    def last_item(self):
        """Return last item number"""
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}(page={self.page!r},page_size={self.page_size!r})'

def _pagination_parameters_schema_factory(def_page, def_page_size, def_max_page_size):
    """Generate a PaginationParametersSchema"""
    pass

class Page:
    """Pager for simple types such as lists.

    Can be subclassed to provide a pager for a specific data object.
    """

    def __init__(self, collection, page_params):
        """Create a Page instance

        :param sequence collection: Collection of items to page through
        :page PaginationParameters page_params: Pagination parameters
        """
        self.collection = collection
        self.page_params = page_params
        self.page_params.item_count = self.item_count

    @property
    def items(self):
        return list(self.collection[self.page_params.first_item:self.page_params.last_item + 1])

    @property
    def item_count(self):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}(collection={self.collection!r},page_params={self.page_params!r})'

class PaginationMetadataSchema(ma.Schema):
    """Pagination metadata schema

    Used to serialize pagination metadata.
    Its main purpose is to document the pagination metadata.
    """
    total = ma.fields.Int(metadata={'description': 'Total number of items.'})
    total_pages = ma.fields.Int(metadata={'description': 'Total number of pages.'})
    first_page = ma.fields.Int(metadata={'description': 'First available page number.'})
    last_page = ma.fields.Int(metadata={'description': 'Last available page number.'})
    page = ma.fields.Int(metadata={'description': 'Current page number.'})
    previous_page = ma.fields.Int(metadata={'description': 'Previous page number.'})
    next_page = ma.fields.Int(metadata={'description': 'Next page number.'})
PAGINATION_HEADER = {'description': 'Pagination metadata', 'schema': PaginationMetadataSchema}

class PaginationMixin:
    """Extend Blueprint to add Pagination feature"""
    PAGINATION_ARGUMENTS_PARSER = FlaskParser()
    PAGINATION_HEADER_NAME = 'X-Pagination'
    DEFAULT_PAGINATION_PARAMETERS = {'page': 1, 'page_size': 10, 'max_page_size': 100}

    def paginate(self, pager=None, *, page=None, page_size=None, max_page_size=None):
        """Decorator adding pagination to the endpoint

        :param type[Page] pager: Page class used to paginate response data
        :param int page: Default requested page number (default: 1)
        :param int page_size: Default requested page size (default: 10)
        :param int max_page_size: Maximum page size (default: 100)

        If a :class:`Page <Page>` class is provided, it is used to paginate the
        data returned by the view function, typically a lazy database cursor.

        Otherwise, pagination is handled in the view function.

        The decorated function may return a tuple including status and/or
        headers, like a typical flask view function. It may not return a
        ``Response`` object.

        See :doc:`Pagination <pagination>`.
        """
        pass

    @staticmethod
    def _make_pagination_metadata(page, page_size, item_count):
        """Build pagination metadata from page, page size and item count

        Override this to use another pagination metadata structure
        """
        pass

    def _set_pagination_metadata(self, page_params, result, headers):
        """Add pagination metadata to headers

        Override this to set pagination data another way
        """
        pass

    def _document_pagination_metadata(self, spec, resp_doc):
        """Document pagination metadata header

        Override this to document custom pagination metadata
        """
        pass

    def _prepare_pagination_doc(self, doc, doc_info, *, spec, **kwargs):
        pass
