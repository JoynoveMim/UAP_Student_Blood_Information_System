from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    # Additional fields for user profile
    blood_group = forms.ChoiceField(
        choices=UserProfile.BLOOD_GROUPS,
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