from django.db import models

from chemreg.common.models import CommonInfo, ControlledVocabulary, HTMLTextField
from chemreg.lists.utils import build_rid
from chemreg.users.models import User


class AccessibilityType(ControlledVocabulary):
    """Controlled vocabulary for Accessibility Types

    Attributes:
        name (str): Less than 50 character, url safe, unique (required)
        label (str): Less than 100 characters, unique (required)
        short_description (str): Less than 500 characters (required)
        long_description (str): Text (required)
    """

    pass


class IdentifierType(ControlledVocabulary):
    """Controlled vocabulary for Identifier Types

    Attributes:
        name (str): Less than 50 character, url safe, unique (required)
        label (str): Less than 100 characters, unique (required)
        short_description (str): Less than 500 characters (required)
        long_description (str): Text (required)
    """

    pass


class ExternalContact(CommonInfo):
    """External Contact Information

    Attributes:
        name (str): (Less than 49 characters, unique, required)
        email (str): (Less than 49 characters, unique, required)
        phone (str): (Less than 15 characters, unique, required)
    """

    name = models.CharField(max_length=49, unique=True, blank=False)
    email = models.CharField(max_length=49, unique=True, blank=False)
    phone = models.CharField(max_length=15, unique=True, blank=False)


class List(CommonInfo):
    """List Model Definition

    Attributes:
        name (str): Less than 50 character, url safe, unique
        label (str): Less than 255 characters, unique
        short_description (str): HTML Sanitized description with a 1000 char length limit
        long_description (str): HTML Sanitized description with a large length limit
        list_accessibility (AccessibilityType): An Accessibility Type model instance
        owners (many-to-many): A list of users, default current user
        source_url (str, optional): Less than 500 characters
        source_reference (str, optional): Less than 500 characters
        source_doi (str, optional): Less than 500 characters
        external_contact (ExternalContact, optional): A External Contact model instance
        date_of_source_collection (date): Date that this information was collected
        types (many-to-many, optional): Linkage between List and ListType Models
    """

    name = models.SlugField(max_length=49, unique=True)
    label = models.CharField(max_length=255, unique=True, blank=False)
    short_description = HTMLTextField(max_length=1000, blank=False)
    long_description = HTMLTextField(blank=False)
    list_accessibility = models.ForeignKey(
        "AccessibilityType", on_delete=models.PROTECT, null=False
    )
    owners = models.ManyToManyField(User)
    source_url = models.CharField(max_length=500, blank=True)
    source_reference = models.CharField(max_length=500, blank=True)
    source_doi = models.CharField(max_length=500, blank=True)
    external_contact = models.ForeignKey(
        "ExternalContact", on_delete=models.PROTECT, null=True
    )
    date_of_source_collection = models.DateTimeField(blank=False)
    types = models.ManyToManyField("ListType", blank=True, related_name="lists")


class ListType(ControlledVocabulary):
    """Controlled vocabulary for List Types

    Attributes:
        name (str): Less than 50 character, url safe, unique, (required)
        label (str): Less than 100 characters, unique, (required)
        short_description (str): Less than 500 characters, (required)
        long_description (str): Text (required)
    """

    pass


class Record(CommonInfo):
    """Store all the identifiers associated with a member of a List

    Attributes:
        id (str): Generated ID starting with DTXRID.  Contains a checksum
        external_id (str): ID for external use
        list (foreign key): Foreign Key reference to a List (one to many)
        substance (foreign key, optional): Foreign Key reference to a Substance (one to many)
        score (float, optional): Score of this Record
        message (str, optional): Message describing this Record
        is_validated (bool): Boolean of this Record's validity
    """

    id = models.CharField(
        default=build_rid, primary_key=True, max_length=50, unique=True
    )
    external_id = models.CharField(max_length=500, blank=False)
    message = models.CharField(max_length=500, blank=True)
    score = models.FloatField(null=True)
    is_validated = models.BooleanField()
    list = models.ForeignKey("List", on_delete=models.PROTECT)
    substance = models.ForeignKey(
        "substance.Substance", on_delete=models.PROTECT, null=True
    )

    class Meta:
        ordering = ["pk"]
        constraints = [
            models.UniqueConstraint(
                fields=["external_id", "list"], name="unique_external_id"
            )
        ]


class RecordIdentifier(CommonInfo):
    """Store all the identifiers associated with a member of a Source List

    Attributes:
        record (Record): (required)
        identifier (text): (required)
        identifier_type (IdentifierType): (optional)
        identifier_label (str): (Less than 100 characters, required)
    """

    record = models.ForeignKey(
        "Record", on_delete=models.PROTECT, null=False, related_name="identifiers",
    )
    identifier = models.TextField(blank=False)
    identifier_type = models.ForeignKey(
        "IdentifierType", on_delete=models.PROTECT, null=True
    )
    identifier_label = models.CharField(max_length=100, blank=False)
