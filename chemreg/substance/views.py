from chemreg.common.mixins import DeprecateDeleteMixin
from chemreg.jsonapi.views import ModelViewSet
from chemreg.substance.models import (
    QCLevelsType,
    RelationshipType,
    Source,
    Substance,
    SubstanceRelationship,
    SubstanceType,
    Synonym,
    SynonymQuality,
    SynonymType,
)
from chemreg.substance.serializers import (
    QCLevelsTypeSerializer,
    RelationshipTypeSerializer,
    SourceSerializer,
    SubstanceRelationshipSerializer,
    SubstanceSerializer,
    SubstanceTypeSerializer,
    SynonymQualitySerializer,
    SynonymSerializer,
    SynonymTypeSerializer,
)


class QCLevelsTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = QCLevelsType.objects.all()
    serializer_class = QCLevelsTypeSerializer


class SynonymTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = SynonymType.objects.all()
    serializer_class = SynonymTypeSerializer


class SourceViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class SubstanceViewSet(ModelViewSet):

    queryset = Substance.objects.all()
    serializer_class = SubstanceSerializer


class SubstanceTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = SubstanceType.objects.all()
    serializer_class = SubstanceTypeSerializer


class RelationshipTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = RelationshipType.objects.all()
    serializer_class = RelationshipTypeSerializer


class SynonymQualityViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = SynonymQuality.objects.all()
    serializer_class = SynonymQualitySerializer


class SynonymViewSet(ModelViewSet):

    queryset = Synonym.objects.all()
    serializer_class = SynonymSerializer
    filterset_fields = ["substance__id"]


class SubstanceRelationshipViewSet(ModelViewSet):

    queryset = SubstanceRelationship.objects.all()
    serializer_class = SubstanceRelationshipSerializer
