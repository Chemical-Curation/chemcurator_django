from chemreg.common.tests import controlled_vocabulary_test_helper
from chemreg.lists.models import ListType


def test_list_type():
    """Tests the validity of the List Type Model's attributes"""

    controlled_vocabulary_test_helper(ListType)
