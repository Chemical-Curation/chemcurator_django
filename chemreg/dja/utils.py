class ResourceRegistry:
    """singleton"""

    @classmethod
    def get_serializer_from_instance(cls, instance):
        pass

    @classmethod
    def get_view_for_serializer(cls, serializer):
        pass

    @classmethod
    def register_instance(cls, serializer, instance):
        pass

    @classmethod
    def register_view(cls, serializer, view):
        pass
