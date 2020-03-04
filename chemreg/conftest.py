from django.apps import apps
from django.conf import settings
from django.db import models
from rest_framework.test import APIClient

import pytest

from chemreg.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    return UserFactory()


def is_chemreg_model(model: models.Model) -> bool:
    """Sees if a model is from the `chemreg` application."""
    return model.__module__.startswith("chemreg")


@pytest.fixture(params=filter(is_chemreg_model, apps.get_models()))
def chemreg_model(request) -> models.Model:
    """A model from the chemreg application."""
    return request.param
