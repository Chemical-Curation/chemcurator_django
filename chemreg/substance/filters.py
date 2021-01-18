from django.apps import apps
from django.db.models import Q

from django_filters import rest_framework as filters

from chemreg.resolution.indices import SubstanceIndex


class SubstanceFilter(filters.FilterSet):

    search = filters.CharFilter(method="search_resolver")

    def search_resolver(self, queryset, name, value):
        """Search resolver for the search value"""
        resp_json = SubstanceIndex().search(value)
        ids = [row["id"] for row in resp_json["data"]]
        # todo: This will need some reason + score annotating
        qs = queryset.filter(pk__in=ids)

        for obj in qs:
            row = resp_json["data"][ids.index(obj.pk)]
            obj.matches = row["attributes"]["matches"]
            obj.score = row["attributes"]["score"]

        return qs

    class Meta:
        model = apps.get_model("substance", "Substance")
        fields = ["search"]


class SubstanceRelationshipFilter(filters.FilterSet):
    """FilterSet handling substance relationships

    Attributes:
        from_substance__id (:obj: filter): Filters by the "from" substance's id
        to_substance__id (:obj:`filter`): Filters by the "to" substance's id
        to_substance__id (:obj:`filter`): Filters both "from" or "to" for references
            to this substance id
    """

    substance__id = filters.CharFilter(method="filter_substance")

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
