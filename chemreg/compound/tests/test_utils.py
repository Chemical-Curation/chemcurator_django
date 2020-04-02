import re
from random import randint

from django.core.cache import cache

import pytest

from chemreg.compound.models import BaseCompound
from chemreg.compound.settings import compound_settings
from chemreg.compound.utils import build_cid, compute_checksum, extract_int


def test_compute_checksum():
    i = randint(2000000, 9999999)
    computed = (
        (1 * int(str(i)[0]))
        + (2 * int(str(i)[1]))
        + (3 * int(str(i)[2]))
        + (4 * int(str(i)[3]))
        + (5 * int(str(i)[4]))
        + (6 * int(str(i)[5]))
        + (7 * int(str(i)[6]))
    ) % 10
    checksum = compute_checksum(i)
    assert computed == checksum
    assert 0 <= checksum < 10


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
    BaseCompound.objects.create(cid=build_cid(test_i))  # valid CID
    BaseCompound.objects.create(cid="FOO8")  # legacy CID
    cid = build_cid()
    assert cid_re.match(cid)
    assert extract_int(cid) == test_i + 1
