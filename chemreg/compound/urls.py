from django.urls import include, path

from chemreg.compound import views
from chemreg.jsonapi.routers import SimpleRouter

# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(views.DefinedCompoundViewSet)
router.register(views.IllDefinedCompoundViewSet)
router.register(views.QueryStructureTypeViewSet)
router.register(views.CompoundViewSet, prefix="compounds")


urlpatterns = [
    path("", include(router.urls)),
]
