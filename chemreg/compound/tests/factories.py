import factory

from chemreg.compound.models import BaseCompound
from chemreg.compound.tests.fakers import CIDFaker

factory.Faker.add_provider(CIDFaker)


class BaseCompoundFactory(factory.DjangoModelFactory):
    """Manufactures BaseCompound models."""

    cid = factory.Faker("cid")
    structure = factory.Faker("text")

    class Meta:
        model = BaseCompound
