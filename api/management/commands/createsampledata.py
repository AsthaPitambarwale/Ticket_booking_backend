from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Movie, Show
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Create sample users, movies and shows"

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(username='demo', defaults={'email': 'demo@example.com'})
        if not user.has_usable_password():
            user.set_password('demopass')
            user.save()
        self.stdout.write("Created demo user: username=demo password=demopass")

        m1, _ = Movie.objects.get_or_create(title='Inception', duration_minutes=148)
        m2, _ = Movie.objects.get_or_create(title='Interstellar', duration_minutes=169)

        now = timezone.now()
        Show.objects.get_or_create(movie=m1, screen_name='Screen 1', date_time=now + timedelta(days=1), total_seats=20)
        Show.objects.get_or_create(movie=m1, screen_name='Screen 2', date_time=now + timedelta(days=2), total_seats=15)
        Show.objects.get_or_create(movie=m2, screen_name='Screen 1', date_time=now + timedelta(days=1, hours=3), total_seats=10)

        self.stdout.write(self.style.SUCCESS("Sample movies and shows created"))
