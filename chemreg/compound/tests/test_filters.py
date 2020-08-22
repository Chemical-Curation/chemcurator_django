import pytest


@pytest.mark.parametrize("search_type", ["V3000", "V2000", "SMILES"])
@pytest.mark.django_db
def test_defined_compound_filters(
    search_type,
    defined_compound_factory,
    defined_compound_v2000_factory,
    defined_compound_smiles_factory,
    user,
    client,
):
    factory_dict = {
        "V3000": ("molfile_v3000", defined_compound_factory),
        "V2000": ("molfile_v2000", defined_compound_v2000_factory),
        "SMILES": ("smiles", defined_compound_smiles_factory),
    }
    client.force_authenticate(user=user)
    field, factory = factory_dict.get(search_type)
    # Add additional results to be filtered out.
    factory.create()
    compound = factory.build()
    assert compound.is_valid()
    obj = compound.save()
    # Alter the molfile so that we can ensure the lookup is done on the inchikey
    # URL encode spaces and newlines
    mol = compound.initial_data[field]

    # Test the filter with valid molfile
    response = client.get("/definedCompounds?", {f"filter[{field}]": mol})
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["cid"] == obj.cid

    # Test with invalid molfile
    response = client.get(f"/definedCompounds?filter[{field}]=foo")
    assert f"Structure is not in {search_type} format" in response.data[0]["detail"]
