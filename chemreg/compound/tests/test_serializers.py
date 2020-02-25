from chemreg.compound.serializers import BaseCompoundSerializer


def test_invalid_compound_deserialize(basecompound_json, invalid_cid):
    """Test that bad IDs will raise validation errors."""
    basecompound_json["id"] = invalid_cid
    assert not BaseCompoundSerializer(data=basecompound_json).is_valid()


def test_compound_deserialize(basecompound_json):
    """Test that a compound JSON is properly deserialized."""
    assert BaseCompoundSerializer(data=basecompound_json).is_valid()


def test_compound_serialize(basecompound):
    """Test that a compound JSON is properly serialized."""
    serialized = BaseCompoundSerializer(basecompound)
    assert serialized.data["id"] == basecompound.cid
