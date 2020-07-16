import pytest

from chemreg.substance.serializers import (
    HyperlinkedModelSerializer,
    SourceSerializer,
    SubstanceTypeSerializer,
    SynonymTypeSerializer,
)


@pytest.mark.django_db
def test_synonym_type_serializer():
    assert issubclass(SynonymTypeSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_synonym_type(synonym_type_factory):
    serializer = synonym_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_source_serializer():
    assert issubclass(SourceSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_source(source_factory):
    serializer = source_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_substance_type_serializer():
    assert issubclass(SubstanceTypeSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_substance_type(substance_type_factory):
    serializer = substance_type_factory.build()
    assert serializer.is_valid()
    serializer.save()
