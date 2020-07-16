from pytest_factoryboy import register

from chemreg.substance.tests.factories import (
    SourceFactory,
    SubstanceTypeFactory,
    SynonymTypeFactory,
)

register(SynonymTypeFactory)
register(SourceFactory)
register(SubstanceTypeFactory)
