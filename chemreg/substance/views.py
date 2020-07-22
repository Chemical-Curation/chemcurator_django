from chemreg.jsonapi.views import ModelViewSet
from chemreg.substance.models import (
    QCLevelsType,
    RelationshipType,
    Source,
    Substance,
    SubstanceType,
    SynonymQuality,
    SynonymType,
)
from chemreg.substance.serializers import (
    QCLevelsTypeSerializer,
    RelationshipTypeSerializer,
    SourceSerializer,
    SubstanceSerializer,
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


class SubstanceViewSet(ModelViewSet):

    queryset = Substance.objects.all()
    serializer_class = SubstanceSerializer


class SubstanceTypeViewSet(ModelViewSet):

    queryset = SubstanceType.objects.all()
    serializer_class = SubstanceTypeSerializer


class RelationshipTypeViewSet(ModelViewSet):

    queryset = RelationshipType.objects.all()
    serializer_class = RelationshipTypeSerializer


class SynonymQualityViewSet(ModelViewSet):

    queryset = SynonymQuality.objects.all()
    serializer_class = SynonymQualitySerializer
