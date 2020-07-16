import time
from typing import Optional

from django.apps import apps
from django.core.cache import cache
from django.db.models import IntegerField, Max
from django.db.models.functions import Cast, Substr

from chemreg.common.utils import compute_checksum
from chemreg.substance.settings import substance_settings


def build_sid(i=None) -> str:
    """Builds a unique SID.

    Args:
        i (int): The substance integer to use. If set to `None`, the integer will be incremented
            from the cache sequence. Defaults to `None`.

    Returns:
        A SID string.

    """
    seq_key = substance_settings.SEQUENCE_KEY
    while i is None:
        try:
            i = cache.incr(seq_key)
        except ValueError:
            # The sequence is down. Let's try to set it.
            if cache.add(seq_key + ".lock", None, timeout=5):
                prefix = substance_settings.PREFIX
                incr_start = substance_settings.INCREMENT_START
                try:
                    Substance = apps.get_model("substance", "Substance")
                    last_id = Substance.objects.filter(
                        sid__regex=fr"^{prefix}SID\d0([2-9]\d{{6}}|[1-9]\d{{7,}})$"
                    ).aggregate(
                        max_sid=Max(
                            Cast(
                                Substr("sid", len(prefix) + 5),
                                output_field=IntegerField(),
                            )
                        )
                    ).get(
                        "max_sid"
                    ) or (
                        incr_start - 1
                    )
                    cache.add(seq_key, last_id, timeout=(365 * 24 * 60 * 60))
                finally:
                    cache.delete(seq_key + ".lock")
            time.sleep(0.01)

    checksum = compute_checksum(i)
    return f"{substance_settings.PREFIX}SID{checksum}0{i}"


def extract_int(sid: str) -> Optional[int]:
    """Extracts the compound integer from the SID.

    Args:
        sid: A SID string.

    Returns:
        The substance integer.

    """
    meta = f"{substance_settings.PREFIX}SID$0"
    try:
        return int(sid[len(meta) :])
    except ValueError:
        return None
