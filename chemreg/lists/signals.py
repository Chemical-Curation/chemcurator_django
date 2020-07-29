from django.db.models.signals import post_save
from django.dispatch import receiver

from crum import get_current_user

from chemreg.lists.models import List


@receiver(post_save, sender=List)
def add_default_owners(instance, **kwargs):
    user = get_current_user()
    if instance and not instance.owners.count() and user:
        instance.owners.add(user)
