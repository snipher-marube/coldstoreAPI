import os
import django
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random
from django.contrib.gis.geos import Point
from coldrooms.models import ColdRoom

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coldstore.settings.base')
django.setup()

fake = Faker()
User = get_user_model()

class Command(BaseCommand):
    help = 'Prepopulate coldroom registered'

    def handle(self, *args, **options):
        self.stdout.write('Seeding...')
        self.create_coldroom()
        self.stdout.write(self.style.SUCCESS('Successfully seeded the data'))

    def create_coldroom(self):
        created_count = 0
        attempt_count = 0
        max_attempts = 2000

        coldroom_owner = User.objects.filter(user_type='COLD_ROOM_OWNER')
        temperature_units = [choice[0] for choice in ColdRoom.TemperatureUnit.choices]
        
        availability_schedule = [
            '6AM-7AM', '7AM-8AM', '9AM-10AM', '10AM-11AM',
            '12PM-1PM', '1PM-2PM', '3PM-4PM', '5PM-6PM'
        ]

        while created_count < 1000 and attempt_count < max_attempts:
            attempt_count += 1
            try:
                owner = random.choice(coldroom_owner)
                availability_sample = random.sample(availability_schedule, random.randint(2, 4))
                location_data = fake.location_on_land()  
                
                ColdRoom.objects.create(
                    owner=owner,
                    name=fake.sentence(nb_words=3),
                    location=Point(float(location_data[1]), float(location_data[0]), srid=4326),
                    capacity=random.randint(1, 200),
                    temp_min=random.randint(0, 10),
                    temp_max=random.randint(10, 100), 
                    temp_unit=random.choice(temperature_units),
                    availability_schedule=availability_sample,
                )
                created_count += 1
            
                if created_count % 100 == 0:
                    self.stdout.write(f'Created {created_count} cold rooms...')

            except IntegrityError as e:
                continue  
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating coldroom: {e}'))
                continue
            
            

