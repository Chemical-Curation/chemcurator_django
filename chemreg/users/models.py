from django.contrib.auth.models import AbstractUser

from chemreg.common.models import CommonInfo


class User(CommonInfo, AbstractUser):
    pass
