from base64 import b64encode

import pytest


@pytest.mark.django_db
def test_login_view(user, client, settings):
    """Test that the login view can login and logout."""

    login_url = f"/{settings.LOGIN_URL.strip('/')}/"

    # Django doesn't store the raw password, so we need to set one we know.
    password = "A test password"
    user.set_password(password)
    user.save()

    # Test login with valid credentials
    auth_str = b64encode(f"{user.username}:{password}".encode()).decode()
    client.credentials(HTTP_AUTHORIZATION=f"Basic {auth_str}")
    response = client.post(login_url)
    assert response.status_code == 200
    assert response.data["username"] == user.username
    assert response.data["email"] == user.email

    # Get user using just session ID
    client.credentials()
    response = client.get(login_url)
    assert response.status_code == 200
    assert response.data["username"] == user.username
    assert response.data["email"] == user.email

    # Logout using just session ID
    response = client.delete(login_url)
    assert response.status_code == 200
    assert not response.data["username"]
    assert not response.data["email"]

    # Test with invalid credentials
    response = client.post(login_url)
    assert response.status_code == 403
    response = client.get(login_url)
    assert response.status_code == 403
    response = client.delete(login_url)
    assert response.status_code == 403
