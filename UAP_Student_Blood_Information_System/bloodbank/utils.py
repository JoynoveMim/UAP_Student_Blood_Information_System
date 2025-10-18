from django.contrib.auth.models import User
from .models import Notification, BloodRequest, UserProfile

def create_notification(user, notification_type, title, message, blood_request=None):
    """
    Utility function to create notifications
    """
    notification = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        blood_request=blood_request
    )
    return notification

def send_blood_request_notifications(blood_request):
    """
    Send notifications to potential donors when a new blood request is created
    """
    # Find available donors with matching blood group
    matching_donors = UserProfile.objects.filter(
        blood_group=blood_request.blood_group,
        is_donor=True,
        is_available=True
    ).exclude(user=blood_request.requester)
    
    for donor_profile in matching_donors:
        create_notification(
            user=donor_profile.user,
            notification_type='blood_request',
            title=f"🩸 New Blood Request for {blood_request.blood_group}",
            message=f"Urgent: {blood_request.requester.username} needs {blood_request.units_required} unit(s) of {blood_request.blood_group} blood at {blood_request.hospital_name}. Please check if you can help.",
            blood_request=blood_request
        )

def send_request_accepted_notification(blood_request):
    """
    Send notification to requester when their request is accepted
    """
    create_notification(
        user=blood_request.requester,
        notification_type='request_accepted',
        title=f"✅ Your Blood Request Was Accepted!",
        message=f"Great news! {blood_request.accepted_by.username} has accepted your blood request for {blood_request.blood_group}. Please contact them to arrange donation.",
        blood_request=blood_request
    )

def send_donor_available_notifications(blood_request):
    """
    Send notifications to requesters when new donors become available
    """
    # Find pending requests that match the donor's blood group
    matching_requests = BloodRequest.objects.filter(
        blood_group=blood_request.blood_group,
        status='pending'
    )
    
    for request in matching_requests:
        create_notification(
            user=request.requester,
            notification_type='donor_available',
            title=f"👥 New Donor Available for {request.blood_group}",
            message=f"A new donor with {blood_request.blood_group} blood type has become available in your area.",
            blood_request=request
        )