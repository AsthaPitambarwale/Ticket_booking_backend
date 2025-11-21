from django.urls import path
from .views import SignupView, MovieListView, ShowListView, BookSeatView, CancelBookingView, MyBookingsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('movies/', MovieListView.as_view(), name='movies-list'),
    path('movies/<int:id>/shows/', ShowListView.as_view(), name='movie-shows'),
    path('shows/<int:id>/book/', BookSeatView.as_view(), name='book-seat'),
    path('bookings/<int:id>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
    path('my-bookings/', MyBookingsView.as_view(), name='my-bookings'),
]
