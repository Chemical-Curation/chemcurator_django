from indigo import Indigo


def get_molfile_v3000(compound: str) -> str:
    """Computes the molfile v3000 from a compound string.

    Args:
        compound: A molfile (either v2000 or v3000), MRV file, etc.

    Returns:
        The molfile v3000.

    """
    indigo = Indigo()
    indigo.setOption("molfile-saving-mode", "3000")
    molecule = indigo.loadMolecule(compound)
    return molecule.molfile()
