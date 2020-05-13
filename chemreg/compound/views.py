from rest_framework.permissions import IsAdminUser

from chemreg.compound.models import (
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.serializers import (
    DefinedCompoundDetailSerializer,
    DefinedCompoundSerializer,
    IllDefinedCompoundSerializer,
    QueryStructureTypeSerializer,
)
from chemreg.jsonapi.views import ModelViewSet


class DefinedCompoundViewSet(ModelViewSet):

    queryset = DefinedCompound.objects.all()
    serializer_class = DefinedCompoundSerializer
    serializer_action_classes = {
        "retrieve": DefinedCompoundDetailSerializer,
    }
    valid_post_query_params = ["override"]

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


class IllDefinedCompoundViewSet(ModelViewSet):

    queryset = IllDefinedCompound.objects.all()
    serializer_class = IllDefinedCompoundSerializer


class QueryStructureTypeViewSet(ModelViewSet):

    queryset = QueryStructureType.objects.all()
    serializer_class = QueryStructureTypeSerializer
