import pytest


@pytest.mark.django_db
def test_substance_save_signal(substance_factory):
    substance_factory()


@pytest.mark.django_db
def test_synonym_save_signal(synonym_factory):
    synonym_factory()
