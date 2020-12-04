from unittest.mock import patch

from django.core.management import call_command

import pytest


@pytest.mark.django_db
def test_substance_index_substance_list(substance_factory, batch_size=2):
    with patch("requests.post") as mocked_post, patch(
        "requests.delete"
    ) as mocked_delete:
        substance_factory.create_batch(batch_size)
        mocked_post.reset_mock()

        call_command("sync")

        # The below asserts could be replaced with a mock for SubstanceIndex
        # Assert substance index was cleared
        assert mocked_delete.call_count == 1
        # Assert a post request was sent for every substance
        assert mocked_post.call_count == batch_size
