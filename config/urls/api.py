from django.urls import include, path

urlpatterns = [
    path("", include("chemreg.auth.urls")),
    path("", include("chemreg.compound.urls")),
]
