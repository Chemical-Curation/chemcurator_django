from django.db import models
from django.utils.functional import cached_property

from indigo import Indigo, IndigoException
from polymorphic.models import PolymorphicModel

from chemreg.common.models import CommonInfo
from chemreg.compound.fields import StructureAliasField
from chemreg.compound.utils import build_cid
from chemreg.compound.validators import (
    validate_inchikey_computable,
    validate_molfile_v3000,
)
from chemreg.indigo.inchi import get_inchikey


class BaseCompound(CommonInfo, PolymorphicModel):
    """The base class for compounds.

    This model shouldn't exist on it's own. It will always be subclassed
    by a concrete compound. The `chemreg.compound.fields.StructureAliasField`
    can be used to reference the `structure` field on subclassed models. This
    field can then have a more sensible name and varied validation logic
    applied to it.

    Attributes:
        cid (str): The compound CID.
        structure (str): Definitive structure string

    """

    cid = models.CharField(default=build_cid, max_length=50, unique=True)
    structure = models.TextField()


class DefinedCompound(BaseCompound):
    """A defined compound.

    Attributes:
        molfile_v3000 (str): A v3000 molfile. Alias to definitive structure string.
        inchikey (str): A hashed key based off of the chemical structure.

    """

    molfile_v3000 = StructureAliasField(
        validators=[validate_molfile_v3000, validate_inchikey_computable]
    )
    inchikey = models.CharField(null=True, max_length=29)

    @property
    def _inchikey(self):
        """Computes the inchikey from the molfile."""
        try:
            return get_inchikey(self.molfile_v3000)
        except IndigoException:
            return None

    @cached_property
    def indigo_structure(self):
        indigo = Indigo()
        indigo.setOption("molfile-saving-mode", "3000")
        return indigo.loadStructure(structureStr=self.molfile_v3000)


class QueryStructureType(CommonInfo):
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
    )
    label = models.CharField(
        max_length=99,
        verbose_name="label",
        help_text="Query structure type label",
        unique=True,
    )
    short_description = models.CharField(
        max_length=499,
        verbose_name="short description",
        help_text="Query structure type short description",
    )
    long_description = models.TextField(
        verbose_name="long description",
        help_text="Query structure type long description",
    )

    def __str__(self):
        return self.label


def get_illdefined_qst():
    """Default value for `IllDefinedCompound.query_structure_type`.

    This object is created in a data migration. Calling `get_or_create` here will
    cause migrations to fail if `QueryStructureType` has been modified: the new model
    would be used to create the model prior to new columns made in the database.
    """
    return QueryStructureType.objects.get(name="ill-defined").pk


class IllDefinedCompound(BaseCompound):
    """An ill-defined compound.

    Attributes:
        mrvfile (str): Alias to definitive structure string.
        query_structure_type (foreign key): A foreign key to the "ill-defined" record in the "query structure type"
         controlled vocabulary

    """

    mrvfile = StructureAliasField()
    query_structure_type = models.ForeignKey(
        "QueryStructureType", on_delete=models.PROTECT, default=get_illdefined_qst
    )

    class Meta:
        verbose_name = "ill-defined compound"
