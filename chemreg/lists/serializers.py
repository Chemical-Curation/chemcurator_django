from chemreg.common.serializers import ControlledVocabSerializer
from chemreg.lists.models import AccessibilityType, IdentifierType, ListType


class ListTypeSerializer(ControlledVocabSerializer):
    """The serializer for List Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = ListType


class AccessibilityTypeSerializer(ControlledVocabSerializer):
    """The serializer for Accessibility Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = AccessibilityType


class IdentifierTypeSerializer(ControlledVocabSerializer):
    """The serializer for List Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = IdentifierType
