import re

from django.core.exceptions import ValidationError
from rest_framework import serializers

import partialsmiles as ps
from indigo import IndigoException

from chemreg.compound.settings import compound_settings
from chemreg.compound.utils import compute_checksum, extract_checksum, extract_int
from chemreg.indigo.inchi import get_inchikey


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


def validate_smiles(smiles: str) -> None:
    """Validates that the SMILES string posted to a defined compound
    is formatted properly

    Args:
        smiles: The SMILES string

    Raises:
        ValidationError: If the SMILES string is not properly formatted
    """
    try:
        ps.ParseSmiles(smiles, partial=False)
    except ps.ValenceError:
        pass
    except ps.SMILESSyntaxError as e:
        raise serializers.ValidationError(e)
