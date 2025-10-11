from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    is_donor = models.BooleanField(default=True)
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"


class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5, choices=UserProfile.BLOOD_GROUPS)
    message = models.TextField()
    location = models.CharField(max_length=255)
    is_urgent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Request for {self.blood_group} by {self.requester.username}"