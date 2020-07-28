from chemreg.common.tests import controlled_vocabulary_test_helper
from chemreg.lists.models import AccessibilityType


def test_accessibility_type():
    """Tests the validity of the Accessibility Type Model's attributes"""

    controlled_vocabulary_test_helper(AccessibilityType)
