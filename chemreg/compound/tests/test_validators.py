import pytest


@pytest.mark.django_db
def test_validate_inchikey_computable(defined_compound_factory):
    serializer = defined_compound_factory.build(molfile_v3000="\n\n\nfoo")
    assert not serializer.is_valid()
    assert "InChIKey not computable for provided structure." in (
        str(err) for err in serializer.errors["molfile_v3000"]
    )


@pytest.mark.django_db
def test_validate_molfile_V3000(defined_compound_factory):
    # the V2000=True argument creates a DefinedCompound JSON object
    # where the `molfile_v3000` field uses the V2000 format and is
    # therefore invalid.
    serializer = defined_compound_factory.build(V2000=True)
    assert not serializer.is_valid()
    assert "Structure is not in V3000 format." in (
        str(err) for err in serializer.errors["molfile_v3000"]
    )


@pytest.mark.django_db
def test_validate_no_structure(defined_compound_v2000_factory):
    # check for no provided structure strings at all

    # Build a DefinedCompound JSON object with a valid V2000
    # molfile, then remove the molfile_v2000 attribute, leaving
    # no structure string at all.
    dc = defined_compound_v2000_factory.build()
    dc.initial_data.pop("molfile_v2000")
    assert not dc.is_valid()
    assert (
        str(dc.errors.get("non_field_errors"))
        == "One of ['molfileV2000', 'molfileV3000', 'smiles'] required."
    )


@pytest.mark.django_db
def test_validate_molfile_v2000(defined_compound_v2000_factory):
    # make a valid V2000 molfile string
    dc = defined_compound_v2000_factory.build()
    assert dc.is_valid()

    str_v2k = dc.initial_data["molfile_v2000"]
    str_v2k_invalid = str_v2k.replace("V2000", "V2x00")
    dc_invalid = defined_compound_v2000_factory.build(molfile_v2000=str_v2k_invalid)

    assert not dc_invalid.is_valid()
    # fails because the V2000 molfile string is no longer valid


@pytest.mark.django_db
def test_validate_single_structure(
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
    assert not dcsmiles.is_valid()
    assert "non_field_errors" in dcsmiles.errors.keys()
    assert (
        str(dcsmiles.errors.get("non_field_errors"))
        == "Only one of ['molfileV2000', 'molfileV3000', 'smiles'] allowed. Recieved ['molfileV2000', 'smiles']."
    )
