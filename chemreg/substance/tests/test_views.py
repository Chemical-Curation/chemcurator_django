import pytest

from chemreg.substance.views import ModelViewSet, SourceViewSet, SynonymTypeViewSet


@pytest.mark.django_db
def test_qc_levels_type_post(client, admin_user, qc_levels_type_factory):
    client.force_authenticate(user=admin_user)
    model_dict = qc_levels_type_factory.build()
    resp = client.post(
        "/qcLevels",
        {"data": {"type": "qcLevel", "attributes": model_dict.initial_data}},
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_qc_levels_type_list(client, admin_user, qc_levels_type_factory):
    client.force_authenticate(user=admin_user)
    qc_levels_type_factory.create()
    resp = client.get("/qcLevels")
    assert resp.status_code == 200
    for result in resp.data["results"]:
        assert "name" in result
        assert "label" in result
        assert "short_description" in result
        assert "long_description" in result
        assert "rank" in result


@pytest.mark.django_db
def test_qc_levels_type_fetch(client, admin_user, qc_levels_type_factory):
    client.force_authenticate(user=admin_user)
    original_model = qc_levels_type_factory.create().instance
    resp = client.get("/qcLevels/{}".format(original_model.pk))
    assert resp.status_code == 200
    for key in resp.data.keys() - {"url"}:
        assert resp.data[key] == getattr(original_model, key)


@pytest.mark.django_db
def test_qc_levels_type_patch(client, admin_user, qc_levels_type_factory):
    client.force_authenticate(user=admin_user)
    original_model = qc_levels_type_factory.create().instance
    model_dict = qc_levels_type_factory.build().initial_data
    resp = client.patch(
        "/qcLevels/{}".format(original_model.pk),
        {
            "data": {
                "type": "qcLevel",
                "id": original_model.pk,
                "attributes": model_dict,
            }
        },
    )
    assert resp.status_code == 200
    for key in resp.data.keys() - {"url"}:
        assert resp.data[key] == model_dict[key]


@pytest.mark.django_db
def test_qc_levels_type_delete(client, admin_user, qc_levels_type_factory):
    client.force_authenticate(user=admin_user)
    original_model = qc_levels_type_factory.create().instance
    resp = client.delete("/qcLevels/{}".format(original_model.pk))
    assert resp.status_code == 204
    with pytest.raises(original_model.DoesNotExist):
        original_model.refresh_from_db()


def test_synonym_type_view():
    """Tests that the Synonym Type View Set, is a sub class of the Model View Set."""
    assert issubclass(SynonymTypeViewSet, ModelViewSet)


@pytest.mark.django_db
def test_synonym_type_post(client, admin_user, synonym_type_factory):
    client.force_authenticate(user=admin_user)
    stf = synonym_type_factory.build()
    resp = client.post(
        "/synonymTypes",
        {"data": {"type": "synonymType", "attributes": stf.initial_data}},
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_synonym_type_get(client, admin_user, synonym_type_factory):
    client.force_authenticate(user=admin_user)
    synonym_type_factory.create()
    resp = client.get("/synonymTypes")
    assert resp.status_code == 200
    for result in resp.data["results"]:
        assert "name" in result
        assert "label" in result
        assert "short_description" in result
        assert "long_description" in result
        assert "score_modifier" in result


def test_source_view():
    """Tests that the Source View Set, is a sub class of the Model View Set."""
    assert issubclass(SourceViewSet, ModelViewSet)


@pytest.mark.django_db
def test_source_post(client, admin_user, source_factory):
    client.force_authenticate(user=admin_user)
    stf = source_factory.build()
    resp = client.post(
        "/sources", {"data": {"type": "source", "attributes": stf.initial_data}},
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_source_get(client, admin_user, source_factory):
    client.force_authenticate(user=admin_user)
    source_factory.create()
    resp = client.get("/sources")
    assert resp.status_code == 200
    for result in resp.data["results"]:
        assert "name" in result
        assert "label" in result
        assert "short_description" in result
        assert "long_description" in result


@pytest.mark.django_db
def test_source_patch(client, admin_user, source_factory):
    client.force_authenticate(user=admin_user)
    source = source_factory.create()
    pk = source.instance.pk
    new_name = {"name": "a-new-name"}
    resp = client.patch(
        f"/sources/{pk}",
        {"data": {"id": pk, "type": "source", "attributes": new_name}},
    )
    assert resp.status_code == 200
    assert resp.data["name"] == "a-new-name"
