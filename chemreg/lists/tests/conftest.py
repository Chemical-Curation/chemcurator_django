from pytest_factoryboy import register

from chemreg.lists.tests.factories import (
    AccessibilityTypeFactory,
    ExternalContactFactory,
    IdentifierTypeFactory,
    ListFactory,
    ListTypeFactory,
    RecordFactory,
)
from chemreg.users.tests.factories import UserFactory

register(AccessibilityTypeFactory)
register(ExternalContactFactory)
register(IdentifierTypeFactory)
register(ListFactory)
register(ListTypeFactory)
register(RecordFactory)
register(UserFactory)
