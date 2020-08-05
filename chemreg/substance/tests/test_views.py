import json
from collections import OrderedDict

from django.contrib.auth.models import Permission

import pytest
from rest_framework_json_api.utils import get_included_serializers

from chemreg.substance.serializers import SubstanceSerializer
from chemreg.substance.views import (
    ModelViewSet,
    RelationshipTypeViewSet,
    SourceViewSet,
    SubstanceRelationshipViewSet,
    SubstanceTypeViewSet,
    SynonymQualityViewSet,
    SynonymTypeViewSet,
)
from chemreg.users.models import User


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
        assert "deprecated" in result


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
    qcl = qc_levels_type_factory.create()
    assert qcl.instance.deprecated is False
    client.force_authenticate(user=admin_user)
    resp = client.delete(f"/qcLevels/{qcl.instance.pk}")
    assert resp.status_code == 204
    qcl.instance.refresh_from_db()
    assert qcl.instance.deprecated is True
    QcLevelsType = qcl.instance._meta.model
    assert QcLevelsType.objects.filter(pk=f"{qcl.instance.pk}").exists()


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
        assert "deprecated" in result


@pytest.mark.django_db
def test_synonym_type_delete(admin_user, client, synonym_type_factory):
    """DELETE will deprecate the record but not remove from DB"""
    stf = synonym_type_factory.create()
    assert stf.instance.deprecated is False
    client.force_authenticate(user=admin_user)
    resp = client.delete(f"/synonymTypes/{stf.instance.pk}")
    assert resp.status_code == 204
    stf.instance.refresh_from_db()
    assert stf.instance.deprecated is True
    SynonymType = stf.instance._meta.model
    assert SynonymType.objects.filter(pk=f"{stf.instance.pk}").exists()


def test_source_view():
    """Tests that the Source View Set, is a sub class of the Model View Set."""
    assert issubclass(SourceViewSet, ModelViewSet)


