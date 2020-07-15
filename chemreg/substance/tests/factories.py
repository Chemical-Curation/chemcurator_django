import factory

from chemreg.common.factory import DjangoSerializerFactory
from chemreg.substance.serializers import SourceSerializer, SynonymTypeSerializer


class SynonymTypeFactory(DjangoSerializerFactory):
    """Manufactures `SynonymType` models."""

    name = factory.Faker("slug").generate()
    label = factory.LazyAttribute(lambda o: o.name.replace("-", " "))
    short_description = factory.Faker("text")
    long_description = factory.Faker("text")
    validation_regular_expression = ".*"
    score_modifier = factory.Faker("pyfloat")

    class Meta:
        model = SynonymTypeSerializer


class SourceFactory(DjangoSerializerFactory):
    """Manufactures `Source` models."""

    name = factory.Faker("slug").generate()
    label = factory.LazyAttribute(lambda o: o.name.replace("-", " "))
    short_description = factory.Faker("text")
    long_description = factory.Faker("text")

    class Meta:
        model = SourceSerializer
