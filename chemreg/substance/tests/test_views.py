import pytest

from chemreg.substance.views import ModelViewSet, SourceViewSet, SynonymTypeViewSet


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
