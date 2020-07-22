import pytest
from rest_framework_json_api.utils import get_included_serializers

from chemreg.compound.serializers import CompoundSerializer
from chemreg.substance.serializers import (
    HyperlinkedModelSerializer,
    QCLevelsTypeSerializer,
    RelationshipTypeSerializer,
    SourceSerializer,
    SubstanceSerializer,
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
def test_substance_serializer():
    assert issubclass(SubstanceSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_substance_serializer_includes():
    serializer = get_included_serializers(SubstanceSerializer)
    assert serializer["source"] is SourceSerializer
    assert serializer["substance_type"] is SubstanceTypeSerializer
    assert serializer["qc_level"] is QCLevelsTypeSerializer
    assert serializer["associated_compound"] is CompoundSerializer


@pytest.mark.django_db
def test_substance_no_associated_compound(substance_factory):
    serializer = substance_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_substance_defined_compound(substance_factory):
    serializer = substance_factory.build(defined=True)
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_substance_ill_defined_compound(substance_factory):
    serializer = substance_factory.build(illdefined=True)
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
def test_relationship_type_serializer():
    assert issubclass(RelationshipTypeSerializer, HyperlinkedModelSerializer)


@pytest.mark.django_db
def test_relationship_type(relationship_type_factory):
    serializer = relationship_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


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
