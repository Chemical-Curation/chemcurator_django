import os

from django.http import HttpResponse
from django.views.generic.base import TemplateView, View

import _jsonnet as jsonnet

from chemreg.compound.settings import compound_settings


class RedocView(TemplateView):
    """The Redoc documentation."""

    template_name = "redoc.html"


class OpenAPIView(View):
    """The OpenAPI spec file."""

    http_method_names = ["get"]

    base_spec = jsonnet.evaluate_file(
        os.path.join(os.path.dirname(__file__), "schemas", "schema.jsonnet"),
        ext_vars={
            "baseServer": "__BASE_SERVER__",
            "COMPOUND_PREFIX": compound_settings.PREFIX,
        },
    )

    def get(self, request, *args, **kwargs):
        base_server = f"{request.scheme}://{request.get_host()}"
        spec = self.base_spec.replace("__BASE_SERVER__", base_server)
        return HttpResponse(spec, content_type="application/json")
