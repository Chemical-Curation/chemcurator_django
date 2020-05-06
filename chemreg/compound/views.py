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
from chemreg.jsonapi.views import ModelViewSet


class DefinedCompoundViewSet(ModelViewSet):

    queryset = DefinedCompound.objects.all()
    serializer_class = DefinedCompoundSerializer


class IllDefinedCompoundViewSet(ModelViewSet):

    queryset = IllDefinedCompound.objects.all()
    serializer_class = IllDefinedCompoundSerializer


class QueryStructureTypeViewSet(ModelViewSet):

    queryset = QueryStructureType.objects.all()
    serializer_class = QueryStructureTypeSerializer
