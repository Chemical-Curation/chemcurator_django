from rest_framework import viewsets

from chemreg.compound.models import DefinedCompound, IllDefinedCompound
from chemreg.compound.serializers import (
    DefinedCompoundSerializer,
    IllDefinedCompoundSerializer,
)


class DefinedCompoundViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `detail` ,`update`, `destroy` actions.
    """

    queryset = DefinedCompound.objects.all()
    serializer_class = DefinedCompoundSerializer


class IllDefinedCompoundViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `detail` ,`update`, `destroy` actions.
    """

    queryset = IllDefinedCompound.objects.all()
    serializer_class = IllDefinedCompoundSerializer
