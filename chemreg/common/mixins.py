from rest_framework import status
from rest_framework.response import Response


class DeprecateDeleteMixin:
    def destroy(self, request, *args, **kwargs):
        """Deprecate the structure on delete."""

        instance = self.get_object()
        instance.deprecated = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
