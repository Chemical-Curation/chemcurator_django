from rest_framework.exceptions import ValidationError

from rest_framework_json_api.utils import format_value


class OneOfValidator:
    """Validates that only one of the fields is included."""

    def __init__(self, *fields: str, required=True):
        """Initialize the validator.

        Args:
            *fields: The fields to check against.
            required (bool): An optional keyword argument to check that at least
                one of the fields is included.
        """

        self.fields = {f for f in fields}
        self.formatted_fields = [format_value(f) for f in sorted(fields)]
        self.required = required

    def __call__(self, data: dict):
        """Run the validation on the data."""

        matched_fields = self.fields & set(data.keys())
        formatted_matched_fields = [format_value(f) for f in sorted(matched_fields)]
        if len(matched_fields) > 1:
            raise ValidationError(
                f"Only one of {self.formatted_fields} allowed. Recieved {formatted_matched_fields}."
            )
        if self.required and len(matched_fields) == 0:
            raise ValidationError(f"One of {sorted(self.formatted_fields)} required.")
