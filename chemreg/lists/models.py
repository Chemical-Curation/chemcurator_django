from django.db import models

from chemreg.common.models import CommonInfo, ControlledVocabulary
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
        name (str): (Less than 50 character, url safe, unique, required field)
        label (str): (Less than 255 characters, unique, required field)
        short_description (str): String (Less than 1000 characters, required field)
        long_description (str): TEXT (required)

        list_accessibility: (AccessibilityType) (required)
        owners: (A list of users, default current user)
        source_url (str): (Less than 500 characters, optional field)
        source_reference (str): (Less than 500 characters, optional field)
        source_doi (str): (Less than 500 characters, optional field)
        external_contact (ExternalContact): (optional)
        date_of_source_collection (date): (required)
    """

    name = models.SlugField(max_length=49, unique=True)
    label = models.CharField(max_length=255, unique=True, blank=False)
    short_description = models.TextField(max_length=1000, blank=False)
    long_description = models.TextField(blank=False)
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
    date_of_source_collection = models.DateTimeField(editable=False, blank=False)


class ListType(ControlledVocabulary):
    """Controlled vocabulary for List Types

    Attributes:
        name (str): Less than 50 character, url safe, unique, (required)
        label (str): Less than 100 characters, unique, (required)
        short_description (str): Less than 500 characters, (required)
        long_description (str): Text (required)
    """

    pass
