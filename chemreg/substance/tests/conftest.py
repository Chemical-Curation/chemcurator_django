from pytest_factoryboy import register

from chemreg.substance.tests.factories import SourceFactory, SynonymTypeFactory

register(SynonymTypeFactory)
register(SourceFactory)
