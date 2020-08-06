from chemreg.common.mixins import DeprecateDeleteMixin
from chemreg.jsonapi.views import ModelViewSet
from chemreg.lists.models import IdentifierType, ListType
from chemreg.lists.serializers import IdentifierTypeSerializer, ListTypeSerializer


class ListTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = ListType.objects.all()
    serializer_class = ListTypeSerializer


class IdentifierTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = IdentifierType.objects.all()
    serializer_class = IdentifierTypeSerializer
