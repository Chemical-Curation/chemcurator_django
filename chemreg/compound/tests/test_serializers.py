import re

from rest_framework.exceptions import ParseError

import pytest


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
    serializer.save()
    serialized = defined_compound_factory.build(**serializer.initial_data)
    assert not serialized.is_valid()
    assert "molfile_v3000" in serialized.errors
    assert str(serialized.errors["molfile_v3000"][0]) == "InChIKey already exists."


@pytest.mark.django_db
def test_override_unique_inchikey(defined_compound_factory):
    serializer = defined_compound_factory.build()
    assert serializer.is_valid()
    one = serializer.save()
    data = serializer.initial_data
    data["override"] = True
    serialized = defined_compound_factory.build(**data)
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
    with pytest.raises(Exception) as e:
        serializer = defined_compound_smiles_factory.build(smiles=invalid_smiles)
        serializer.is_valid()
    assert "The SMILES string cannot be converted to a molfile." in str(
        e.value.detail["smiles"]
    )

    # Test a valence that partialsmiles doesn't like but we are accepting anyway
    serializer = defined_compound_smiles_factory.build(smiles="[S]")
    assert serializer.is_valid()

    # There are some exotic SMILES strings that partialsmiles rejects
    # CC(=O)N1CCN(CC1)C1=CC=C(OC[C@H]2COC@@(O2)C2=CC=C(Cl)C=C2Cl)C=C1
    #                                    ^  this is rejected by partialsmiles

    with pytest.raises(ParseError) as e:
        serializer = defined_compound_smiles_factory.build(
            smiles="CC(=O)N1CCN(CC1)C1=CC=C(OC[C@H]2COC@@(O2)C2=CC=C(Cl)C=C2Cl)C=C1"
        )
        serializer.is_valid()
    assert e.typename == "ParseError"
    assert "The SMILES string cannot be converted to a molfile." in str(
        e.value.detail["smiles"]
    )

    # CC(=O)N1CCN(CC1)C1=CC=C(OC[C@H]2CO[C@H](O2)C2=CC=C(Cl)C=C2Cl)C=C1
    #                                    ^  this is okay but the molfile doesn't work
    serializer = defined_compound_smiles_factory.build(
        smiles="CC(=O)N1CCN(CC1)C1=CC=C(OC[C@H]2CO[C@H](O2)C2=CC=C(Cl)C=C2Cl)C=C1"
    )
    assert not serializer.is_valid()


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

    data["override"] = True
    serialized = defined_compound_smiles_factory.build(**data)
    assert serialized.is_valid()  # succeeds with override
    two = serialized.save()
    assert one.cid != two.cid
    assert one.inchikey == two.inchikey


@pytest.mark.django_db
def test_invalid_v2000_molfile(defined_compound_v2000_factory):
    # make a valid V2000 molfile string
    dc = defined_compound_v2000_factory.build()
    assert dc.is_valid()

    str_v2k = dc.initial_data["molfile_v2000"]
    str_v2k_invalid = str_v2k.replace("V2000", "V2x00")
    dc_invalid = defined_compound_v2000_factory.build(molfile_v2000=str_v2k_invalid)

    assert not dc_invalid.is_valid()
    # fails because the V2000 molfile string is no longer valid


@pytest.mark.django_db
def test_defined_compound_from_v2000_molfile(defined_compound_v2000_factory):
    dc = defined_compound_v2000_factory.build()
    assert dc.is_valid()
    instance = dc.save()
    # test inchikey creation
    assert "inchikey" not in dc.initial_data
    assert re.match(r"^[A-Z]{14}-[A-Z]{10}-[A-Z]$", instance.inchikey)


@pytest.mark.django_db
def test_too_many_structures(
    defined_compound_v2000_factory, defined_compound_smiles_factory
):
    dc2k = defined_compound_v2000_factory.build()
    assert dc2k.is_valid()

    # a v2000 serializer with an added SMILES string
    dc = defined_compound_v2000_factory.build()
    # assign the smiles
    dc.initial_data["smiles"] = "CC(=O)OC1=C(C=CC=C1)C(O)=O"
    assert not dc.is_valid()

    # a smiles serializer with an added V2000 string
    dcsmiles = defined_compound_smiles_factory.build(
        smiles="CC(=O)OC1=C(C=CC=C1)C(O)=O"
    )
    # assign the V2000 molfile from the first object
    dcsmiles.initial_data["molfile_v2000"] = dc2k.initial_data.get("molfile_v2000")
    assert not dc.is_valid()
