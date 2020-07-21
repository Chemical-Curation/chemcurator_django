import pytest

from chemreg.substance.serializers import (
    HyperlinkedModelSerializer,
    QCLevelsTypeSerializer,
    SourceSerializer,
    SubstanceTypeSerializer,
    SynonymQualitySerializer,
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


@pytest.mark.django_db
def test_substance_type_serializer():
    assert issubclass(SubstanceTypeSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_substance_type(substance_type_factory):
    serializer = substance_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_synonym_quality_serializer():
    assert issubclass(SynonymQualitySerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_synonym_quality(synonym_quality_factory):
    serializer = synonym_quality_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_synonym_quality_score_weight_validation(synonym_quality_factory):
    model_dict = synonym_quality_factory.build().initial_data
    # Negative score_weights are forbidden
    model_dict.update(score_weight=-1.0)
    assert not SynonymQualitySerializer(data=model_dict).is_valid()
