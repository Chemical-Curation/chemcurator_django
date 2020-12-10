from django.db import models

from chemreg.substance.models import SubstanceType


def test_substance_type():
    """Tests the validity of the Substance Type Model's attributes"""
    name = SubstanceType._meta.get_field("name")
    assert isinstance(name, models.SlugField)
    assert name.max_length == 49
    assert name.unique
    assert not name.blank
    label = SubstanceType._meta.get_field("label")
    assert isinstance(label, models.CharField)
    assert label.max_length == 99
    assert label.unique
    assert not label.blank
    short_description = SubstanceType._meta.get_field("short_description")
    assert isinstance(short_description, models.CharField)
    assert short_description.max_length == 499
    assert not short_description.blank
    long_description = SubstanceType._meta.get_field("long_description")
    assert isinstance(long_description, models.TextField)
    assert not long_description.blank
