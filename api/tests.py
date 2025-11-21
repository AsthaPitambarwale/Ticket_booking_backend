from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Movie, Show, Booking
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
import threading

class BookingTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='u1', password='pass1')
        self.user2 = User.objects.create_user(username='u2', password='pass2')
        self.movie = Movie.objects.create(title='Test Movie', duration_minutes=120)
        self.show = Show.objects.create(movie=self.movie, screen_name='S1', date_time=timezone.now()+timedelta(days=1), total_seats=2)

    def test_basic_booking_and_cancel(self):
        client = APIClient()
        client.login(username='u1', password='pass1')
        client.force_authenticate(user=self.user1)

        resp = client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 1}, format='json')
        self.assertEqual(resp.status_code, 201)
        booking_id = resp.data['id']

        # Now cancel
        cancel_resp = client.post(f'/api/bookings/{booking_id}/cancel/')
        self.assertEqual(cancel_resp.status_code, 200)
        b = Booking.objects.get(pk=booking_id)
        self.assertEqual(b.status, Booking.STATUS_CANCELLED)

    def test_cannot_cancel_others_booking(self):
        client1 = APIClient()
        client1.force_authenticate(user=self.user1)
        resp = client1.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 1}, format='json')
        self.assertEqual(resp.status_code, 201)
        booking_id = resp.data['id']

        client2 = APIClient()
        client2.force_authenticate(user=self.user2)
        cancel_resp = client2.post(f'/api/bookings/{booking_id}/cancel/')
        self.assertEqual(cancel_resp.status_code, 403)  # forbidden

    def test_concurrent_booking_attempts_same_seat(self):
        """
        Simulate two threads attempting to book the same seat concurrently.
        One will succeed, the other will fail with 409 or 500 after retries.
        """
        results = []
        lock = threading.Lock()

        def attempt_booking(user):
            client = APIClient()
            client.force_authenticate(user=user)
            resp = client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 1}, format='json')
            with lock:
                results.append((user.username, resp.status_code, resp.data))

        t1 = threading.Thread(target=attempt_booking, args=(self.user1,))
        t2 = threading.Thread(target=attempt_booking, args=(self.user2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        created = [r for r in results if r[1] == 201]
        self.assertEqual(len(created), 1)
        failed = [r for r in results if r[1] != 201]
        self.assertEqual(len(failed), 1)
