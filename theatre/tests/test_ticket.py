import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from theatre.models import (
    Ticket,
    Reservation,
    Performance,
    Play,
    Genre,
    TheatreHall,
)

User = get_user_model()


@pytest.mark.django_db
def test_list_tickets_as_authenticated_user():
    user = User.objects.create_user("user", "user@example.com", "pass1234")
    genre = Genre.objects.create(name="Drama")
    play = Play.objects.create(
        title="Hamlet", description="Tragedy", genre=genre
    )
    hall = TheatreHall.objects.create(
        name="Main Hall", rows=10, seats_in_row=20
    )
    perf = Performance.objects.create(
        play=play, theatre_hall=hall, show_time="2026-07-30T19:00:00Z"
    )
    reservation = Reservation.objects.create(user=user)
    Ticket.objects.create(
        performance=perf, reservation=reservation, row=1, seat=5
    )

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/tickets/")
    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_create_ticket_as_authenticated_user():
    user = User.objects.create_user("user", "user@example.com", "pass1234")
    genre = Genre.objects.create(name="Drama")
    play = Play.objects.create(
        title="Macbeth", description="Tragedy", genre=genre
    )
    hall = TheatreHall.objects.create(
        name="Big Hall", rows=15, seats_in_row=25
    )
    perf = Performance.objects.create(
        play=play, theatre_hall=hall, show_time="2026-07-30T19:00:00Z"
    )
    reservation = Reservation.objects.create(user=user)

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(
        "/api/tickets/",
        {
            "performance": perf.id,
            "reservation": reservation.id,
            "row": 2,
            "seat": 10,
        },
        format="json",
    )
    assert response.status_code == 201
    assert Ticket.objects.filter(
        reservation=reservation, performance=perf
    ).exists()


@pytest.mark.django_db
def test_create_ticket_as_anonymous():
    genre = Genre.objects.create(name="Drama")
    play = Play.objects.create(
        title="Unauthorized", description="Fail", genre=genre
    )
    hall = TheatreHall.objects.create(
        name="Small Hall", rows=5, seats_in_row=10
    )
    perf = Performance.objects.create(
        play=play, theatre_hall=hall, show_time="2026-07-30T19:00:00Z"
    )
    reservation = Reservation.objects.create(
        user=User.objects.create_user("user", "u@example.com", "pass1234")
    )

    client = APIClient()
    response = client.post(
        "/api/tickets/",
        {
            "performance": perf.id,
            "reservation": reservation.id,
            "row": 1,
            "seat": 1,
        },
        format="json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_cannot_access_other_tickets():
    user1 = User.objects.create_user("user1", "u1@example.com", "pass1234")
    user2 = User.objects.create_user("user2", "u2@example.com", "pass1234")
    genre = Genre.objects.create(name="Drama")
    play = Play.objects.create(
        title="Hamlet", description="Tragedy", genre=genre
    )
    hall = TheatreHall.objects.create(name="Hall", rows=10, seats_in_row=20)
    perf = Performance.objects.create(
        play=play, theatre_hall=hall, show_time="2026-07-30T19:00:00Z"
    )
    reservation = Reservation.objects.create(user=user1)
    ticket = Ticket.objects.create(
        performance=perf, reservation=reservation, row=1, seat=5
    )

    client = APIClient()
    client.force_authenticate(user=user2)
    response = client.get(f"/api/tickets/{ticket.id}/")
    assert response.status_code == 403
