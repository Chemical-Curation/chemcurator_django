from pytest_factoryboy import register

from chemreg.substance.tests.factories import (
    SubstanceFactory,
    SynonymFactory,
    SynonymQualityFactory,
    SynonymTypeFactory,
)

register(SubstanceFactory)
register(SynonymFactory)
register(SynonymQualityFactory)
register(SynonymTypeFactory)
