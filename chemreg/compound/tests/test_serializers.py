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
    DefinedCompoundSerializer = type(serializer)
    assert serializer.is_valid()
    serializer.save()
    serialized = DefinedCompoundSerializer(data=serializer.initial_data)
    assert not serialized.is_valid()
    assert "molfile_v3000" in serialized.errors
    assert str(serialized.errors["molfile_v3000"][0]) == "InChIKey already exists."


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
