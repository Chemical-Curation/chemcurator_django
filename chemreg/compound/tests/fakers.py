import bz2
import os
import pickle

from faker.providers import BaseProvider
from indigo import Indigo

from chemreg.compound.utils import build_cid, format_mrvfile

with bz2.open(os.path.join(os.path.dirname(__file__), "compounds.bz2"), "rb") as f:
    COMPOUNDS = pickle.load(f)


class CompoundFaker(BaseProvider):
    compounds = COMPOUNDS
    indigo = Indigo()

    def molecule(self):
        smiles_str = self.random_element(self.compounds)
        return self.indigo.loadMolecule(smiles_str)

    def cid(self):
        return build_cid(self.random_int(2000000, 3000000))

    def molfile(self, v2000=False):
        if v2000:
            self.indigo.setOption("molfile-saving-mode", "2000")
        else:
            self.indigo.setOption("molfile-saving-mode", "3000")
        return self.molecule().molfile()

    def mrvfile(self):
        s = format_mrvfile(self.molecule().cml())
        print(s)
        return s

    def molfile_v2000(self):
        smiles_str = self.random_element(self.compounds)
        self.indigo.setOption("molfile-saving-mode", "2000")
        return self.indigo.loadMolecule(smiles_str).molfile()
