import re

from django.core.cache import cache

import pytest

from chemreg.lists.settings import record_settings
from chemreg.lists.tests.factories import RecordFactory
from chemreg.lists.utils import build_rid, extract_int


@pytest.mark.django_db
def test_build_rid():
    rid_re = re.compile(
        fr"^{record_settings.PREFIX}RID\d0([2-9]\d{{6}}|[1-9]\d{{7,}})$"
    )
    # Nothing in database, sequence unset
    cache.delete(record_settings.SEQUENCE_KEY)
    cache.delete(record_settings.SEQUENCE_KEY + ".lock")
    rid = build_rid()
    assert rid_re.match(rid)
    assert extract_int(rid) == record_settings.INCREMENT_START
    # Nothing in database, sequence set
    rid = build_rid()
    assert rid_re.match(rid)
    assert extract_int(rid) == record_settings.INCREMENT_START + 1
    # Substance in database, sequence unset
    cache.delete(record_settings.SEQUENCE_KEY)
    cache.delete(record_settings.SEQUENCE_KEY + ".lock")
    test_i = 2345678
    RecordFactory(id=build_rid(test_i),)  # valid rid
    RecordFactory(id="FOO8")  # legacy rid
    rid = build_rid()
    assert rid_re.match(rid)
    assert extract_int(rid) == test_i + 1
