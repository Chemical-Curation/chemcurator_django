from chemreg.jsonapi.views import ModelViewSet
from chemreg.substance.models import Source, SynonymType
from chemreg.substance.serializers import SourceSerializer, SynonymTypeSerializer


class SynonymTypeViewSet(ModelViewSet):

    queryset = SynonymType.objects.all()
    serializer_class = SynonymTypeSerializer


class SourceViewSet(ModelViewSet):

    queryset = Source.objects.all()
    serializer_class = SourceSerializer
