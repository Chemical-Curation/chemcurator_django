from datetime import datetime

import factory

from chemreg.common.factory import ControlledVocabularyFactory
from chemreg.lists.models import AccessibilityType, List, Record


# todo: convert to serializer factory
class AccessibilityTypeFactory(ControlledVocabularyFactory):
    """Manufactures `AccessibilityType` models."""

    class Meta:
        model = AccessibilityType


# todo: convert to serializer factory
class ListFactory(factory.DjangoModelFactory):
    """Manufactures `List` models."""

    name = factory.Faker("text", max_nb_chars=49)
    label = factory.Faker("text", max_nb_chars=255)
    short_description = factory.Faker("text", max_nb_chars=1000)
    long_description = factory.Faker("text")
    list_accessibility = factory.SubFactory(AccessibilityTypeFactory)
    date_of_source_collection = datetime.now()

    class Meta:
        model = List


# todo: convert to serializer factory
class RecordFactory(factory.DjangoModelFactory):
    """Manufactures `Record` models."""

    external_id = factory.Sequence(lambda n: n)
    score = factory.Faker("pyfloat")
    message = factory.Faker("text", max_nb_chars=500)
    is_validated = factory.Faker("pybool")

    # Related Factories
    list = factory.SubFactory(ListFactory)

    class Meta:
        model = Record
