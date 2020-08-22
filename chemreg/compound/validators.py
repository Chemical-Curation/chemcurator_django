import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import partialsmiles as ps
from indigo import IndigoException

from chemreg.compound.settings import compound_settings
from chemreg.compound.utils import chemreg_checksum, extract_checksum, extract_int
from chemreg.indigo.inchi import get_inchikey
from chemreg.indigo.molfile import get_molfile_v3000


def validate_inchikey_computable(molfile: str) -> None:
    """Validates that an InChIKey can be computed from the provided molfile.

    Args:
        molfile: The molfile string

    Raises:
        ValidationError: If the InChIKey cannot be computed.
    """
    try:
        get_inchikey(molfile)
    except IndigoException:
        raise ValidationError("InChIKey not computable for provided structure.")


def validate_smiles(smiles: str) -> None:
    """Validates that the `partialsmiles` library can convert the POST's SMILES string
    to a structure. This validator will ignore PartialSmiles' rejection of uncommon
    valences like `[S]` but will raise an error when it hits chirality described with
    `@@(`. For example, `[C@H](...` is valid but `C@@(...` is not.

    Args:
        smiles: The SMILES string

    Raises:
        ParseError: If the SMILES string cannot be interpreted according to the SMILES
        dialect used by `partialsmiles`. The error message includes the index at which
        the parser encountered an invalid character.
    """
    try:
        ps.ParseSmiles(smiles, partial=False)
    except ps.ValenceError:
        pass
    except ps.SMILESSyntaxError as e:
        raise ValidationError(f"Structure is not in SMILES format: {e}")


def validate_molfile_v3000(molfile: str) -> None:
    """Validates that a molfile specifies version V3000.

    Args:
        molfile: The molfile string

    Raises:
        ValidationError: The counts line does not specify V3000.
    """
    try:
        # last 5 non-whitespace chars of the 4th line.
        # page 9, here:  https://www.daylight.com/meetings/mug05/Kappler/ctfile.pdf
        version = molfile.split("\n")[3].strip()[-5:]
        assert version == "V3000"
    except (AssertionError, IndexError):
        raise ValidationError("Structure is not in V3000 format.")


def validate_molfile_v2000(molfile: str) -> None:
    """Validates that a molfile specifies version V2000.

    Args:
        molfile: The molfile string

    Raises:
        ValidationError: The counts line does not specify "V2000"
    """
    try:
        # last 5 non-whitespace chars of the 4th line.
        # page 9, here:  https://www.daylight.com/meetings/mug05/Kappler/ctfile.pdf
        version = molfile.split("\n")[3].strip()[-5:]
        assert version == "V2000"
    except (AssertionError, IndexError):
        raise serializers.ValidationError("Structure is not in V2000 format.")


def validate_molfile_v3000_computable(structure: str) -> None:
    """Validates that the structure can be loaded into Indigo without exception.

    Args:
        structure: the structure string ("molfile_v2000", "smiles")

    Raises:
        ValidationError: If the InChIKey cannot be computed.
    """
    try:
        get_molfile_v3000(structure)
    except IndigoException:
        raise ValidationError("Cannot be converted into a molfile.")


# DEPRECATED -- these need to remain defined for migration 0001


def validate_cid_regex(cid: str) -> None:
    """Validates the general form of the CID.

    Args:
        cid: The CID string

    Raises:
        ValidationError: If the CID cannot be parsed.

    """
    if not re.match(fr"^{compound_settings.PREFIX}CID\d0\d+$", cid):
        raise ValidationError(
            f"Invalid format. Expected {compound_settings.PREFIX}CID$0######."
        )


def validate_cid_checksum(cid: str) -> None:
    """Validates that the CID contains a valid checksum.

    Args:
        cid: The CID string

    Raises:
        ValidationError: If the CID contains an invalid checksum.

    """
    given_checksum = extract_checksum(cid)
    i = extract_int(cid)
    real_checksum = chemreg_checksum(i)
    if not given_checksum == real_checksum:
        raise ValidationError(f"Invalid checksum. Expected {real_checksum}.")
