from random import randint

from django.db import models

import pytest
from crum import impersonate

from chemreg.common.models import CommonInfo
from chemreg.common.utils import compute_checksum


def test_compute_checksum():
    i = randint(2000000, 9999999)
    computed = (
        (1 * int(str(i)[0]))
        + (2 * int(str(i)[1]))
        + (3 * int(str(i)[2]))
        + (4 * int(str(i)[3]))
        + (5 * int(str(i)[4]))
        + (6 * int(str(i)[5]))
        + (7 * int(str(i)[6]))
    ) % 10
    checksum = compute_checksum(i)
    assert computed == checksum
    assert 0 <= checksum < 10


def test_commoninfo_attr():
    """Test basic attributes of the CommonInfo abstract model."""
    assert CommonInfo._meta.abstract
    assert hasattr(CommonInfo, "created_at")
    assert hasattr(CommonInfo, "updated_at")
    created_at = CommonInfo._meta.get_field("created_at")
    updated_at = CommonInfo._meta.get_field("updated_at")
    assert isinstance(created_at, models.DateTimeField)
    assert isinstance(updated_at, models.DateTimeField)
    assert created_at.auto_now_add
    assert not created_at.auto_now
    assert updated_at.auto_now
    assert not updated_at.auto_now_add


def test_inherits_commoninfo(chemreg_model):
    """Test that all ChemReg models inherit CommonInfo."""
    assert issubclass(chemreg_model, CommonInfo)


@pytest.mark.django_db
def test_user_link(user_factory):
    """Test that created_by/updated_by are saved."""
    user_1 = user_factory()
    assert user_1.created_by_id is None
    assert user_1.updated_by_id is None
    with impersonate(user_1):
        user_2 = user_factory()
        assert user_2.created_by_id == user_1.pk
        assert user_2.updated_by_id == user_1.pk
    with impersonate(user_2):
        user_2.save()
        assert user_2.created_by_id == user_1.pk
        assert user_2.updated_by_id == user_2.pk


def test_prometheus_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
