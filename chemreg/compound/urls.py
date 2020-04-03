from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from chemreg.compound import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"defined-compounds", views.DefinedCompoundViewSet)
router.register(r"ill-defined-compounds", views.IllDefinedCompoundViewSet)
router.register(r"query-structure-types", views.QueryStructureTypeViewSet)


urlpatterns = [
    path("", include(router.urls)),
    # ill-defined related fields
    url(
        regex=r"^ill-defined-compounds/(?P<pk>[^/.]+)/(?P<related_field>[^/.]+)/$",
        view=views.IllDefinedCompoundViewSet.as_view({"get": "retrieve_related"}),
        name="ill-defined-compounds-related",
    ),
    url(
        regex=r"^ill-defined-compounds/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)/$",
        view=views.IllDefinedCompoundRelationshipView.as_view(),
        name="ill-defined-compounds-relationships",
    ),
]
