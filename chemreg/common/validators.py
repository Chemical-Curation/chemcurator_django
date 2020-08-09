from rest_framework.exceptions import ValidationError


def validate_deprecated(vocab):
    """Validates that the ControlledVocabulary is not deprecated.

    Args:
        vocab: the ControlledVocabulary object ("QueryStructureType", "SubstanceType")

    Raises:
        ValidationError: If the vocab is deprecated.
    """
    if vocab.deprecated:
        raise ValidationError(
            f"The {vocab._meta.object_name} submitted is no longer supported."
        )
    return vocab
