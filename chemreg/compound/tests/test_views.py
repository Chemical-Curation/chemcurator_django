from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

import pytest

from chemreg.compound.models import DefinedCompound
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
        "molecular_weight",
        "molecular_formula",
        "calculated_inchikey",
        "url",
    ]


@pytest.mark.django_db
def test_ill_defined_compound_admin_user(user_factory, ill_defined_compound_factory):
    """Tests and Validates the outcomes of multiple POST requests performed by an
    User both with and without ADMIN permissions"""
    client = APIClient()
    user = user_factory.build()
    user.is_staff = True
    client.force_authenticate(user=user)
    idc = ill_defined_compound_factory.build()
    idc.initial_data.update(cid="CID")
    response = client.post(
        "/illDefinedCompounds",
        {"data": {"type": "illDefinedCompound", "attributes": idc.initial_data}},
    )
    assert response.status_code == 201
    client = APIClient()
    user = user_factory.build()
    assert user.is_staff is False
    client.force_authenticate(user=user)
    idc = ill_defined_compound_factory.build()
    idc.initial_data.update(cid="XXX")
    response = client.post(
        "/illDefinedCompounds",
        {"data": {"type": "illDefinedCompound", "attributes": idc.initial_data}},
    )
    assert response.status_code == 403


def test_defined_compound_view():
    """Tests that the Defined Compound View Set includes cid and InChIKey as filterset fields."""
    assert DefinedCompoundViewSet.filterset_class.Meta.fields == [
        "cid",
        "inchikey",
        "molfile_v3000",
    ]


def test_compound_view():
    """Tests that the Compound View Set, is ReadOnly and has the inclusion of cid as a filterset field."""
    assert issubclass(CompoundViewSet, ReadOnlyModelViewSet)
    assert CompoundViewSet.filterset_fields == ["cid"]


@pytest.mark.django_db
def test_definedcompound_admin_user(user_factory, defined_compound_factory):
    """Tests and Validates the outcomes of multiple POST requests performed by an
    User both with and without ADMIN permissions"""
    client = APIClient()
    user = user_factory.build()
    user.is_staff = True
    client.force_authenticate(user=user)
    dc = defined_compound_factory.build()
    dc.initial_data.update(cid="CID")
    response = client.post(
        "/definedCompounds",
        {"data": {"type": "definedCompound", "attributes": dc.initial_data}},
    )
    assert response.status_code == 400
    assert response.exception is True
    assert (
        str(response.data[0]["detail"])
        == "InchIKey must be included when CID is defined."
    )
    dc.initial_data.update(inchikey="INCHI")
    response = client.post(
        "/definedCompounds",
        {"data": {"type": "definedCompound", "attributes": dc.initial_data}},
    )
    assert response.status_code == 201
    dc.initial_data.pop("cid")
    response = client.post(
        "/definedCompounds",
        {"data": {"type": "definedCompound", "attributes": dc.initial_data}},
    )
    assert response.status_code == 400
    assert response.exception is True
    assert (
        str(response.data[0]["detail"])
        == "CID must be included when InchIKey is defined."
    )
    client = APIClient()
    user = user_factory.build()
    assert user.is_staff is False
    client.force_authenticate(user=user)
    dc = defined_compound_factory.build()
    dc.initial_data.update(cid="XXX", inchikey="XXX")
    response = client.post(
        "/definedCompounds",
        {"data": {"type": "definedCompound", "attributes": dc.initial_data}},
    )
    assert response.status_code == 403
    assert response.exception is True
    assert (
        str(response.data[0]["detail"])
        == "You do not have permission to perform this action."
    )


