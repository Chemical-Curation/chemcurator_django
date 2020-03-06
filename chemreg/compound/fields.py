from django.apps import apps
from django.db import models
from django.db.models.query_utils import DeferredAttribute


class StructureDescriptor(DeferredAttribute):
    """Sets both Compound.structure and SubCompound.StructureAliasField."""

    def __get__(self, instance, cls=None):
        value = getattr(instance, "structure", cls)
        instance.__dict__[self.field.attname] = value
        return value

    def __set__(self, instance, value):
        instance.structure = value
        instance.__dict__[self.field.attname] = value


class StructureAliasField(models.Field):
    """A field that aliases to structure, but can be called something else."""

    descriptor_class = StructureDescriptor

    def contribute_to_class(self, cls, name, private_only=False):
        """Performs some extra setup when the field is added to a model.

        * Force field to be `private_only` i.e. not in the database.
        * Force field to reference the `structure` column in the database.
        * Force field to reference the `chemreg.compound.Compound` model in the database.

        """
        super().contribute_to_class(cls, name, private_only=True)
        self.column = "structure"
        self.model = apps.get_model("compound", "BaseCompound", require_ready=False)
