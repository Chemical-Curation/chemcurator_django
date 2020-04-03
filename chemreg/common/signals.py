from django.db.models.signals import pre_save
from django.dispatch import receiver

from chemreg.common.models import CommonInfo
from chemreg.common.utils import get_current_user_pk


@receiver(pre_save)
def set_updated_by(sender, instance, **kwargs):
    """Signal to set the `CommonInfo.updated_by`.

    Arguments:
        sender: the model class.
        instance: the model instance.
    """
    if isinstance(instance, CommonInfo):
        instance.updated_by_id = get_current_user_pk()
