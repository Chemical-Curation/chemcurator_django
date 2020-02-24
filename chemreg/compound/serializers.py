from rest_framework import serializers

from chemreg.compound.models import BaseCompound, DefinedCompound


class BaseCompoundSerializer(serializers.ModelSerializer):
    """The base class for serializing compounds."""

    id = serializers.CharField(
        source="cid", validators=BaseCompound._meta.get_field("cid").validators
    )

    class Meta:
        model = BaseCompound
        fields = ("id", "structure")


class DefinedCompoundSerializer(BaseCompoundSerializer):
    """The serializer for defined compounds."""

    class Meta:
        model = DefinedCompound
        fields = ("id", "molefile", "inchikey")
