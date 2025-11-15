from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, BloodRequest
from datetime import datetime
from django.core.validators import FileExtensionValidator


class ProfileEditForm(forms.ModelForm):
    # User model fields
    first_name = forms.CharField(max_length=30, required=False, help_text="Your first name")
    last_name = forms.CharField(max_length=30, required=False, help_text="Your last name")
    email = forms.EmailField(help_text="Your email address")

    # Profile picture field
    profile_picture = forms.ImageField(
        required=False,
        help_text='Upload a JPG, JPEG, or PNG image (max 2MB)',
        widget=forms.FileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png'})
    )

    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email', 'profile_picture',
            'blood_group', 'phone', 'address', 'date_of_birth',
            'is_donor', 'is_available', 'last_donation_date'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your current address...'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'last_donation_date': forms.DateInput(attrs={'type': 'date'})
        }
        help_texts = {
            'is_available': 'Toggle this if you are currently available to donate blood',
            'last_donation_date': 'When did you last donate blood? (Important for eligibility)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for User model fields
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Check file size (2MB limit)
            if picture.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Profile picture must be less than 2MB')

            # Check file extension
            ext = os.path.splitext(picture.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError('Only JPG, JPEG, and PNG files are allowed')

        return picture

    def save(self, commit=True):
        # Save UserProfile first
        profile = super().save(commit=False)

        # Update User model fields
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()

            # Handle profile picture
            if 'profile_picture' in self.changed_data:
                profile.save()  # This will trigger the resize method

            profile.save()

        return profile

# Import BLOOD_GROUPS from models
from .models import BLOOD_GROUPS

class CustomUserCreationForm(UserCreationForm):
    # Additional fields for user profile
    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUPS,
        required=True,
        help_text="Select your blood group"
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter your phone number"
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True,
        help_text="Enter your current address"
    )
    date_of_birth = forms.DateField(
        required=True,
        help_text="Format: YYYY-MM-DD",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',
                 'blood_group', 'phone', 'address', 'date_of_birth']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create UserProfile with additional data
            UserProfile.objects.create(
                user=user,
                blood_group=self.cleaned_data['blood_group'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                is_donor=True  # Default to donor when registering
            )
        return user

class BloodRequestForm(forms.ModelForm):
    # Custom field for needed_by date
    needed_by_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date()}),
        help_text="Date when blood is needed",
        initial=datetime.now().date()  # Set default to today
    )
    needed_by_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        help_text="Time when blood is needed",
        initial='12:00'  # Set default time
    )

    class Meta:
        model = BloodRequest
        fields = [
            'blood_group', 'units_required', 'urgency', 'message',
            'hospital_name', 'hospital_address', 'contact_person', 'contact_phone',
            'needed_by_date', 'needed_by_time'
        ]
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Any additional information for potential donors...'}),
            'hospital_address': forms.Textarea(attrs={'rows': 3}),
            'hospital_name': forms.TextInput(attrs={'placeholder': 'e.g., UAP Medical Center'}),
            'contact_person': forms.TextInput(attrs={'placeholder': 'Name of contact person'}),
            'contact_phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
        }
        help_texts = {
            'units_required': 'Number of units of blood required (1 unit = 450ml)',
            'contact_person': 'Person to contact at the hospital',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for new fields
        self.fields['hospital_name'].initial = 'UAP Medical Center'
        self.fields['hospital_address'].initial = 'UAP Campus, Kuratoli, Dhaka'
        self.fields['contact_person'].initial = 'Medical Staff'
        self.fields['contact_phone'].initial = '0123456789'
    
    def save(self, commit=True):
        # Combine date and time into needed_by field
        instance = super().save(commit=False)
        needed_by_date = self.cleaned_data['needed_by_date']
        needed_by_time = self.cleaned_data['needed_by_time']
        instance.needed_by = datetime.combine(needed_by_date, needed_by_time)

        if commit:
            instance.save()
        return instance

class ProfileEditForm(forms.ModelForm):
    # User model fields
    first_name = forms.CharField(max_length=30, required=False, help_text="Your first name")
    last_name = forms.CharField(max_length=30, required=False, help_text="Your last name")
    email = forms.EmailField(help_text="Your email address")

    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email',  # User model fields
            'blood_group', 'phone', 'address', 'date_of_birth',
            'is_donor', 'is_available', 'last_donation_date'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your current address...'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'last_donation_date': forms.DateInput(attrs={'type': 'date'})
        }
        help_texts = {
            'is_available': 'Toggle this if you are currently available to donate blood',
            'last_donation_date': 'When did you last donate blood? (Important for eligibility)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for User model fields
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        # Save UserProfile first
        profile = super().save(commit=False)
        
        # Update User model fields
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            profile.save()
        
        return profile