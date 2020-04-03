from crum import get_current_user


def get_current_user_pk():
    """Retrieve the current user's primary key.

    Returns:
        The primary key of the current request's user.
    """
    current_user = get_current_user()
    if not current_user:
        return None
    return current_user.pk
