from django.apps import apps
from django.db import models

from chemreg.substance.models import SubstanceRelationship


def test_substance_relationship_model_attributes():
    """Tests the validity of the SubstanceRelationship Model's attributes"""
    assert type(SubstanceRelationship.from_substance.field) is models.ForeignKey
    assert SubstanceRelationship.from_substance.field.related_model is apps.get_model(
        "substance", "Substance"
    )

    assert type(SubstanceRelationship.to_substance.field) is models.ForeignKey
    assert SubstanceRelationship.to_substance.field.related_model is apps.get_model(
        "substance", "Substance"
    )

    assert type(SubstanceRelationship.source.field) is models.ForeignKey
    assert SubstanceRelationship.source.field.related_model is apps.get_model(
        "substance", "Source"
    )

    assert type(SubstanceRelationship.relationship_type.field) is models.ForeignKey
    assert (
        SubstanceRelationship.relationship_type.field.related_model
        is apps.get_model("substance", "RelationshipType")
    )

    assert type(SubstanceRelationship.qc_note.field) is models.CharField
    assert SubstanceRelationship.qc_note.field.max_length == 1024
    assert SubstanceRelationship.qc_note.field.blank


def test_substance_relationship_constraints():
    assert (
        "from_substance",
        "to_substance",
        "source",
        "relationship_type",
    ) in SubstanceRelationship._meta.unique_together
