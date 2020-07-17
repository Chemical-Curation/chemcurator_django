from pytest_factoryboy import register

from chemreg.substance.tests.factories import (
    QCLevelsTypeFactory,
    SourceFactory,
    SubstanceTypeFactory,
    SynonymTypeFactory,
)

register(QCLevelsTypeFactory)
register(SynonymTypeFactory)
register(SourceFactory)
register(SubstanceTypeFactory)
