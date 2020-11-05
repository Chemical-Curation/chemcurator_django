from pytest_factoryboy import register

from chemreg.substance.tests.factories import SubstanceFactory, SynonymFactory

register(SubstanceFactory)
register(SynonymFactory)
