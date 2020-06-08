from django.conf import settings
from django.db import models

from chemreg.common.utils import get_current_user_pk


class CommonInfo(models.Model):
    """Common information to be applied to all models.

    Attributes:
        created_at (datetime.datetime): When the model was created.
        created_by (chemreg.user.models.User): Who created this model.
        updated_at (datetime.datetime): When the model was updated.
        updated_by (chemreg.user.models.User): Who updated this model.

    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=get_current_user_pk,
        editable=False,
        related_name="%(class)s_created_by_set",
        null=True,
        on_delete=models.PROTECT,
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        related_name="%(class)s_updated_by_set",
        null=True,
        on_delete=models.PROTECT,
    )

    class Meta:
        abstract = True
        ordering = ["pk"]


class ControlledVocabulary(CommonInfo):

    name = models.SlugField(max_length=49, unique=True)
    label = models.CharField(max_length=99, unique=True)
    short_description = models.CharField(max_length=499)
    long_description = models.TextField()
    deprecated = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label


class Source(ControlledVocabulary):
    """Controlled vocabulary for Sources

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
    """

    pass


class SubstanceType(ControlledVocabulary):
    """Controlled vocabulary for Substances

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
    """

    pass
