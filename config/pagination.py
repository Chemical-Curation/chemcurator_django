from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param


class DefaultPagination(pagination.PageNumberPagination):
    ordering = "created_at"
    page_size_query_param = "size"
    page_size = 100
    max_page_size = 1000

    def get_self_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page.number
        return replace_query_param(url, self.page_query_param, page_number)

    def get_first_link(self):
        url = self.request.build_absolute_uri()
        page_number = 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_last_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        return Response(
            {
                "meta": {
                    "totalPages": self.page.paginator.num_pages,
                    "page_size": self.page.paginator.per_page,
                    "apiVersion": "1.0.0-beta",
                },
                "data": data,
                "links": {
                    "self": self.get_self_link(),
                    "first": self.get_first_link(),
                    "previous": self.get_previous_link(),
                    "next": self.get_next_link(),
                    "last": self.get_last_link(),
                },
            }
        )
