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
        public_qc_note (str): Note from Quality Control.  Visible to everyone
        private_qc_note (str): Note from Quality Control.
        associated_compound (foreign key): ForeignKey connecting a substance to a compound
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
    """

    score_weight = models.FloatField(default=1.0)
    is_restrictive = models.BooleanField(default=False)


class Synonym(CommonInfo):
    """Information to be shared across Synonyms

    Attributes:
        identifier (str): Identifier for synonym. 1024 character limit (required)
        qc_notes (str): Quality Control note.  1024 character limit (optional)
        substance (foreign key) : Link to a Substance (optional)
        source (foreign key): Link to a Source (required)
        synonym_quality (foreign key): Link to a Synonym Quality (required)
        synonym_type (foreign key): Link to a Synonym Type (optional)
    """

    identifier = models.TextField(max_length=1024)
    qc_notes = models.TextField(max_length=1024, null=True)
    substance = models.ForeignKey("Substance", on_delete=models.PROTECT)
    source = models.ForeignKey("Source", on_delete=models.PROTECT)
    synonym_quality = models.ForeignKey("SynonymQuality", on_delete=models.PROTECT)
    synonym_type = models.ForeignKey("SynonymType", null=True, on_delete=models.PROTECT)


class RelationshipType(ControlledVocabulary):
    """Controlled vocabulary for Substances

    Attributes:
        name (str): Slug field of the relationship type (Less than 50 character, url safe, unique, required field)
        label (str): Readable string field of the relationship type (Less than 100 characters, unique, required field)
        short_description (str): Short description of the relationship type (Less than 500 characters, required field)
        long_description (str): Long description of the relationship type (required field)
        corrolary_label (str): (Less than 100 characters, unique, required field)
        corrolary_short_description (str): (Less than 500 characters, required field)
    """

    corrolary_label = models.CharField(max_length=99)
    corrolary_short_description = models.CharField(max_length=499)
