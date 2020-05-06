import re

from rest_framework_json_api import filters


class QueryParameterValidationFilter(filters.QueryParameterValidationFilter):
    """Allows setting additional query parameters in the view."""

    view = None

    @property
    def query_regex(self):
        query_params = ["sort", "include"]
        if self.view:
            query_params += getattr(self.view, "query_params", [])
        return re.compile(
            fr"^({'|'.join(query_params)})$|^(filter|fields|page)(\[[\w\.\-]+\])?$"
        )

    def filter_queryset(self, request, queryset, view):
        self.view = view
        return super().filter_queryset(request, queryset, view)
