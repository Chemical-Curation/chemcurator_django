import factory
import pytest

from chemreg.compound.models import BaseCompound
from chemreg.compound.settings import compound_settings
from chemreg.compound.tests.factories import BaseCompoundFactory


@pytest.fixture
def basecompound() -> BaseCompound:
    """A manufactured BaseCompound model."""
    return BaseCompoundFactory.build()


@pytest.fixture
def basecompound_json() -> dict:
    """A manufactured BaseCompound JSON."""
    d = factory.build(dict, FACTORY_CLASS=BaseCompoundFactory)
    d["id"] = d.pop("cid")
    return d


INVALID_CIDS = [
    "FOOCID000",  # bad prefix
    f"{compound_settings.PREFIX}CID00",  # does not have ID
    f"{compound_settings.PREFIX}CDI000",  # malformed meta text
    f"{compound_settings.PREFIX}CID090",  # incorrect checksum separator
    f"{compound_settings.PREFIX}CIDA00",  # non-integer checksum
    f"{compound_settings.PREFIX}CID00A",  # non-integer ID
    f"{compound_settings.PREFIX}CID900",  # bad checksum
]
"""A collection of invalid CIDs."""


@pytest.fixture(params=INVALID_CIDS)
def invalid_cid(request) -> str:
    """An invalid CID."""
    return request.param
