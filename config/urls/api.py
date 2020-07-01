from django.urls import include, path, url

urlpatterns = [
    path("", include("chemreg.openapi.urls")),
    path("", include("chemreg.auth.urls")),
    path("", include("chemreg.compound.urls")),
    url("", include("django_prometheus.urls")),
]
