from chemreg.common.mixins import DeprecateDeleteMixin
from chemreg.jsonapi.views import ModelViewSet
from chemreg.lists.models import ListType
from chemreg.lists.serializers import ListTypeSerializer


class ListTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = ListType.objects.all()
    serializer_class = ListTypeSerializer
