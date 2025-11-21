from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Show, Booking
from django.utils import timezone

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'duration_minutes']


class ShowSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = ['id', 'movie', 'screen_name', 'date_time', 'total_seats', 'available_seats']

    def get_available_seats(self, obj):
        booked_count = obj.bookings.filter(status=Booking.STATUS_BOOKED).count()
        return max(obj.total_seats - booked_count, 0)


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    show_detail = ShowSerializer(source='show', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'show', 'show_detail', 'seat_number', 'status', 'created_at']
        read_only_fields = ['status', 'created_at', 'user']

class BookSeatInputSerializer(serializers.Serializer):
    seat_number = serializers.IntegerField(min_value=1)

    def validate_seat_number(self, value):
        show = self.context.get('show')
        if show is None:
            raise serializers.ValidationError("Show context is required")
        if value < 1 or value > show.total_seats:
            raise serializers.ValidationError(f"Seat number must be between 1 and {show.total_seats}")
        return value
