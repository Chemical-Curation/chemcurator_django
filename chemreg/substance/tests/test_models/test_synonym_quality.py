from django.db import models

from chemreg.substance.models import SynonymQuality


def test_synonym_quality():
    """Tests the validity of the Synonym Quality Model's attributes"""

    name = SynonymQuality._meta.get_field("name")
    assert isinstance(name, models.SlugField)
    assert name.max_length == 49
    assert name.unique
    assert not name.blank
    label = SynonymQuality._meta.get_field("label")
    assert isinstance(label, models.CharField)
    assert label.max_length == 99
    assert label.unique
    assert not label.blank
    short_description = SynonymQuality._meta.get_field("short_description")
    assert isinstance(short_description, models.CharField)
    assert short_description.max_length == 499
    assert not short_description.blank
    long_description = SynonymQuality._meta.get_field("long_description")
    assert isinstance(long_description, models.TextField)
    assert not long_description.blank
    score_weight = SynonymQuality._meta.get_field("score_weight")
    assert isinstance(score_weight, models.FloatField)
    assert score_weight.default == 1.0
    assert not score_weight.blank
    is_restrictive = SynonymQuality._meta.get_field("is_restrictive")
    assert isinstance(is_restrictive, models.BooleanField)
    assert is_restrictive.default is False
    assert not is_restrictive.blank
