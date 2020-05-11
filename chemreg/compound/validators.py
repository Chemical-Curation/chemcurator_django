import re

from django.apps import apps
from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError

import partialsmiles as ps
from indigo import IndigoException

from chemreg.compound.settings import compound_settings
from chemreg.compound.utils import compute_checksum, extract_checksum, extract_int
from chemreg.indigo.inchi import get_inchikey, load_structure


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
    real_checksum = compute_checksum(i)
    if not given_checksum == real_checksum:
        raise ValidationError(f"Invalid checksum. Expected {real_checksum}.")


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


def validate_inchikey_unique(molfile: str) -> None:
    """Validates that an InChIKey computed from the provided molfile is unique.

    Typically, we'd use unique=True to enforce this at the database level, however,
    sometimes a non-unique inchikey can exist. An admin must verify this is allowed.

    Args:
        molfile: The molfile string

    Raises:
        ValidationError: If the InChIKey is not unique.
    """
    DefinedCompound = apps.get_model("compound", "DefinedCompound")
    try:
        inchikey = get_inchikey(molfile)
        qs = DefinedCompound.objects.filter(inchikey=inchikey)
        if qs.exists():
            msg = f"InChIKey already exists.\nConflicting compound ID: {qs.last().pk}"
            raise serializers.ValidationError({"inchikey": msg})
    except IndigoException:
        pass


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
        message = f"The SMILES string cannot be converted to a molfile.\n {e}"
        raise ParseError({"smiles": message})


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
        raise serializers.ValidationError(
            {
                "molfile_v3000": "Molfile format is invalid. Molfile v2000 format expected."
            }
        )


def validate_single_structure(structures) -> None:
    """Validates that the initial JSON data for a defined compound
    only includes data in one of the fields that can be used for
    structure.

    Args:
        structures: the list of populated structure fields
        other than molfile_v3000 passed from the serializer

    Raises:
        ValidationError: Too many potential structures provided.
    """
    try:
        alt_structure_keys = ["molfile_v3000", "molfile_v2000", "smiles"]
        matched = [x for x in alt_structure_keys if x in structures]
        assert len(matched) == 1
    except AssertionError:
        raise serializers.ValidationError(
            {
                "molfile_v3000": f"The data includes too many potential non-V3000 molfile structures in {matched}."
            }
        )


def validate_structure(structure: str) -> None:
    """Validates that the structure can be loaded into Indigo
    without exception.

    Args:
        structure: the structure string ("molfile_v2000", "smiles")

    Raises:
        ValidationError: The error thrown by Indigo.
    """
    try:
        load_structure(structure)
    except IndigoException as e:
        raise ValidationError({"molfile_v3000": e})
