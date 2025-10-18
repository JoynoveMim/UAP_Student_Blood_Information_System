from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bloodbank.models import UserProfile
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Add sample donor data for testing'

    def handle(self, *args, **options):
        sample_donors = [
            {'username': 'tasnim_tayeba', 'blood_group': 'A+', 'phone': '0123456789', 'address': 'UAP Campus, Dhaka'},
            {'username': 'joynove_mim', 'blood_group': 'O+', 'phone': '0123456790', 'address': 'Mirpur, Dhaka'},
            {'username': 'fabia_rahman', 'blood_group': 'B+', 'phone': '0123456791', 'address': 'Dhanmondi, Dhaka'},
            {'username': 'shahriar_saad', 'blood_group': 'A+', 'phone': '0123456792', 'address': 'UAP Campus, Dhaka'},
            {'username': 'samia_zaman', 'blood_group': 'B-', 'phone': '0123456793', 'address': 'Gulshan, Dhaka'},
            {'username': 'nabil_hossain', 'blood_group': 'O+', 'phone': '0123456794', 'address': 'Banani, Dhaka'},
            {'username': 'robayet_ismum', 'blood_group': 'O+', 'phone': '0123456795', 'address': 'Uttara, Dhaka'},
        ]

        for donor_data in sample_donors:
            # Create user if not exists
            user, created = User.objects.get_or_create(
                username=donor_data['username'],
                defaults={'email': f"{donor_data['username']}@uap.edu.bd"}
            )
            
            if created:
                user.set_password('password123')  # Simple password for testing
                user.save()
                
                # Create user profile
                UserProfile.objects.create(
                    user=user,
                    blood_group=donor_data['blood_group'],
                    phone=donor_data['phone'],
                    address=donor_data['address'],
                    is_donor=True,
                    is_available=True,
                    date_of_birth='1998-01-01'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created donor: {donor_data["username"]}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully added sample donors!')
        )