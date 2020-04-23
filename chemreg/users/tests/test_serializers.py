import pytest

from chemreg.users.serializers import UserSerializer


@pytest.mark.django_db
def test_user_fields(user_factory):
    user = user_factory.build()
    serializer = UserSerializer(user)
    for k in ["username", "first_name", "last_name", "email", "is_superuser"]:
        assert k in serializer.data.keys()
