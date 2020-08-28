from django.utils.translation import gettext_lazy as _

from chemreg.common.serializers import ControlledVocabSerializer
from chemreg.common.validators import ExternalIdUniqueTogetherValidator
from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.lists.models import (
    AccessibilityType,
    ExternalContact,
    IdentifierType,
    List,
    ListType,
    Record,
    RecordIdentifier,
)
from chemreg.substance.serializers import SubstanceSerializer
from chemreg.users.serializers import UserSerializer


class AccessibilityTypeSerializer(ControlledVocabSerializer):
    """The serializer for Accessibility Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = AccessibilityType


class IdentifierTypeSerializer(ControlledVocabSerializer):
    """The serializer for Identifier Types."""

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


class RecordSerializer(HyperlinkedModelSerializer):
    """The serializer for Records."""

    list = ListSerializer
    substance = SubstanceSerializer

    class Meta:
        model = Record
        fields = [
            "rid",
            "external_id",
            "message",
            "score",
            "is_validated",
            "list",
            "substance",
        ]
        validators = [
            ExternalIdUniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("external_id", "list"),
                message=_(
                    "External IDs must be unique within a list. The External ID submitted is already associated with '{duplicate_field}'"
                ),
                duplicate_field="rid",
            )
        ]


class RecordIdentifierSerializer(HyperlinkedModelSerializer):
    """The serializer for Record Identifiers."""

    record = RecordSerializer
    identifier_type = IdentifierTypeSerializer

    class Meta:
        model = RecordIdentifier
        fields = [
            "record",
            "identifier",
            "identifier_type",
            "identifier_label",
        ]
