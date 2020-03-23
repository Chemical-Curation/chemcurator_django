import re

from django.core.cache import cache
from django.db import models

import pytest
from polymorphic.models import PolymorphicModel

from chemreg.compound.fields import StructureAliasField
from chemreg.compound.models import BaseCompound, DefinedCompound
from chemreg.compound.settings import compound_settings
from chemreg.compound.tests.factories import BaseCompoundFactory
from chemreg.compound.tests.fakers import MolfileFaker
from chemreg.compound.utils import build_cid, extract_int
from chemreg.compound.validators import (
    validate_cid_checksum,
    validate_cid_regex,
    validate_inchikey_computable,
)


def test_compound_attr():
    """Test basic attributes of the `BaseCompound` model."""
    assert issubclass(BaseCompound, PolymorphicModel)
    assert hasattr(BaseCompound, "cid")
    assert hasattr(BaseCompound, "structure")
    cid = BaseCompound._meta.get_field("cid")
    structure = BaseCompound._meta.get_field("structure")
    assert isinstance(cid, models.CharField)
    assert cid.default == build_cid
    assert cid.max_length == 50
    assert cid.unique
    assert validate_cid_checksum in cid.validators
    assert validate_cid_regex in cid.validators
    assert isinstance(structure, models.TextField)


def test_definedcompound_attr():
    """Test basic attributes of the `DefinedCompound` model."""
    assert issubclass(DefinedCompound, BaseCompound)
    molfile = DefinedCompound._meta.get_field("molfile")
    inchikey = DefinedCompound._meta.get_field("inchikey")
    assert isinstance(molfile, StructureAliasField)
    assert isinstance(inchikey, models.CharField)
    assert inchikey.max_length == 29
    assert validate_inchikey_computable in molfile.validators


@pytest.mark.parametrize("molfile", MolfileFaker.molfiles)
def test_definedcompound_inchikey(molfile):
    """Test inchikey calculation of the `DefinedCompound` model."""
    compound = DefinedCompound(molfile=molfile)
    assert re.match(r"^[A-Z]{14}-[A-Z]{10}-[A-Z]$", compound.inchikey)


@pytest.mark.django_db
def test_build_cid():
    """Test that the cache increment CID works."""
    cid_re = re.compile(
        fr"^{compound_settings.PREFIX}CID\d0([2-9]\d{{6}}|[1-9]\d{{7,}})$"
    )
    # Nothing in database, sequence unset
    cache.delete(compound_settings.SEQUENCE_KEY)
    cache.delete(compound_settings.SEQUENCE_KEY + ".lock")
    cid = build_cid()
    assert cid_re.match(cid)
    assert extract_int(cid) == compound_settings.INCREMENT_START
    # Nothing in database, sequence set
    cid = build_cid()
    assert cid_re.match(cid)
    assert extract_int(cid) == compound_settings.INCREMENT_START + 1
    # Compound in database, sequence unset
    cache.delete(compound_settings.SEQUENCE_KEY)
    cache.delete(compound_settings.SEQUENCE_KEY + ".lock")
    test_i = 2345678
    BaseCompoundFactory(cid=build_cid(test_i))  # valid CID
    BaseCompoundFactory(cid="FOO8")  # invalid (legacy) CID
    cid = build_cid()
    assert cid_re.match(cid)
    assert extract_int(cid) == test_i + 1
