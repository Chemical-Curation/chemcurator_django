from pytest_factoryboy import register

from chemreg.compound.tests.factories import (
    DefinedCompoundFactory,
    DefinedCompoundSmilesFactory,
    DefinedCompoundV2000Factory,
    IllDefinedCompoundFactory,
    QueryStructureTypeFactory,
)

register(DefinedCompoundFactory)
register(DefinedCompoundSmilesFactory)
register(IllDefinedCompoundFactory)
register(QueryStructureTypeFactory)
register(DefinedCompoundV2000Factory)
