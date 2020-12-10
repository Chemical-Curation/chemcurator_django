from chemreg.common.models import CommonInfo, ControlledVocabulary
from chemreg.jsonapi.serializers import HyperlinkedModelSerializer


class CommonInfoSerializer(HyperlinkedModelSerializer):
    included_serializers = {
        "created_by": "chemreg.users.serializers.UserSerializer",
        "updated_by": "chemreg.users.serializers.UserSerializer",
    }

    created_by = "chemreg.users.serializers.UserSerializer"
    updated_by = "chemreg.users.serializers.UserSerializer"

    class Meta:
        model = CommonInfo
        fields = [
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
        ]
        abstract = True


class ControlledVocabSerializer(CommonInfoSerializer):
    class Meta(CommonInfoSerializer.Meta):
        model = ControlledVocabulary
        fields = CommonInfoSerializer.Meta.fields + [
            "name",
            "label",
            "short_description",
            "long_description",
            "deprecated",
        ]
        abstract = True
