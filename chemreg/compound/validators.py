import re

from django.core.exceptions import ValidationError

from chemreg.compound.settings import compound_settings
from chemreg.compound.utils import compute_checksum, extract_checksum, extract_int


def validate_cid_prefix(cid: str) -> None:
    """Validates that the CID begins with a valid prefix.

    Args:
        cid: The CID string

    Raises:
        ValidationError: If the CID does not have a valid prefix.

    """
    if not cid.startswith(compound_settings.PREFIX):
        raise ValidationError(
            f"Invalid prefix. Expected {compound_settings.PREFIX}CID$0######."
        )


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
