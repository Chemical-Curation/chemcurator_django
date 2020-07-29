from django.db import models

from chemreg.lists.models import AccessibilityType, ExternalContact, List
from chemreg.users.models import User


def test_list():
    """Tests the validity of the List Model's attributes"""

    name = List._meta.get_field("name")
    assert name.max_length == 49
    assert name.unique
    assert not name.blank
    label = List._meta.get_field("label")
    assert label.max_length == 255
    assert label.unique
    assert not label.blank
    short_description = List._meta.get_field("short_description")
    assert short_description.max_length == 1000
    assert not short_description.blank
    long_description = List._meta.get_field("long_description")
    assert not long_description.blank
    assert List.list_accessibility.field.related_model is AccessibilityType
    assert List.owners.field.related_model is User
    source_url = List._meta.get_field("source_url")
    assert isinstance(source_url, models.CharField)
    assert source_url.max_length == 500
    assert source_url.blank
    source_reference = List._meta.get_field("source_reference")
    assert isinstance(source_reference, models.CharField)
    assert source_reference.max_length == 500
    assert source_reference.blank
    source_doi = List._meta.get_field("source_doi")
    assert isinstance(source_doi, models.CharField)
    assert source_doi.max_length == 500
    assert source_doi.blank
    assert List.external_contact.field.related_model is ExternalContact
    date_of_source_collection = List._meta.get_field("date_of_source_collection")
    assert isinstance(date_of_source_collection, models.DateField)
    assert not date_of_source_collection.editable
    assert not date_of_source_collection.blank
