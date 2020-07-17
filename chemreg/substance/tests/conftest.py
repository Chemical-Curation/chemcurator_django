from pytest_factoryboy import register

from chemreg.substance.tests.factories import (
    QCLevelsTypeFactory,
    SourceFactory,
    SynonymTypeFactory,
)

register(QCLevelsTypeFactory)
register(SynonymTypeFactory)
register(SourceFactory)
