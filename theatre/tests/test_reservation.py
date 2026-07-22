import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from theatre.models import Reservation

User = get_user_model()


@pytest.mark.django_db
def test_list_reservations_as_authenticated_user():
    user = User.objects.create_user("user", "user@example.com", "pass1234")
    Reservation.objects.create(user=user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/reservations/")
    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_create_reservation_as_authenticated_user():
    user = User.objects.create_user("user", "user@example.com", "pass1234")
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post("/api/reservations/", {}, format="json")
    assert response.status_code == 201
    assert Reservation.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_create_reservation_as_anonymous():
    client = APIClient()
    response = client.post("/api/reservations/", {}, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_cannot_access_other_reservations():
    user1 = User.objects.create_user("user1", "u1@example.com", "pass1234")
    user2 = User.objects.create_user("user2", "u2@example.com", "pass1234")
    reservation = Reservation.objects.create(user=user1)

    client = APIClient()
    client.force_authenticate(user=user2)
    response = client.get(f"/api/reservations/{reservation.id}/")
    assert response.status_code == 403
