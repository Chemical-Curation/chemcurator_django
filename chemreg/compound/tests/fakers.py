from faker.providers import BaseProvider

from chemreg.compound.utils import build_cid


class CIDFaker(BaseProvider):
    """Provides a CID provider to Faker."""

    def cid(self):
        return build_cid(self.random_int(2000000, 3000000))
