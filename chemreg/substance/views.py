from chemreg.jsonapi.views import ModelViewSet
from chemreg.substance.models import SynonymType
from chemreg.substance.serializers import SynonymTypeSerializer


class SynonymTypeViewSet(ModelViewSet):

    queryset = SynonymType.objects.all()
    serializer_class = SynonymTypeSerializer
