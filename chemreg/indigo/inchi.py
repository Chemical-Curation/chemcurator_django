from indigo import Indigo
from indigo.inchi import IndigoInchi


def get_inchikey(compound: str) -> str:
    """Computes the InChIKey from a compound string.

    Args:
        compound: A molfile (either v2000 or v3000), MRV file, etc.

    Returns:
        The InChIKey for the compound.

    """
    indigo = Indigo()
    indigo_inchi = IndigoInchi(indigo)
    molecule = indigo.loadMolecule(compound)
    inchi = indigo_inchi.getInchi(molecule)
    return indigo_inchi.getInchiKey(inchi)


def load_structure(structure: str) -> str:
    """Use Indigo to load structure and return w/ V3000 format.

    Args:
        structure: A molfile string (either v2000 or smiles)

    Returns:
        The IndigoObject for the compound.

    """
    indigo = Indigo()
    indigo.setOption("molfile-saving-mode", "3000")
    return indigo.loadStructure(structureStr=structure)
