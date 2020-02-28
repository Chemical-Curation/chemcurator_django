from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _

from chemreg.common.models import CommonInfo


class User(CommonInfo, AbstractUser):
    name = CharField(_("Name of User"), blank=True, max_length=255)
