import re

from django.core.cache import cache

import pytest

from chemreg.compound.models import BaseCompound
from chemreg.compound.settings import compound_settings
from chemreg.compound.utils import build_cid, extract_int


@pytest.mark.django_db
def test_build_cid():
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
    BaseCompound.objects.create(id=build_cid(test_i))  # valid CID
    BaseCompound.objects.create(id="FOO8")  # legacy CID
    cid = build_cid()
    assert cid_re.match(cid)
    assert extract_int(cid) == test_i + 1
