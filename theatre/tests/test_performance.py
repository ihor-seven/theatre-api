import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from theatre.models import Performance, Play, Genre, Actor, TheatreHall

User = get_user_model()


@pytest.mark.django_db
def test_list_performances_as_admin():
    admin = User.objects.create_superuser("admin", "admin@example.com", "pass1234")
    genre = Genre.objects.create(name="Drama")
    actor = Actor.objects.create(first_name="John", last_name="Doe")
    play = Play.objects.create(title="Hamlet", description="Tragedy", genre=genre)
    play.actor.add(actor)
    hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
    Performance.objects.create(play=play, theatre_hall=hall, show_time="2026-07-30T19:00:00Z")

    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.get("/api/performances/")
    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) >= 1


@pytest.mark.django_db
def test_create_performance_as_admin():
    admin = User.objects.create_superuser("admin", "admin@example.com", "pass1234")
    genre = Genre.objects.create(name="Drama")
    actor = Actor.objects.create(first_name="John", last_name="Doe")
    play = Play.objects.create(title="Macbeth", description="Tragedy", genre=genre)
    play.actor.add(actor)
    hall = TheatreHall.objects.create(name="Big Hall", rows=15, seats_in_row=25)

    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.post("/api/performances/", {
        "play": play.id,
        "theatre_hall": hall.id,
        "show_time": "2026-07-30T19:00:00Z"
    }, format="json")
    assert response.status_code == 201
    assert Performance.objects.filter(play=play, theatre_hall=hall).exists()


@pytest.mark.django_db
def test_create_performance_as_anonymous():
    genre = Genre.objects.create(name="Drama")
    play = Play.objects.create(title="Unauthorized", description="Fail", genre=genre)
    hall = TheatreHall.objects.create(name="Small Hall", rows=5, seats_in_row=10)

    client = APIClient()
    response = client.post("/api/performances/", {
        "play": play.id,
        "theatre_hall": hall.id,
        "show_time": "2026-07-30T19:00:00Z"
    }, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_performance_as_admin():
    admin = User.objects.create_superuser("admin", "admin@example.com", "pass1234")
    genre = Genre.objects.create(name="Drama")
    play = Play.objects.create(title="Old Play", description="Desc", genre=genre)
    hall = TheatreHall.objects.create(name="Hall", rows=10, seats_in_row=20)
    perf = Performance.objects.create(play=play, theatre_hall=hall, show_time="2026-07-30T19:00:00Z")

    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.put(f"/api/performances/{perf.id}/", {
        "play": play.id,
        "theatre_hall": hall.id,
        "show_time": "2026-08-01T20:00:00Z"
    }, format="json")
    assert response.status_code == 200
    perf.refresh_from_db()
    assert str(perf.show_time).startswith("2026-08-01")


@pytest.mark.django_db
def test_delete_performance_as_admin():
    admin = User.objects.create_superuser("admin", "admin@example.com", "pass1234")
    genre = Genre.objects.create(name="Drama")
    play = Play.objects.create(title="ToDelete", description="Desc", genre=genre)
    hall = TheatreHall.objects.create(name="Hall", rows=10, seats_in_row=20)
    perf = Performance.objects.create(play=play, theatre_hall=hall, show_time="2026-07-30T19:00:00Z")

    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.delete(f"/api/performances/{perf.id}/")
    assert response.status_code == 204
    assert not Performance.objects.filter(id=perf.id).exists()
