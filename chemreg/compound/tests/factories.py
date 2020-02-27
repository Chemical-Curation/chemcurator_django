import factory

from chemreg.compound.models import BaseCompound, DefinedCompound, QueryStructureType
from chemreg.compound.tests.fakers import CIDFaker, InChIKeyFaker

factory.Faker.add_provider(CIDFaker)
factory.Faker.add_provider(InChIKeyFaker)


class BaseCompoundFactory(factory.DjangoModelFactory):
    """Manufactures `BaseCompound` models."""

    cid = factory.Faker("cid")
    structure = factory.Faker("text")

    class Meta:
        model = BaseCompound


class DefinedCompoundFactory(factory.DjangoModelFactory):
    """Manufactures `DefinedCompound` models."""

    cid = factory.Faker("cid")
    molefile = factory.Faker("text")
    inchikey = factory.Faker("inchikey")

    class Meta:
        model = DefinedCompound


class DefinedCompoundJSONFactory(factory.DictFactory):
    """Manufactures `DefinedCompound` dictionaries."""

    id = factory.Faker("cid")
    molefile = factory.Faker("text")
    inchikey = factory.Faker("inchikey")


class QueryStructureTypeFactory(factory.DjangoModelFactory):
    """Manufactures `QueryStructureType` models."""

    label = factory.Sequence(lambda n: "label%s" % n)
    short_description = factory.Faker("text")
    long_description = factory.Faker("text")

    class Meta:
        model = QueryStructureType

