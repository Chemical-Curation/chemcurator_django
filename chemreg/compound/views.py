from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from chemreg.compound.filters import DefinedCompoundFilter
from chemreg.compound.models import (
    BaseCompound,
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.serializers import (
    CompoundDeleteSerializer,
    CompoundSerializer,
    DefinedCompoundDetailSerializer,
    DefinedCompoundSerializer,
    IllDefinedCompoundSerializer,
    QueryStructureTypeSerializer,
)
from chemreg.jsonapi.views import ModelViewSet, ReadOnlyModelViewSet


class CIDPermissionsMixin:
    """
    You must be an admin if POSTing a CID.
    """

    def get_permissions(self):
        if self.action == "create" and "cid" in self.request.data:
            return [IsAdminUser()]
        return super().get_permissions()


class SoftDeleteCompoundMixin:
    """
    A Compound cannot be deleted until an admin user provides another compound's
    CID and a qc_note explaining why the compound was deleted in favor of the
    replacement.
    """

    @property
    def _is_admin(self):
        return IsAdminUser().has_permission(self.request, self)

    def destroy(self, request, *args, **kwargs):
        """Perform a soft delete."""

        instance = self.get_object()
        serializer = CompoundDeleteSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer(self, *args, **kwargs):
        if self._is_admin:
            kwargs["is_admin"] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        if self._is_admin:
            return qs
        return qs.filter(replaced_by__isnull=True)


class DefinedCompoundViewSet(
    SoftDeleteCompoundMixin, CIDPermissionsMixin, ModelViewSet
):

    queryset = DefinedCompound.objects.all()
    serializer_class = DefinedCompoundSerializer
    valid_post_query_params = ["override"]
    filterset_class = DefinedCompoundFilter

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve":
            return DefinedCompoundDetailSerializer
        return super().get_serializer_class(*args, **kwargs)

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


class IllDefinedCompoundViewSet(
    SoftDeleteCompoundMixin, CIDPermissionsMixin, ModelViewSet
):

    queryset = IllDefinedCompound.objects.all()
    serializer_class = IllDefinedCompoundSerializer
    filterset_fields = ["cid"]


class QueryStructureTypeViewSet(ModelViewSet):

    queryset = QueryStructureType.objects.all()
    serializer_class = QueryStructureTypeSerializer


class CompoundViewSet(SoftDeleteCompoundMixin, ReadOnlyModelViewSet):

    queryset = BaseCompound.objects.all()
    serializer_class = CompoundSerializer
    filterset_fields = ["cid"]
