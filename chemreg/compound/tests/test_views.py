from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient

import pytest

from chemreg.compound.validators import validate_inchikey_unique
from chemreg.compound.views import CompoundViewSet, DefinedCompoundViewSet
from chemreg.jsonapi.views import ReadOnlyModelViewSet
from chemreg.compound.models import DefinedCompound


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
    assert list(attrs.keys()) == [
        "cid",
        "inchikey",
        "molfile_v3000",
        "replaced_by",
        "url",
    ]

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
        "replaced_by",
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


@pytest.mark.django_db
def test_compound_soft_delete(user_factory, defined_compound_factory):
    """
    Tests:
    Compound records cannot be hard-deleted
    Soft delete of Compounds can only be done by an Admin user who
    is also providing a valid replacement CID and a QC note
    """
    client = APIClient()
    # Create a pair of tautomers
    # acetone | 67-64-1 | DTXSID8021482 | CC(C)=O
    mol1 = "\n  Mrv1533009301517212D          \n\n  0  0  0     0  0            999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 4 3 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 C 2.3093 0 0 0\nM  V30 2 C 1.5386 -1.3333 0 0\nM  V30 3 C 2.3093 -2.6667 0 0\nM  V30 4 O 0 -1.3333 0 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 2 2 4\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n"

    # Propen-2-ol | 29456-04-0 | DTXSID20183662
    mol2 = "\n  Mrv1533009301517412D          \n\n  0  0  0     0  0            999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 4 3 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 O 5.7475 1.1551 0 0\nM  V30 2 C 3.08 1.1551 0 0\nM  V30 3 C 4.4137 0.3851 0 0\nM  V30 4 C 4.4137 -1.1551 0 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 3\nM  V30 2 1 2 3\nM  V30 3 2 3 4\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n"

    assert DefinedCompound.objects.count() == 0

    serializer_1 = defined_compound_factory.build(molfile_v3000=mol1)

    assert serializer_1.is_valid()
    compound_1 = serializer_1.save()

    serializer_2 = defined_compound_factory.build(molfile_v3000=mol2)
    serializer_2.is_valid()
    compound_2 = serializer_2.save()

    # There should now be two defined compounds with the same structure.
    admin_user = user_factory.build(username="karyn", is_staff=True)
    client.force_authenticate(user=admin_user)
    resp = client.get(f"/compounds/{compound_1.id}")

    client.force_authenticate(user=admin_user)
    # Both should have different inchikeys
    assert not compound_1.inchikey == compound_2.inchikey
    resp = client.get(f"/compounds/{compound_1.id}")
    assert compound_1.inchikey == resp.data.get("inchikey")

    resp = client.get(f"/compounds/{compound_2.id}")
    assert compound_2.inchikey == resp.data.get("inchikey")

    # One can be deleted.

    #
    destroy_data = {"qc_note": "replacing with another", "replaced_by": compound_2.cid}

    resp = client.delete(f"/compounds/{compound_1.id}", data=destroy_data)

    assert DefinedCompound.objects.filter(pk=compound_1.id, is_deleted=True).exists()
    client.logout()
