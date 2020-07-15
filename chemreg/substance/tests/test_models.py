from django.db import models

from chemreg.substance.models import (
    QCLevelsType,
    Source,
    SubstanceType,
    Synonym,
    SynonymQuality,
    SynonymType,
)


def test_source_model():
    """Tests the validity of the Source Model's attributes"""
    name = Source._meta.get_field("name")
    assert isinstance(name, models.SlugField)
    assert name.max_length == 49
    assert name.unique
    assert not name.blank
    label = Source._meta.get_field("label")
    assert isinstance(label, models.CharField)
    assert label.max_length == 99
    assert label.unique
    assert not label.blank
    short_description = Source._meta.get_field("short_description")
    assert isinstance(short_description, models.CharField)
    assert short_description.max_length == 499
    assert not short_description.blank
    long_description = Source._meta.get_field("long_description")
    assert isinstance(long_description, models.TextField)
    assert not long_description.blank


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


def test_qc_levels_type():
    """Tests the validity of the QC Levels Type Model's attributes"""

    name = QCLevelsType._meta.get_field("name")
    assert isinstance(name, models.SlugField)
    assert name.max_length == 49
    assert name.unique
    assert not name.blank
    label = QCLevelsType._meta.get_field("label")
    assert isinstance(label, models.CharField)
    assert label.max_length == 99
    assert label.unique
    assert not label.blank
    short_description = QCLevelsType._meta.get_field("short_description")
    assert isinstance(short_description, models.CharField)
    assert short_description.max_length == 499
    assert not short_description.blank
    long_description = QCLevelsType._meta.get_field("long_description")
    assert isinstance(long_description, models.TextField)
    assert not long_description.blank
    rank = QCLevelsType._meta.get_field("rank")
    assert isinstance(rank, models.IntegerField)
    assert rank.unique
    assert not rank.blank


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


def test_synonym():
    """Tests the validity of the Synonym Model's attributes"""

    identifier = Synonym._meta.get_field("identifier")
    assert isinstance(identifier, models.TextField)
    assert identifier.max_length == 1024
    assert not identifier.blank
    assert Synonym.synonym_quality.field.related_model is SynonymQuality
    assert Synonym.source.field.related_model is Source
    assert Synonym.synonym_type.field.related_model is SynonymType
    qc_notes = Synonym._meta.get_field("qc_notes")
    assert isinstance(qc_notes, models.TextField)
    assert qc_notes.max_length == 1024
    assert not qc_notes.blank
