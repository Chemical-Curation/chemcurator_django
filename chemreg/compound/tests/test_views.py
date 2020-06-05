from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

import pytest

from chemreg.compound.models import DefinedCompound, IllDefinedCompound
from chemreg.compound.tests.factories import (
    DefinedCompoundFactory,
    IllDefinedCompoundFactory,
)
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


@pytest.mark.parametrize(
    "compound_factory", [DefinedCompoundFactory, IllDefinedCompoundFactory]
)
@pytest.mark.django_db
def test_compound_soft_delete(user, admin_user, compound_factory):
    """
    Tests:
    Compound records cannot be hard-deleted
    Soft delete of Compounds can only be done by an Admin user who
    is also providing a valid replacement CID and a QC note
    """
    if compound_factory == DefinedCompoundFactory:
        compound_json_type = "definedCompound"
        model = DefinedCompound
    elif compound_factory == IllDefinedCompoundFactory:
        compound_json_type = "illDefinedCompound"
        model = IllDefinedCompound
    client = APIClient()
    compounds = [serializer.instance for serializer in compound_factory.create_batch(3)]

    # Compound 1 will replace 2 and 3
    client.force_authenticate(user=admin_user)
    for compound in compounds[1:]:
        destroy_data = {
            "data": {
                "type": compound_json_type,
                "id": compound.id,
                "attributes": {
                    "replacementCid": compounds[0].cid,
                    "qcNote": f"replacing compound {compound.id} with compound {compounds[0].id}",
                },
            }
        }
        resp = client.delete(f"/{compound_json_type}s/{compound.id}", data=destroy_data)
        assert resp.status_code == 204
        deleted_compound = model.objects.with_deleted().get(pk=compound.pk)
        assert deleted_compound.replaced_by == compounds[0]
        assert (
            deleted_compound.qc_note
            == f"replacing compound {compound.id} with compound {compounds[0].id}"
        )

    # the deleted compounds should be visible to an admin user
    for endpoint in [f"{compound_json_type}s", "compounds"]:
        client.force_authenticate(user=admin_user)
        resp = client.get(f"/{endpoint}")
        cid_set = set(c["cid"] for c in resp.data["results"])
        assert len(cid_set) == 3
        # it should NOT be visible to non-admin user
        client.force_authenticate(user=user)
        resp = client.get(f"/{endpoint}")
        cid_set = set(c["cid"] for c in resp.data["results"])
        assert len(cid_set) == 1
        assert compounds[1].cid not in cid_set
        assert compounds[2].cid not in cid_set


@pytest.mark.parametrize(
    "compound_factory", [DefinedCompoundFactory, IllDefinedCompoundFactory]
)
@pytest.mark.django_db
def test_compound_forbidden_soft_delete(user, compound_factory):
    """
    Tests:
    A non-admin user cannot perform the soft-deleted done in the test above
    """
    if compound_factory == DefinedCompoundFactory:
        compound_json_type = "definedCompound"
    elif compound_factory == IllDefinedCompoundFactory:
        compound_json_type = "illDefinedCompound"
    client = APIClient()

    serializers = compound_factory.create_batch(2)
    compound_1 = serializers[0].instance
    compound_2 = serializers[1].instance

    # The standard user should not be allowed to delete the compound
    destroy_data = {
        "data": {
            "type": compound_json_type,
            "id": compound_1.id,
            "attributes": {
                "replacementCid": compound_2.cid,
                "qcNote": "replacing with another",
            },
        }
    }

    resp = client.delete(f"/{compound_json_type}s/{compound_1.id}", data=destroy_data)
    client.force_authenticate(user)
    assert resp.status_code == 403
    assert resp.data[0]["detail"].code == "not_authenticated"


@pytest.mark.parametrize(
    "compound_factory", [DefinedCompoundFactory, IllDefinedCompoundFactory]
)
@pytest.mark.django_db
def test_compound_redirect(user, admin_user, compound_factory):
    """Tests that soft-deleted compounds will redirect when non-admin."""
    if compound_factory == DefinedCompoundFactory:
        compound_json_type = "definedCompound"
    elif compound_factory == IllDefinedCompoundFactory:
        compound_json_type = "illDefinedCompound"
    client = APIClient()

    serializers = compound_factory.create_batch(3)
    compound_1 = serializers[0].instance
    compound_2 = serializers[1].instance
    compound_3 = serializers[2].instance

    # compound_2 will replace compound_3
    client.force_authenticate(user=admin_user)
    destroy_data = {
        "data": {
            "type": compound_json_type,
            "id": compound_3.id,
            "attributes": {
                "replacement_cid": compound_2.cid,
                "qc_note": "replacing with another",
            },
        }
    }
    resp = client.delete(f"/{compound_json_type}s/{compound_3.id}", data=destroy_data)
    assert resp.status_code == 204
    # compound_1 will replace compound_2
    destroy_data = {
        "data": {
            "type": compound_json_type,
            "id": compound_2.id,
            "attributes": {
                "replacement_cid": compound_1.cid,
                "qc_note": "replacing with another",
            },
        }
    }
    resp = client.delete(f"/{compound_json_type}s/{compound_2.id}", data=destroy_data)
    assert resp.status_code == 204

    for endpoint in [f"{compound_json_type}s", "compounds"]:
        # Non-admin should be redirected
        client.force_authenticate(user=user)
        resp = client.get(f"/{endpoint}/{compound_3.id}")
        assert resp.status_code == 301
        assert compound_2.id == int(resp.url.split("/")[-1])
        resp = client.get(f"/{endpoint}/{compound_2.id}")
        assert resp.status_code == 301
        assert compound_1.id == int(resp.url.split("/")[-1])

        # Admin should be able to retrieve it
        client.force_authenticate(user=admin_user)
        resp = client.get(f"/{endpoint}/{compound_3.id}")
        assert resp.status_code == 200
        resp = client.get(f"/{endpoint}/{compound_2.id}")
        assert resp.status_code == 200


@pytest.mark.django_db
def test_compound_field_exclusion(
    user, admin_user, defined_compound_factory, ill_defined_compound_factory, client
):
    """Tests that `replaced_by` and `qc_note` are only visible to admins."""
    defined_compound_factory.create()
    ill_defined_compound_factory.create()
    for compound_endpoint in ["definedCompounds", "illDefinedCompounds"]:
        for endpoint in ["compounds", compound_endpoint]:
            # Admins should see replaced_by and qc_note
            client.force_authenticate(admin_user)
            resp = client.get(f"/{endpoint}")
            for result in resp.data["results"]:
                assert "replaced_by" in result
                assert "qc_note" in result
            # Non-admins shouldn't see replaced_by and qc_note
            client.force_authenticate(user)
            resp = client.get(f"/{endpoint}")
            for result in resp.data["results"]:
                assert "replaced_by" not in result
                assert "qc_note" not in result
