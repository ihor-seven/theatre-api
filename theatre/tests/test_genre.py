import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from theatre.models import Genre

User = get_user_model()


@pytest.mark.django_db
def test_create_genre_as_admin():
    admin = User.objects.create_superuser(
        "admin", "admin@example.com", "pass1234"
    )
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.post("/api/genres/", {"name": "Drama"}, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "Drama"
    assert Genre.objects.filter(name="Drama").exists()


@pytest.mark.django_db
def test_create_genre_as_anonymous():
    client = APIClient()
    response = client.post("/api/genres/", {"name": "Comedy"}, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_genres_as_admin():
    admin = User.objects.create_superuser(
        "admin", "admin@example.com", "pass1234"
    )
    Genre.objects.create(name="Tragedy")
    Genre.objects.create(name="Comedy")
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.get("/api/genres/")
    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) >= 2


@pytest.mark.django_db
def test_update_genre_as_admin():
    admin = User.objects.create_superuser(
        "admin", "admin@example.com", "pass1234"
    )
    genre = Genre.objects.create(name="OldName")
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.put(
        f"/api/genres/{genre.id}/", {"name": "NewName"}, format="json"
    )
    assert response.status_code == 200
    genre.refresh_from_db()
    assert genre.name == "NewName"


@pytest.mark.django_db
def test_delete_genre_as_admin():
    admin = User.objects.create_superuser(
        "admin", "admin@example.com", "pass1234"
    )
    genre = Genre.objects.create(name="ToDelete")
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.delete(f"/api/genres/{genre.id}/")
    assert response.status_code == 204
    assert not Genre.objects.filter(id=genre.id).exists()
