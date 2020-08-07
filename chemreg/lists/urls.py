from django.urls import include, path

from chemreg.jsonapi.routers import SimpleRouter
from chemreg.lists import views

# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(views.AccessibilityTypeViewSet)
router.register(views.ListTypeViewSet)
router.register(views.IdentifierTypeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
