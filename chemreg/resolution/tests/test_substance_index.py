import json
from unittest.mock import patch

import pytest

from chemreg.resolution.indices import SubstanceIndex


@pytest.mark.django_db
def test_substance_index_substance_list_add(substance_factory):
    with patch("requests.post") as mocked_post:
        substances = [
            substance.instance for substance in substance_factory.create_batch(2)
        ]
        mocked_post.reset_mock()
        SubstanceIndex().sync_instances(substances)

        # Assert a post request was sent for every substance in the list
        assert mocked_post.call_count == len(substances)
        # Assert a post request was sent corresponding to each sid
        for substance in substances:
            assert substance.pk in [
                json.loads(call.args[1])["data"]["id"]
                for call in mocked_post.mock_calls
            ]


@pytest.mark.django_db
def test_substance_index_single_substance_add(substance_factory):
    with patch("requests.post") as mocked_post:
        substance = substance_factory().instance
        mocked_post.reset_mock()
        SubstanceIndex().sync_instances(substance)

        # Assert a post request was sent for the substance
        mocked_post.assert_called_once()
        # Assert a post request was sent corresponding to the sid
        assert (
            json.loads(mocked_post.mock_calls[0].args[1])["data"]["id"] == substance.pk
        )


@pytest.mark.django_db
def test_substance_index_substance_list_delete(substance_factory):
    with patch("requests.delete") as mocked_delete:
        substances = [
            substance.instance for substance in substance_factory.create_batch(2)
        ]

        # We are not deleting.  Just calling SubstanceIndex as if a delete had occured
        SubstanceIndex().sync_instances(substances, delete=True)

        # Assert a delete request was sent for every substance in the list
        assert mocked_delete.call_count == len(substances)

        mock_urls = [call.args[0] for call in mocked_delete.mock_calls]
        for substance in substances:
            # See if this sid occurs in any of the urls from the mocked_delete
            assert any(substance.pk in url for url in mock_urls)


@pytest.mark.django_db
def test_substance_index_single_substance_delete(substance_factory):
    with patch("requests.delete") as mocked_delete:
        substance = substance_factory().instance

        # We are not deleting.  Just calling SubstanceIndex as if a delete had occured
        SubstanceIndex().sync_instances(substance, delete=True)

        mocked_delete.assert_called_once()

        # See if this sid occurs in the url from the mocked_delete
        mock_url = mocked_delete.mock_calls[0].args[0]
        assert substance.pk in mock_url


def test_substance_index_delete_all():
    with patch("requests.delete") as mocked_delete:
        SubstanceIndex().delete_all_instances()

        # Assert a delete request was sent
        mocked_delete.assert_called_once()
