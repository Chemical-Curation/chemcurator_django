from django.db import models

from chemreg.substance.models import SynonymType


def test_synonym_type():
    """Tests the validity of the Synonym Type Model's attributes"""

    name = SynonymType._meta.get_field("name")
    assert isinstance(name, models.SlugField)
    assert name.max_length == 49
    assert name.unique
    assert not name.blank
    label = SynonymType._meta.get_field("label")
    assert isinstance(label, models.CharField)
    assert label.max_length == 99
    assert label.unique
    assert not label.blank
    short_description = SynonymType._meta.get_field("short_description")
    assert isinstance(short_description, models.CharField)
    assert short_description.max_length == 499
    assert not short_description.blank
    long_description = SynonymType._meta.get_field("long_description")
    assert isinstance(long_description, models.TextField)
    assert not long_description.blank
    validation_regular_expression = SynonymType._meta.get_field(
        "validation_regular_expression"
    )
    assert isinstance(validation_regular_expression, models.TextField)
    assert validation_regular_expression.blank is True
    score_modifier = SynonymType._meta.get_field("score_modifier")
    assert isinstance(score_modifier, models.FloatField)
    assert score_modifier.default == 0.0
