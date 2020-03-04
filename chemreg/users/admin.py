from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from chemreg.users.models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    pass
