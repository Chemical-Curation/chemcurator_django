from faker.providers import BaseProvider

from chemreg.compound.utils import build_cid


class CIDFaker(BaseProvider):
    """Provides a CID provider to Faker."""

    def cid(self):
        return build_cid(self.random_int(2000000, 3000000))


class InChIKeyFaker(BaseProvider):
    """Provides an InChIKey provider to Faker.

    InChIKey consists of hyphen-separated three parts, of 14, 10 and one
    character(s), respectively, like XXXXXXXXXXXXXX-YYYYYYYYYY-Z. The first
    14 characters result from a hash of the connectivity information of the
    InChI. The second part consists of 8 characters resulting from a hash of
    the remaining layers of the InChI, a single character indicating the kind
    of InChIKey and a single character indicating the version of InChI used.
    At last, a single character indicates protonation.[1]

    [1] https://en.wikipedia.org/wiki/International_Chemical_Identifier#InChIKey
    """

    def inchikey(self):
        connectivity_hash = "".join(self.random_letters(14)).upper()
        layer_hash = "".join(self.random_letters(10)).upper()
        protonation = self.random_letter().upper()
        return f"{connectivity_hash}-{layer_hash}-{protonation}"


class MRVFileFaker(BaseProvider):
    """Provides a MRVFile string provider to Faker."""

    def mrvfile(self):
        return f'<cml><MDocument><MChemicalStruct><molecule molID="m1"><atomArray><atom id="a1" elementType="C" x2="-1.1102230246251565e-16" y2="0"/><atom id="a2" elementType="O" x2="1.54" y2="1.1102230246251565e-16" lonePair="2"/></atomArray><bondArray><bond atomRefs2="a1 a2" order="2" id="b1"/></bondArray></molecule></MChemicalStruct><MElectronContainer occupation="0 0" radical="0" id="o1"><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/></MElectronContainer><MElectronContainer occupation="0 0" radical="0" id="o2"><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/></MElectronContainer></MDocument></cml>'

