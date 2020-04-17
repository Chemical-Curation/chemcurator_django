from pytest_factoryboy import register

from chemreg.compound.tests.factories import (
    DefinedCompoundFactory,
    DefinedCompoundSmilesFactory,
    IllDefinedCompoundFactory,
    QueryStructureTypeFactory,
)

register(DefinedCompoundFactory)
register(DefinedCompoundSmilesFactory)
register(IllDefinedCompoundFactory)
register(QueryStructureTypeFactory)
