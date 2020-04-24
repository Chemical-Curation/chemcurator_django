import pytest

from chemreg.compound.settings import compound_settings


@pytest.mark.django_db
@pytest.mark.parametrize(
    "cid",
    [
        f"FOO{compound_settings.PREFIX}CID000",  # invalid prefix
        f"{compound_settings.PREFIX}CID00",  # does not have ID
        f"{compound_settings.PREFIX}CDI000",  # malformed meta text
        f"{compound_settings.PREFIX}CID090",  # incorrect checksum separator
        f"{compound_settings.PREFIX}CIDA00",  # non-integer checksum
        f"{compound_settings.PREFIX}CID00A",  # non-integer ID
    ],
)
def test_validate_cid_regex(defined_compound_factory, cid):
    serializer = defined_compound_factory.build(cid=cid)
    assert not serializer.is_valid()
    assert f"Invalid format. Expected {compound_settings.PREFIX}CID$0######." in (
        str(err) for err in serializer.errors["cid"]
    )


@pytest.mark.django_db
def test_validate_cid_checksum(defined_compound_factory):
    serializer = defined_compound_factory.build(
        cid=f"{compound_settings.PREFIX}CID00123"
    )
    assert not serializer.is_valid()
    assert "Invalid checksum. Expected 4." in (
        str(err) for err in serializer.errors["cid"]
    )


@pytest.mark.django_db
def test_validate_inchikey_computable(defined_compound_factory):
    serializer = defined_compound_factory.build(molfile_v3000="\n\n\nfoo")
    assert not serializer.is_valid()
    assert "InChIKey not computable for provided structure." in (
        str(err) for err in serializer.errors["molfile_v3000"]
    )


@pytest.mark.django_db
def test_validate_molfile_V3000(defined_compound_factory):
    serializer = defined_compound_factory.build(V2000=True)
    assert not serializer.is_valid()
    assert "Structure is not in V3000 format." in (
        str(err) for err in serializer.errors["molfile_v3000"]
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
    assert "molfile_v3000" in dcsmiles.errors.keys()
    assert (
        str(dcsmiles.errors.get("molfile_v3000"))
        == "The data includes too many potential non-V3000 molfile structures in ['molfile_v2000', 'smiles']."
    )
