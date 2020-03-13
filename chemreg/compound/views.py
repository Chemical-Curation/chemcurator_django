from rest_framework import viewsets

from config.pagination import DefaultPagination

from chemreg.compound.models import DefinedCompound
from chemreg.compound.serializers import DefinedCompoundSerializer


class DefinedCompoundViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `detail` ,`update`, `destroy` actions.
    """

    queryset = DefinedCompound.objects.all()
    serializer_class = DefinedCompoundSerializer
    lookup_field = "cid"
    pagination_class = DefaultPagination
