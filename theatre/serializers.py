from rest_framework import serializers
from theatre.models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name"]


class PlaySerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
    actor = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(), many=True
    )

    class Meta:
        model = Play
        fields = ["id", "title", "description", "genre", "actor"]


class PlayDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    actor = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ["id", "title", "description", "genre", "actor"]


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ["id", "name", "rows", "seats_in_row"]


class PerformanceSerializer(serializers.ModelSerializer):
    play = serializers.PrimaryKeyRelatedField(queryset=Play.objects.all())
    theatre_hall = serializers.PrimaryKeyRelatedField(
        queryset=TheatreHall.objects.all()
    )

    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class TicketSerializer(serializers.ModelSerializer):
    performance = serializers.PrimaryKeyRelatedField(
        queryset=Performance.objects.all()
    )
    reservation = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all()
    )

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance", "reservation"]


class TicketDetailSerializer(serializers.ModelSerializer):
    performance = PerformanceSerializer(read_only=True)
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance", "reservation"]
