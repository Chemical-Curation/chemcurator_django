import pytest

from chemreg.jsonapi.views import ModelViewSet
from chemreg.lists.views import AccessibilityTypeViewSet, ListTypeViewSet


def test_list_type_view():
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


def test_accessibility_type_view():
    """Tests that the Accessibility Type View Set, is a sub class of the Model View Set."""
    assert issubclass(AccessibilityTypeViewSet, ModelViewSet)


@pytest.mark.django_db
def test_accessibility_type_post(client, admin_user, accessibility_type_factory):
    client.force_authenticate(user=admin_user)
    accessibilityType = accessibility_type_factory.build()
    resp = client.post(
        "/accessibilityTypes",
        {
            "data": {
                "type": "accessibilityType",
                "attributes": accessibilityType.initial_data,
            }
        },
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_accessibility_type_get(client, admin_user, accessibility_type_factory):
    client.force_authenticate(user=admin_user)
    accessibility_type_factory.create()
    resp = client.get("/accessibilityTypes")
    assert resp.status_code == 200
    for result in resp.data["results"]:
        assert "name" in result
        assert "label" in result
        assert "short_description" in result
        assert "long_description" in result
        assert "deprecated" in result


@pytest.mark.django_db
def test_accessibility_type_patch(client, admin_user, accessibility_type_factory):
    client.force_authenticate(user=admin_user)
    accessibilityType = accessibility_type_factory.create()
    pk = accessibilityType.instance.pk
    new_name = {"name": "new-name"}
    resp = client.patch(
        f"/accessibilityTypes/{pk}",
        {"data": {"id": pk, "type": "accessibilityType", "attributes": new_name}},
    )
    assert resp.status_code == 200
    assert resp.data["name"] == "new-name"


def test_identifier_type_view():
    assert issubclass(ListTypeViewSet, ModelViewSet)


@pytest.mark.django_db
def test_identifier_type_post(client, admin_user, identifier_type_factory):
    client.force_authenticate(user=admin_user)
    identifierType = identifier_type_factory.build()
    resp = client.post(
        "/identifierTypes",
        {"data": {"type": "identifierType", "attributes": identifierType.initial_data}},
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_identifier_type_get(client, admin_user, identifier_type_factory):
    client.force_authenticate(user=admin_user)
    identifier_type_factory.create()
    resp = client.get("/identifierTypes")
    assert resp.status_code == 200
    for result in resp.data["results"]:
        assert "name" in result
        assert "label" in result
        assert "short_description" in result
        assert "long_description" in result
        assert "deprecated" in result


@pytest.mark.django_db
def test_identifier_type_patch(client, admin_user, identifier_type_factory):
    client.force_authenticate(user=admin_user)
    identifierType = identifier_type_factory.create()
    pk = identifierType.instance.pk
    new_name = {"name": "new-name"}
    resp = client.patch(
        f"/identifierTypes/{pk}",
        {"data": {"id": pk, "type": "identifierType", "attributes": new_name}},
    )
    assert resp.status_code == 200
    assert resp.data["name"] == "new-name"


@pytest.mark.django_db
def test_list_post(client, admin_user, list_factory, list_type_factory, user_factory):
    client.force_authenticate(user=admin_user)
    lf = list_factory.build().initial_data
    resp = client.post(
        "/lists",
        {
            "data": {
                "type": "list",
                "attributes": lf,
                "relationships": {
                    "accessibilityType": {
                        "data": {
                            "id": lf["list_accessibility"]["id"],
                            "type": "accessibilityType",
                        }
                    },
                    "externalContact": {
                        "data": {
                            "id": lf["external_contact"]["id"],
                            "type": "externalContact",
                        }
                    },
                    "user": {"data": {"id": user_factory().pk, "type": "user"}},
                    "listType": {
                        "data": {
                            "id": list_type_factory().instance.pk,
                            "type": "listType",
                        }
                    },
                },
            }
        },
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_list_get(client, admin_user, list_factory):
    client.force_authenticate(user=admin_user)
    list_factory()
    resp = client.get("/lists")
    assert resp.status_code == 200
    # Check that all results contain
    for result in resp.data["results"]:
        assert "name" in result
        assert "label" in result
        assert "short_description" in result
        assert "long_description" in result
        assert "list_accessibility" in result
        assert "owners" in result
        assert "source_url" in result
        assert "source_reference" in result
        assert "external_contact" in result
        assert "date_of_source_collection" in result
        assert "types" in result


@pytest.mark.django_db
def test_record_post(client, admin_user, record_factory):
    client.force_authenticate(user=admin_user)
    rf = record_factory.build().initial_data
    resp = client.post(
        "/records",
        {
            "data": {
                "type": "record",
                "attributes": rf,
                "relationships": {
                    "list": {"data": {"id": rf["list"]["id"], "type": "list"}},
                    "substance": {
                        "data": {"id": rf["substance"]["id"], "type": "substance"}
                    },
                },
            }
        },
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_record_get(client, admin_user, record_factory):
    client.force_authenticate(user=admin_user)
    record_factory()
    resp = client.get("/records")
    assert resp.status_code == 200
    # Check that all results contain
    for result in resp.data["results"]:
        assert "rid" in result
        assert "external_id" in result
        assert "list" in result
        assert "substance" in result
        assert "score" in result
        assert "message" in result
        assert "is_validated" in result


@pytest.mark.django_db
def test_record_identifer_post(
    client, admin_user, record_identifier_factory, record_factory
):
    client.force_authenticate(user=admin_user)
    rif = record_identifier_factory.build().initial_data
    resp = client.post(
        "/recordIdentifiers",
        {
            "data": {
                "type": "recordIdentifier",
                "attributes": rif,
                "relationships": {
                    "identifier_type": {
                        "data": {
                            "id": rif["identifier_type"]["id"],
                            "type": "identifierType",
                        }
                    },
                    "record": {
                        "data": {"id": record_factory().instance.pk, "type": "record"}
                    },
                },
            }
        },
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_record_identifier_get(client, admin_user, record_identifier_factory):
    client.force_authenticate(user=admin_user)
    record_identifier_factory()
    resp = client.get("/recordIdentifiers")
    assert resp.status_code == 200
    # Check that all results contain
    for result in resp.data["results"]:
        assert "record" in result
        assert "identifier" in result
        assert "identifier_type" in result
        assert "identifier_label" in result
