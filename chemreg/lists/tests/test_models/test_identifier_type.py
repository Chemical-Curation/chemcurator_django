from chemreg.common.tests import controlled_vocabulary_test_helper
from chemreg.lists.models import IdentifierType


def test_identifier_type():
    """Tests the validity of the Identifier Type Model's attributes"""

    controlled_vocabulary_test_helper(IdentifierType)
