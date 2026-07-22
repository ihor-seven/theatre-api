import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


User = get_user_model()

@pytest.mark.django_db
def test_user_register():
    client = APIClient()
    response = client.post("/api/users/register/", {
        "username": "alla",
        "email": "alla@example.com",
        "password": "alla1234"
    }, format="json")
    assert response.status_code == 201
    assert response.data["username"] == "alla"
    assert "password" not in response.data

@pytest.mark.django_db
def test_user_login_and_me():
    User.objects.create_user(username="alla", email="alla@example.com", password="alla1234")
    client = APIClient()
    token = client.post("/api/token/", {
        "username": "alla",
        "password": "alla1234"
    }).data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.get("/api/users/me/")
    assert response.status_code == 200
    assert response.data["email"] == "alla@example.com"
