from pytest_factoryboy import register

from chemreg.lists.tests.factories import (
    AccessibilityTypeFactory,
    ListFactory,
    ListTypeFactory,
    RecordFactory,
)

register(AccessibilityTypeFactory)
register(ListFactory)
register(ListTypeFactory)
register(RecordFactory)
