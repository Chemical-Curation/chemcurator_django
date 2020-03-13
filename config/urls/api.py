from django.urls import include, path
from rest_framework.routers import DefaultRouter

from chemreg.compound import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"defined-compounds", views.DefinedCompoundViewSet)


urlpatterns = [
    path("", include("chemreg.auth.urls")),
    path("", include(router.urls)),
]
