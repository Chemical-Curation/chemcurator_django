from django.conf import settings


class SubstanceSettings:
    """Loads the Substance app settings from the main settings.

    This centralizes the logic of user modifiable global variables. It
    looks for a `django.conf.settings.SUBSTANCE` dictionary and uses the
    setting found there if it exists. Otherwise, it falls back to defaults
    defined in the `SubstanceSettings.defaults` class attribute.

    Attributes:
        defaults (dict): The default settings to fallback to.
        INCREMENT_START (int): Added to the substance primary key to derive
            the SID. Defaults to 2,000,000.
        PREFIX (str): The prefix to place in the SID. Defaults to "DTX".
        SEQUENCE_KEY (bool): The cache key to store the sequence under.

    """

    defaults = {
        "INCREMENT_START": 2000000,
        "PREFIX": "DTX",
        "SEQUENCE_KEY": "substance_seq",
    }

    def __init__(self, user_settings):
        self.user_settings = user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f"Invalid compound setting: '{attr}'")
        if (
            hasattr(self.user_settings, "SUBSTANCE")
            and attr in self.user_settings.SUBSTANCE
        ):
            val = self.user_settings.SUBSTANCE[attr]
        else:
            val = self.defaults[attr]

        setattr(self, attr, val)
        return val


substance_settings = SubstanceSettings(settings)
"""The singleton instance of SubstanceSettings."""