@pytest.mark.django_db
def test_compound_soft_delete(user_factory, defined_compound_factory):
    """
    Tests:
    Compound records cannot be hard-deleted
    Soft delete of Compounds can only be done by an Admin user who
    is also providing a valid replacement CID and a QC note
    """
    client = APIClient()
    standard_user = user_factory.build(is_staff=False)
    admin_user = user_factory.build(is_staff=True)
    compounds = [
        serializer.instance for serializer in defined_compound_factory.create_batch(4)
    ]

    # Compound 1 will replace 2 and 3
    client.force_authenticate(user=admin_user)
    for compound in compounds[2:]:
        destroy_data = {
            "data": {
                "type": "definedCompound",
                "id": compound.id,
                "attributes": {
                    "replacementCid": compounds[1].cid,
                    "qcNote": f"replacing compound {compound.id} with compound {compounds[1].id}",
                },
            }
        }
        resp = client.delete(f"/definedCompounds/{compound.id}", data=destroy_data)
        assert resp.status_code == 204
        deleted_compound = DefinedCompound.objects.with_deleted().get(pk=compound.pk)
        assert deleted_compound.replaced_by == compounds[1]
        assert (
            deleted_compound.qc_note
            == f"replacing compound {compound.id} with compound {compounds[1].id}"
        )

    # the deleted compounds should be visible to an admin user
    client.force_authenticate(user=admin_user)
    resp = client.get(f"/definedCompounds")
    cid_set = set(c["cid"] for c in resp.data["results"])
    assert len(cid_set) == 4
    # it should NOT be visible to non-admin user
    client.force_authenticate(user=standard_user)
    resp = client.get(f"/definedCompounds")
    cid_set = set(c["cid"] for c in resp.data["results"])
    assert len(cid_set) == 2
    assert compounds[2].cid not in cid_set
    assert compounds[3].cid not in cid_set

    # Compound 0 will replace compound 1
    client.force_authenticate(user=admin_user)
    destroy_data = {
        "data": {
            "type": "definedCompound",
            "id": compounds[1].id,
            "attributes": {
                "replacementCid": compounds[0].cid,
                "qcNote": f"replacing compound {compounds[1].id} with compound {compounds[0].id}",
            },
        }
    }
    resp = client.delete(f"/definedCompounds/{compounds[1].id}", data=destroy_data)
    assert resp.status_code == 204
    deleted_compounds = [
        DefinedCompound.objects.with_deleted().get(pk=compound.pk)
        for compound in compounds
    ]
    # Compounds 1, 2, and 3 should be replaced by compound 0
    for deleted_compound in deleted_compounds[1:]:
        assert deleted_compound.replaced_by == compounds[0]
    assert (
        deleted_compounds[1].qc_note
        == f"replacing compound {compounds[1].id} with compound {compounds[0].id}"
    )
    # Make sure the qc_note for compounds 2 and 3 are unchanged
    assert (
        deleted_compounds[2].qc_note
        == f"replacing compound {compounds[2].id} with compound {compounds[1].id}"
    )
    assert (
        deleted_compounds[3].qc_note
        == f"replacing compound {compounds[3].id} with compound {compounds[1].id}"
    )


@pytest.mark.django_db
def test_compound_forbidden_soft_delete(user_factory, defined_compound_factory):
    """
    Tests:
    A non-admin user cannot perform the soft-deleted done in the test above
    """
    client = APIClient()

    serializers = defined_compound_factory.create_batch(2)
    compound_1 = serializers[0].instance
    compound_2 = serializers[1].instance

    # There should now be two defined compounds with the same structure.
    standard_user = user_factory.build(is_staff=False)
    client.force_authenticate(user=standard_user)
    resp = client.get(f"/compounds/{compound_1.id}")

    # The standard user should not be allowed to delete the compound
    destroy_data = {
        "data": {
            "type": "definedCompound",
            "id": compound_1.id,
            "attributes": {
                "replacement_cid": compound_2.cid,
                "qc_note": "replacing with another",
            },
        }
    }

    resp = client.delete(f"/compounds/{compound_1.id}", data=destroy_data)
    assert resp.status_code == 403
    assert resp.data[0]["detail"].code == "permission_denied"


@pytest.mark.django_db
def test_compound_redirect(user_factory, defined_compound_factory):
    """Tests that soft-deleted compounds will redirect when non-admin."""

    client = APIClient()
    admin_user = user_factory.build(is_staff=True)
    standard_user = user_factory.build(is_staff=False)

    serializers = defined_compound_factory.create_batch(2)
    compound_1 = serializers[0].instance
    compound_2 = serializers[1].instance

    destroy_data = {
        "data": {
            "type": "definedCompound",
            "id": compound_1.id,
            "attributes": {
                "replacement_cid": compound_2.cid,
                "qc_note": "replacing with another",
            },
        }
    }
    client.force_authenticate(user=admin_user)
    resp = client.delete(f"/definedCompounds/{compound_1.id}", data=destroy_data)
    assert resp.status_code == 204

    # Non-admin should be redirected
    client.force_authenticate(user=standard_user)
    resp = client.get(f"/compounds/{compound_1.id}")
    assert resp.status_code == 301
    assert compound_2.id == int(resp.url.split("/")[-1])

    # Admin should be able to retrieve it
    client.force_authenticate(user=admin_user)
    resp = client.get(f"/compounds/{compound_1.id}")
    assert resp.status_code == 200
