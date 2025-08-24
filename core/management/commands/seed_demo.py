from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.utils import timezone

from core.models import Destination, PointOfInterest, BlogPost, Course, Exam


class Command(BaseCommand):
    help = "Seed demo data for destinations, POIs, blog, courses, and exams"

    def handle(self, *args, **options):
        # Create destinations
        dests = [
            {
                'name': 'Darjeeling',
                'location': 'Darjeeling, West Bengal',
                'description': 'Hill station known for tea and the Himalayan Railway.',
                'price_per_person': 4999,
                'duration': 3,
                'destination_type': 'mountain',
                'near_mountain': True,
                'near_beach': False,
                'is_featured': True,
            },
            {
                'name': 'Sundarbans',
                'location': 'South 24 Parganas, West Bengal',
                'description': 'Largest mangrove forest and home to the Royal Bengal Tiger.',
                'price_per_person': 5999,
                'duration': 2,
                'destination_type': 'wildlife',
                'near_mountain': False,
                'near_beach': True,
                'is_featured': True,
            },
        ]

        for d in dests:
            dest, _ = Destination.objects.get_or_create(
                name=d['name'],
                defaults={
                    'location': d['location'],
                    'description': d['description'],
                    'price_per_person': d['price_per_person'],
                    'duration': d['duration'],
                    'destination_type': d['destination_type'],
                    'near_mountain': d['near_mountain'],
                    'near_beach': d['near_beach'],
                    'is_featured': d['is_featured'],
                    'is_active': True,
                }
            )
            # Minimal placeholder image if missing
            if not dest.image:
                dest.image.save(
                    f"{slugify(dest.name)}.jpg",
                    ContentFile(b"\xff\xd8\xff\xd9"),  # tiny invalid jpeg placeholder
                    save=True,
                )
            if not dest.map_image:
                dest.map_image.save(
                    f"{slugify(dest.name)}-map.jpg",
                    ContentFile(b"\xff\xd8\xff\xd9"),
                    save=True,
                )
            # Add some POIs
            if not dest.points_of_interest.exists():
                PointOfInterest.objects.create(
                    destination=dest,
                    name=f"{dest.name} Center",
                    x_percent=50,
                    y_percent=50,
                    latitude=27.036007,
                    longitude=88.262675,
                    description="Town center",
                )
                PointOfInterest.objects.create(
                    destination=dest,
                    name=f"{dest.name} View Point",
                    x_percent=70,
                    y_percent=40,
                    latitude=27.060000,
                    longitude=88.260000,
                    description="Scenic viewpoint",
                )

        # Blog posts
        posts = [
            {
                'title': 'Exploring Darjeeling Tea Gardens',
                'excerpt': 'A serene walk through lush tea estates.',
                'content': 'Darjeeling offers beautiful vistas and rich culture.'
            },
            {
                'title': 'Sundarbans Safari Tips',
                'excerpt': 'Prepare well for your mangrove adventure.',
                'content': 'Respect wildlife and follow your guide at all times.'
            },
        ]
        for p in posts:
            BlogPost.objects.get_or_create(
                title=p['title'],
                defaults={
                    'excerpt': p['excerpt'],
                    'content': p['content'],
                    'is_new': True,
                }
            )

        # Courses
        for cname in ["Travel Operations", "Tour Guide Basics", "Destination Marketing"]:
            Course.objects.get_or_create(name=cname, defaults={'description': f'{cname} course.'})

        # Exams
        Exam.objects.get_or_create(
            title='Tour Guide Entrance Exam',
            defaults={'description': 'Qualify to become a certified tour guide.', 'scheduled_at': timezone.now()}
        )
        Exam.objects.get_or_create(
            title='Travel Operations Assessment',
            defaults={'description': 'Assessment for operations course.', 'scheduled_at': timezone.now()}
        )

        self.stdout.write(self.style.SUCCESS('Demo data seeded.'))


