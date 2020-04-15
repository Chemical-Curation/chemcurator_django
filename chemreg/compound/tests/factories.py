import factory

from chemreg.common.factory import DjangoSerializerFactory
from chemreg.compound.serializers import (
    DefinedCompoundSerializer,
    IllDefinedCompoundSerializer,
    QueryStructureTypeSerializer,
)
from chemreg.compound.tests.fakers import CompoundFaker

factory.Faker.add_provider(CompoundFaker)


class DefinedCompoundFactory(DjangoSerializerFactory):
    """Manufactures `DefinedCompound` models."""

    molfile_v3000 = factory.Faker("molfile")

    class Meta:
        model = DefinedCompoundSerializer

    class Params:
        V2000 = factory.Trait(molfile_v3000=factory.Faker("molfile", v2000=True))


class DefinedCompoundSmilesFactory(DjangoSerializerFactory):
    """Manufactures `DefinedCompound` models without molfile input."""

    smiles = "CC(=O)NC1=CC=C(O)C=C1"

    class Meta:
        model = DefinedCompoundSerializer


class IllDefinedCompoundFactory(DjangoSerializerFactory):
    """Manufactures `IllDefinedCompound` models."""

    mrvfile = factory.Faker("mrvfile")

    class Meta:
        model = IllDefinedCompoundSerializer


class QueryStructureTypeFactory(DjangoSerializerFactory):
    """Manufactures `QueryStructureType` models."""

    name = factory.Faker("slug")
    label = factory.LazyAttribute(lambda o: o.name.replace("-", " "))
    short_description = factory.Faker("text")
    long_description = factory.Faker("text")

    class Meta:
        model = QueryStructureTypeSerializer
