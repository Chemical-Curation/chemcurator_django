from django.db import models

import pytest
from crum import impersonate

from chemreg.common.models import CommonInfo, Source


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


def test_source_model():
    """Tests the validity of the Source Model's attributes"""
    name = Source._meta.get_field("name")
    assert isinstance(name, models.SlugField)
    assert name.max_length == 49
    assert name.unique
    label = Source._meta.get_field("label")
    assert isinstance(label, models.CharField)
    assert label.max_length == 99
    assert label.unique
    short_description = Source._meta.get_field("short_description")
    assert isinstance(short_description, models.CharField)
    assert short_description.max_length == 499
    long_description = Source._meta.get_field("long_description")
    assert isinstance(long_description, models.TextField)
