from django.conf.urls import url
from rest_framework import routers

import inflection
from rest_framework_json_api import utils, views

from chemreg.jsonapi.views import RelationshipView


class SimpleRouter(routers.SimpleRouter):
    """Automatically adds prefix and related views."""

    def __init__(self):
        super().__init__(trailing_slash=False)

    def register(self, viewset):
        if hasattr(viewset, "resource_name"):
            prefix = viewset.resource_name
        else:
            prefix = utils.get_resource_type_from_serializer(viewset.serializer_class)
        return super().register(inflection.pluralize(prefix), viewset)

    def get_urls(self):
        urls = super().get_urls()
        for prefix, viewset, basename in self.registry:
            if issubclass(viewset, views.ModelViewSet):
                relationship_viewset = type(
                    f"{basename}RelationshipViewset",
                    (RelationshipView,),
                    {"queryset": viewset.queryset},
                )
                urls += [
                    url(
                        regex=fr"^{prefix}/(?P<pk>[^/.]+)/(?P<related_field>[^/.]+)$",
                        view=viewset.as_view({"get": "retrieve_related"}),
                        name=f"{basename}-related",
                    ),
                    url(
                        regex=fr"^{prefix}/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$",
                        view=relationship_viewset.as_view(),
                        name=f"{basename}-relationships",
                    ),
                ]
        return urls
