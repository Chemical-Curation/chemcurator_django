import pytest


def test_invalid_cid(compound, invalid_cid):
    """Test that bad IDs will raise validation errors."""
    serializer = compound["serializer"]
    json_factory = compound["json_factory"]
    json = json_factory.build()
    json["id"] = invalid_cid
    assert not serializer(data=json).is_valid()


@pytest.mark.parametrize("compound", ["DefinedCompound"], indirect=["compound"])
def test_invalid_inchikey(compound, invalid_inchikey):
    """Test that bad InChIKeys will raise validation errors."""
    serializer = compound["serializer"]
    json_factory = compound["json_factory"]
    json = json_factory.build()
    json["inchikey"] = invalid_inchikey
    assert not serializer(data=json).is_valid()


@pytest.mark.parametrize("compound", ["IllDefinedCompound"], indirect=["compound"])
def test_mrvfile(compound, mrvfile):
    """Test that an ill-defined compound can be created with the provided mrvfile."""
    serializer = compound["serializer"]
    json_factory = compound["json_factory"]
    json = json_factory.build()
    json["mrvfile"] = mrvfile
    print("Validating:")
    print(serializer(data=json).is_valid())
    print(serializer(data=json).__dict__)
    assert serializer(data=json).is_valid()


@pytest.mark.django_db(transaction=True)
def test_query_structure_type(query_structure_type):
    """Test that a query structure type name with reserved chars is invalid"""
    serializer = query_structure_type["serializer"]
    json_factory = query_structure_type["json_factory"]
    json = json_factory.build()
    json["name"] = "query structure type"
    assert not serializer(data=json).is_valid()

    json["name"] = "querystructuretype1"
    json["label"] = "Query Structure Type 1"
    assert serializer(data=json).is_valid()

    json["name"] = "query-structure-type-2"
    json["label"] = "Query Structure Type 2"
    assert serializer(data=json).is_valid()

    # a duplicate name or label should be invalid,
    # so re-serializing the same data should not work
    json["label"] = "Query Structure Type 2 duplicated"
    assert not serializer(data=json).is_valid()


@pytest.mark.django_db(transaction=True)
def test_compound_deserialize(compound):
    """Test that a compound JSON is properly deserialized."""
    serializer = compound["serializer"]
    json_factory = compound["json_factory"]
    json = json_factory.build()
    assert serializer(data=json).is_valid()


@pytest.mark.django_db(transaction=True)
def test_compound_serialize(compound):
    """Test that a compound model is properly serialized."""
    serializer = compound["serializer"]
    factory = compound["factory"]
    model = factory.build()
    serialized = serializer(model)
    assert serialized.data["id"] == model.cid
