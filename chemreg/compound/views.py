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
from chemreg.jsonapi.views import ModelViewSet, RelationshipView


class DefinedCompoundViewSet(ModelViewSet):
    """
    This viewset automatically provides `list`, `detail` ,`update`, `destroy` actions.
    """

    queryset = DefinedCompound.objects.all()
    serializer_class = DefinedCompoundSerializer


class IllDefinedCompoundViewSet(ModelViewSet):
    """
    This viewset automatically provides `list`, `detail` ,`update`, `destroy` actions.
    """

    queryset = IllDefinedCompound.objects.all()
    serializer_class = IllDefinedCompoundSerializer


class IllDefinedCompoundRelationshipView(RelationshipView):
    queryset = IllDefinedCompound.objects


class QueryStructureTypeViewSet(ModelViewSet):
    """
    This viewset provides `list`, `detail` ,`update`, and `destroy` actions for the
    QueryStructureType model
    """

    queryset = QueryStructureType.objects.all()
    serializer_class = QueryStructureTypeSerializer
