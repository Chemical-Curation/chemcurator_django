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
