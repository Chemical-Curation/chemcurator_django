import pytest

from chemreg.compound.models import DefinedCompound
from chemreg.compound.serializers import DefinedCompoundSerializer
from chemreg.compound.settings import compound_settings
from chemreg.compound.tests.factories import (
    DefinedCompoundFactory,
    DefinedCompoundJSONFactory,
)

COMPOUND_REGISTRY = {
    "DefinedCompound": {
        "factory": DefinedCompoundFactory,
        "json_factory": DefinedCompoundJSONFactory,
        "model": DefinedCompound,
        "serializer": DefinedCompoundSerializer,
    }
}


@pytest.fixture(params=COMPOUND_REGISTRY.keys())
def compound(request):
    """The registry entry for all subclasses of `BaseCompound`."""
    return COMPOUND_REGISTRY[request.param]


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


INVALID_INCHIKEYS = [
    f"{'A'*13}-{'A'*10}-{'A'*1}",  # wrong character count - 0
    f"{'A'*14}-{'A'*7}-{'A'*1}",  # wrong character count - 1
    f"{'A'*14}-{'A'*10}-{'A'*2}",  # wrong character count - 2
    f"{'A'*14}-{'A'*10}{'A'*1}",  # missing dash - 0
    f"{'A'*14}{'A'*10}-{'A'*1}",  # missing dash - 1
    f"{'1'*14}{'A'*10}-{'A'*1}",  # numbers not letters - 0
    f"{'A'*14}{'1'*10}-{'A'*1}",  # numbers not letters - 1
    f"{'A'*14}{'A'*10}-{'1'*1}",  # numbers not letters - 2
    f"{'a'*14}{'A'*10}-{'A'*1}",  # lowercase - 0
    f"{'A'*14}{'a'*10}-{'A'*1}",  # lowercase - 1
    f"{'A'*14}{'A'*10}-{'a'*1}",  # lowercase - 2
]
"""A collection of invalid InchiKeys."""


@pytest.fixture(params=INVALID_INCHIKEYS)
def invalid_inchikey(request) -> str:
    """An invalid InchiKey string."""
    return request.param
