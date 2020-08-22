import pytest

from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.lists.serializers import (
    AccessibilityTypeSerializer,
    ExternalContactSerializer,
    IdentifierTypeSerializer,
    ListSerializer,
    ListTypeSerializer,
    RecordIdentifierSerializer,
    RecordSerializer,
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


def test_external_contact_serializer():
    assert issubclass(ExternalContactSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_external_contact(external_contact_factory):
    serializer = external_contact_factory.build()
    assert serializer.is_valid()
    serializer.save()


def test_list_serializer():
    assert issubclass(ListSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_list(list_factory):
    serializer = list_factory.build()
    assert serializer.is_valid()
    serializer.save()


def test_record_serializer():
    assert issubclass(RecordSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_record(record_factory):
    serializer = record_factory.build()
    assert serializer.is_valid()
    serializer.save()


def test_record_identifier_serializer():
    assert issubclass(RecordIdentifierSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_record_identifier(record_identifier_factory):
    serializer = record_identifier_factory.build()
    assert serializer.is_valid()
    serializer.save()