@pytest.mark.django_db
def test_source_post(client, admin_user, source_factory):
    client.force_authenticate(user=admin_user)
    source = source_factory.build()
    resp = client.post(
        "/sources", {"data": {"type": "source", "attributes": source.initial_data}},
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
        assert "deprecated" in result


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


@pytest.mark.django_db
def test_source_delete(admin_user, client, source_factory):
    """DELETE will deprecate the record but not remove from DB"""
    source = source_factory.create()
    assert source.instance.deprecated is False
    client.force_authenticate(user=admin_user)
    resp = client.delete(f"/sources/{source.instance.pk}")
    assert resp.status_code == 204
    source.instance.refresh_from_db()
    assert source.instance.deprecated is True
    Source = source.instance._meta.model
    assert Source.objects.filter(pk=f"{source.instance.pk}").exists()


@pytest.mark.django_db
def test_substance_post(client, admin_user, substance_factory):
    client.force_authenticate(user=admin_user)
    model_dict = substance_factory.build(defined=True).initial_data
    resp = client.post(
        "/substances",
        {
            "data": {
                "type": "substance",
                "attributes": model_dict,
                "relationships": {
                    "qcLevel": {
                        "data": {"id": model_dict["qc_level"]["id"], "type": "qcLevel"}
                    },
                    "source": {
                        "data": {"id": model_dict["source"]["id"], "type": "source"}
                    },
                    "substanceType": {
                        "data": {
                            "id": model_dict["substance_type"]["id"],
                            "type": "substanceType",
                        }
                    },
                    "associatedCompound": {
                        "data": {
                            "id": model_dict["associated_compound"]["id"],
                            "type": "definedCompound",
                        }
                    },
                },
            }
        },
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_required_subresource_not_specified(client, admin_user, substance_factory):
    client.force_authenticate(user=admin_user)
    model_dict = substance_factory.build(defined=True).initial_data
    model_dict.pop("qc_level")
    resp = client.post(
        "/substances",
        {
            "data": {
                "type": "substance",
                "attributes": model_dict,
                "relationships": {
                    "source": {
                        "data": {"id": model_dict["source"]["id"], "type": "source"}
                    },
                    "substanceType": {
                        "data": {
                            "id": model_dict["substance_type"]["id"],
                            "type": "substanceType",
                        }
                    },
                    "associatedCompound": {
                        "data": {
                            "id": model_dict["associated_compound"]["id"],
                            "type": "definedCompound",
                        }
                    },
                },
            }
        },
    )
    assert resp.status_code == 400
    assert str(resp.data[0]["detail"]) == "This field is required."
    assert resp.data[0]["source"]["pointer"] == "/data/attributes/qcLevel"


@pytest.mark.django_db
def test_required_subresource_deprecated(
    client, admin_user, substance_factory, qc_levels_type_factory
):
    client.force_authenticate(user=admin_user)
    qc_level = qc_levels_type_factory.create().instance
    qc_level.deprecated = True
    qc_level.save()
    model_dict = substance_factory.build(defined=True).initial_data
    resp = client.post(
        "/substances",
        {
            "data": {
                "type": "substance",
                "attributes": model_dict,
                "relationships": {
                    "qcLevel": {"data": {"id": f"{qc_level.pk}", "type": "qcLevel"}},
                    "source": {
                        "data": {"id": model_dict["source"]["id"], "type": "source"}
                    },
                    "substanceType": {
                        "data": {
                            "id": model_dict["substance_type"]["id"],
                            "type": "substanceType",
                        }
                    },
                    "associatedCompound": {
                        "data": {
                            "id": model_dict["associated_compound"]["id"],
                            "type": "definedCompound",
                        }
                    },
                },
            }
        },
    )
    assert resp.status_code == 400
    assert (
        str(resp.data[0]["detail"])
        == "The QCLevelsType submitted is no longer supported."
    )
    assert resp.data[0]["source"]["pointer"] == "/data/attributes/qcLevel"


@pytest.mark.django_db
def test_substance_list(client, admin_user, substance_factory):
    client.force_authenticate(user=admin_user)
    substance_factory()
    resp = client.get("/substances")
    assert resp.status_code == 200
    # Check that all results contain
    for result in resp.data["results"]:
        assert "sid" in result
        assert "preferred_name" in result
        assert "display_name" in result
        assert "description" in result
        assert "public_qc_note" in result
        assert "private_qc_note" in result
        assert "casrn" in result
        assert "source" in result
        assert "substance_type" in result
        assert "qc_level" in result
        assert "associated_compound" in result


@pytest.mark.django_db
def test_substance_fetch(client, admin_user, substance_factory):
    client.force_authenticate(user=admin_user)
    original_model = substance_factory.create(illdefined=True).instance
    resp = client.get("/substances/{}".format(original_model.pk))
    assert resp.status_code == 200
    for key in resp.data.keys() - {"url"}:
        # Verify Attributes
        if isinstance(resp.data[key], str):
            assert resp.data[key] == getattr(original_model, key)
        # Verify Related Resources
        elif type(resp.data[key]) is OrderedDict:
            assert resp.data[key]["id"] == str(getattr(original_model, key).id)


@pytest.mark.django_db
def test_substance_fetch_includes(client, admin_user, substance_factory):
    client.force_authenticate(user=admin_user)
    model = substance_factory(illdefined=True).instance
    requested_includes = get_included_serializers(SubstanceSerializer)
    resp = client.get(
        "/substances/{}".format(model.pk),
        data={"include": ",".join(requested_includes)},
    )
    assert resp.status_code == 200
    response_included = json.loads(resp.content.decode("utf-8"))["included"]
    # Assert there is an include resource for every requested include
    assert len(requested_includes) == len(response_included)


@pytest.mark.django_db
def test_substance_patch(client, admin_user, substance_factory):
    client.force_authenticate(user=admin_user)
    original_model = substance_factory.create(defined=True).instance
    model_dict = substance_factory.build(illdefined=True).initial_data
    model_dict.update(sid="DTXSID205000001")
    resp = client.patch(
        "/substances/{}".format(original_model.pk),
        {
            "data": {
                "type": "substance",
                "id": original_model.pk,
                "attributes": model_dict,
                "relationships": {
                    "qcLevel": {
                        "data": {"id": model_dict["qc_level"]["id"], "type": "qcLevel"}
                    },
                    "source": {
                        "data": {"id": model_dict["source"]["id"], "type": "source"}
                    },
                    "substanceType": {
                        "data": {
                            "id": model_dict["substance_type"]["id"],
                            "type": "substanceType",
                        }
                    },
                    "associatedCompound": {
                        "data": {
                            "id": model_dict["associated_compound"]["id"],
                            "type": "definedCompound",
                        }
                    },
                },
            }
        },
    )
    original_model.refresh_from_db()
    assert resp.status_code == 200
    for key in resp.data.keys() - {"url"}:
        # Verify Attributes
        if isinstance(resp.data[key], str):
            assert resp.data[key] == model_dict[key]
        # Verify Related Resources
        elif type(resp.data[key]) is OrderedDict:
            assert resp.data[key]["id"] == model_dict[key]["id"]


@pytest.mark.django_db
def test_substance_delete(client, admin_user, substance_factory):
    client.force_authenticate(user=admin_user)
    original_model = substance_factory.create().instance
    resp = client.delete("/substances/{}".format(original_model.pk))
    assert resp.status_code == 204
    with pytest.raises(original_model.DoesNotExist):
        original_model.refresh_from_db()


def test_substance_type_view():
    """Tests that the Substance Type View Set, is a sub class of the Model View Set."""
    assert issubclass(SubstanceTypeViewSet, ModelViewSet)


@pytest.mark.django_db
def test_substance_type_post(client, admin_user, substance_type_factory):
    client.force_authenticate(user=admin_user)
    stf = substance_type_factory.build()
    resp = client.post(
        "/substanceTypes",
        {"data": {"type": "substanceType", "attributes": stf.initial_data}},
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_substance_type_get(client, admin_user, substance_type_factory):
    client.force_authenticate(user=admin_user)
    substance_type_factory.create()
    resp = client.get("/substanceTypes")
    assert resp.status_code == 200
    assert resp.data["results"]
    for result in resp.data["results"]:
        assert "name" in result
        assert "label" in result
        assert "short_description" in result
        assert "long_description" in result
        assert "deprecated" in result


def test_relationship_type_view():
    """Tests that the Source View Set, is a sub class of the Model View Set."""
    assert issubclass(RelationshipTypeViewSet, ModelViewSet)


@pytest.mark.django_db
def test_relationship_type_create(client, admin_user, relationship_type_factory):
    client.force_authenticate(user=admin_user)
    stf = relationship_type_factory.build()
    resp = client.post(
        "/relationshipTypes",
        {"data": {"type": "relationshipType", "attributes": stf.initial_data}},
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_relationship_type_list(client, admin_user, relationship_type_factory):
    client.force_authenticate(user=admin_user)
    relationship_type_factory.create()
    resp = client.get("/relationshipTypes")
    assert resp.status_code == 200
    assert resp.data["results"]
    for result in resp.data["results"]:
        assert "name" in result
        assert "label" in result
        assert "short_description" in result
        assert "long_description" in result
        assert "corrolary_label" in result
        assert "corrolary_short_description" in result
        assert "deprecated" in result


@pytest.mark.django_db
def test_relationship_type_fetch(client, admin_user, relationship_type_factory):
    client.force_authenticate(user=admin_user)
    original_model = relationship_type_factory.create().instance
    resp = client.get("/relationshipTypes/{}".format(original_model.pk))
    assert resp.status_code == 200
    for key in resp.data.keys() - {"url"}:
        # Verify Attributes
        if isinstance(resp.data[key], str):
            assert resp.data[key] == getattr(original_model, key)


@pytest.mark.django_db
def test_relationship_type_patch(client, admin_user, relationship_type_factory):
    client.force_authenticate(user=admin_user)
    original_model = relationship_type_factory.create().instance
    model_dict = relationship_type_factory.build().initial_data
    model_dict.update(sid="DTXSID205000001")
    resp = client.patch(
        "/relationshipTypes/{}".format(original_model.pk),
        {
            "data": {
                "type": "relationshipType",
                "id": original_model.pk,
                "attributes": model_dict,
            }
        },
    )
    assert resp.status_code == 200
    for key in resp.data.keys() - {"url"}:
        # Verify Attributes
        if isinstance(resp.data[key], str):
            assert resp.data[key] == model_dict[key]


@pytest.mark.django_db
def test_relationship_type_delete(client, admin_user, relationship_type_factory):
    rt = relationship_type_factory.create()
    assert rt.instance.deprecated is False
    client.force_authenticate(user=admin_user)
    resp = client.delete(f"/relationshipTypes/{rt.instance.pk}")
    assert resp.status_code == 204
    rt.instance.refresh_from_db()
    assert rt.instance.deprecated is True
    RelationshipType = rt.instance._meta.model
    assert RelationshipType.objects.filter(pk=f"{rt.instance.pk}").exists()


def test_synonym_quality_view():
    """Tests that the Synonym Quality View Set, is a sub class of the Model View Set."""
    assert issubclass(SynonymQualityViewSet, ModelViewSet)


@pytest.mark.django_db
def test_synonym_quality_post(client, admin_user, synonym_quality_factory):
    client.force_authenticate(user=admin_user)
    stf = synonym_quality_factory.build()
    resp = client.post(
        "/synonymQualities",
        {"data": {"type": "synonymQuality", "attributes": stf.initial_data}},
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_synonym_quality_get(client, admin_user, synonym_quality_factory):
    client.force_authenticate(user=admin_user)
    synonym_quality_factory.create()
    resp = client.get("/synonymQualities")
    assert resp.status_code == 200
    assert resp.data["results"]
    for result in resp.data["results"]:
        assert "name" in result
        assert "label" in result
        assert "short_description" in result
        assert "long_description" in result
        assert "score_weight" in result
        assert "is_restrictive" in result
        assert "deprecated" in result


@pytest.mark.django_db
def test_synonym_post(client, admin_user, synonym_factory):
    client.force_authenticate(user=admin_user)
    sf = synonym_factory.build().initial_data
    resp = client.post(
        "/synonyms",
        {
            "data": {
                "type": "synonym",
                "attributes": sf,
                "relationships": {
                    "source": {"data": {"id": sf["source"]["id"], "type": "source"}},
                    "synonymQuality": {
                        "data": {
                            "id": sf["synonym_quality"]["id"],
                            "type": "synonymQuality",
                        }
                    },
                    "synonymType": {
                        "data": {"id": sf["synonym_type"]["id"], "type": "synonymType"}
                    },
                },
            }
        },
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_synonym_list(client, admin_user, synonym_factory):
    client.force_authenticate(user=admin_user)
    synonym_factory.create()
    resp = client.get("/synonyms")
    assert resp.status_code == 200
    # Check that all results contain
    for result in resp.data["results"]:
        assert "identifier" in result
        assert "qc_notes" in result
        assert "source" in result
        assert "substance" in result
        assert "synonym_quality" in result
        assert "synonym_type" in result


@pytest.mark.django_db
def test_intermediate_user_access(client, admin_user, synonym_type_factory):
    """Tests that a non-admin user can only perform the allowed
    operations that have been specified in the admin panel
    DELETE https://api.chemreg.epa.gov/synonym-types/{id}
        user.has_perm(‘foo.delete_bar’)
    PATCH https://api.chemreg.epa.gov/synonym-types/{id}
        user.has_perm(‘foo.change_bar’)
    """

    client.force_authenticate(user=admin_user)
    stf = synonym_type_factory.build()
    resp = client.post(
        "/synonymTypes",
        {"data": {"type": "synonymType", "attributes": stf.initial_data}},
    )
    assert resp.status_code == 201
    json_data = json.loads(resp.content)
    st_url = json_data["data"]["links"]["self"]

    # make a new non-admin user
    mook = User.objects.create_user("mook", "mook_user@epa.gov", "mookpassword")
    permission = Permission.objects.get(codename="view_synonymtype",)
    mook.user_permissions.add(permission)
    client.force_authenticate(user=mook)

    # the user should be able to see the record
    resp = client.get(st_url)
    assert resp.status_code == 200

    # test that the attempt to create a new record fails
    stf = synonym_type_factory.build()
    resp = client.post(
        "/synonymTypes",
        {"data": {"type": "synonymType", "attributes": stf.initial_data}},
    )
    assert resp.status_code == 403


@pytest.mark.django_db
def test_intermediate_user_post(client, admin_user, synonym_type_factory):
    """Tests that a non-admin user can only perform a valid POST request
        POST https://api.chemreg.epa.gov/synonym-types
        user.has_perm(‘foo.add_bar’)
    """

    mook = User.objects.create_user("mook", "mook_user@epa.gov", "mookpassword")
    permission = Permission.objects.get(codename="add_synonymtype",)
    mook.user_permissions.add(permission)

    client.force_authenticate(user=mook)
    if hasattr(mook, "_perm_cache"):
        delattr(mook, "_perm_cache")

    stf = synonym_type_factory.build()
    resp = client.post(
        "/synonymTypes",
        {"data": {"type": "synonymType", "attributes": stf.initial_data}},
    )
    assert resp.status_code == 201


def test_substance_relationship_view():
    """Tests that the Substance Relationship View Set, is a sub class of the Model View Set."""
    assert issubclass(SubstanceRelationshipViewSet, ModelViewSet)


@pytest.mark.django_db
def test_substance_relationship_list(
    client, admin_user, substance_relationship_factory
):
    client.force_authenticate(user=admin_user)
    substance_relationship_factory.create()
    resp = client.get("/substanceRelationships")
    assert resp.status_code == 200
    # Check that all results contain
    for result in resp.data["results"]:
        assert "qc_notes" in result
        assert "source" in result
        assert "to_substance" in result
        assert "from_substance" in result
        assert "relationship_type" in result


@pytest.mark.django_db
def test_substance_relationship_post(
    client, admin_user, substance_relationship_factory
):
    client.force_authenticate(user=admin_user)
    srf = substance_relationship_factory.build().initial_data
    resp = client.post(
        "/substanceRelationships",
        {
            "data": {
                "type": "substanceRelationship",
                "attributes": srf,
                "relationships": {
                    "from_substance": {
                        "data": {"id": srf["from_substance"]["id"], "type": "substance"}
                    },
                    "to_substance": {
                        "data": {"id": srf["to_substance"]["id"], "type": "substance"}
                    },
                    "source": {"data": {"id": srf["source"]["id"], "type": "source"}},
                    "relationship_type": {
                        "data": {
                            "id": srf["relationship_type"]["id"],
                            "type": "relationshipType",
                        }
                    },
                },
            }
        },
    )
    assert resp.status_code == 201
