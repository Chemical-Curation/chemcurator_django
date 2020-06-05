from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.test import force_authenticate

import pytest

from chemreg.compound.validators import validate_inchikey_unique
from chemreg.compound.views import CompoundViewSet, DefinedCompoundViewSet
from chemreg.jsonapi.views import ReadOnlyModelViewSet


def test_definedcompound_override(api_request_factory):
    """Test that passing an override query parameter works in DefinedCompoundViewSet."""
    view = DefinedCompoundViewSet(
        action_map={"post": "create"}, kwargs={}, format_kwarg={}
    )

    view.request = view.initialize_request(
        api_request_factory.post("/definedCompounds")
    )
    for field in ("molfile_v2000", "molfile_v3000", "smiles"):
        assert (
            validate_inchikey_unique in view.get_serializer().fields[field].validators
        )

    view.request = view.initialize_request(
        api_request_factory.post("/definedCompounds?override")
    )
    assert any(isinstance(p, IsAdminUser) for p in view.get_permissions())
    for field in ("molfile_v2000", "molfile_v3000", "smiles"):
        assert (
            validate_inchikey_unique
            not in view.get_serializer().fields[field].validators
        )

    view.request = view.initialize_request(
        api_request_factory.post("/definedCompounds?overRide")
    )
    with pytest.raises(ValidationError) as err:
        view.create(view.request)
    assert err.value.status_code == 400
    assert err.value.default_code == "invalid"
    assert err.value.args[0] == "invalid query parameter: overRide"


@pytest.mark.django_db
def test_definedcompound_detail_attrs(
    user_factory, defined_compound_factory, api_request_factory
):
    """Test that detail view includes extra SerializerMethodField attributes."""
    view = DefinedCompoundViewSet.as_view({"get": "list"})
    serializer = defined_compound_factory.build()
    assert serializer.is_valid()
    compound = serializer.save()
    request = api_request_factory.get("/definedCompounds")
    user = user_factory.build()
    force_authenticate(request, user=user)
    response = view(request)
    attrs = response.data["results"].pop()
    assert list(attrs.keys()) == ["cid", "inchikey", "molfile_v3000", "url"]

    view = DefinedCompoundViewSet.as_view({"get": "retrieve"})
    request = api_request_factory.get("/definedCompounds")
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
def test_ill_defined_compound_admin_user(
    user_factory, ill_defined_compound_factory, client
):
    """Tests and Validates the outcomes of multiple POST requests performed by an
    User both with and without ADMIN permissions"""
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
def test_definedcompound_admin_user(user_factory, defined_compound_factory, client):
    """Tests and Validates the outcomes of multiple POST requests performed by an
    User both with and without ADMIN permissions"""
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
def test_query_structure_type_delete(
    user_factory, query_structure_type_factory, client
):
    """DELETE will deprecate the structure but not remove from DB"""
    qst = query_structure_type_factory.build()
    assert qst.is_valid()
    instance = qst.save()
    assert instance.deprecated is False
    user = user_factory.build()
    client.force_authenticate(user=user)
    resp = client.delete(f"/queryStructureTypes/{instance.pk}")
    assert resp.status_code == 204
    instance.refresh_from_db()
    assert instance.deprecated is True
    QueryStructureType = instance._meta.model  # should we just import this?
    assert QueryStructureType.objects.filter(pk=f"{instance.pk}").exists()


@pytest.mark.django_db
def test_deprecated_qst_in_illdefined(
    user_factory, query_structure_type_factory, ill_defined_compound_factory, client
):
    user = user_factory.build()
    client.force_authenticate(user=user)
    qst = query_structure_type_factory.build(deprecated=True)
    assert qst.is_valid()
    deprecated_structure = qst.save()
    idc = ill_defined_compound_factory.build()
    post_data = {
        "data": {
            "type": "illDefinedCompound",
            "attributes": idc.initial_data,  # mrvfile
            "relationships": {
                "query_structure_type": {
                    "data": {
                        "type": "queryStructureType",
                        "id": deprecated_structure.pk,
                    }
                },
            },
        }
    }
    response = client.post("/illDefinedCompounds", post_data)
    assert response.status_code == 400
    assert (
        str(response.data[0]["detail"])
        == "The Query Structure Type submitted for this compound is no longer supported."
    )
