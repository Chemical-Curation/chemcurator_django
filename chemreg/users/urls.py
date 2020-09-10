from django.urls import include, path

from chemreg.jsonapi.routers import SimpleRouter
from chemreg.users import views

# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
