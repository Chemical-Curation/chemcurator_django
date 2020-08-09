from chemreg.common.models import ControlledVocabulary
from chemreg.jsonapi.serializers import HyperlinkedModelSerializer


class ControlledVocabSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ControlledVocabulary
        fields = [
            "name",
            "label",
            "short_description",
            "long_description",
            "deprecated",
        ]
        abstract = True
