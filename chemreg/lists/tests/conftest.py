from pytest_factoryboy import register

from chemreg.lists.tests.factories import (
    AccessibilityTypeFactory,
    ExternalContactFactory,
    IdentifierTypeFactory,
    ListFactory,
    ListTypeFactory,
    RecordFactory,
    RecordIdentifierFactory,
)
from chemreg.substance.tests.factories import SubstanceFactory
from chemreg.users.tests.factories import UserFactory

register(AccessibilityTypeFactory)
register(ExternalContactFactory)
register(IdentifierTypeFactory)
register(ListFactory)
register(ListTypeFactory)
register(RecordFactory)
register(RecordIdentifierFactory)
register(UserFactory)
register(SubstanceFactory)
