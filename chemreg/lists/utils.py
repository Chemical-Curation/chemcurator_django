import time
from typing import Optional

from django.apps import apps
from django.core.cache import cache
from django.db.models import IntegerField, Max
from django.db.models.functions import Cast, Substr

from chemreg.common.utils import chemreg_checksum
from chemreg.lists.settings import record_settings


def build_rid(i=None) -> str:
    """Builds a unique RID.

    Args:
        i (int): The record integer to use. If set to `None`, the integer will be incremented
            from the cache sequence. Defaults to `None`.

    Returns:
        A RID string.

    """
    seq_key = record_settings.SEQUENCE_KEY
    while i is None:
        try:
            i = cache.incr(seq_key)
        except ValueError:
            # The sequence is down. Let's try to set it.
            if cache.add(seq_key + ".lock", None, timeout=5):
                prefix = record_settings.PREFIX
                incr_start = record_settings.INCREMENT_START
                try:
                    Record = apps.get_model("lists", "Record")
                    last_id = Record.objects.filter(
                        rid__regex=fr"^{prefix}RID\d0([2-9]\d{{6}}|[1-9]\d{{7,}})$"
                    ).aggregate(
                        max_rid=Max(
                            Cast(
                                Substr("rid", len(prefix) + 5),
                                output_field=IntegerField(),
                            )
                        )
                    ).get(
                        "max_rid"
                    ) or (
                        incr_start - 1
                    )
                    cache.add(seq_key, last_id, timeout=(365 * 24 * 60 * 60))
                finally:
                    cache.delete(seq_key + ".lock")
            time.sleep(0.01)

    checksum = chemreg_checksum(i)
    return f"{record_settings.PREFIX}RID{checksum}0{i}"


def extract_int(rid: str) -> Optional[int]:
    """Extracts the record integer from the RID.

    Args:
        rid: A RID string.

    Returns:
        The record integer.

    """
    meta = f"{record_settings.PREFIX}RID$0"
    try:
        return int(rid[len(meta) :])
    except ValueError:
        return None
