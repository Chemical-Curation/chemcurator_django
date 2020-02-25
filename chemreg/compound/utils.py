import time

from django.apps import apps
from django.core.cache import cache
from django.db.models import IntegerField, Max
from django.db.models.functions import Cast, Substr

from chemreg.compound.settings import compound_settings


def compute_checksum(i: int) -> int:
    """Computes the checksum from the compound integer.

    Args:
        i: A compound integer.

    Returns:
        The CID checksum.

    """
    return 0


def build_cid(i=None) -> str:
    """Builds a unique CID.

    Args:
        i (int): The compound integer to use. If set to `None`, the integer will be incremented
            from the cache sequence. Defaults to `None`.

    Returns:
        A CID string.

    """
    seq_key = compound_settings.SEQUENCE_KEY
    while i is None:
        try:
            i = cache.incr(seq_key)
        except ValueError:
            # The sequence is down. Let's try to set it.
            if cache.add(seq_key + ".lock", None, timeout=5):
                prefix = compound_settings.PREFIX
                incr_start = compound_settings.INCREMENT_START
                try:
                    BaseCompound = apps.get_model("compound", "BaseCompound")
                    last_id = BaseCompound.objects.filter(
                        cid__regex=fr"^{prefix}CID\d0([2-9]\d{{6}}|[1-9]\d{{7,}})$"
                    ).aggregate(
                        max_cid=Max(
                            Cast(
                                Substr("cid", len(prefix) + 5),
                                output_field=IntegerField(),
                            )
                        )
                    ).get(
                        "max_cid"
                    ) or (
                        incr_start - 1
                    )
                    cache.add(
                        seq_key, last_id, timeout=(365 * 24 * 60 * 60),
                    )
                finally:
                    cache.delete(seq_key + ".lock")
            time.sleep(0.01)

    checksum = compute_checksum(i)
    return f"{compound_settings.PREFIX}CID{checksum}0{i}"


def extract_int(cid: str) -> int:
    """Extracts the compound integer from the CID.

    Args:
        cid: A CID string.

    Returns:
        The compound integer.

    """
    meta = f"{compound_settings.PREFIX}CID$0"
    try:
        return int(cid[len(meta) :])
    except ValueError:
        return None


def extract_checksum(cid: str) -> int:
    """Extracts the compound checksum from the CID.

    Args:
        cid: A CID string.

    Returns:
        The compound checksum.

    """
    meta = f"{compound_settings.PREFIX}CID"
    try:
        return int(cid[len(meta)])
    except ValueError:
        return None
