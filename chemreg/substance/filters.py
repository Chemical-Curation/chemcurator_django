from django.apps import apps
from django.db.models import Q

from django_filters import rest_framework as filters


class SubstanceRelationshipFilter(filters.FilterSet):
    """FilterSet handling substance relationships

    Attributes:
        from_substance__id (:obj: filter): Filters by the "from" substance's id
        to_substance__id (:obj:`filter`): Filters by the "to" substance's id
        to_substance__id (:obj:`filter`): Filters both "from" or "to" for references
            to this substance id
    """

    substance__id = filters.NumberFilter(method="filter_substance")

    def filter_substance(self, queryset, name, value):
        """Filters for any SubstanceRelationships containing the substance id in `value`

        Args:
            queryset: The first parameter.
            name: The name of the filter using this function
            value: The id being filtered

        Returns:
            Filtered queryset containing all SubstanceRelationships that contain the provided value
            in either the "to_substance" or "from_substance" attributes

        """
        to_substance = Q(to_substance__id=value)
        from_substance = Q(from_substance__id=value)
        return queryset.filter(to_substance | from_substance)

    class Meta:
        model = apps.get_model("substance", "SubstanceRelationship")
        fields = [
            "from_substance__id",
            "to_substance__id",
            "substance__id",
        ]
