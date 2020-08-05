import pytest

from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.lists.serializers import ListTypeSerializer


@pytest.mark.django_db
def test_list_type_serializer():
    assert issubclass(ListTypeSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_list_type(list_type_factory):
    serializer = list_type_factory.build()
    assert serializer.is_valid()
    serializer.save()
