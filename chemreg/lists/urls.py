from django.urls import include, path

from chemreg.jsonapi.routers import SimpleRouter
from chemreg.lists import views

# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(views.AccessibilityTypeViewSet)
router.register(views.IdentifierTypeViewSet)
router.register(views.ListViewSet)
router.register(views.ListTypeViewSet)
router.register(views.RecordViewSet)
router.register(views.RecordIdentifierViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
