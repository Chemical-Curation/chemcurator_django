import factory

from chemreg.common.factory import DjangoSerializerFactory
from chemreg.substance.serializers import SynonymTypeSerializer


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
