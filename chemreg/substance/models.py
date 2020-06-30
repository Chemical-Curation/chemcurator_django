from django.db import models

from chemreg.common.models import ControlledVocabulary


class Source(ControlledVocabulary):
    """Controlled vocabulary for Sources

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
    """

    pass


class SubstanceType(ControlledVocabulary):
    """Controlled vocabulary for Substances

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
    """

    pass


class SynonymType(ControlledVocabulary):
    """Controlled vocabulary for Synonyms

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
        Validation Regular Expression = String (not required)
        Score modifier = Float (default 0)
    """

    validation_regular_expression = models.TextField(blank=True)
    score_modifier = models.FloatField(default=0)


class QCLevelsType(ControlledVocabulary):
    """Controlled vocabulary for qc_levels

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
        rank = integer unique
    """

    rank = models.IntegerField(unique=True)


class SynonymQuality(ControlledVocabulary):
    """Controlled vocabulary for SynonymQuality

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
        score_weight = Float (default 1.0) greater than 0
        is_restrictive = Boolean
    TODO: Add Validation in Serializer for score_weight, unable to set minimum value for FloatField's
    """

    score_weight = models.FloatField(default=1.0)
    is_restrictive = models.BooleanField()
