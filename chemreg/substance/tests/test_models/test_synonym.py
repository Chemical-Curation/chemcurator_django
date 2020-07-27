from django.db import models

from chemreg.substance.models import (
    Source,
    Substance,
    Synonym,
    SynonymQuality,
    SynonymType,
)


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
    assert type(Synonym.substance.field) is models.ForeignKey
    assert Synonym.substance.field.related_model is Substance
    assert qc_notes.blank
