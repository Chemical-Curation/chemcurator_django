from django.apps import apps

import factory

from chemreg.common.factory import (
    ChemicalProvider,
    ControlledVocabularyFactory,
    DjangoSerializerFactory,
)
from chemreg.substance.serializers import (
    QCLevelsTypeSerializer,
    SourceSerializer,
    SubstanceTypeSerializer,
    SynonymQualitySerializer,
    SynonymTypeSerializer,
)

factory.Faker.add_provider(ChemicalProvider)


class SourceFactory(DjangoSerializerFactory, ControlledVocabularyFactory):
    """Manufactures `Source` models."""

    class Meta:
        model = SourceSerializer


class SubstanceTypeFactory(DjangoSerializerFactory, ControlledVocabularyFactory):
    """Manufactures `SubstanceType` models."""

    class Meta:
        model = SubstanceTypeSerializer


class QCLevelsTypeFactory(DjangoSerializerFactory, ControlledVocabularyFactory):
    """Manufactures `QCLevelsType` models.

    This inherits from ControlledVocabularyFactory but uses the serializer
    methods from DjangoSerializerFactory
    """

    rank = factory.Sequence(lambda n: n)

    class Meta:
        model = QCLevelsTypeSerializer


class SubstanceFactory(factory.DjangoModelFactory):
    """Manufactures `Substance` models.

    Todo: On creation of Substance Serializer convert this to a DjangoSerializerFactory"""

    preferred_name = factory.Sequence(
        lambda n: f"{factory.Faker('slug').generate()}-{n}"
    )
    display_name = factory.LazyAttribute(lambda o: o.preferred_name.replace("-", " "))
    description = factory.Faker("text")
    public_qc_note = factory.Faker("text")
    private_qc_note = factory.Faker("text")
    casrn = factory.Faker("cas_number")

    # Related Factories
    # Todo: This is a work around to allow SerializerFactories as SubFactories. Remove when converting
    source = factory.LazyAttribute(lambda _: SourceFactory().instance)
    substance_type = factory.LazyAttribute(lambda _: SubstanceTypeFactory().instance)
    qc_level = factory.LazyAttribute(lambda _: QCLevelsTypeFactory().instance)

    class Meta:
        model = apps.get_model("substance", "Substance")


class SynonymTypeFactory(DjangoSerializerFactory, ControlledVocabularyFactory):
    """Manufactures `SynonymType` models."""

    validation_regular_expression = ".*"
    score_modifier = factory.Faker("pyfloat")

    class Meta:
        model = SynonymTypeSerializer


class SynonymQualityFactory(DjangoSerializerFactory, ControlledVocabularyFactory):
    """Manufactures `SynonymQuality` Serializers."""

    score_weight = factory.Faker("pyfloat", positive=True)
    is_restrictive = factory.Faker("boolean")

    class Meta:
        model = SynonymQualitySerializer
