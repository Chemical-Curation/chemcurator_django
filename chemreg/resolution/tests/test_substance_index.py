import json
from unittest.mock import Mock, patch

from rest_framework.exceptions import APIException

import pytest
import requests

from chemreg.resolution.indices import SubstanceIndex


def test_substance_index_substance_search():
    sample_response = {
        "data": [
            {"id": "DTXSID", "type": "substance", "attributes": {"identifiers": {}}}
        ]
    }
    identifier = "foobar"
    with patch("requests.get") as mocked_get:
        # Mock the requests.response
        mocked_response = Mock()
        # return our dict as .json()
        mocked_response.json.return_value = sample_response
        # calls to requests.get returns our mocked response automatically
        mocked_get.return_value = mocked_response

        search_url = SubstanceIndex().search_url
        json = SubstanceIndex().search(identifier)

        # Assert a get request was sent
        mocked_get.assert_called_once()
        # Assert url was requested [call_number][request_args_tuple][tuple_portion]
        assert mocked_get.mock_calls[0][1][0] == search_url
        assert mocked_get.mock_calls[0][2]["params"]["identifier"] == identifier
        # Assert the response was processed into the proper json object
        assert json == sample_response


def test_substance_index_substance_search_connection_error():
    def mocked_function():
        raise requests.exceptions.ConnectionError()

    with patch("requests.get") as mocked_get:
        mocked_get.return_value = mocked_function

        with pytest.raises(APIException) as exception:
            SubstanceIndex().search("foobar")
            assert exception
            assert str(exception) == "The Resolver service is not available right now"


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
def test_substance_index_identifiers(substance_factory):
    expected_identifier_keys = [
        "compound_id",
        "inchikey",
        "preferred_name",
        "display_name",
        "casrn",
        "synonyms",
    ]

    substance = substance_factory().instance
    identifiers = SubstanceIndex().get_model_document(substance).get("data")

    assert identifiers
    assert identifiers["id"] == substance.pk
    assert (
        list(identifiers["attributes"]["identifiers"].keys())
        == expected_identifier_keys
    )


@pytest.mark.django_db
def test_synonym_indexing(
    substance_factory, synonym_factory, synonym_quality_factory, synonym_type_factory
):
    synonym_quality = synonym_quality_factory.create(is_restrictive=False).instance

    synonym_type = synonym_type_factory().instance

    substance = substance_factory.create(preferred_name="Moon Pie",).instance

    synonym = synonym_factory.create(
        substance={"type": "substance", "id": substance.pk},
        identifier="marshmallow sandwich",
        synonym_type={"type": "synonymType", "id": synonym_type.pk},
        synonym_quality={"type": "synonymQuality", "id": synonym_quality.pk},
    ).instance

    identifiers = SubstanceIndex().get_model_document(substance)["data"]["attributes"][
        "identifiers"
    ]
    weight = synonym_quality.score_weight + synonym_type.score_modifier
    assert identifiers["synonyms"][0]["identifier"] == synonym.identifier
    assert identifiers["synonyms"][0]["weight"] == weight


@pytest.mark.django_db
def test_substance_index_identifiers_cid(substance_factory):
    sub = substance_factory().instance
    def_sub = substance_factory(defined=True).instance

    idents = SubstanceIndex().get_model_document(sub)["data"]["attributes"][
        "identifiers"
    ]
    def_idents = SubstanceIndex().get_model_document(def_sub)["data"]["attributes"][
        "identifiers"
    ]

    # No Compound
    assert idents["compound_id"] is None
    # With Compound
    assert def_idents["compound_id"] == def_sub.associated_compound.pk


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
