import pytest

from chemreg.jsonapi.views import ModelViewSet
from chemreg.lists.views import ListTypeViewSet


def test_list_type_view():
    """Tests that the List Type View Set, is a sub class of the Model View Set."""
    assert issubclass(ListTypeViewSet, ModelViewSet)


@pytest.mark.django_db
def test_list_type_post(client, admin_user, list_type_factory):
    client.force_authenticate(user=admin_user)
    listType = list_type_factory.build()
    resp = client.post(
        "/listTypes",
        {"data": {"type": "listType", "attributes": listType.initial_data}},
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_list_type_get(client, admin_user, list_type_factory):
    client.force_authenticate(user=admin_user)
    list_type_factory.create()
    resp = client.get("/listTypes")
    assert resp.status_code == 200
    for result in resp.data["results"]:
        assert "name" in result
        assert "label" in result
        assert "short_description" in result
        assert "long_description" in result
        assert "deprecated" in result


@pytest.mark.django_db
def test_list_type_patch(client, admin_user, list_type_factory):
    client.force_authenticate(user=admin_user)
    listType = list_type_factory.create()
    pk = listType.instance.pk
    new_name = {"name": "new-name"}
    resp = client.patch(
        f"/listTypes/{pk}",
        {"data": {"id": pk, "type": "listType", "attributes": new_name}},
    )
    assert resp.status_code == 200
    assert resp.data["name"] == "new-name"
