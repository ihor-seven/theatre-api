import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from theatre.models import Actor

User = get_user_model()


@pytest.mark.django_db
def test_create_actor_as_admin():
    admin = User.objects.create_superuser("admin", "admin@example.com", "pass1234")
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.post("/api/actors/", {
        "first_name": "John",
        "last_name": "Doe"
    }, format="json")
    assert response.status_code == 201
    assert response.data["first_name"] == "John"
    assert response.data["last_name"] == "Doe"
    assert Actor.objects.filter(first_name="John", last_name="Doe").exists()


@pytest.mark.django_db
def test_create_actor_as_anonymous():
    client = APIClient()
    response = client.post("/api/actors/", {
        "first_name": "Jane",
        "last_name": "Doe"
    }, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_actors_as_admin():
    admin = User.objects.create_superuser("admin", "admin@example.com", "pass1234")
    Actor.objects.create(first_name="Actor", last_name="One")
    Actor.objects.create(first_name="Actor", last_name="Two")
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.get("/api/actors/")
    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) >= 2


@pytest.mark.django_db
def test_update_actor_as_admin():
    admin = User.objects.create_superuser("admin", "admin@example.com", "pass1234")
    actor = Actor.objects.create(first_name="Old", last_name="Name")
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.put(f"/api/actors/{actor.id}/", {
        "first_name": "New",
        "last_name": "Name"
    }, format="json")
    assert response.status_code == 200
    actor.refresh_from_db()
    assert actor.first_name == "New"


@pytest.mark.django_db
def test_delete_actor_as_admin():
    admin = User.objects.create_superuser("admin", "admin@example.com", "pass1234")
    actor = Actor.objects.create(first_name="To", last_name="Delete")
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.delete(f"/api/actors/{actor.id}/")
    assert response.status_code == 204
    assert not Actor.objects.filter(id=actor.id).exists()
