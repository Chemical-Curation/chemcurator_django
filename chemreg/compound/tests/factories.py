import factory

from chemreg.compound.models import (
    BaseCompound,
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.tests.fakers import CIDFaker, MolfileFaker, MRVFileFaker

factory.Faker.add_provider(CIDFaker)
factory.Faker.add_provider(MolfileFaker)
factory.Faker.add_provider(MRVFileFaker)


class BaseCompoundFactory(factory.DjangoModelFactory):
    """Manufactures `BaseCompound` models."""

    cid = factory.Faker("cid")
    structure = factory.Faker("text")

    class Meta:
        model = BaseCompound


class DefinedCompoundFactory(factory.DjangoModelFactory):
    """Manufactures `DefinedCompound` models."""

    cid = factory.Faker("cid")
    molfile = factory.Faker("molfile_v3000")
    created_at = factory.Faker("date_time_this_century")

    class Meta:
        model = DefinedCompound


class DefinedCompoundJSONFactory(factory.DictFactory):
    """Manufactures `DefinedCompound` dictionaries."""

    id = factory.Faker("cid")
    molfile = factory.Faker("molfile_v3000")


class QueryStructureTypeFactory(factory.DjangoModelFactory):
    """Manufactures `QueryStructureType` models."""

    name = factory.Faker("slug")
    label = factory.Sequence(lambda n: "label%s" % n)
    short_description = factory.Faker("text")
    long_description = factory.Faker("text")

    class Meta:
        model = QueryStructureType


class QueryStructureTypeJSONFactory(factory.DictFactory):
    """Manufactures `QueryStructureType` dictionaries."""

    name = factory.Faker("slug")
    label = factory.Faker("pystr", max_chars=15)
    short_description = factory.Faker("text")
    long_description = factory.Faker("text")


class IllDefinedCompoundFactory(factory.DjangoModelFactory):
    """Manufactures `IllDefinedCompound` models."""

    cid = factory.Faker("cid")
    mrvfile = factory.Faker("mrvfile")
    query_structure_type = factory.SubFactory(QueryStructureTypeFactory)

    class Meta:
        model = IllDefinedCompound


class IllDefinedCompoundJSONFactory(factory.DictFactory):
    """Manufactures `IllDefinedCompound` dictionaries."""

    id = factory.Faker("cid")
    mrvfile = factory.Faker("text")
    # query_structure_type = factory.build(
    #     dict,
    #     FACTORY_CLASS=QueryStructureTypeFactory,
    #     name="ill-defined",
    #     label="Ill Defined",
    #     short_description="An ill-defined compound",
    #     long_description="A longer description of an ill-defined compound",
    # )
