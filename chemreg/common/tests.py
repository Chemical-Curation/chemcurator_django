from random import randint

from django.db import models
from rest_framework.exceptions import ValidationError

import pytest
from crum import impersonate

from chemreg.common.models import CommonInfo, HTMLTextField
from chemreg.common.utils import casrn_checksum, chemreg_checksum
from chemreg.common.validators import validate_casrn_checksum, validate_is_regex


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
    assert validate_casrn_checksum(valid_casrn) is None


def test_validate_casrn_checksum():
    invalid_checksum = "1234567-89-1"

    with pytest.raises(ValidationError) as exception:
        validate_casrn_checksum(invalid_checksum)
    # Assert string throws an errors for checksum, not formatting
    assert ["checksum"] == exception.value.get_codes()


def test_validate_is_regex():
    valid_regex = ".*"
    invalid_regex = "\\"

    assert validate_is_regex(valid_regex) is None

    with pytest.raises(ValidationError):
        validate_is_regex(invalid_regex)


def test_htmltextfield():
    class HTMLTextModel(models.Model):
        field = HTMLTextField(sanitizer_type="default")

        def pre_save(self):
            """Perform pre_save validations

            pre_save validation is typically called before saving.  As we
            do not have a migration for this anonymous model it makes more
            sense to simply call the function responsible for making the
            data ready to be saved

            Note:
                This only pre_saves the HTMLTextField"""
            f = [
                f
                for f in self._meta.local_concrete_fields
                if isinstance(f, HTMLTextField)
            ][0]
            f.pre_save(self, False)

    m = HTMLTextModel()
    m.field = '<script>evil()</script><b>foo</b><em>bar</em><a href="http://www.google.com/">Link'
    m.pre_save()

    assert (
        m.field
        == '<strong>foo</strong><em>bar</em><a href="http://www.google.com/">Link</a>'
    )


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
