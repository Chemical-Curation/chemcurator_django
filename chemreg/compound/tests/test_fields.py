from random import randint

from chemreg.compound.fields import StructureAliasField
from chemreg.compound.utils import compute_checksum


def test_structure_alias_field(compound):
    """Test that StructureAliasField only acts as an alias to Compound.structure"""
    # Test setting the parameters
    factory = compound["factory"]
    model = factory.build()
    for field in model._meta.get_fields():
        if isinstance(field, StructureAliasField):
            alias = field
    assert getattr(model, alias.attname) == model.structure
    setattr(model, alias.attname, "modded alias")
    assert getattr(model, alias.attname) == model.structure == "modded alias"
    model.structure = "modded structure"
    assert getattr(model, alias.attname) == model.structure == "modded structure"
    # Test that underlying database functions are identical
    structure = model._meta.get_field("structure")
    assert alias.model == structure.model
    assert alias.column == structure.column


def test_checksum():
    i = randint(2000000, 9999999)
    computed = (
        (1 * int(str(i)[0]))
        + (2 * int(str(i)[1]))
        + (3 * int(str(i)[2]))
        + (4 * int(str(i)[3]))
        + (5 * int(str(i)[4]))
        + (6 * int(str(i)[5]))
        + (7 * int(str(i)[6]))
    ) % 10
    checksum = compute_checksum(i)
    assert computed == checksum
    assert 0 <= checksum < 10
