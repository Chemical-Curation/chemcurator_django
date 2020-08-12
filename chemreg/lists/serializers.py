from chemreg.common.serializers import ControlledVocabSerializer
from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.lists.models import (
    AccessibilityType,
    ExternalContact,
    IdentifierType,
    List,
    ListType,
)
from chemreg.users.serializers import UserSerializer


class AccessibilityTypeSerializer(ControlledVocabSerializer):
    """The serializer for Accessibility Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = AccessibilityType


class IdentifierTypeSerializer(ControlledVocabSerializer):
    """The serializer for List Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = IdentifierType


class ExternalContactSerializer(HyperlinkedModelSerializer):
    """The serializer for External Contacts."""

    class Meta:
        model = ExternalContact
        fields = [
            "name",
            "email",
            "phone",
        ]


class ListTypeSerializer(ControlledVocabSerializer):
    """The serializer for List Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = ListType


class ListSerializer(HyperlinkedModelSerializer):
    """The serializer for Lists."""

    list_accessibility = AccessibilityTypeSerializer
    external_contact = ExternalContactSerializer
    owners = UserSerializer(read_only=True, many=True)
    types = ListTypeSerializer

    class Meta:
        model = List
        fields = [
            "name",
            "label",
            "short_description",
            "long_description",
            "list_accessibility",
            "owners",
            "source_url",
            "source_reference",
            "source_doi",
            "external_contact",
            "date_of_source_collection",
            "types",
        ]
