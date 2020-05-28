from rest_framework.permissions import IsAdminUser

from chemreg.compound.filters import DefinedCompoundFilter
from chemreg.compound.models import (
    BaseCompound,
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.serializers import (
    CompoundSerializer,
    DefinedCompoundDetailSerializer,
    DefinedCompoundSerializer,
    IllDefinedCompoundSerializer,
    QueryStructureTypeSerializer,
)
from chemreg.jsonapi.views import ModelViewSet, ReadOnlyModelViewSet


class CIDPermissionsMixin:
    def get_permissions(self):
        # return permission_classes depending on `action`
        if "cid" in self.request.data:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        else:
            return [permission() for permission in self.permission_classes]


class DefinedCompoundViewSet(CIDPermissionsMixin, ModelViewSet):

    queryset = DefinedCompound.objects.all()
    serializer_class = DefinedCompoundSerializer
    serializer_action_classes = {
        "retrieve": DefinedCompoundDetailSerializer,
    }
    valid_post_query_params = ["override"]
    filterset_class = DefinedCompoundFilter
    permission_classes_by_action = {
        "create": [IsAdminUser],
    }

    def get_serializer_class(self, *args, **kwargs):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return self.serializer_class

    @property
    def override(self):
        return "override" in self.request.query_params

    def get_permissions(self):
        if self.override:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer(self, *args, **kwargs):
        if self.override:
            kwargs["admin_override"] = True
        return super().get_serializer(*args, **kwargs)


class IllDefinedCompoundViewSet(CIDPermissionsMixin, ModelViewSet):

    queryset = IllDefinedCompound.objects.all()
    serializer_class = IllDefinedCompoundSerializer
    filterset_fields = ["cid"]
    permission_classes_by_action = {
        "create": [IsAdminUser],
    }


class QueryStructureTypeViewSet(ModelViewSet):

    queryset = QueryStructureType.objects.all()
    serializer_class = QueryStructureTypeSerializer


class CompoundViewSet(ReadOnlyModelViewSet):

    queryset = BaseCompound.objects.all()
    serializer_class = CompoundSerializer
    filterset_fields = ["cid"]
