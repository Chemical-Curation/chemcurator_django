from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Permission
from django.db import models
from django.test import RequestFactory
from rest_framework.test import APIClient, APIRequestFactory

import pytest

from chemreg.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture  # isn't this already in fixtures as "rf" | $ pytest --fixtures
def request_factory() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
def api_request_factory() -> APIRequestFactory:
    return APIRequestFactory(enforce_csrf_checks=True)


def get_chemreg_models():
    for model in apps.get_models():
        if model.__module__.startswith("chemreg"):
            yield model


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    return UserFactory()


@pytest.fixture
def admin_user() -> settings.AUTH_USER_MODEL:
    admin = UserFactory(is_staff=True)
    for p in Permission.objects.all():
        admin.user_permissions.add(p.pk)
    return admin


@pytest.fixture
def user_factory() -> UserFactory:
    return UserFactory


def is_chemreg_model(model: models.Model) -> bool:
    """Sees if a model is from the `chemreg` application."""
    return model.__module__.startswith("chemreg")


@pytest.fixture(params=filter(is_chemreg_model, apps.get_models()))
def chemreg_model(request) -> models.Model:
    """A model from the chemreg application."""
    return request.param
