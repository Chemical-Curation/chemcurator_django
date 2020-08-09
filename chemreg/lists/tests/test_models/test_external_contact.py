from django.db import models

from chemreg.lists.models import ExternalContact


def test_external_contact():
    """Tests the validity of the External Contact Model's attributes"""

    name = ExternalContact._meta.get_field("name")
    assert isinstance(name, models.CharField)
    assert name.max_length == 49
    assert name.unique
    assert not name.blank
    email = ExternalContact._meta.get_field("email")
    assert isinstance(email, models.CharField)
    assert email.max_length == 49
    assert email.unique
    assert not email.blank
    phone = ExternalContact._meta.get_field("phone")
    assert isinstance(phone, models.CharField)
    assert phone.max_length == 15
    assert phone.unique
    assert not phone.blank
