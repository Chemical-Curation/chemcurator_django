from django.http import HttpResponse
from django.urls import path


def apidoc_placeholder(request):
    return HttpResponse("placeholder for api documentation")


urlpatterns = [
    path("", apidoc_placeholder),
]
