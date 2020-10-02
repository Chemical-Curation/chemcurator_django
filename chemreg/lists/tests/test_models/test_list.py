from django.db import models

import pytest

from chemreg.common.models import HTMLTextField
from chemreg.common.tests import controlled_vocabulary_test_helper
from chemreg.lists.models import AccessibilityType, ExternalContact, List, ListType
from chemreg.lists.tests.factories import ListFactory, ListTypeFactory
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
    assert isinstance(short_description, HTMLTextField)
    assert short_description.max_length == 1000
    assert not short_description.blank
    long_description = List._meta.get_field("long_description")
    assert isinstance(long_description, HTMLTextField)
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
    assert not date_of_source_collection.blank


def test_list_type():
    """Tests the validity of the List Type Model's attributes"""

    controlled_vocabulary_test_helper(ListType)


@pytest.mark.django_db
def test_lists_to_types():
    """Tests the many-to-many relationship between `List` and `ListType` objects"""

    list = ListFactory().instance
    assert list.types.count() == 0

    types = [ListTypeFactory().instance, ListTypeFactory().instance]
    assert len(types) == 2
    list.types.set(types)
    assert list.types.count() == 2
    type = types[0]
    list_rel = type.lists.first()
    assert list_rel == list


@pytest.mark.django_db
def test_lists_html_fields(list_factory):
    unsanitized_html = '<script>func</script>Foobar<a href="https://www.google.com/">'
    sanitized_html = 'Foobar<a href="https://www.google.com/"></a>'

    m = list_factory.build(
        long_description=unsanitized_html, short_description=unsanitized_html
    )

    assert not m.is_valid()
    assert m.errors

    # 0 is the index of the string in the error detail tuple.
    assert sanitized_html in m.errors["short_description"][0]
    assert sanitized_html in m.errors["long_description"][0]
