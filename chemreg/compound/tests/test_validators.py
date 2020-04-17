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
