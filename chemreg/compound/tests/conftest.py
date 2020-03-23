import pytest

from chemreg.compound.models import (
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.serializers import (
    DefinedCompoundSerializer,
    IllDefinedCompoundSerializer,
    QueryStructureTypeSerializer,
)
from chemreg.compound.settings import compound_settings
from chemreg.compound.tests.factories import (
    DefinedCompoundFactory,
    DefinedCompoundJSONFactory,
    IllDefinedCompoundFactory,
    IllDefinedCompoundJSONFactory,
    QueryStructureTypeFactory,
    QueryStructureTypeJSONFactory,
)

COMPOUND_REGISTRY = {
    "DefinedCompound": {
        "factory": DefinedCompoundFactory,
        "json_factory": DefinedCompoundJSONFactory,
        "model": DefinedCompound,
        "serializer": DefinedCompoundSerializer,
    },
    "IllDefinedCompound": {
        "factory": IllDefinedCompoundFactory,
        "json_factory": IllDefinedCompoundJSONFactory,
        "model": IllDefinedCompound,
        "serializer": IllDefinedCompoundSerializer,
    },
}

QUERY_STRUCTURE_TYPE_REGISTRY = {
    "QueryStructureType": {
        "factory": QueryStructureTypeFactory,
        "json_factory": QueryStructureTypeJSONFactory,
        "model": QueryStructureType,
        "serializer": QueryStructureTypeSerializer,
    },
}


@pytest.fixture(params=QUERY_STRUCTURE_TYPE_REGISTRY.keys())
def query_structure_type(request):
    """The registry entry for the `QueryStructureType`."""
    return QUERY_STRUCTURE_TYPE_REGISTRY[request.param]


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


MRVFILES = [
    '<cml><MDocument><MChemicalStruct><molecule molID="m1"><atomArray><atom id="a1" elementType="C" x2="-1.1102230246251565e-16" y2="0"/><atom id="a2" elementType="O" x2="1.54" y2="1.1102230246251565e-16" lonePair="2"/></atomArray><bondArray><bond atomRefs2="a1 a2" order="2" id="b1"/></bondArray></molecule></MChemicalStruct><MElectronContainer occupation="0 0" radical="0" id="o1"><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/></MElectronContainer><MElectronContainer occupation="0 0" radical="0" id="o2"><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/><MElectron atomRefs="m1.a2" difLoc="0.0 0.0 0.0"/></MElectronContainer></MDocument></cml>',
]


@pytest.fixture(params=MRVFILES)
def mrvfile(request) -> str:
    """A valid mrvfile."""
    return request.param
