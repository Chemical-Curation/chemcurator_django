from rest_framework_json_api import pagination


class JsonApiPageNumberPagination(pagination.JsonApiPageNumberPagination):
    """Sets the maximum page count to 1000."""

    max_page_size = 1000
