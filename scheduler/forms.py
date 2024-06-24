from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Appointment, ServiceProvider,Service

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat password')
    is_service_provider = forms.BooleanField(required=False, label='Register as service provider')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'is_service_provider']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['category', 'name', 'description', 'location']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration']               