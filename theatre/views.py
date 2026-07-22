from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS
from .models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket
)
from .serializers import (
    GenreSerializer,
    ActorSerializer,
    PlaySerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TicketSerializer,
    PlayDetailSerializer,
    TicketDetailSerializer
)



class ReadOnlyOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class ReservationPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class TicketPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reservation.user == request.user


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminUser]


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    permission_classes = [ReadOnlyOrAdmin]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PlayDetailSerializer
        return PlaySerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = [IsAdminUser]


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAdminUser()]

    def get_queryset(self):
        return Performance.objects.all()

    def get_serializer_class(self):
        return PerformanceSerializer

    def get_allowed_methods(self):
        return ["GET", "POST"]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, ReservationPermission]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, TicketPermission]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TicketDetailSerializer
        return TicketSerializer
