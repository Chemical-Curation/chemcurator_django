from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAdminUser

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


class SoftDeleteCompoundMixin:
    """
    A Compound cannot be deleted until an admin user provides another compound's
    CID and a qc_note explaining why the compound was deleted in favor of the
    replacement.
    """

    def destroy(self, request, *args, **kwargs):
        print("---deleting a compound---")
        print(request.__dict__)
        print(kwargs)

        # user must be an Admin
        if not IsAdminUser():
            raise APIException("You are not authorized to delete a compound")

        if self.request.data.get("replaced_by"):
            replacement_cid = self.request.data.get("replaced_by")
        else:
            raise APIException(
                "The request data must include a CID in the replaced_by attribute"
            )
        qc_note = self.request.data.get("qc_note")

        # the CID that was provided must match a non-deleted Compound
        if (
            BaseCompound.objects.filter(replaced_by__isnull=True)
            .filter(cid=replacement_cid)
            .exists()
        ):
            self.replacement_cid = (
                BaseCompound.objects.filter(replaced_by__isnull=True)
                .filter(cid=replacement_cid)
                .first()
            )
        else:
            raise APIException(
                f"The CID provided, {replacement_cid} does not match an existing compound"
            )
        # make sure there is a qc_note
        if qc_note.strip():
            self.qc_note = qc_note
        else:
            raise APIException(
                "No QC note was provided to explain the compound replacement"
            )

        return super().destroy(request, *args, **kwargs)


class DefinedCompoundViewSet(SoftDeleteCompoundMixin, ModelViewSet):

    queryset = DefinedCompound.objects.all()
    serializer_class = DefinedCompoundSerializer
    serializer_action_classes = {
        "retrieve": DefinedCompoundDetailSerializer,
    }
    valid_post_query_params = ["override"]
    filterset_fields = ["cid", "inchikey"]

    def get_serializer_class(self, *args, **kwargs):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
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


class IllDefinedCompoundViewSet(SoftDeleteCompoundMixin, ModelViewSet):

    queryset = IllDefinedCompound.objects.all()
    serializer_class = IllDefinedCompoundSerializer
    filterset_fields = ["cid"]


class QueryStructureTypeViewSet(ModelViewSet):

    queryset = QueryStructureType.objects.all()
    serializer_class = QueryStructureTypeSerializer


class CompoundViewSet(ReadOnlyModelViewSet):

    queryset = BaseCompound.objects.all()
    serializer_class = CompoundSerializer
    filterset_fields = ["cid"]
