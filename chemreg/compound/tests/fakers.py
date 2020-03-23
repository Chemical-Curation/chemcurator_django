from faker.providers import BaseProvider

from chemreg.compound.utils import build_cid


class CIDFaker(BaseProvider):
    """Provides a CID provider to Faker."""

    def cid(self):
        return build_cid(self.random_int(2000000, 3000000))


class MolfileFaker(BaseProvider):
    """Provides a Molfile string provider to Faker."""

    molfiles_v2000 = [
        "\n  Marvin  10310613082D          \n\n  6  6  0  0  0  0            999 V2000\n    0.7145   -0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n    0.0000   -0.8250    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n    0.7145    0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n    0.0000    0.8250    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n   -0.7145   -0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n   -0.7145    0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n  2  1  2  0  0  0  0\n  3  1  1  0  0  0  0\n  4  3  2  0  0  0  0\n  5  2  1  0  0  0  0\n  6  4  1  0  0  0  0\n  5  6  2  0  0  0  0\nM  END\n"
    ]
    molfiles_v3000 = [
        "\n  Mrv1805 09121917092D          \n\n  0  0  0     0  0            999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 26 28 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 O 5.535 -11.0776 0 0\nM  V30 2 C 4.9086 -9.6708 0 0\nM  V30 3 C 3.377 -9.5098 0 0\nM  V30 4 C 2.4718 -10.7557 0 0\nM  V30 5 C 0.9403 -10.5947 0 0\nM  V30 6 C 0.3139 -9.1879 0 0\nM  V30 7 F -1.2177 -9.0269 0 0\nM  V30 8 C 1.2191 -7.942 0 0\nM  V30 9 C 2.7506 -8.1029 0 0\nM  V30 10 C 5.8138 -8.4249 0 0\nM  V30 11 C 7.3453 -8.5859 0 0\nM  V30 12 C 8.2505 -7.34 0 0\nM  V30 13 N 9.7821 -7.5009 0 0\nM  V30 14 C 10.6873 -6.2551 0 0\nM  V30 15 C 12.2188 -6.416 0 0\nM  V30 16 C 12.8452 -7.8229 0 0\nM  V30 17 O 14.1219 -6.9617 0 0\nM  V30 18 C 13.915 -8.9307 0 0\nM  V30 19 C 15.4092 -8.5581 0 0\nM  V30 20 C 16.479 -9.6659 0 0\nM  V30 21 C 16.0545 -11.1462 0 0\nM  V30 22 C 14.5603 -11.5188 0 0\nM  V30 23 C 13.4905 -10.411 0 0\nM  V30 24 C 17.1243 -12.254 0 0\nM  V30 25 C 11.94 -9.0688 0 0\nM  V30 26 C 10.4085 -8.9078 0 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 2 1 2\nM  V30 2 1 2 3\nM  V30 3 2 3 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  V30 6 1 6 7\nM  V30 7 1 6 8\nM  V30 8 2 8 9\nM  V30 9 1 3 9\nM  V30 10 1 2 10\nM  V30 11 1 10 11\nM  V30 12 1 11 12\nM  V30 13 1 12 13\nM  V30 14 1 13 14\nM  V30 15 1 14 15\nM  V30 16 1 15 16\nM  V30 17 1 16 17\nM  V30 18 1 16 18\nM  V30 19 2 18 19\nM  V30 20 1 19 20\nM  V30 21 2 20 21\nM  V30 22 1 21 22\nM  V30 23 2 22 23\nM  V30 24 1 18 23\nM  V30 25 1 21 24\nM  V30 26 1 16 25\nM  V30 27 1 25 26\nM  V30 28 1 13 26\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n"
    ]
    molfiles = molfiles_v2000 + molfiles_v3000

    def molfile(self):
        return self.random_element(self.molfiles)

    def molfile_v2000(self):
        return self.random_element(self.molfiles_v2000)

    def molfile_v3000(self):
        return self.random_element(self.molfiles_v3000)


class MRVFileFaker(BaseProvider):
    """Provides a MRVFile string provider to Faker."""

    def mrvfile(self):
        return f'<cml><MDocument><MChemicalStruct><molecule molID="m1"><atomArray><atom id="a1" elementType="C" x2="-1.1102230246251565e-16" y2="0"/><atom id="a2" elementType="O" x2="1.54" y2="1.1102230246251565e-16" lonePair="2"/></atomArray><bondArray><bond atomRefs2="a1 a2" order="2" id="b1"/></bondArray></molecule></MChemicalStruct><MElectronContainer occupation="0 0" radical="0" id="o1"><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/></MElectronContainer><MElectronContainer occupation="0 0" radical="0" id="o2"><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/></MElectronContainer></MDocument></cml>'
