import os

from django.http import HttpResponse
from django.views.generic.base import TemplateView, View

from config.settings import STATIC_URL

from chemreg.compound.settings import compound_settings
from chemreg.substance.settings import substance_settings

try:
    import _jsonnet as jsonnet
except ImportError:
    print("[WARNING] Documentation disabled. Only unix systems can build jsonnet.\n")


class RedocView(TemplateView):
    """The Redoc documentation."""

    template_name = "redoc.html"

    def get_context_data(self, **kwargs):
        try:
            jsonnet
            return {"jsonnet": True}
        except NameError:
            return {"jsonnet": False}


class OpenAPIView(View):
    """The OpenAPI spec file."""

    http_method_names = ["get"]

    try:
        base_spec = jsonnet.evaluate_file(
            os.path.join(os.path.dirname(__file__), "schemas", "schema.jsonnet"),
            ext_vars={
                "STATIC_URL": STATIC_URL,
                "baseServer": "__BASE_SERVER__",
                "COMPOUND_PREFIX": compound_settings.PREFIX,
                "SUBSTANCE_PREFIX": substance_settings.PREFIX,
            },
            jpathdir=os.path.join(os.path.dirname(__file__), "schemas"),
        )
    except NameError:
        base_spec = ""

    def get(self, request, *args, **kwargs):
        request_host = request.get_host()
        if request_host[-4:] == ".gov":
            request_scheme = "https"
        else:
            request_scheme = request.scheme
        base_server = f"{request_scheme}://{request_host}"
        spec = self.base_spec.replace("__BASE_SERVER__", base_server)
        return HttpResponse(spec, content_type="application/json")
