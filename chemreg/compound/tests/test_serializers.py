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


def test_query_structure_type(querystructuretype):
    """Test that a query structure type with a non-slugged name is invalid"""
    serializer = querystructuretype["serializer"]
    json_factory = querystructuretype["json_factory"]


def test_compound_deserialize(compound):
    """Test that a compound JSON is properly deserialized."""
    serializer = compound["serializer"]
    json_factory = compound["json_factory"]
    json = json_factory.build()
    assert serializer(data=json).is_valid()


def test_compound_serialize(compound):
    """Test that a compound model is properly serialized."""
    serializer = compound["serializer"]
    factory = compound["factory"]
    model = factory.build()
    serialized = serializer(model)
    assert serialized.data["id"] == model.cid
