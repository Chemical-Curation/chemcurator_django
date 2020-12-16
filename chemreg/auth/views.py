from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chemreg.users.serializers import UserSerializer


class LoginView(APIView):
    """Establishes a server-side session for a user.

    The application is configured to accept both HTTP Basic Authentication and
    session based authentication. A simple and secure authentication flow for
    the browser is to post to this endpoint using HTTP Basic Authentication
    to establish a session. Subsequent requests will use session based
    authentication. This obviates the insecure practice of handling user
    credentials at rest in the browser.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get the currently logged in user."""
        return self.response(request)

    def post(self, request):
        """Log the user in."""
        login(request, request.user)
        return self.response(request)

    def delete(self, request):
        """Log the user out."""
        logout(request)
        return self.response(request)

    def response(self, request):
        """The response for all requests.

        Returns:
            A `rest_framework.response.Response` with status code 200
            containing a JSON serialization of the `User` making the request.
            The response also includes instructions for the browser to set the
            session cookie when loggin in.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=200)
