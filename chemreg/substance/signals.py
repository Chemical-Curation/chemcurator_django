from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

from chemreg.resolution.indices import SubstanceIndex


@receiver(post_save, sender=apps.get_model("substance.Substance"))
def substance_sync(**kwargs):
    SubstanceIndex().index(kwargs.get("instance"))


@receiver(post_save, sender=apps.get_model("substance.Synonym"))
def synonym_sync(**kwargs):
    SubstanceIndex().index(kwargs.get("instance").substance)
