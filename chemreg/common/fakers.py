from faker.providers import BaseProvider

from chemreg.common.utils import casrn_checksum


class ChemicalProvider(BaseProvider):
    """Provider to allow faker to generate cas numbers.

    To add to factory_boy's instance of faker add
    `factory.Faker.add_provider(ChemicalProvider)`
    to the beginning of your factory file.
    """

    def cas_number(self):
        """
        Returns a CAS string
        """
        seg1 = self.generator.random.randrange(10, 9999999)
        seg2 = self.generator.random.randrange(10, 99)
        seg3 = casrn_checksum(int(f"{seg1}{seg2}"))
        return f"{seg1}-{seg2}-{seg3}"
