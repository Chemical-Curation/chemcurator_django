from rest_framework_json_api import views

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


class DefinedCompoundViewSet(views.ModelViewSet):
    """
    This viewset automatically provides `list`, `detail` ,`update`, `destroy` actions.
    """

    queryset = DefinedCompound.objects.all()
    serializer_class = DefinedCompoundSerializer


class IllDefinedCompoundViewSet(views.ModelViewSet):
    """
    This viewset automatically provides `list`, `detail` ,`update`, `destroy` actions.
    """

    queryset = IllDefinedCompound.objects.all()
    serializer_class = IllDefinedCompoundSerializer


class IllDefinedCompoundRelationshipView(views.RelationshipView):
    queryset = IllDefinedCompound.objects


class QueryStructureTypeViewSet(views.ModelViewSet):
    """
    This viewset provides `list`, `detail` ,`update`, and `destroy` actions for the
    QueryStructureType model
    """

    queryset = QueryStructureType.objects.all()
    serializer_class = QueryStructureTypeSerializer
