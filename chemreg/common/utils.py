from typing import Optional

from crum import get_current_user


def chemreg_checksum(i: Optional[int]) -> int:
    """Computes the checksum from the compound, substance, or record integer.

    Args:
        i: A compound, substance, or record integer.

    Returns:
        The CID, SID, or RID checksum.

    """
    try:
        loci = (x for x in range(1, len(str(i)) + 1))
        vals = (int(x) for x in str(i))
        return sum(x * y for x, y in zip(loci, vals)) % 10
    except ValueError:
        return None


def casrn_checksum(value: Optional[int]) -> int:
    """Computes the checksum from an integer.

    Checksum is the:
     - Reverse of the original integer
     - Each digit multiplied by the index
     - Summed
     - Mod by 10

    789 => (9 * 1) + (8 * 2) + (7 * 3) => 46 % 10 => 6

    Args:
        value (int): A CAS-RN.

    Returns:
        The CAS-RN checksum integer.

    """
    return sum([i * int(x) for i, x in enumerate(str(value)[::-1], 1)]) % 10


def get_current_user_pk():
    """Retrieve the current user's primary key.

    Returns:
        The primary key of the current request's user.
    """
    current_user = get_current_user()
    if not current_user:
        return None
    return current_user.pk
