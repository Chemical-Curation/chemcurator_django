from datetime import datetime

import factory

from chemreg.common.factory import ControlledVocabularyFactory, DjangoSerializerFactory
from chemreg.lists.models import List, Record, RecordIdentifier
from chemreg.lists.serializers import (
    AccessibilityTypeSerializer,
    IdentifierTypeSerializer,
    ListTypeSerializer,
)


class AccessibilityTypeFactory(DjangoSerializerFactory, ControlledVocabularyFactory):
    """Manufactures `AccessibilityType` models and serializers."""

    class Meta:
        model = AccessibilityTypeSerializer


class IdentifierTypeFactory(DjangoSerializerFactory, ControlledVocabularyFactory):
    """Manufactures `IdentifierType` models."""

    class Meta:
        model = IdentifierTypeSerializer


class ListTypeFactory(DjangoSerializerFactory, ControlledVocabularyFactory):
    """Manufactures `ListType` models and serializers."""

    class Meta:
        model = ListTypeSerializer


# todo: convert to serializer factory
class ListFactory(factory.DjangoModelFactory):
    """Manufactures `List` models."""

    name = factory.Faker("text", max_nb_chars=49)
    label = factory.Faker("text", max_nb_chars=255)
    short_description = factory.Faker("text", max_nb_chars=1000)
    long_description = factory.Faker("text")
    list_accessibility = factory.SubFactory(AccessibilityTypeFactory)
    date_of_source_collection = datetime.now()

    # Related Factories
    list_accessibility = factory.LazyAttribute(
        lambda _: AccessibilityTypeFactory().instance
    )

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


# todo: convert to serializer factory
class RecordIdentifierFactory(factory.DjangoModelFactory):
    """Manufactures `RecordIdentifier` models."""

    identifier = factory.Faker("text")
    identifier_label = factory.Faker("text", max_nb_chars=100)

    # Related Factories
    record = factory.SubFactory(RecordFactory)
    identifier_type = factory.SubFactory(IdentifierTypeFactory)

    class Meta:
        model = RecordIdentifier
