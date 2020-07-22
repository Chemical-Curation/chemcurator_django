from pytest_factoryboy import register

from chemreg.substance.tests.factories import (
    QCLevelsTypeFactory,
    RelationshipTypeFactory,
    SourceFactory,
    SubstanceFactory,
    SubstanceTypeFactory,
    SynonymQualityFactory,
    SynonymTypeFactory,
)

register(QCLevelsTypeFactory)
register(RelationshipTypeFactory)
register(SynonymTypeFactory)
register(SourceFactory)
register(SubstanceFactory)
register(SubstanceTypeFactory)
register(SynonymQualityFactory)

