from rest_framework import viewsets

from config.pagination import DefaultPagination

from chemreg.compound.models import (
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.serializers import (
    DefinedCompoundSerializer,
    IllDefinedCompoundSerializer,
    QueryStructureTypeSerializer,
)


class DefinedCompoundViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `detail` ,`update`, `destroy` actions.
    """

    queryset = DefinedCompound.objects.all()
    serializer_class = DefinedCompoundSerializer
    lookup_field = "cid"
    pagination_class = DefaultPagination


class IllDefinedCompoundViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `detail` ,`update`, `destroy` actions.
    """

    queryset = IllDefinedCompound.objects.all()
    serializer_class = IllDefinedCompoundSerializer
    lookup_field = "cid"
    pagination_class = DefaultPagination


class QueryStructureTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `detail` ,`update`, and `destroy` actions for the
    QueryStructureType model
    """

    queryset = QueryStructureType.objects.all()
    serializer_class = QueryStructureTypeSerializer
    lookup_field = "name"
    pagination_class = DefaultPagination
