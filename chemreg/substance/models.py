from django.db import models

from chemreg.common.models import CommonInfo, ControlledVocabulary
from chemreg.substance.utils import build_sid


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

    class JSONAPIMeta:
        resource_name = "qcLevel"


class Source(ControlledVocabulary):
    """Controlled vocabulary for Sources

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
    """

    pass


class Substance(CommonInfo):
    """Substances document chemical concepts

    Attributes:
        substance_id (str): Generated SID for external use
        preferred_name (str): Name of the substance
        display_name (str): User friendly name of the substance
        source (foreign key): ForeignKey
        substance_type (foreign key): Controlled vocabulary for Substances
        qc_level (foreign key): ForeignKey
        description (str): A description of the substance
        public_qc_note (str): unknown
        private_qc_note (str): unknown
        associated_compound (foreign key): ForeignKey
        casrn (str): CAS registry number. It is an identifier from the CAS Registry
            (https://www.cas.org/support/documentation/chemical-substances) for a chemical substance.
        synonyms (QuerySet): One to Many Synonym resources
        substance_histories (QuerySet): Many to Many Substance history resources (not implemented yet)
    """

    sid = models.CharField(default=build_sid, max_length=50, unique=True)
    preferred_name = models.CharField(max_length=255, unique=True, blank=False)
    display_name = models.CharField(max_length=255, unique=True, blank=False)
    source = models.ForeignKey("Source", on_delete=models.PROTECT, null=False)
    substance_type = models.ForeignKey(
        "SubstanceType", on_delete=models.PROTECT, null=False
    )
    qc_level = models.ForeignKey("QCLevelsType", on_delete=models.PROTECT, null=False)
    description = models.CharField(max_length=1024)
    public_qc_note = models.CharField(max_length=1024)
    private_qc_note = models.CharField(max_length=1024)
    associated_compound = models.ForeignKey(
        "compound.BaseCompound", on_delete=models.PROTECT, null=True
    )
    casrn = models.CharField(max_length=50, unique=True)


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
    """Controlled vocabulary for SynonymTypes

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
    is_restrictive = models.BooleanField(default=False)


class Synonym(CommonInfo):
    """Information to be shared across Synonyms

    Attributes:
        Identifier = String (1024)) (required)
        Synonym Quality (required)
        Source (required)
        Synonym Type (optional)
        qc_notes = String (1024) (optional)
    """

    substance = models.ForeignKey("Substance", on_delete=models.PROTECT)
    identifier = models.TextField(max_length=1024)
    synonym_quality = models.ForeignKey(SynonymQuality, on_delete=models.PROTECT)
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    synonym_type = models.ForeignKey(SynonymType, null=True, on_delete=models.PROTECT)
    qc_notes = models.TextField(max_length=1024, null=True)


class RelationshipType(ControlledVocabulary):
    """Controlled vocabulary for Substances

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
        corrolary label = String (Less than 100 characters, unique, required field)
        corrolary short description = String (Less than 500 characters, required field)
    """

    corrolary_label = models.CharField(max_length=99)
    corrolary_short_description = models.CharField(max_length=499)
