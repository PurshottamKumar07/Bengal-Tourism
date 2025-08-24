from django.core.management.base import BaseCommand
from core.models import Caravan
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed the database with sample caravans'

    def handle(self, *args, **options):
        caravans_data = [
            {
                'name': 'Luxury Family Caravan',
                'caravan_type': 'luxury',
                'description': 'Experience ultimate comfort with our premium luxury family caravan. Features include leather seating, premium sound system, and luxury amenities.',
                'short_description': 'Ultimate comfort with premium amenities for family adventures',
                'capacity': 6,
                'beds': 3,
                'has_ac': True,
                'has_kitchen': True,
                'has_bathroom': True,
                'has_generator': True,
                'fuel_type': 'diesel',
                'transmission': 'automatic',
                'mileage': 12,
                'year': 2023,
                'daily_rate': Decimal('8000.00'),
                'weekly_rate': Decimal('50000.00'),
                'security_deposit': Decimal('25000.00'),
                'pickup_locations': 'Kolkata, Darjeeling, Kalimpong',
                'max_distance': 500,
                'amenities': 'LED TV, WiFi, GPS Navigation, Backup Camera, Climate Control',
                'rules': 'Valid driving license required. Minimum age 25. No smoking inside.',
                'insurance_info': 'Comprehensive insurance included. Additional coverage available.',
                'is_featured': True,
            },
            {
                'name': 'Adventure Explorer Caravan',
                'caravan_type': 'adventure',
                'description': 'Built for adventure seekers! This rugged caravan can handle rough terrains and provides essential amenities for outdoor enthusiasts.',
                'short_description': 'Rugged and reliable for outdoor adventures',
                'capacity': 4,
                'beds': 2,
                'has_ac': True,
                'has_kitchen': True,
                'has_bathroom': True,
                'has_generator': True,
                'fuel_type': 'diesel',
                'transmission': 'manual',
                'mileage': 15,
                'year': 2022,
                'daily_rate': Decimal('5000.00'),
                'weekly_rate': Decimal('30000.00'),
                'security_deposit': Decimal('20000.00'),
                'pickup_locations': 'Darjeeling, Kalimpong, Gangtok',
                'max_distance': 800,
                'amenities': 'Off-road tires, Roof rack, Solar panels, Water tank',
                'rules': 'Valid driving license required. Minimum age 23. Off-road driving experience preferred.',
                'insurance_info': 'Basic insurance included. Adventure package available.',
                'is_featured': True,
            },
            {
                'name': 'Eco-Friendly Compact Caravan',
                'caravan_type': 'eco',
                'description': 'Environmentally conscious travel with zero emissions. Perfect for eco-tourism and sustainable travel experiences.',
                'short_description': 'Zero emissions for eco-conscious travelers',
                'capacity': 2,
                'beds': 1,
                'has_ac': True,
                'has_kitchen': True,
                'has_bathroom': True,
                'has_generator': False,
                'fuel_type': 'electric',
                'transmission': 'automatic',
                'mileage': 0,
                'year': 2024,
                'daily_rate': Decimal('6000.00'),
                'weekly_rate': Decimal('35000.00'),
                'security_deposit': Decimal('15000.00'),
                'pickup_locations': 'Kolkata, Shantiniketan, Digha',
                'max_distance': 300,
                'amenities': 'Solar charging, LED lighting, Eco-friendly materials, Mobile app control',
                'rules': 'Valid driving license required. Minimum age 21. Charging stations available.',
                'insurance_info': 'Comprehensive eco-insurance included.',
                'is_featured': True,
            },
            {
                'name': 'Premium Business Caravan',
                'caravan_type': 'premium',
                'description': 'Professional-grade caravan for business travelers. Features conference setup, high-speed internet, and executive amenities.',
                'short_description': 'Professional setup for business travelers',
                'capacity': 4,
                'beds': 2,
                'has_ac': True,
                'has_kitchen': True,
                'has_bathroom': True,
                'has_generator': True,
                'fuel_type': 'hybrid',
                'transmission': 'automatic',
                'mileage': 18,
                'year': 2023,
                'daily_rate': Decimal('7000.00'),
                'weekly_rate': Decimal('45000.00'),
                'security_deposit': Decimal('20000.00'),
                'pickup_locations': 'Kolkata, Howrah, Salt Lake',
                'max_distance': 400,
                'amenities': 'Conference table, WiFi hotspot, Printer, Coffee machine, Business center',
                'rules': 'Valid driving license required. Minimum age 25. Business purpose preferred.',
                'insurance_info': 'Business insurance included.',
                'is_featured': False,
            },
            {
                'name': 'Compact Weekend Getaway',
                'caravan_type': 'compact',
                'description': 'Perfect for weekend trips and short getaways. Easy to drive and park, ideal for couples and small families.',
                'short_description': 'Compact and easy to drive for weekend trips',
                'capacity': 3,
                'beds': 2,
                'has_ac': True,
                'has_kitchen': True,
                'has_bathroom': True,
                'has_generator': False,
                'fuel_type': 'petrol',
                'transmission': 'manual',
                'mileage': 14,
                'year': 2021,
                'daily_rate': Decimal('3500.00'),
                'weekly_rate': Decimal('20000.00'),
                'security_deposit': Decimal('15000.00'),
                'pickup_locations': 'Kolkata, Digha, Mandarmani',
                'max_distance': 200,
                'amenities': 'Compact design, Easy parking, Fuel efficient, USB charging',
                'rules': 'Valid driving license required. Minimum age 21. Perfect for beginners.',
                'insurance_info': 'Basic insurance included.',
                'is_featured': False,
            },
            {
                'name': 'Family Adventure Caravan',
                'caravan_type': 'family',
                'description': 'Spacious family caravan with entertainment options for kids. Perfect for long family road trips with comfort and safety.',
                'short_description': 'Spacious and family-friendly with entertainment options',
                'capacity': 8,
                'beds': 4,
                'has_ac': True,
                'has_kitchen': True,
                'has_bathroom': True,
                'has_generator': True,
                'fuel_type': 'diesel',
                'transmission': 'automatic',
                'mileage': 10,
                'year': 2022,
                'daily_rate': Decimal('6500.00'),
                'weekly_rate': Decimal('40000.00'),
                'security_deposit': Decimal('25000.00'),
                'pickup_locations': 'Kolkata, Darjeeling, Puri',
                'max_distance': 600,
                'amenities': 'Kids entertainment system, Multiple USB ports, Safety features, Spacious interior',
                'rules': 'Valid driving license required. Minimum age 25. Family-friendly destinations.',
                'insurance_info': 'Family insurance package included.',
                'is_featured': True,
            }
        ]

        for caravan_data in caravans_data:
            caravan, created = Caravan.objects.get_or_create(
                name=caravan_data['name'],
                defaults=caravan_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created caravan: {caravan.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Caravan already exists: {caravan.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded caravans')
        )
