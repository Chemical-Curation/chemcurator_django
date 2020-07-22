from pytest_factoryboy import register

from chemreg.substance.tests.factories import (
    QCLevelsTypeFactory,
    SourceFactory,
    SubstanceFactory,
    SubstanceTypeFactory,
    SynonymQualityFactory,
    SynonymTypeFactory,
)

register(QCLevelsTypeFactory)
register(SynonymTypeFactory)
register(SourceFactory)
register(SubstanceFactory)
register(SubstanceTypeFactory)
register(SynonymQualityFactory)
