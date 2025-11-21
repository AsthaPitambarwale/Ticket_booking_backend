import time
import random
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.db.models import F
from .models import Movie, Show, Booking
from .serializers import (SignupSerializer, MovieSerializer, ShowSerializer,BookingSerializer, BookSeatInputSerializer)
from .permissions import IsBookingOwner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Signup
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]


# Movies list
class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()


# Shows for a movie
class ShowListView(generics.ListAPIView):
    serializer_class = ShowSerializer

    def get_queryset(self):
        movie_id = self.kwargs.get('id')
        return Show.objects.filter(movie_id=movie_id).order_by('date_time')


# Booking with concurrency protection and retry
class BookSeatView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BookSeatInputSerializer,
        responses={201: BookingSerializer, 400: 'Bad Request', 409: 'Conflict'}
    )
    def post(self, request, id):
        show = get_object_or_404(Show, pk=id)

        serializer = BookSeatInputSerializer(data=request.data, context={'show': show})
        serializer.is_valid(raise_exception=True)
        seat_number = serializer.validated_data['seat_number']

        max_attempts = 5
        base_wait = 0.05  # 50ms
        attempt = 0

        while attempt < max_attempts:
            attempt += 1
            try:
                with transaction.atomic():
                    # Lock the show row to avoid overbooking
                    show_locked = Show.objects.select_for_update().get(pk=show.pk)

                    # Check seat number again
                    if Booking.objects.filter(show=show_locked, seat_number=seat_number, status=Booking.STATUS_BOOKED).exists():
                        return Response({"detail": "Seat already booked"}, status=status.HTTP_409_CONFLICT)

                    # Check capacity (booked seats < total_seats)
                    booked_count = Booking.objects.filter(show=show_locked, status=Booking.STATUS_BOOKED).count()
                    if booked_count >= show_locked.total_seats:
                        return Response({"detail": "Show fully booked"}, status=status.HTTP_409_CONFLICT)

                    # Create booking
                    booking = Booking.objects.create(
                        user=request.user,
                        show=show_locked,
                        seat_number=seat_number,
                    )
                    data = BookingSerializer(booking).data
                    return Response(data, status=status.HTTP_201_CREATED)

            except IntegrityError as e:
                # Likely due to unique constraint race - retry with backoff
                if attempt >= max_attempts:
                    return Response({"detail": "Could not allocate seat, try again"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                sleep_time = base_wait * (2 ** (attempt - 1)) + random.uniform(0, base_wait)
                time.sleep(sleep_time)
                continue

        return Response({"detail": "Failed to book seat"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Cancel booking
class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated, IsBookingOwner]

    def post(self, request, id):
        booking = get_object_or_404(Booking, pk=id)
        # permission check (i.e IsBookingOwner)
        self.check_object_permissions(request, booking)

        if booking.status == Booking.STATUS_CANCELLED:
            return Response({"detail": "Booking already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = Booking.STATUS_CANCELLED
        booking.save(update_fields=['status'])
        return Response({"detail": "Booking cancelled"}, status=status.HTTP_200_OK)


# My bookings
class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')
