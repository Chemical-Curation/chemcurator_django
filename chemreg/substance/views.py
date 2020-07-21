from chemreg.jsonapi.views import ModelViewSet
from chemreg.substance.models import (
    QCLevelsType,
    Source,
    SubstanceType,
    SynonymQuality,
    SynonymType,
)
from chemreg.substance.serializers import (
    QCLevelsTypeSerializer,
    SourceSerializer,
    SubstanceTypeSerializer,
    SynonymQualitySerializer,
    SynonymTypeSerializer,
)


class QCLevelsTypeViewSet(ModelViewSet):

    queryset = QCLevelsType.objects.all()
    serializer_class = QCLevelsTypeSerializer


class SynonymTypeViewSet(ModelViewSet):

    queryset = SynonymType.objects.all()
    serializer_class = SynonymTypeSerializer


class SourceViewSet(ModelViewSet):

    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class SubstanceTypeViewSet(ModelViewSet):

    queryset = SubstanceType.objects.all()
    serializer_class = SubstanceTypeSerializer


class SynonymQualityViewSet(ModelViewSet):

    queryset = SynonymQuality.objects.all()
    serializer_class = SynonymQualitySerializer
