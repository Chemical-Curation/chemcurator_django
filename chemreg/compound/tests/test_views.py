from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.test import APIRequestFactory, force_authenticate

import pytest

from chemreg.compound.validators import validate_inchikey_unique
from chemreg.compound.views import CompoundViewSet, DefinedCompoundViewSet
from chemreg.jsonapi.views import ReadOnlyModelViewSet


def test_definedcompound_override():
    """Test that passing an override query parameter works in DefinedCompoundViewSet."""
    factory = APIRequestFactory()
    view = DefinedCompoundViewSet(
        action_map={"post": "create"}, kwargs={}, format_kwarg={}
    )

    view.request = view.initialize_request(factory.post("/definedCompounds"))
    assert not any(isinstance(p, IsAdminUser) for p in view.get_permissions())
    for field in ("molfile_v2000", "molfile_v3000", "smiles"):
        assert (
            validate_inchikey_unique in view.get_serializer().fields[field].validators
        )

    view.request = view.initialize_request(factory.post("/definedCompounds?override"))
    assert any(isinstance(p, IsAdminUser) for p in view.get_permissions())
    for field in ("molfile_v2000", "molfile_v3000", "smiles"):
        assert (
            validate_inchikey_unique
            not in view.get_serializer().fields[field].validators
        )

    view.request = view.initialize_request(factory.post("/definedCompounds?overRide"))
    with pytest.raises(ValidationError) as err:
        view.create(view.request)
    assert err.value.status_code == 400
    assert err.value.default_code == "invalid"
    assert err.value.args[0] == "invalid query parameter: overRide"


@pytest.mark.django_db
def test_definedcompound_detail_attrs(user_factory, defined_compound_factory):
    """Test that detail view includes extra SerializerMethodField attributes."""
    factory = APIRequestFactory()
    view = DefinedCompoundViewSet.as_view({"get": "list"})
    serializer = defined_compound_factory.build()
    assert serializer.is_valid()
    compound = serializer.save()
    request = factory.get("/definedCompounds")
    user = user_factory.build()
    force_authenticate(request, user=user)
    response = view(request)
    attrs = response.data["results"].pop()
    assert list(attrs.keys()) == ["cid", "inchikey", "molfile_v3000", "url"]

    view = DefinedCompoundViewSet.as_view({"get": "retrieve"})
    request = factory.get("/definedCompounds/")
    force_authenticate(request, user=user)
    response = view(request, pk=compound.pk)
    attrs = response.data
    assert list(attrs.keys()) == [
        "cid",
        "inchikey",
        "molfile_v3000",
        "smiles",
        "molecular_weight",
        "molecular_formula",
        "calculated_inchikey",
        "url",
    ]


def test_defined_compound_view():
    """Tests that the Defined Compound View Set includes cid and InChIKey as filterset fields."""
    assert DefinedCompoundViewSet.filterset_fields == ["cid", "inchikey"]


def test_compound_view():
    """Tests that the Compound View Set, is ReadOnly and has the inclusion of cid as a filterset field."""
    assert issubclass(CompoundViewSet, ReadOnlyModelViewSet)
    assert CompoundViewSet.filterset_fields == ["cid"]
