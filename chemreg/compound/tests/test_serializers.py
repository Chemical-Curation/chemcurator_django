import re

import pytest


@pytest.mark.django_db
def test_defined_compound(defined_compound_factory):
    serializer = defined_compound_factory.build()
    assert serializer.is_valid()
    instance = serializer.save()
    # test inchikey creation
    assert "inchikey" not in serializer.initial_data
    assert re.match(r"^[A-Z]{14}-[A-Z]{10}-[A-Z]$", instance.inchikey)


@pytest.mark.django_db
def test_ill_defined_compound(ill_defined_compound_factory):
    serializer = ill_defined_compound_factory.build()
    assert serializer.is_valid()
    instance = serializer.save()
    # test default querystructuretype
    assert "query_structure_type" not in serializer.initial_data
    assert instance.query_structure_type.name == "ill-defined"


@pytest.mark.django_db
def test_query_structure_type(query_structure_type_factory):
    serializer = query_structure_type_factory.build()
    assert serializer.is_valid()
    serializer.save()
