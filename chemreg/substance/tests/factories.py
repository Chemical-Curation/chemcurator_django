from django.apps import apps

import factory

from chemreg.common.factory import (
    ChemicalProvider,
    ControlledVocabularyFactory,
    DjangoSerializerFactory,
)
from chemreg.substance.serializers import SourceSerializer, SynonymTypeSerializer

factory.Faker.add_provider(ChemicalProvider)


class SourceFactory(DjangoSerializerFactory):
    """Manufactures `Source` models."""

    name = factory.Faker("slug").generate()
    label = factory.LazyAttribute(lambda o: o.name.replace("-", " "))
    short_description = factory.Faker("text")
    long_description = factory.Faker("text")

    class Meta:
        model = SourceSerializer


class SubstanceTypeFactory(ControlledVocabularyFactory):
    """Manufactures `SubstanceType` models."""

    class Meta:
        model = apps.get_model("substance", "SubstanceType")


class QCLevelsTypeFactory(ControlledVocabularyFactory):
    """Manufactures `QCLevelsType` models."""

    rank = factory.Sequence(lambda n: n)

    class Meta:
        model = apps.get_model("substance", "QCLevelsType")


class SubstanceFactory(factory.DjangoModelFactory):
    """Manufactures `Substance` models."""

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
