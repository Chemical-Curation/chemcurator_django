import factory

from chemreg.common.factory import ControlledVocabularyFactory, DjangoSerializerFactory
from chemreg.common.fakers import ChemicalProvider
from chemreg.compound.tests.factories import (
    DefinedCompoundFactory,
    IllDefinedCompoundFactory,
)
from chemreg.substance.serializers import (
    QCLevelsTypeSerializer,
    SourceSerializer,
    SubstanceSerializer,
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


class SubstanceFactory(DjangoSerializerFactory):
    """Manufactures `Substance` models.
    """

    preferred_name = factory.Sequence(
        lambda n: f"{factory.Faker('slug').generate()}-{n}"
    )
    display_name = factory.LazyAttribute(lambda o: o.preferred_name.replace("-", " "))
    description = factory.Faker("text")
    public_qc_note = factory.Faker("text")
    private_qc_note = factory.Faker("text")
    casrn = factory.Faker("cas_number")

    # Related Factories
    source = factory.SubFactory(SourceFactory)
    substance_type = factory.SubFactory(SubstanceTypeFactory)
    qc_level = factory.SubFactory(QCLevelsTypeFactory)
    associated_compound = None

    class Meta:
        model = SubstanceSerializer

    class Params:
        defined = factory.Trait(
            associated_compound=factory.SubFactory(
                DefinedCompoundFactory, _is_sub_factory=True
            )
        )
        illdefined = factory.Trait(
            associated_compound=factory.SubFactory(
                IllDefinedCompoundFactory, _is_sub_factory=True
            )
        )


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
