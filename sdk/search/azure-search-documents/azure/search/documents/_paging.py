# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from typing import List, Optional, Dict, cast, Any, MutableMapping

import base64
import itertools
import json

from azure.core.paging import ItemPaged, PageIterator, ReturnType
from ._generated.models import SearchRequest, SearchDocumentsResult, QueryAnswerResult, DebugInfo
from ._api_versions import DEFAULT_VERSION


def convert_search_result(result):
    ret = result.additional_properties
    ret["@search.score"] = result.score
    ret["@search.reranker_score"] = result.reranker_score
    ret["@search.highlights"] = result.highlights
    ret["@search.captions"] = result.captions
    ret["@search.document_debug_info"] = result.document_debug_info
    ret["@search.reranker_boosted_score"] = result.reranker_boosted_score
    return ret


def pack_continuation_token(response, api_version=DEFAULT_VERSION):
    if response.next_page_parameters is not None:
        token = {
            "apiVersion": api_version,
            "nextLink": response.next_link,
            "nextPageParameters": response.next_page_parameters.serialize(),
        }
        return base64.b64encode(json.dumps(token).encode("utf-8"))
    return None


def unpack_continuation_token(token):
    unpacked_token = json.loads(base64.b64decode(token))
    next_link = unpacked_token["nextLink"]
    next_page_parameters = unpacked_token["nextPageParameters"]
    next_page_request = SearchRequest.deserialize(next_page_parameters)
    return next_link, next_page_request


class SearchItemPaged(ItemPaged[ReturnType]):
    """A pageable list of search results."""

    def __init__(self, *args, **kwargs) -> None:
        super(SearchItemPaged, self).__init__(*args, **kwargs)
        self._first_page_iterator_instance: Optional[SearchPageIterator] = None

    def __next__(self) -> ReturnType:
        if self._page_iterator is None:
            first_iterator = self._first_iterator_instance()
            self._page_iterator = itertools.chain.from_iterable(first_iterator)
        return next(self._page_iterator)

    def _first_iterator_instance(self) -> "SearchPageIterator":
        if self._first_page_iterator_instance is None:
            self._first_page_iterator_instance = cast(SearchPageIterator, self.by_page())
        return self._first_page_iterator_instance

    def get_facets(self) -> Optional[Dict]:
        """Return any facet results if faceting was requested.

        :return: facet results
        :rtype: dict or None
        """
        return cast(Dict, self._first_iterator_instance().get_facets())

    def get_coverage(self) -> float:
        """Return the coverage percentage, if `minimum_coverage` was
        specificied for the query.

        :return: coverage percentage
        :rtype: float
        """
        return cast(float, self._first_iterator_instance().get_coverage())

    def get_count(self) -> int:
        """Return the count of results if `include_total_count` was
        set for the query.

        :return: count of results
        :rtype: int
        """
        return cast(int, self._first_iterator_instance().get_count())

    def get_answers(self) -> Optional[List[QueryAnswerResult]]:
        """Return semantic answers. Only included if the semantic ranker is used
        and answers are requested in the search query via the query_answer parameter.

        :return: answers
        :rtype: list[~azure.search.documents.models.QueryAnswerResult] or None
        """
        return cast(List[QueryAnswerResult], self._first_iterator_instance().get_answers())

    def get_debug_info(self) -> DebugInfo:
        """Return the debug information for the query.

        :return: the debug information for the query
        :rtype: ~azure.search.documents.models.DebugInfo
        """
        return cast(DebugInfo, self._first_iterator_instance().get_debug_info())


# The pylint error silenced below seems spurious, as the inner wrapper does, in
# fact, become a method of the class when it is applied.
def _ensure_response(f):
    # pylint:disable=protected-access
    def wrapper(self, *args, **kw):
        if self._current_page is None:
            self._response = self._get_next(self.continuation_token)
            self.continuation_token, self._current_page = self._extract_data(self._response)
        return f(self, *args, **kw)

    return wrapper


class SearchPageIterator(PageIterator):
    """An iterator over search results."""

    def __init__(self, client, initial_query, kwargs, continuation_token=None) -> None:
        super(SearchPageIterator, self).__init__(
            get_next=self._get_next_cb,
            extract_data=self._extract_data_cb,
            continuation_token=continuation_token,
        )
        self._client = client
        self._initial_query = initial_query
        self._kwargs = kwargs
        self._facets: Optional[MutableMapping[str, List[MutableMapping[str, Any]]]] = None
        self._api_version = kwargs.pop("api_version", DEFAULT_VERSION)

    def _get_next_cb(self, continuation_token):
        if continuation_token is None:
            return self._client.documents.search_post(search_request=self._initial_query.request, **self._kwargs)

        _next_link, next_page_request = unpack_continuation_token(continuation_token)

        return self._client.documents.search_post(search_request=next_page_request, **self._kwargs)

    def _extract_data_cb(self, response):
        continuation_token = pack_continuation_token(response, api_version=self._api_version)
        results = [convert_search_result(r) for r in response.results]
        return continuation_token, results

    @_ensure_response
    def get_facets(self) -> Optional[MutableMapping[str, Any]]:
        self.continuation_token = None
        response = cast(SearchDocumentsResult, self._response)
        facets = response.facets
        if facets is not None and self._facets is None:
            assert facets.items() is not None  # Hint for mypy
            self._facets = {k: [x.as_dict() for x in v] for k, v in facets.items()}
        return self._facets

    @_ensure_response
    def get_coverage(self) -> float:
        self.continuation_token = None
        response = cast(SearchDocumentsResult, self._response)
        return cast(float, response.coverage)

    @_ensure_response
    def get_count(self) -> int:
        self.continuation_token = None
        response = cast(SearchDocumentsResult, self._response)
        return cast(int, response.count)

    @_ensure_response
    def get_answers(self) -> Optional[List[QueryAnswerResult]]:
        self.continuation_token = None
        response = cast(SearchDocumentsResult, self._response)
        return response.answers

    @_ensure_response
    def get_debug_info(self) -> DebugInfo:
        self.continuation_token = None
        response = cast(SearchDocumentsResult, self._response)
        return cast(DebugInfo, response.debug_info)
