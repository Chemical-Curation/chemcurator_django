from django.conf import settings
from django.urls import path

from chemreg.auth.views import LoginView

urlpatterns = [
    path(settings.LOGIN_URL, LoginView.as_view()),
]
