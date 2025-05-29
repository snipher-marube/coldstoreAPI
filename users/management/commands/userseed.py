import os
import django
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random
from django.db.utils import IntegrityError

# set up django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coldstore.settings.base')
django.setup()


User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seed and populate the dummy users'

    def handle(self, *args, **options):
        self.stdout.write('Seeding user dummy data...')
        self.create_user()
        self.stdout.write(self.style.SUCCESS('Successfully pupulated data of dummy users'))

    def create_user(self):
        user_types = [choice[0] for choice in User.UserType.choices]
        created_count = 0
        attempt_count = 0
        max_attempts = 2000  # Allow more attempts since we're not checking duplicates first
    
        while created_count < 1000 and attempt_count < max_attempts:
            attempt_count += 1
        
            try:
                # Let UserManager handle username generation
                user = User.objects.create_user(
                    email=fake.email(),
                    password='password1234',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone=fake.phone_number(),
                    user_type=random.choice(user_types))
            
                created_count += 1
            
                if created_count % 100 == 0:
                    self.stdout.write(f'Created {created_count} users...')
                
            except IntegrityError as e:
                continue  # Duplicate entry, try again
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))
                continue