from django.core.management.base import BaseCommand
from core.models import Course
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed the database with sample courses'

    def handle(self, *args, **options):
        courses_data = [
            {
                'name': 'Tourism & Hospitality Management',
                'description': 'Comprehensive course covering all aspects of tourism and hospitality management including customer service, operations, marketing, and business strategies.',
                'short_description': 'Learn the fundamentals of tourism and hospitality management with practical industry insights.',
                'category': 'tourism',
                'price': Decimal('15000.00'),
                'duration_weeks': 12,
                'max_students': 25,
                'syllabus': '• Introduction to Tourism Industry\n• Hospitality Operations\n• Customer Service Excellence\n• Marketing in Tourism\n• Financial Management\n• Human Resource Management\n• Quality Assurance\n• Sustainable Tourism Practices',
                'requirements': 'Basic understanding of business concepts. No prior experience required.',
                'benefits': '• Industry-recognized certification\n• Practical hands-on training\n• Job placement assistance\n• Networking opportunities\n• Internship opportunities',
                'is_featured': True,
            },
            {
                'name': 'Professional Tour Guide Certification',
                'description': 'Become a certified tour guide with comprehensive training in guiding techniques, local history, cultural knowledge, and safety protocols.',
                'short_description': 'Get certified as a professional tour guide with expert training and local knowledge.',
                'category': 'guide',
                'price': Decimal('8000.00'),
                'duration_weeks': 8,
                'max_students': 20,
                'syllabus': '• Tour Guiding Fundamentals\n• Local History & Culture\n• Communication Skills\n• Safety & First Aid\n• Customer Service\n• Itinerary Planning\n• Group Management\n• Cultural Sensitivity',
                'requirements': 'Good communication skills and passion for local culture.',
                'benefits': '• Government-recognized certification\n• Practical field training\n• Local knowledge expertise\n• Safety certification\n• Employment opportunities',
                'is_featured': True,
            },
            {
                'name': 'Cultural Heritage Studies',
                'description': 'Explore the rich cultural heritage of West Bengal through this comprehensive course covering art, literature, music, dance, and traditional crafts.',
                'short_description': 'Discover the rich cultural heritage of West Bengal through art, literature, and traditions.',
                'category': 'culture',
                'price': Decimal('12000.00'),
                'duration_weeks': 10,
                'max_students': 30,
                'syllabus': '• Introduction to Cultural Heritage\n• Art & Architecture\n• Literature & Poetry\n• Music & Dance Forms\n• Traditional Crafts\n• Festivals & Celebrations\n• Cultural Tourism\n• Heritage Conservation',
                'requirements': 'Interest in cultural studies and local heritage.',
                'benefits': '• Deep cultural understanding\n• Heritage appreciation\n• Cultural tourism skills\n• Traditional knowledge\n• Community engagement',
                'is_featured': False,
            },
            {
                'name': 'Bengali Language for Tourism',
                'description': 'Learn Bengali language essentials specifically designed for tourism professionals to better serve local and international visitors.',
                'short_description': 'Master essential Bengali phrases and cultural communication for tourism professionals.',
                'category': 'language',
                'price': Decimal('6000.00'),
                'duration_weeks': 6,
                'max_students': 15,
                'syllabus': '• Basic Bengali Greetings\n• Tourism-related Vocabulary\n• Cultural Expressions\n• Business Communication\n• Local Dialects\n• Cultural Context',
                'requirements': 'No prior Bengali knowledge required.',
                'benefits': '• Basic Bengali proficiency\n• Cultural communication skills\n• Better guest relations\n• Local market advantage\n• Cultural sensitivity',
                'is_featured': False,
            },
            {
                'name': 'Travel Photography Masterclass',
                'description': 'Master the art of travel photography with professional techniques, composition skills, and storytelling through images.',
                'short_description': 'Learn professional travel photography techniques and storytelling through images.',
                'category': 'photography',
                'price': Decimal('18000.00'),
                'duration_weeks': 14,
                'max_students': 18,
                'syllabus': '• Photography Fundamentals\n• Travel Photography Techniques\n• Composition & Framing\n• Lighting & Exposure\n• Storytelling Through Images\n• Post-processing Skills\n• Equipment & Gear\n• Business of Photography',
                'requirements': 'Basic camera knowledge recommended but not required.',
                'benefits': '• Professional photography skills\n• Portfolio development\n• Business opportunities\n• Creative expression\n• Travel documentation',
                'is_featured': True,
            },
            {
                'name': 'Local Cuisine & Cooking',
                'description': 'Learn authentic Bengali cooking techniques, traditional recipes, and culinary heritage to enhance tourism experiences.',
                'short_description': 'Master authentic Bengali cooking techniques and traditional recipes.',
                'category': 'cooking',
                'price': Decimal('10000.00'),
                'duration_weeks': 8,
                'max_students': 12,
                'syllabus': '• Bengali Cuisine Basics\n• Traditional Recipes\n• Spice Blending\n• Cooking Techniques\n• Food Presentation\n• Cultural Significance\n• Seasonal Cooking\n• Food Safety',
                'requirements': 'Basic cooking skills helpful but not required.',
                'benefits': '• Culinary expertise\n• Traditional recipe collection\n• Food business opportunities\n• Cultural appreciation\n• Tourism enhancement',
                'is_featured': False,
            },
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                name=course_data['name'],
                defaults=course_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created course: {course.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Course already exists: {course.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded courses database')
        )
