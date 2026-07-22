import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from theatre.models import Play, Genre, Actor

User = get_user_model()


@pytest.mark.django_db
def test_list_plays_as_anonymous():
    genre = Genre.objects.create(name="Comedy")
    play = Play.objects.create(
        title="Hamlet", description="Tragedy play", genre=genre
    )
    client = APIClient()
    response = client.get("/api/plays/")
    assert response.status_code == 200
    assert "results" in response.data
    assert response.data["results"][0]["title"] == "Hamlet"


@pytest.mark.django_db
def test_create_play_as_admin():
    admin = User.objects.create_superuser(
        "admin", "admin@example.com", "pass1234"
    )
    genre = Genre.objects.create(name="Drama")
    actor = Actor.objects.create(first_name="John", last_name="Doe")
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.post(
        "/api/plays/",
        {
            "title": "Macbeth",
            "description": "Another tragedy",
            "genre": genre.id,
            "actor": [actor.id],
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.data["title"] == "Macbeth"
    assert Play.objects.filter(title="Macbeth").exists()


@pytest.mark.django_db
def test_create_play_as_anonymous():
    genre = Genre.objects.create(name="Drama")
    client = APIClient()
    response = client.post(
        "/api/plays/",
        {
            "title": "Unauthorized Play",
            "description": "Should fail",
            "genre": genre.id,
            "actor": [],
        },
        format="json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_play_as_admin():
    admin = User.objects.create_superuser(
        "admin", "admin@example.com", "pass1234"
    )
    genre = Genre.objects.create(name="Drama")
    play = Play.objects.create(
        title="Old Title", description="Desc", genre=genre
    )
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.put(
        f"/api/plays/{play.id}/",
        {
            "title": "New Title",
            "description": "Updated desc",
            "genre": genre.id,
            "actor": [],
        },
        format="json",
    )
    assert response.status_code == 200
    play.refresh_from_db()
    assert play.title == "New Title"


@pytest.mark.django_db
def test_delete_play_as_admin():
    admin = User.objects.create_superuser(
        "admin", "admin@example.com", "pass1234"
    )
    genre = Genre.objects.create(name="Drama")
    play = Play.objects.create(
        title="ToDelete", description="Desc", genre=genre
    )
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.delete(f"/api/plays/{play.id}/")
    assert response.status_code == 204
    assert not Play.objects.filter(id=play.id).exists()
