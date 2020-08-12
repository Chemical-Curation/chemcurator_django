from random import randint

from django.db import models
from rest_framework.exceptions import ValidationError

import pytest
from crum import impersonate

from chemreg.common.models import CommonInfo
from chemreg.common.utils import casrn_checksum, chemreg_checksum
from chemreg.common.validators import validate_casrn_checksum, validate_casrn_format


def test_casrn_checksum():
    i = randint(2000000, 9999999)
    computed = (
        (1 * int(str(i)[-1]))
        + (2 * int(str(i)[-2]))
        + (3 * int(str(i)[-3]))
        + (4 * int(str(i)[-4]))
        + (5 * int(str(i)[-5]))
        + (6 * int(str(i)[-6]))
        + (7 * int(str(i)[-7]))
    ) % 10
    checksum = casrn_checksum(i)
    assert computed == checksum
    assert 0 <= checksum < 10


def test_chemreg_checksum():
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
    checksum = chemreg_checksum(i)
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


def test_validate_casrn_valid():
    valid_casrn = "1234567-89-5"
    # No exception thrown, Nothing was returned
    assert validate_casrn_format(valid_casrn) is None
    assert validate_casrn_checksum(valid_casrn) is None


def test_validate_casrn_formatting():
    invalid_strings = [
        "abcdefg",  # invalid characters
        "1-89-0",  # seg 1 too short
        "12345678-89-0",  # seg 1 too long
        "1234567-8-0",  # seg 2 too short
        "12345678-890-0",  # seg2 too long
        "1234567-89-",  # no checksum
        "1234567-89-05",  # multiple checksums
    ]

    for invalid_string in invalid_strings:
        with pytest.raises(ValidationError) as exception:
            validate_casrn_format(invalid_string)
        # Assert all codes are throwing errors for formatting, not checksum
        assert ["format"] == exception.value.get_codes()


def test_validate_casrn_checksum():
    invalid_checksum = "1234567-89-1"

    with pytest.raises(ValidationError) as exception:
        validate_casrn_checksum(invalid_checksum)
    # Assert string throws an errors for checksum, not formatting
    assert ["checksum"] == exception.value.get_codes()


def controlled_vocabulary_test_helper(model):
    """ Tests the base attributes that models inheriting from ControlledVocabulary

     This tests the fields that models inheriting from ControlledVocabulary are required to have.
     This test is not meant to run in isolation, but is meant to be called with the inherited model.

     Args:
        model (class): Django Model class inheriting from ControlledVocabulary
    """
    name = model._meta.get_field("name")
    assert isinstance(name, models.SlugField)
    assert name.max_length == 49
    assert name.unique
    assert not name.blank
    label = model._meta.get_field("label")
    assert isinstance(label, models.CharField)
    assert label.max_length == 99
    assert label.unique
    assert not label.blank
    short_description = model._meta.get_field("short_description")
    assert isinstance(short_description, models.CharField)
    assert short_description.max_length == 499
    assert not short_description.blank
    long_description = model._meta.get_field("long_description")
    assert isinstance(long_description, models.TextField)
    assert not long_description.blank
