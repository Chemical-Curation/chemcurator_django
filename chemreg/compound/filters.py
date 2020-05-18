from django_filters import rest_framework as filters

from chemreg.compound.models import DefinedCompound


class DefinedCompoundFilter(filters.FilterSet):
    class Meta:
        model = DefinedCompound
        fields = ["cid", "inchikey"]
