import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_booking.settings")
django.setup()

from api.models import Movie

def seed_movies():
    movie_data = [
        {"title": "Avengers: Endgame", "description": "Superhero blockbuster", "duration": 180},
        {"title": "Inception", "description": "Mind-bending sci-fi", "duration": 150},
        {"title": "Interstellar", "description": "Space & time adventure", "duration": 165},
    ]

    for movie in movie_data:
        Movie.objects.get_or_create(**movie)

    print("🎉 Database seeded successfully!")

if __name__ == "__main__":
    seed_movies()
