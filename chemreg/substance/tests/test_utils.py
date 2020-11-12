import re

from django.core.cache import cache

import pytest

from chemreg.substance.settings import substance_settings
from chemreg.substance.tests.factories import SubstanceFactory
from chemreg.substance.utils import build_sid, extract_int


@pytest.mark.django_db
def test_build_sid():
    sid_re = re.compile(
        fr"^{substance_settings.PREFIX}SID\d0([2-9]\d{{6}}|[1-9]\d{{7,}})$"
    )
    # Nothing in database, sequence unset
    cache.delete(substance_settings.SEQUENCE_KEY)
    cache.delete(substance_settings.SEQUENCE_KEY + ".lock")
    sid = build_sid()
    assert sid_re.match(sid)
    assert extract_int(sid) == substance_settings.INCREMENT_START
    # Nothing in database, sequence set
    sid = build_sid()
    assert sid_re.match(sid)
    assert extract_int(sid) == substance_settings.INCREMENT_START + 1
    # Substance in database, sequence unset
    cache.delete(substance_settings.SEQUENCE_KEY)
    cache.delete(substance_settings.SEQUENCE_KEY + ".lock")
    test_i = 2345678
    SubstanceFactory(id=build_sid(test_i),)  # valid SID
    SubstanceFactory(id="FOO8")  # legacy SID
    sid = build_sid()
    assert sid_re.match(sid)
    assert extract_int(sid) == test_i + 1
