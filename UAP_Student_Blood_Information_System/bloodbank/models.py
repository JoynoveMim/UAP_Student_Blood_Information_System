# from django.contrib.auth.models import User
# from django.db import models
# from django.utils import timezone
#
#
#
# # Define blood groups at the module level to avoid circular imports
# BLOOD_GROUPS = [
#     ('A+', 'A+'), ('A-', 'A-'),
#     ('B+', 'B+'), ('B-', 'B-'),
#     ('O+', 'O+'), ('O-', 'O-'),
#     ('AB+', 'AB+'), ('AB-', 'AB-'),
# ]
#
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
#     phone = models.CharField(max_length=15)
#     address = models.TextField()
#     date_of_birth = models.DateField(null=True, blank=True)
#     is_donor = models.BooleanField(default=True)
#     last_donation_date = models.DateField(null=True, blank=True)
#     is_available = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     latitude = models.FloatField(null=True, blank=True)
#     longitude = models.FloatField(null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.blood_group}"
#
# class BloodRequest(models.Model):
#     STATUS_CHOICES = [
#         ('pending', '🟡 Pending'),
#         ('accepted', '✅ Accepted'),
#         ('completed', '🟢 Completed'),
#         ('cancelled', '🔴 Cancelled'),
#         ('expired', '⏰ Expired'),
#     ]
#
#     URGENCY_CHOICES = [
#         ('normal', '🟢 Normal'),
#         ('urgent', '🟡 Urgent'),
#         ('emergency', '🔴 Emergency'),
#     ]
#
#     # Request details
#     requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
#     blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
#     units_required = models.PositiveIntegerField(default=1)
#     urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='normal')
#     message = models.TextField(help_text="Additional information for donors", blank=True)
#
#     # Location details
#     hospital_name = models.CharField(max_length=255, default='UAP Medical Center')
#     hospital_address = models.TextField(default='UAP Campus, Kuratoli, Dhaka')
#     contact_person = models.CharField(max_length=100, default='Medical Staff')
#     contact_phone = models.CharField(max_length=15, default='0123456789')
#
#     # Status tracking
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     needed_by = models.DateTimeField(help_text="When the blood is needed by", default=timezone.now)
#
#     # Donor assignment (when someone accepts)
#     accepted_by = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='accepted_requests'
#     )
#     accepted_at = models.DateTimeField(null=True, blank=True)
#
#     def __str__(self):
#         return f"Request for {self.blood_group} by {self.requester.username}"
#
#     @property
#     def is_active(self):
#         return self.status in ['pending', 'accepted']
#
#     @property
#     def urgency_color(self):
#         colors = {
#             'normal': 'green',
#             'urgent': 'orange',
#             'emergency': 'red'
#         }
#         return colors.get(self.urgency, 'green')
#
# class Notification(models.Model):
#     NOTIFICATION_TYPES = [
#         ('blood_request', '🔴 New Blood Request'),
#         ('request_accepted', '📌 Request Accepted'),
#         ('request_completed', '🟢 Request Completed'),
#         ('request_cancelled', '🔴 Request Cancelled'),
#         ('donor_available', '🟢 Donor Available'),
#         ('system', '🔵 System Notification'),
#     ]
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
#     title = models.CharField(max_length=255)
#     message = models.TextField()
#     blood_request = models.ForeignKey('BloodRequest', on_delete=models.CASCADE, null=True, blank=True)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"{self.get_notification_type_display()} - {self.user.username}"
#
#     @property
#     def is_recent(self):
#         return (timezone.now() - self.created_at).days < 1


from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Define blood groups at the module level to avoid circular imports
BLOOD_GROUPS = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
]


class UserProfile(models.Model):
    # One-to-One relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    is_donor = models.BooleanField(default=True)
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Geolocation Fields
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Define string representation for the model
    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"

    # Define an explicit app_label in case it is necessary
    class Meta:
        app_label = 'bloodbank'  # Explicitly set the app_label for this model


class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', '🟡 Pending'),
        ('accepted', '✅ Accepted'),
        ('completed', '🟢 Completed'),
        ('cancelled', '🔴 Cancelled'),
        ('expired', '⏰ Expired'),
    ]

    URGENCY_CHOICES = [
        ('normal', '🟢 Normal'),
        ('urgent', '🟡 Urgent'),
        ('emergency', '🔴 Emergency'),
    ]

    # Request details
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    units_required = models.PositiveIntegerField(default=1)
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='normal')
    message = models.TextField(help_text="Additional information for donors", blank=True)

    # Location details
    hospital_name = models.CharField(max_length=255, default='UAP Medical Center')
    hospital_address = models.TextField(default='UAP Campus, Kuratoli, Dhaka')
    contact_person = models.CharField(max_length=100, default='Medical Staff')
    contact_phone = models.CharField(max_length=15, default='0123456789')

    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    needed_by = models.DateTimeField(help_text="When the blood is needed by", default=timezone.now)

    # Donor assignment (when someone accepts)
    accepted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_requests'
    )
    accepted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request for {self.blood_group} by {self.requester.username}"

    @property
    def is_active(self):
        return self.status in ['pending', 'accepted']

    @property
    def urgency_color(self):
        colors = {
            'normal': 'green',
            'urgent': 'orange',
            'emergency': 'red'
        }
        return colors.get(self.urgency, 'green')


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('blood_request', '🔴 New Blood Request'),
        ('request_accepted', '📌 Request Accepted'),
        ('request_completed', '🟢 Request Completed'),
        ('request_cancelled', '🔴 Request Cancelled'),
        ('donor_available', '🟢 Donor Available'),
        ('system', '🔵 System Notification'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    blood_request = models.ForeignKey('BloodRequest', on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.username}"

    @property
    def is_recent(self):
        return (timezone.now() - self.created_at).days < 1
