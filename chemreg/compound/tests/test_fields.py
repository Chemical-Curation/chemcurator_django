from chemreg.compound.fields import StructureAliasField


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
