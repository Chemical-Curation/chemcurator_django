from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from chemreg.compound import views

# Create a router and register our viewsets with it.
router = SimpleRouter(trailing_slash=False)
router.register(r"definedCompounds", views.DefinedCompoundViewSet)
router.register(r"illDefinedCompounds", views.IllDefinedCompoundViewSet)
router.register(r"queryStructureTypes", views.QueryStructureTypeViewSet)


urlpatterns = [
    path("", include(router.urls)),
    # illDefinedCompound related fields
    url(
        regex=r"^illDefinedCompounds/(?P<pk>[^/.]+)/(?P<related_field>[^/.]+)$",
        view=views.IllDefinedCompoundViewSet.as_view({"get": "retrieve_related"}),
        name="ill-defined-compounds-related",
    ),
    url(
        regex=r"^illDefinedCompounds/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$",
        view=views.IllDefinedCompoundRelationshipView.as_view(),
        name="ill-defined-compounds-relationships",
    ),
]
