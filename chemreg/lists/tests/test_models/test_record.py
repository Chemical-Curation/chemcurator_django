from django.db import models

from chemreg.lists.models import List, Record
from chemreg.lists.utils import build_rid
from chemreg.substance.models import Substance


def test_record():
    """Tests the validity of the Record Model's attributes"""

    # Primitives
    assert type(Record.id.field) is models.CharField
    assert Record.id.field.max_length == 50
    assert not Record.id.field.blank
    assert not Record.id.field.null
    assert Record.id.field.unique
    assert Record.id.field.default is build_rid

    assert type(Record.external_id.field) is models.CharField
    assert Record.external_id.field.max_length == 500
    assert not Record.external_id.field.blank
    assert not Record.external_id.field.null

    assert type(Record.message.field) is models.CharField
    assert Record.message.field.max_length == 500
    assert Record.message.field.blank
    assert not Record.message.field.null

    assert type(Record.score.field) is models.FloatField
    assert Record.score.field.null

    assert type(Record.is_validated.field) is models.BooleanField
    assert not Record.is_validated.field.null

    # Foreign Keys
    assert type(Record.list.field) is models.ForeignKey
    assert Record.list.field.related_model is List
    assert not Record.list.field.null

    assert type(Record.substance.field) is models.ForeignKey
    assert Record.substance.field.related_model is Substance
    assert Record.substance.field.null
