from chemreg.jsonapi.views import ModelViewSet
from chemreg.substance.models import Source, SubstanceType, SynonymType
from chemreg.substance.serializers import (
    SourceSerializer,
    SubstanceTypeSerializer,
    SynonymTypeSerializer,
)


class SynonymTypeViewSet(ModelViewSet):

    queryset = SynonymType.objects.all()
    serializer_class = SynonymTypeSerializer


class SourceViewSet(ModelViewSet):

    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class SubstanceTypeViewSet(ModelViewSet):

    queryset = SubstanceType.objects.all()
    serializer_class = SubstanceTypeSerializer
