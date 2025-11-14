from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from django.http import JsonResponse
from .forms import CustomUserCreationForm, BloodRequestForm, ProfileEditForm
from .models import UserProfile, BloodRequest, Notification
from .utils import send_blood_request_notifications, send_request_accepted_notification, send_donor_available_notifications
from django.shortcuts import render

from .geolocation import geocode_address, get_nearby_donors
from .models import BLOOD_GROUPS

from .models import UserProfile, BloodRequest, Notification, BLOOD_GROUPS

from django.contrib.auth import logout
from django.contrib import messages


def home(request):
    """Home page view"""
    return render(request, 'home.html')




@login_required
def donor_list(request):
    # Get search parameters from GET request
    blood_group = request.GET.get('blood_group', '')
    location = request.GET.get('location', '')
    use_radius = request.GET.get('use_radius', False)
    
    # Start with all available donors (excluding current user)
    donors = UserProfile.objects.filter(
        is_donor=True,
        is_available=True
    ).exclude(user=request.user)

    # Apply blood group filter if provided
    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    # Apply location filter if provided (simple text search in address)
    if location:
        donors = donors.filter(address__icontains=location)

    # FIX: Use BLOOD_GROUPS from models instead of UserProfile.BLOOD_GROUPS
    from .models import BLOOD_GROUPS  # Add this import
    blood_groups = BLOOD_GROUPS

    # For radius search demonstration (mock data)
    search_type = 'radius' if use_radius else 'text'
    if use_radius:
        for donor in donors:
            donor.distance = round(0.5 + (donor.id * 0.1), 2)  # Mock distance

    unread_count = get_unread_notification_count(request.user)

    return render(request, 'donor_list.html', {
        'donors': donors,
        'blood_groups': blood_groups,  # Use the imported BLOOD_GROUPS
        'selected_blood_group': blood_group,
        'selected_location': location,
        'search_type': search_type,
        'unread_count': unread_count,
    })



@login_required
def request_history(request):
    # Get user's blood requests
    user_requests = BloodRequest.objects.filter(requester=request.user).order_by('-created_at')
    unread_count = get_unread_notification_count(request.user)
    
    return render(request, 'request_history.html', {
        'user_requests': user_requests,  # This was missing!
        'user': request.user,
        'unread_count': unread_count,
    })




@login_required
def request_blood(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.save()
            
            # ✅ ADD NOTIFICATION: Send to matching donors
            from .utils import send_blood_request_notifications
            send_blood_request_notifications(blood_request)
            
            messages.success(request, 'Blood request submitted successfully!')
            return redirect('request_history')
    else:
        form = BloodRequestForm()

    unread_count = get_unread_notification_count(request.user)
    return render(request, 'request_blood.html', {
        'form': form,
        'user': request.user,
        'unread_count': unread_count,
    })






#register
# In bloodbank/views.py - UPDATE register FUNCTION:

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Geocode address and save coordinates
            profile = UserProfile.objects.get(user=user)
            lat, lng = geocode_address(profile.address)
            profile.latitude = lat
            profile.longitude = lng
            profile.save()
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})




#dashboard
@login_required
def dashboard(request):
    # Get user profile data
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    # Get user's blood requests
    user_requests = BloodRequest.objects.filter(requester=request.user).order_by('-created_at')[:5]

    # Get pending requests for user's blood group (if user is donor)
    pending_requests = []
    if profile and profile.is_donor and profile.is_available:
        pending_requests = BloodRequest.objects.filter(
            blood_group=profile.blood_group,
            status='pending'
        ).exclude(requester=request.user).order_by('-urgency', '-created_at')[:3]

    # Get recent notifications
    recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Calculate unread count
    unread_count = get_unread_notification_count(request.user)

    return render(request, 'dashboard.html', {
        'user': request.user,
        'profile': profile,
        'user_requests': user_requests,
        'pending_requests': pending_requests,
        'recent_notifications': recent_notifications,
        'unread_count': unread_count,  # Add this to context
    })


#profile
# Update other views to include unread_count
@login_required
def profile(request):
    try:
        profile_obj = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile_obj = UserProfile.objects.create(user=request.user)
    
    unread_count = get_unread_notification_count(request.user)
    
    return render(request, 'profile.html', {
        'user': request.user,
        'profile': profile_obj,
        'unread_count': unread_count,
    })



#function to calculate unread notifications
def get_unread_notification_count(user):
    return Notification.objects.filter(user=user, is_read=False).count()

    # Start with all available donors (excluding current user)
    donors = UserProfile.objects.filter(
        is_donor=True,
        is_available=True
    ).exclude(user=request.user)

    # Apply blood group filter if provided
    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    # Apply location filter if provided (simple text search in address)
    if location:
        donors = donors.filter(address__icontains=location)

    # Get blood group choices for the dropdown
    blood_groups = UserProfile.BLOOD_GROUPS
    
    unread_count = get_unread_notification_count(request.user)

    return render(request, 'donor_list.html', {
        'donors': donors,
        'blood_groups': blood_groups,
        'selected_blood_group': blood_group,
        'selected_location': location,
        'user': request.user,
        'unread_count': unread_count,
    })




@login_required
# In bloodbank/views.py - UPDATE edit_profile FUNCTION:

@login_required
def edit_profile(request):
    try:
        profile_obj = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile_obj = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile_obj)
        if form.is_valid():
            old_address = profile_obj.address
            profile = form.save()
            
            # ✅ UPDATE GEOLOCATION if address changed
            if old_address != profile.address:
                lat, lng = geocode_address(profile.address)
                profile.latitude = lat
                profile.longitude = lng
                profile.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile_obj)

    unread_count = get_unread_notification_count(request.user)
    return render(request, 'edit_profile.html', {
        'form': form,
        'profile': profile_obj,
        'user': request.user,
        'unread_count': unread_count,
    })
    




@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user)

    # Mark all as read when user visits notifications page
    user_notifications.filter(is_read=False).update(is_read=True)

    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    return render(request, 'notifications.html', {
        'notifications': user_notifications,
        'user': request.user,
        'unread_count': unread_count,
    })





@login_required
def notification_count(request):
    """API endpoint to get unread notification count (for AJAX updates)"""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'count': count})
    return JsonResponse({'error': 'Invalid request'})





@login_required
def toggle_availability(request):
    """Toggle donor availability"""
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        old_availability = profile.is_available
        profile.is_available = not profile.is_available
        profile.save()
        
        # ✅ ADD NOTIFICATION: If becoming available, notify matching requests
        if not old_availability and profile.is_available:
            from .utils import send_donor_available_notifications
            send_donor_available_notifications(profile)
        
        messages.success(request, f'Availability set to {profile.is_available}')
        return redirect('profile')




@login_required
def accept_request(request, request_id):
    """Accept a blood request"""
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    if request.user != blood_request.requester:
        blood_request.accepted_by = request.user
        blood_request.accepted_at = timezone.now()
        blood_request.status = 'accepted'
        blood_request.save()
        
        # ✅ ADD NOTIFICATION: Notify requester
        from .utils import send_request_accepted_notification
        send_request_accepted_notification(blood_request)
        
        messages.success(request, 'Request accepted successfully!')
    else:
        messages.error(request, 'You cannot accept your own request!')
    return redirect('dashboard')




@login_required
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'})



def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('home')
    
    # If GET request, show confirmation page
    unread_count = get_unread_notification_count(request.user)
    return render(request, 'logout.html', {
        'user': request.user,
        'unread_count': unread_count,
    })