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
