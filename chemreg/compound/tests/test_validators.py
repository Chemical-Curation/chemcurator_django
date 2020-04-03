from django.core.exceptions import ValidationError

import pytest

from chemreg.compound.settings import compound_settings
from chemreg.compound.validators import (
    validate_cid_checksum,
    validate_cid_regex,
    validate_inchikey_computable,
)

VALIDATOR_DICTS = [
    {
        "validator": validate_cid_regex,
        "invalid": [
            f"FOO{compound_settings.PREFIX}CID000",  # invalid prefix
            f"{compound_settings.PREFIX}CID00",  # does not have ID
            f"{compound_settings.PREFIX}CDI000",  # malformed meta text
            f"{compound_settings.PREFIX}CID090",  # incorrect checksum separator
            f"{compound_settings.PREFIX}CIDA00",  # non-integer checksum
            f"{compound_settings.PREFIX}CID00A",  # non-integer ID
        ],
        "msg": f"Invalid format. Expected {compound_settings.PREFIX}CID$0######.",
    },
    {
        "validator": validate_cid_checksum,
        "invalid": [f"{compound_settings.PREFIX}CID00123"],
        "msg": "Invalid checksum. Expected 4.",
    },
    {
        "validator": validate_inchikey_computable,
        "invalid": ["foobar"],
        "msg": "InChIKey not computable for provided structure.",
    },
]


@pytest.fixture(params=VALIDATOR_DICTS)
def validator_dict(request) -> str:
    """A dictionary with a validator, invalid inputs, and the expected error message."""
    return request.param


def test_validators(validator_dict):
    """Test that all validators return expected errors."""
    validator = validator_dict["validator"]
    msg = validator_dict["msg"]
    for invalid in validator_dict["invalid"]:
        with pytest.raises(ValidationError) as excinfo:
            validator(invalid)
        assert msg in str(excinfo.value)
