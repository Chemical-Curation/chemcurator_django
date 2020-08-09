from pytest_factoryboy import register

from chemreg.lists.tests.factories import (
    AccessibilityTypeFactory,
    IdentifierTypeFactory,
    ListFactory,
    ListTypeFactory,
    RecordFactory,
)

register(AccessibilityTypeFactory)
register(IdentifierTypeFactory)
register(ListFactory)
register(ListTypeFactory)
register(RecordFactory)
