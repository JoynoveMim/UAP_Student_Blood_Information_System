from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import UserProfile, BloodRequest


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    # Get user profile data
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    return render(request, 'dashboard.html', {
        'user': request.user,
        'profile': profile
    })


@login_required
def profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    return render(request, 'profile.html', {
        'user': request.user,
        'profile': profile
    })


@login_required
def donor_list(request):
    # Get all available donors (excluding current user)
    donors = UserProfile.objects.filter(
        is_donor=True,
        is_available=True
    ).exclude(user=request.user)

    return render(request, 'donor_list.html', {
        'donors': donors,
        'user': request.user
    })


@login_required
def request_blood(request):
    return render(request, 'request_blood.html', {'user': request.user})