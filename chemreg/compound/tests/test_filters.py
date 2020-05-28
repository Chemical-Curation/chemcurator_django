from rest_framework.test import APIClient

import pytest


@pytest.mark.django_db
def test_defined_compound_filters(defined_compound_factory, user):
    client = APIClient()
    client.force_authenticate(user=user)
    compounds = defined_compound_factory.create_batch(2)
    # Alter the molfile so that we can ensure the lookup is done on the inchikey
    # URL encode spaces and newlines
    molfile = (
        compounds[0]
        .instance.molfile_v3000.replace("-INDIGO-", "-CHEMREG-")
        .replace(" ", "+")
        .replace("\n", "%0A")
    )

    # Test the filter with valid molfile
    response = client.get(f"/definedCompounds?filter[molfileV3000]={molfile}")
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["cid"] == compounds[0].instance.cid
