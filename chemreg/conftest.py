from django.apps import apps
from django.conf import settings
from django.db import models
from django.test import RequestFactory

import pytest

from chemreg.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    return UserFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


def get_chemreg_models():
    for model in apps.get_models():
        if model.__module__.startswith("chemreg"):
            yield model


@pytest.fixture(params=get_chemreg_models())
def chemreg_model(request) -> models.Model:
    model = request.param
    yield model
