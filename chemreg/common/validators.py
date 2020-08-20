import re

from rest_framework.exceptions import ValidationError

from chemreg.common.utils import casrn_checksum


def validate_deprecated(vocab):
    """Validates that the ControlledVocabulary is not deprecated.

    Args:
        vocab: the ControlledVocabulary object ("QueryStructureType", "SubstanceType")

    Raises:
        ValidationError: If the vocab is deprecated.
    """
    if vocab.deprecated:
        raise ValidationError(
            f"The {vocab._meta.object_name} submitted is no longer supported."
        )
    return vocab


def validate_casrn_checksum(value):
    """ Validates a CAS-RN's checksum value

    https://en.wikipedia.org/wiki/CAS_Registry_Number#Format

    Args:
        value (str): A formatted CAS-RN string.
            Format should be 2-7 digits hyphen 2 digits hyphen 1 digit.
            The last digit is a checksum of the previous digits.
            For example water is 7732-18-5.
            (8×1 + 1×2 + 2×3 + 3×4 + 7×5 + 7×6) = 105
            105 % 10 = 5

    Raises:
        ValidationError: The provided checksum is invalid

    """
    value_stripped = re.sub("[^0-9]", "", value)  # Strip all non-digits
    if value_stripped and int(value_stripped[-1]) != casrn_checksum(
        int(value_stripped[:-1])
    ):
        raise ValidationError(
            "Provided CAS-RN does not meet checksum requirements.", "checksum"
        )


def validate_is_regex(value):
    """ Validates a string is valid re regex

    https://docs.python.org/3/library/re.html#regular-expression-syntax

    Args:
        value (str): A valid regex string

    Raises:
        ValidationError: The provided RegExp is invalid
    """
    try:
        re.compile(value)
    except re.error:
        raise ValidationError("The provided RegExp is invalid")
