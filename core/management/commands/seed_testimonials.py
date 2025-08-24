from django.core.management.base import BaseCommand
from core.models import Testimonial

class Command(BaseCommand):
    help = 'Seed the database with demo testimonials'

    def handle(self, *args, **options):
        testimonials_data = [
            {
                'name': 'Priya Sharma',
                'position': 'Travel Enthusiast',
                'feedback': 'Amazing experience exploring the Sundarbans! The tour guides were knowledgeable and the accommodations were perfect. Will definitely recommend to friends and family.',
                'rating': 5,
            },
            {
                'name': 'Rajesh Kumar',
                'position': 'Photography Lover',
                'feedback': 'Darjeeling was absolutely breathtaking. The tea gardens, the mountain views, and the local culture made this trip unforgettable. Pacific Tourism made everything seamless.',
                'rating': 5,
            },
            {
                'name': 'Anita Das',
                'position': 'Cultural Explorer',
                'feedback': 'The heritage walk in Kolkata was incredible! Learned so much about the city\'s rich history and colonial architecture. Our guide was passionate and informative.',
                'rating': 4,
            },
            {
                'name': 'Suresh Patel',
                'position': 'Adventure Seeker',
                'feedback': 'Kalimpong was a hidden gem! The trekking routes were challenging but rewarding, and the local homestay experience was authentic. Pacific Tourism exceeded expectations.',
                'rating': 5,
            },
            {
                'name': 'Meera Banerjee',
                'position': 'Food Lover',
                'feedback': 'The culinary tour in Kolkata was a delight! From street food to fine dining, every bite was a revelation. The local food guides knew all the best spots.',
                'rating': 5,
            },
            {
                'name': 'Arjun Singh',
                'position': 'Nature Enthusiast',
                'feedback': 'The wildlife safari in the Sundarbans was incredible. Saw rare species and learned about conservation efforts. The boat tours were well-organized and safe.',
                'rating': 4,
            }
        ]

        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=testimonial_data['name'],
                defaults=testimonial_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created testimonial: {testimonial.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Testimonial already exists: {testimonial.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded testimonials')
        )
