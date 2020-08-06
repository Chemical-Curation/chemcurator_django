from django.db import models

import pytest

from chemreg.lists.models import IdentifierType, Record, RecordIdentifier
from chemreg.lists.tests.factories import (
    IdentifierTypeFactory,
    RecordFactory,
    RecordIdentifierFactory,
)


def test_record_identifier():
    """Tests the validity of the Record Identifier Model's attributes"""

    assert RecordIdentifier.record.field.related_model is Record
    identifier = RecordIdentifier._meta.get_field("identifier")
    assert isinstance(identifier, models.TextField)
    assert not identifier.blank
    identifier_label = RecordIdentifier._meta.get_field("identifier_label")
    assert isinstance(identifier_label, models.CharField)
    assert identifier_label.max_length == 100
    assert not identifier_label.blank
    assert RecordIdentifier.identifier_type.field.related_model is IdentifierType


@pytest.mark.django_db
def test_record_identifier_relationships():
    """ Tests the relationships between the RecordIdentifier, IdentifierType and Record Models"""

    idt_list = [IdentifierTypeFactory().instance, IdentifierTypeFactory().instance]
    assert len(idt_list) == 2
    rec = RecordFactory()
    RecordIdentifierFactory(identifier_type=idt_list[0], record=rec)
    RecordIdentifierFactory(identifier_type=idt_list[1], record=rec)
    assert rec.identifiers.count() == 2
