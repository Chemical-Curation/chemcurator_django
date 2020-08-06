import pytest

from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.lists.serializers import IdentifierTypeSerializer, ListTypeSerializer


@pytest.mark.django_db
def test_list_type_serializer():
    assert issubclass(ListTypeSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_list_type(list_type_factory):
    serializer = list_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_identifier_type_serializer():
    assert issubclass(IdentifierTypeSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_identifier_type(identifier_type_factory):
    serializer = identifier_type_factory.build()
    assert serializer.is_valid()
    serializer.save()
