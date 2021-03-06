from rest_framework import serializers

from chemreg.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """The serializer for `User`."""

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_superuser"]
        read_only_fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
        ]
        extra_kwargs = {field: {"default": "", "read_only": True} for field in fields}
