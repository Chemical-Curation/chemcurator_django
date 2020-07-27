from chemreg.common.models import ControlledVocabulary


class IdentifierType(ControlledVocabulary):
    """Controlled vocabulary for Sources

    Attributes:
        name (str): Less than 50 character, url safe, unique, (required)
        label (str): Less than 100 characters, unique, (required)
        short_description (str): Less than 500 characters, (required)
        long_description (str): Text (required)
    """

    pass
