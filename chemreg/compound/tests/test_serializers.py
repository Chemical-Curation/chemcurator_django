import re

import pytest

from chemreg.compound.settings import compound_settings


@pytest.mark.django_db
def test_defined_compound(defined_compound_factory):
    serializer = defined_compound_factory.build()
    assert serializer.is_valid()
    instance = serializer.save()
    # test inchikey creation
    assert "inchikey" not in serializer.initial_data
    assert re.match(r"^[A-Z]{14}-[A-Z]{10}-[A-Z]$", instance.inchikey)


@pytest.mark.django_db
def test_ill_defined_compound(ill_defined_compound_factory):
    serializer = ill_defined_compound_factory.build()
    assert serializer.is_valid()
    instance = serializer.save()
    # test default querystructuretype
    assert "query_structure_type" not in serializer.initial_data
    assert instance.query_structure_type.name == "ill-defined"


@pytest.mark.django_db
def test_query_structure_type(query_structure_type_factory):
    serializer = query_structure_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_unique_inchikey(defined_compound_factory):
    serializer = defined_compound_factory.build()
    assert serializer.is_valid()
    compound = serializer.save()
    serialized = defined_compound_factory.build(**serializer.initial_data)
    assert not serialized.is_valid()
    assert "molfile_v3000" in serialized.errors
    conflict = f"Conflicting compound ID: {compound.id}"
    assert conflict in str(serialized.errors["molfile_v3000"][0])


@pytest.mark.django_db
def test_override_unique_inchikey(defined_compound_factory):
    serializer = defined_compound_factory.build()
    assert serializer.is_valid()
    one = serializer.save()
    serialized = defined_compound_factory.build(
        **serializer.initial_data, admin_override=True
    )
    assert serialized.is_valid()
    two = serialized.save()
    assert one.cid != two.cid
    assert one.inchikey == two.inchikey


@pytest.mark.django_db
def test_defined_compound_from_smiles(defined_compound_smiles_factory):
    VALID_SMILES = (
        "CC(=O)OC1=C(C=CC=C1)C(O)=O",
        "CC(=O)NC1=CC=C(O)C=C1",
        "CC(C)(C1=CC=C(O)C=C1)C1=CC=C(O)C=C1",
        "ClC(Cl)=C(Cl)Cl",
        "ClC=C(Cl)Cl",
        "C=O",
        # "[S]",       # test below
        "CCNC1=NC(NC(C)C)=NC(Cl)=N1",
        # "CC(=O)N1CCN(CC1)C1=CC=C(OC[C@H]2COC@@(O2)C2=CC=C(Cl)C=C2Cl)C=C1",        # test below
    )
    for smile in VALID_SMILES:
        serializer = defined_compound_smiles_factory.build(smiles=smile)
        assert serializer.is_valid()
        instance = serializer.save()
        # test inchikey creation
        assert "inchikey" not in serializer.initial_data
        assert re.match(r"^[A-Z]{14}-[A-Z]{10}-[A-Z]$", instance.inchikey)

    invalid_smiles = "AN(INVALID(STRING"
    serializer = defined_compound_smiles_factory.build(smiles=invalid_smiles)
    assert not serializer.is_valid()
    assert "Structure is not in SMILES format" in str(
        serializer.errors.get("smiles")[0]
    )

    # Test a valence that partialsmiles doesn't like but we are accepting anyway
    serializer = defined_compound_smiles_factory.build(smiles="[S]")
    assert serializer.is_valid()

    # There are some exotic SMILES strings that partialsmiles rejects
    # CC(=O)N1CCN(CC1)C1=CC=C(OC[C@H]2COC@@(O2)C2=CC=C(Cl)C=C2Cl)C=C1
    #                                    ^  this is rejected by partialsmiles

    serializer = defined_compound_smiles_factory.build(
        smiles="CC(=O)N1CCN(CC1)C1=CC=C(OC[C@H]2COC@@(O2)C2=CC=C(Cl)C=C2Cl)C=C1"
    )
    assert not serializer.is_valid()
    assert "Structure is not in SMILES format" in str(
        serializer.errors.get("smiles")[0]
    )


@pytest.mark.django_db
def test_override_unique_inchikey_via_smiles(defined_compound_smiles_factory):
    serializer = defined_compound_smiles_factory.build(
        smiles="CC(=O)OC1=C(C=CC=C1)C(O)=O"
    )
    assert serializer.is_valid()
    one = serializer.save()
    data = serializer.initial_data
    serialized = defined_compound_smiles_factory.build(**data)
    assert not serialized.is_valid()  # fails without override

    serialized = defined_compound_smiles_factory.build(**data, admin_override=True)
    assert serialized.is_valid()  # succeeds with override
    two = serialized.save()
    assert one.cid != two.cid
    assert one.inchikey == two.inchikey


@pytest.mark.django_db
def test_defined_compound_from_v2000_molfile(defined_compound_v2000_factory):
    dc = defined_compound_v2000_factory.build()
    assert dc.is_valid()
    instance = dc.save()
    # test inchikey creation
    assert "inchikey" not in dc.initial_data
    assert re.match(r"^[A-Z]{14}-[A-Z]{10}-[A-Z]$", instance.inchikey)


@pytest.mark.django_db
def test_defined_compound_prefix(defined_compound_factory):
    serializer = defined_compound_factory.build()
    assert serializer.is_valid()
    instance = serializer.save()
    # assert that the prefix of the serialized defined compound is equivalent to
    # the prefix generated in compound_settings
    assert instance.cid[0 : instance.cid.find("CID")] == compound_settings.PREFIX


@pytest.mark.django_db
def test_defined_compound_custom_prefix(defined_compound_factory):
    compound_settings.PREFIX = "XTX"
    serializer = defined_compound_factory.build()
    assert serializer.is_valid()
    instance = serializer.save()
    # assert that the prefix of the serialized defined compound is equivalent to
    # the prefix assigned for testing purposes
    assert instance.cid[0 : instance.cid.find("CID")] == compound_settings.PREFIX


@pytest.mark.django_db
def test_ill_defined_compound_prefix(ill_defined_compound_factory):
    serializer = ill_defined_compound_factory.build()
    assert serializer.is_valid()
    instance = serializer.save()
    # assert that the prefix of the serialized ill defined compound is equivalent to
    # the prefix generated in compound_settings
    assert instance.cid[0 : instance.cid.find("CID")] == compound_settings.PREFIX
