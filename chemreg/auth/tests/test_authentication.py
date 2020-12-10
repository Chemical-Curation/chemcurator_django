from rest_framework.authentication import SessionAuthentication

from chemreg.auth.authentication import CsrfExemptSessionAuthentication


def test_csrf():
    """Test that CSRF isn't checked."""

    # The authenticate method must not be altered for this test to be valid.
    assert (
        SessionAuthentication.authenticate
        is CsrfExemptSessionAuthentication.authenticate
    )

    # The `enforce_csrf` method should just pass with any request.
    assert CsrfExemptSessionAuthentication().enforce_csrf("foo") is None


def test_settings(settings):
    """Ensure that settings are secure."""

    # Prevents CSRF attacks
    assert settings.SESSION_COOKIE_SAMESITE == "Strict"

    # Allows credentials to be sent on other subdomains
    assert settings.CORS_ALLOW_CREDENTIALS

    # SessionAuthentication must not require CSRF checking
    assert (
        "rest_framework.authentication.SessionAuthentication"
        not in settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]
    )
    assert (
        "chemreg.auth.authentication.CsrfExemptSessionAuthentication"
        in settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]
    )

    # BasicAuthentication is needed to login the first time
    assert (
        "rest_framework.authentication.BasicAuthentication"
        in settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]
    )

    # Authenticated users can perform any request.
    # Unauthorised users will only be permitted if the request
    # method is one of the "safe" methods; GET, HEAD or OPTIONS.
    assert (
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
        in settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"]
    )
