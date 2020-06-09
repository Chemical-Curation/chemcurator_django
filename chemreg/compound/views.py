from django.http import HttpResponsePermanentRedirect
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse

from chemreg.common.mixins import DeprecateDeleteMixin
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
        # return permission_classes depending on `action`
        if "cid" in self.request.data:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        else:
            return [permission() for permission in self.permission_classes]


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

    def retrieve(self, request, *args, **kwargs):
        """Redirect if a non-admin user is accessing a soft-deleted object."""

        instance = self.get_object()
        if instance.is_deleted and not self._is_admin:
            redirect_url = reverse("basecompound-detail", [instance.replaced_by_id])
            return HttpResponsePermanentRedirect(redirect_url)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer(self, *args, **kwargs):
        if self._is_admin:
            kwargs["is_admin"] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        """Filter the queryset to remove soft-deleted compounds.

        Provide all compounds if an admin is making the request. Also, provide
        all compounds if retrieving a single object. This allows us to give a
        redirect if warranted in `self.retrieve()`.
        """

        qs = super().get_queryset()
        if self._is_admin or self.action == "retrieve":
            return qs
        return qs.filter_deleted()


class DefinedCompoundViewSet(
    SoftDeleteCompoundMixin, CIDPermissionsMixin, ModelViewSet
):

    queryset = DefinedCompound.objects.with_deleted().all()
    serializer_class = DefinedCompoundSerializer
    valid_post_query_params = ["override"]
    filterset_class = DefinedCompoundFilter
    permission_classes_by_action = {
        "create": [IsAdminUser],
    }

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

    queryset = IllDefinedCompound.objects.with_deleted().all()
    serializer_class = IllDefinedCompoundSerializer
    filterset_fields = ["cid"]
    permission_classes_by_action = {
        "create": [IsAdminUser],
    }


class QueryStructureTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = QueryStructureType.objects.all()
    serializer_class = QueryStructureTypeSerializer


class CompoundViewSet(SoftDeleteCompoundMixin, ReadOnlyModelViewSet):

    queryset = BaseCompound.objects.with_deleted().all()
    serializer_class = CompoundSerializer
    filterset_fields = ["cid"]
