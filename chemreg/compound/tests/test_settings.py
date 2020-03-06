import pytest

from chemreg.compound.settings import CompoundSettings

SETTINGS_KEYS_DEFAULTS = [("INCREMENT_START", 2000000), ("PREFIX", "DTX")]


def test_invalid_setting(settings):
    """Test that invalid setting raises an AttributeError."""
    compound_settings = CompoundSettings(settings)
    with pytest.raises(AttributeError, match="Invalid compound setting: 'INVALID_KEY'"):
        compound_settings.INVALID_KEY


@pytest.mark.parametrize("key, default", SETTINGS_KEYS_DEFAULTS)
def test_nocompound_setting(settings, key, default):
    """Test that default setting is used with no `settings.COMPOUND`."""
    if hasattr(settings, "COMPOUND"):
        del settings.COMPOUND
    compound_settings = CompoundSettings(settings)
    assert getattr(compound_settings, key) == default


@pytest.mark.parametrize("key, default", SETTINGS_KEYS_DEFAULTS)
def test_compound_setting_default(settings, key, default):
    """Test that default setting is used with no relevant `settings.COMPOUND` setting."""
    settings.COMPOUND = {"INVALID_KEY": None}
    compound_settings = CompoundSettings(settings)
    assert getattr(compound_settings, key) == default


@pytest.mark.parametrize("key, default", SETTINGS_KEYS_DEFAULTS)
def test_compound_setting_set(settings, key, default):
    """Test that setting is used from `settings.COMPOUND`."""
    settings.COMPOUND = {key: "test_key"}
    compound_settings = CompoundSettings(settings)
    assert getattr(compound_settings, key) == "test_key"
