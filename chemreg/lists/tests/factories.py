from datetime import datetime

import factory

from chemreg.common.factory import ControlledVocabularyFactory, DjangoSerializerFactory
from chemreg.lists.serializers import (
    AccessibilityTypeSerializer,
    ExternalContactSerializer,
    IdentifierTypeSerializer,
    ListSerializer,
    ListTypeSerializer,
    RecordIdentifierSerializer,
    RecordSerializer,
)
from chemreg.substance.tests.factories import SubstanceFactory


class AccessibilityTypeFactory(DjangoSerializerFactory, ControlledVocabularyFactory):
    """Manufactures `AccessibilityType` models and serializers."""

    class Meta:
        model = AccessibilityTypeSerializer


class ExternalContactFactory(DjangoSerializerFactory):
    """Manufactures `ExternalContact` models and serializers."""

    name = factory.Faker("text", max_nb_chars=49)
    email = factory.Faker("text", max_nb_chars=49)
    phone = factory.Faker("text", max_nb_chars=15)

    class Meta:
        model = ExternalContactSerializer


class IdentifierTypeFactory(DjangoSerializerFactory, ControlledVocabularyFactory):
    """Manufactures `IdentifierType` models."""

    class Meta:
        model = IdentifierTypeSerializer


class ListTypeFactory(DjangoSerializerFactory, ControlledVocabularyFactory):
    """Manufactures `ListType` models and serializers."""

    class Meta:
        model = ListTypeSerializer


class ListFactory(DjangoSerializerFactory):
    """Manufactures `List` models and serializers."""

    name = factory.Sequence(lambda n: f"{factory.Faker('slug').generate()}-{n}")
    label = factory.Faker("text", max_nb_chars=255)
    short_description = factory.Faker("sentence")
    long_description = factory.Faker("sentence")
    source_url = factory.Faker("text", max_nb_chars=500)
    source_reference = factory.Faker("text", max_nb_chars=500)
    source_doi = factory.Faker("text", max_nb_chars=500)
    date_of_source_collection = datetime.now()

    # Related Factories
    list_accessibility = factory.SubFactory(AccessibilityTypeFactory)
    external_contact = factory.SubFactory(ExternalContactFactory)

    class Meta:
        model = ListSerializer

    @factory.post_generation
    def owners(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.owners.add(extracted)

    @factory.post_generation
    def types(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.types.add(extracted)


class RecordFactory(DjangoSerializerFactory):
    """Manufactures `Record` models and serializers."""

    external_id = factory.Sequence(lambda n: n)
    score = factory.Faker("pyfloat")
    message = factory.Faker("text", max_nb_chars=500)
    is_validated = factory.Faker("pybool")

    # Related Factories
    list = factory.SubFactory(ListFactory)
    substance = factory.SubFactory(SubstanceFactory)

    class Meta:
        model = RecordSerializer


class RecordIdentifierFactory(DjangoSerializerFactory):
    """Manufactures `RecordIdentifier` models and serializers."""

    identifier = factory.Faker("text")
    identifier_label = factory.Faker("text", max_nb_chars=100)

    # Related Factories
    record = factory.SubFactory(RecordFactory)
    identifier_type = factory.SubFactory(IdentifierTypeFactory)

    class Meta:
        model = RecordIdentifierSerializer
