from django.db import models
from config import settings


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Play(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    actor = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return (
            f"{self.play.title} at {self.show_time.strftime('%Y-%m-%d %H:%M')}"
        )


class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Reservation by {self.user} "
            f"on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        )


class Ticket(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self):
        return (
            f"Ticket {self.row}-{self.seat} for {self.performance.play.title}"
        )
