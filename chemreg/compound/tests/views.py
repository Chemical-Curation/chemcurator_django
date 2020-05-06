from django.test import RequestFactory
from rest_framework.permissions import IsAdminUser

from chemreg.compound.validators import validate_inchikey_unique
from chemreg.compound.views import DefinedCompoundViewSet


def test_definedcompound_override():
    """Test that passing an override query parameter works in DefinedCompoundViewSet."""
    factory = RequestFactory()
    view = DefinedCompoundViewSet()

    view.request = factory.get("/definedCompounds")
    assert not any(lambda o: isinstance(o, IsAdminUser), view.get_permissions())
    for field in ("molfile_v2000", "molfile_v3000", "smiles"):
        assert (
            validate_inchikey_unique in view.get_serializer().fields[field].validators
        )

    view.request = factory.get("/definedCompounds?override")
    assert any(lambda o: isinstance(o, IsAdminUser), view.get_permissions())
    for field in ("molfile_v2000", "molfile_v3000", "smiles"):
        assert (
            validate_inchikey_unique
            not in view.get_serializer().fields[field].validators
        )
