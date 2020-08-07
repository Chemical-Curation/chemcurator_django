from chemreg.common.mixins import DeprecateDeleteMixin
from chemreg.jsonapi.views import ModelViewSet
from chemreg.lists.models import AccessibilityType, IdentifierType, ListType
from chemreg.lists.serializers import (
    AccessibilityTypeSerializer,
    IdentifierTypeSerializer,
    ListTypeSerializer,
)


class ListTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = ListType.objects.all()
    serializer_class = ListTypeSerializer


class AccessibilityTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = AccessibilityType.objects.all()
    serializer_class = AccessibilityTypeSerializer


class IdentifierTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = IdentifierType.objects.all()
    serializer_class = IdentifierTypeSerializer
