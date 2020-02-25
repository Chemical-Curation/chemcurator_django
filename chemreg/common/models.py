from django.db import models


class CommonInfo(models.Model):
    """Common information to be applied to all models.

    Attributes:
        created_at (datetime.datetime): When the model was created.
        updated_at (datetime.datetime): When the model was updated.

    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
