import pytest

from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.lists.serializers import (
    AccessibilityTypeSerializer,
    IdentifierTypeSerializer,
    ListTypeSerializer,
)


@pytest.mark.django_db
def test_list_type_serializer():
    assert issubclass(ListTypeSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_list_type(list_type_factory):
    serializer = list_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_accessibility_type_serializer():
    assert issubclass(AccessibilityTypeSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_accessibility_type(accessibility_type_factory):
    serializer = accessibility_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


def test_identifier_type_serializer():
    assert issubclass(IdentifierTypeSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_identifier_type(identifier_type_factory):
    serializer = identifier_type_factory.build()
    assert serializer.is_valid()
    serializer.save()
