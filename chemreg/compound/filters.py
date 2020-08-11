from django_filters import rest_framework as filters

from chemreg.compound.models import DefinedCompound
from chemreg.compound.validators import (
    validate_inchikey_computable,
    validate_molfile_v2000,
    validate_molfile_v3000,
    validate_smiles,
)
from chemreg.indigo.inchi import get_inchikey


class DefinedCompoundFilter(filters.FilterSet):
    molfile_v3000 = filters.CharFilter(method="filter_molfile_v3000", strip=False)
    molfile_v2000 = filters.CharFilter(method="filter_molfile_v2000", strip=False)
    smiles = filters.CharFilter(method="filter_smiles", strip=False)

    def filter_molfile_v3000(self, queryset, name, value):
        validate_molfile_v3000(value)
        validate_inchikey_computable(value)
        inchikey = get_inchikey(value)
        return queryset.filter(inchikey=inchikey)

    def filter_molfile_v2000(self, queryset, name, value):
        validate_molfile_v2000(value)
        validate_inchikey_computable(value)
        inchikey = get_inchikey(value)
        return queryset.filter(inchikey=inchikey)

    def filter_smiles(self, queryset, name, value):
        validate_smiles(value)
        validate_inchikey_computable(value)
        inchikey = get_inchikey(value)
        return queryset.filter(inchikey=inchikey)

    class Meta:
        model = DefinedCompound
        fields = ["cid", "inchikey", "molfile_v3000", "molfile_v2000", "smiles"]
