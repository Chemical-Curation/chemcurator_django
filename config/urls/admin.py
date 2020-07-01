from django.contrib import admin
from django.urls import include, path, url

urlpatterns = [
    path("", admin.site.urls),
    url("", include("django_prometheus.urls")),
]
