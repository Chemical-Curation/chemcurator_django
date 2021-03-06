from pytest_factoryboy import register

from chemreg.substance.tests.factories import (
    QCLevelsTypeFactory,
    RelationshipTypeFactory,
    SourceFactory,
    SubstanceFactory,
    SubstanceRelationshipFactory,
    SubstanceTypeFactory,
    SynonymFactory,
    SynonymQualityFactory,
    SynonymTypeFactory,
)

register(QCLevelsTypeFactory)
register(RelationshipTypeFactory)
register(SourceFactory)
register(SubstanceFactory)
register(SubstanceRelationshipFactory)
register(SubstanceTypeFactory)
register(SynonymFactory)
register(SynonymQualityFactory)
register(SynonymTypeFactory)
