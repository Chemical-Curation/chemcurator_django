from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from html_sanitizer.django import get_sanitizer

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
        ordering = ["pk"]
        abstract = True


class ControlledVocabulary(CommonInfo):

    name = models.SlugField(max_length=49, unique=True)
    label = models.CharField(max_length=99, unique=True)
    short_description = models.CharField(max_length=499)
    long_description = models.TextField()
    deprecated = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    class Meta(CommonInfo.Meta):
        abstract = True


class HTMLTextField(models.TextField):
    """This is a text field that automatically sanitizes HTML.

    This uses html_sanitizer https://github.com/matthiask/html-sanitizer
    to add an automatic sanitizing of input html text.
    """

    description = _("HTMLText")

    def __init__(self, sanitizer_type="default", **kwargs):
        """Builds the class's sanitizer.

        Args:
            sanitizer_type (str, optional): This is the sanitizer from
                django's settings that will be used.  If no sanitizer_type
                is provided, the default sanitizer will be used.

        """
        self.sanitizer_type = sanitizer_type
        self.sanitizer = get_sanitizer(name=sanitizer_type)
        super().__init__(**kwargs)

    def deconstruct(self):
        """Returns the args that are required to build this class instance

        Returns:
            name, path, args, kwargs.
        """
        name, path, args, kwargs = super().deconstruct()
        if self.sanitizer_type != "default":
            kwargs["sanitizer_type"] = self.sanitizer_type
        return name, path, args, kwargs

    def get_internal_type(self):
        """The parent field class that this custom field is most like.

        In this case this will be "TextField" as the database will be building
        this class as if it were a text field with additional checks.

        Returns:
            String representation of the field class this class is most like.
        """
        return "TextField"

    def pre_save(self, model_instance, add):
        """Prepares and Sanitizes the inputted HTML for store

        Returns:
            Sanitized HTML string.
        """
        value = self.sanitizer.sanitize(getattr(model_instance, self.attname))
        setattr(model_instance, self.attname, value)
        return value
