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
