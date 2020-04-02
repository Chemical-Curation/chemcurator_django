from pytest_factoryboy import register

from chemreg.compound.tests.factories import (
    DefinedCompoundFactory,
    IllDefinedCompoundFactory,
    QueryStructureTypeFactory,
)

register(DefinedCompoundFactory)
register(IllDefinedCompoundFactory)
register(QueryStructureTypeFactory)
