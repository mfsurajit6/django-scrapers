from django import forms
from user.models import User


class RegistrationForm(forms.ModelForm):
    """User Registration Form"""
    class Meta:
        model = User
        fields = ("name", "email", "password")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("Email is already registered")
        except User.DoesNotExist:
            return email
