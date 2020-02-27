from django.db import models

from polymorphic.models import PolymorphicModel

from chemreg.common.models import CommonInfo
from chemreg.compound.fields import StructureAliasField
from chemreg.compound.utils import build_cid
from chemreg.compound.validators import (
    validate_cid_checksum,
    validate_cid_prefix,
    validate_cid_regex,
    validate_inchikey_regex,
)

import re
from django.template.defaultfilters import slugify


class BaseCompound(CommonInfo, PolymorphicModel):
    """The base class for compounds.

    This model shouldn't exist on it's own. It will always be subclassed
    by a concrete compound. The `chemreg.compound.fields.StructureAliasField`
    can be used to reference the `structure` field on subclassed models. This
    field can then have a more sesnsible name and varied validation logic
    applied to it.

    Attributes:
        cid (str): The compound CID.
        structure (str): Definitive structure string

    """

    cid = models.CharField(
        default=build_cid,
        max_length=50,
        unique=True,
        validators=[validate_cid_prefix, validate_cid_regex, validate_cid_checksum],
    )
    structure = models.TextField()


class DefinedCompound(BaseCompound):
    """A defined compound.

    Attributes:
        molefile (str): A v3000 molefile. Alias to definitive structure string.
        inchikey (str): A hashed key based off of the chemical structure.

    """

    molefile = StructureAliasField()
    inchikey = models.CharField(max_length=29, validators=[validate_inchikey_regex])


class QueryStructureType(models.Model):
    """A controlled vocabulary

    Attributes:
    Name = String (Less than 50 character, url safe, unique, required field)
    Label = String (Less than 100 characters, unique, required field)
    Short Description = String (Less than 500 characters, required field)
    Long Description = TEXT (required field)
    """

    name = models.SlugField(
        max_length=49,
        verbose_name="name",
        help_text="Query structure type name",
        unique=True,
        blank=False,
    )
    label = models.CharField(
        max_length=99,
        verbose_name="label",
        help_text="Query structure type label",
        unique=True,
        blank=False,
    )
    short_description = models.CharField(
        max_length=499,
        verbose_name="short description",
        help_text="Query structure type short description",
        blank=False,
    )
    long_description = models.TextField(
        verbose_name="long description",
        help_text="Query structure type long description",
        blank=False,
    )

    def __str__(self):
        return self.label

    # from chemreg.compound.models import QueryStructureType
    # qst=QueryStructureType(name="$ slug",label="a label",short_description="something short",long_description="much longer" * 20)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name, "name")
        super(QueryStructureType, self).save()


def unique_slugify(
    instance, value, slug_field_name="slug", queryset=None, slug_separator="-"
):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = "%s%s" % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[: slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = "%s%s" % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator="-"):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ""
    if separator == "-" or not separator:
        re_sep = "-"
    else:
        re_sep = "(?:-|%s)" % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub("%s+" % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != "-":
            re_sep = re.escape(separator)
        value = re.sub(r"^%s+|%s+$" % (re_sep, re_sep), "", value)
    return value
