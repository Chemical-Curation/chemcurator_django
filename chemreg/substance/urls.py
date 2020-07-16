from django.urls import include, path

from chemreg.jsonapi.routers import SimpleRouter
from chemreg.substance import views

# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(views.SynonymTypeViewSet)
router.register(views.SourceViewSet)
router.register(views.SubstanceTypeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
