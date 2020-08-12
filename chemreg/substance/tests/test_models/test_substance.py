from django.apps import apps
from django.db import models

import pytest

from chemreg.substance.models import Substance


def test_substance_model():
    """Tests the validity of the Substance Model's attributes"""
    # Verify CharField attributes
    assert type(Substance.sid.field) is models.CharField
    assert Substance.sid.field.max_length == 50
    assert Substance.sid.field.unique

    assert type(Substance.preferred_name.field) is models.CharField
    assert Substance.preferred_name.field.max_length == 255
    assert Substance.preferred_name.field.unique
    assert not Substance.preferred_name.field.blank

    assert type(Substance.display_name.field) is models.CharField
    assert Substance.display_name.field.max_length == 255
    assert Substance.display_name.field.unique
    assert not Substance.display_name.field.blank

    assert type(Substance.description.field) is models.CharField
    assert Substance.description.field.max_length == 1024

    assert type(Substance.public_qc_note.field) is models.CharField
    assert Substance.public_qc_note.field.max_length == 1024

    assert type(Substance.private_qc_note.field) is models.CharField
    assert Substance.private_qc_note.field.max_length == 1024

    assert type(Substance.casrn.field) is models.CharField
    assert Substance.casrn.field.max_length == 50
    assert Substance.casrn.field.unique

    # Assert Foreign Key Attributes
    assert type(Substance.source.field) is models.ForeignKey
    assert Substance.source.field.related_model is apps.get_model("substance", "Source")

    assert type(Substance.substance_type.field) is models.ForeignKey
    assert Substance.substance_type.field.related_model is apps.get_model(
        "substance", "SubstanceType"
    )

    assert type(Substance.qc_level.field) is models.ForeignKey
    assert Substance.qc_level.field.related_model is apps.get_model(
        "substance", "QCLevelsType"
    )

    assert type(Substance.associated_compound.field) is models.ForeignKey
    assert Substance.associated_compound.field.related_model is apps.get_model(
        "compound", "BaseCompound"
    )

    assert Substance.relationships.field.model is apps.get_model(
        "substance", "SubstanceRelationship"
    )
    # Reverse lookup for relationships
    assert Substance.related_to.field.model is apps.get_model(
        "substance", "SubstanceRelationship"
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "casrn,validity,code",
    [
        ("1234567-89-5", True, None),
        ("Non-CASRN String", False, "format"),
        ("1-89-5", False, "format"),
        ("1234567-89-0", False, "checksum"),
    ],
)
def test_validate_casrn(substance_factory, casrn, validity, code):
    substance = substance_factory.build(casrn=casrn)
    assert substance.is_valid() == validity
    if substance.errors:
        assert substance.errors["casrn"][0].code == code
