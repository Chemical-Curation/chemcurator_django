from pytest_factoryboy import register

from chemreg.compound.tests.factories import (
    DefinedCompoundFactory,
    DefinedCompoundSmilesFactory,
    DefinedCompoundV2000Factory,
    IllDefinedCompoundFactory,
    QueryStructureTypeFactory,
)
from chemreg.substance.tests.factories import SubstanceFactory

register(DefinedCompoundFactory)
register(DefinedCompoundSmilesFactory)
register(IllDefinedCompoundFactory)
register(QueryStructureTypeFactory)
register(DefinedCompoundV2000Factory)
register(SubstanceFactory)
