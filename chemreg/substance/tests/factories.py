from django.apps import apps

import factory

from chemreg.common.factory import (
    ChemicalProvider,
    ControlledVocabularyFactory,
    DjangoSerializerFactory,
)
from chemreg.substance.serializers import (
    SourceSerializer,
    SubstanceTypeSerializer,
    SynonymTypeSerializer,
)

factory.Faker.add_provider(ChemicalProvider)


class SourceFactory(DjangoSerializerFactory):
    """Manufactures `Source` models."""

    name = factory.Faker("slug")
    label = factory.LazyAttribute(lambda o: o.name.replace("-", " "))
    short_description = factory.Faker("text")
    long_description = factory.Faker("text")

    class Meta:
        model = SourceSerializer


class SubstanceTypeFactory(DjangoSerializerFactory):
    """Manufactures `SubstanceType` models."""

    name = factory.Faker("slug")
    label = factory.LazyAttribute(lambda o: o.name.replace("-", " "))
    short_description = factory.Faker("text")
    long_description = factory.Faker("text")

    class Meta:
        model = SubstanceTypeSerializer


class QCLevelsTypeFactory(ControlledVocabularyFactory):
    """Manufactures `QCLevelsType` models."""

    rank = factory.Sequence(lambda n: n)

    class Meta:
        model = apps.get_model("substance", "QCLevelsType")


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
    qc_level = factory.SubFactory(QCLevelsTypeFactory)

    class Meta:
        model = apps.get_model("substance", "Substance")


class SynonymTypeFactory(DjangoSerializerFactory):
    """Manufactures `SynonymType` models."""

    name = factory.Faker("slug")
    label = factory.LazyAttribute(lambda o: o.name.replace("-", " "))
    short_description = factory.Faker("text")
    long_description = factory.Faker("text")
    validation_regular_expression = ".*"
    score_modifier = factory.Faker("pyfloat")

    class Meta:
        model = SynonymTypeSerializer
