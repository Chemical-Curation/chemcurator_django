import pytest


@pytest.mark.django_db
def test_invalid_cid(compound, invalid_cid):
    """Test that bad IDs will raise validation errors."""
    serializer = compound["serializer"]
    json_factory = compound["json_factory"]
    json = json_factory.build()
    json["id"] = invalid_cid
    assert not serializer(data=json).is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize("compound", ["IllDefinedCompound"], indirect=["compound"])
def test_ill_defined_compound(compound, mrvfile):
    """Test that an ill-defined compound can be created with the provided mrvfile."""
    serializer = compound["serializer"]
    json_factory = compound["json_factory"]
    json = json_factory.build()
    json["mrvfile"] = mrvfile
    assert serializer(data=json).is_valid()


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_compound_deserialize(compound):
    """Test that a compound JSON is properly deserialized."""
    serializer = compound["serializer"]
    json_factory = compound["json_factory"]
    json = json_factory.build()
    assert serializer(data=json).is_valid()


@pytest.mark.django_db
def test_compound_serialize(compound):
    """Test that a compound model is properly serialized."""
    serializer = compound["serializer"]
    factory = compound["factory"]
    model = factory.build()
    serialized = serializer(model)
    assert serialized.data["id"] == model.cid
