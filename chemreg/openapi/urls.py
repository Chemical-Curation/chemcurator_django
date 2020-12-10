from django.urls import path

from chemreg.openapi import views

urlpatterns = [
    path("", views.RedocView.as_view()),
    path("openapi.json", views.OpenAPIView.as_view()),
]
