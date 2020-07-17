import pytest

from chemreg.substance.serializers import (
    HyperlinkedModelSerializer,
    QCLevelsTypeSerializer,
    SourceSerializer,
    SynonymTypeSerializer,
)


@pytest.mark.django_db
def test_qc_levels_type_serializer():
    assert issubclass(QCLevelsTypeSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_qc_levels_type(qc_levels_type_factory):
    serializer = qc_levels_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


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
