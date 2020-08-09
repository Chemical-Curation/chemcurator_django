from django.db import models

from chemreg.substance.models import RelationshipType


def test_relationship_type():
    """Tests the validity of the Relationship Type Model's attributes"""
    name = RelationshipType._meta.get_field("name")
    assert isinstance(name, models.SlugField)
    assert name.max_length == 49
    assert name.unique
    assert not name.blank
    label = RelationshipType._meta.get_field("label")
    assert isinstance(label, models.CharField)
    assert label.max_length == 99
    assert label.unique
    assert not label.blank
    short_description = RelationshipType._meta.get_field("short_description")
    assert isinstance(short_description, models.CharField)
    assert short_description.max_length == 499
    assert not short_description.blank
    long_description = RelationshipType._meta.get_field("long_description")
    assert isinstance(long_description, models.TextField)
    assert not long_description.blank
    corrolary_label = RelationshipType._meta.get_field("corrolary_label")
    assert isinstance(corrolary_label, models.CharField)
    assert corrolary_label.max_length == 99
    assert not corrolary_label.blank
    corrolary_short_description = RelationshipType._meta.get_field(
        "corrolary_short_description"
    )
    assert isinstance(corrolary_short_description, models.CharField)
    assert corrolary_short_description.max_length == 499
    assert not corrolary_short_description.blank
