from django_filters import rest_framework as filters

from chemreg.compound.models import DefinedCompound
from chemreg.indigo.inchi import get_inchikey


class DefinedCompoundFilter(filters.FilterSet):
    molfile_v3000 = filters.CharFilter(method="filter_molfile_v3000", strip=False)

    def filter_molfile_v3000(self, queryset, name, value):
        inchikey = get_inchikey(value)
        return queryset.filter(inchikey=inchikey)

    class Meta:
        model = DefinedCompound
        fields = ["cid", "inchikey", "molfile_v3000"]
