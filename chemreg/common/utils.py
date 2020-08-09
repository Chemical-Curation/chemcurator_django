from typing import Optional

from crum import get_current_user


def compute_checksum(i: Optional[int]) -> int:
    """Computes the checksum from the compound or substance integer.

    Args:
        i: A compound or substance integer.

    Returns:
        The CID or SID checksum.

    """
    try:
        loci = (x for x in range(1, len(str(i)) + 1))
        vals = (int(x) for x in str(i))
        return sum(x * y for x, y in zip(loci, vals)) % 10
    except ValueError:
        return None


def get_current_user_pk():
    """Retrieve the current user's primary key.

    Returns:
        The primary key of the current request's user.
    """
    current_user = get_current_user()
    if not current_user:
        return None
    return current_user.pk
