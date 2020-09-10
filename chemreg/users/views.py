from chemreg.jsonapi.views import ModelViewSet
from chemreg.users.models import User
from chemreg.users.serializers import UserSerializer


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
