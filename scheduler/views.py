from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm, UserRegistrationForm, ServiceProviderForm,ServiceForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Appointment, Service,Profile
from django.contrib.auth import login
from django.db import IntegrityError

# Create your views here
def home(request):
    return render(request, 'scheduler/home.html')

####################################################################################################################
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        provider_form = ServiceProviderForm(request.POST)
        print("POST request received")  # Debugging statement

        if user_form.is_valid():
            user = user_form.save()
            is_service_provider = user_form.cleaned_data.get('is_service_provider')
            print(f"User form is valid. is_service_provider: {is_service_provider}")  # Debugging statement

            try:
                profile, created = Profile.objects.get_or_create(user=user, defaults={'is_service_provider': is_service_provider})
                
                if is_service_provider:
                    if provider_form.is_valid():
                        service_provider = provider_form.save(commit=False)
                        service_provider.user = user
                        service_provider.save()
                        print("Service provider form is valid and saved")  # Debugging statement
                    else:
                        user.delete()  # Clean up if service provider form is invalid
                        print("Service provider form is invalid")  # Debugging statement
                        return render(request, 'scheduler/register.html', {'user_form': user_form, 'provider_form': provider_form})
                
                login(request, user)
                print("User logged in successfully")  # Debugging statement
                return redirect('profile')
            except IntegrityError as e:
                user.delete()  # Clean up if profile creation failed
                print(f"IntegrityError: {e}")  # Debugging statement
                return render(request, 'scheduler/register.html', {'user_form': user_form, 'provider_form': provider_form, 'error': 'Could not create profile. Please try again.'})
        else:
            print("User form is invalid")  # Debugging statement
            print(user_form.errors)  # Debugging statement
    else:
        user_form = UserRegistrationForm()
        provider_form = ServiceProviderForm()

    return render(request, 'scheduler/register.html', {'user_form': user_form, 'provider_form': provider_form})
##################################################################################################
@login_required
def profile(request):
    if request.user.profile.is_service_provider:
        services = Service.objects.filter(service_provider=request.user.serviceprovider)
        return render(request, 'scheduler/service_provider_profile.html', {'services': services})
    else:
        appointments = Appointment.objects.filter(client=request.user)
        services = Service.objects.all()  # Fetch all services available for booking
        return render(request, 'scheduler/client_profile.html', {'appointments': appointments, 'services': services})
#########################################################################################################  
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
######################################################################################################
class  CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'
######################################################################################################
@login_required
def book_appointment(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.service = service
            appointment.save()
            return redirect('profile')
    else:
        form = BookingForm()
    return render(request, 'scheduler/book_appointment.html', {'form': form, 'service': service}) 
########################################################################################################   
@login_required
def book_appointment(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.service = service
            appointment.save()
            return redirect('profile')
    else:
        form = BookingForm()
    return render(request, 'scheduler/book_appointment.html', {'form': form, 'service': service})
################################################################################################################
@login_required
def create_service(request):
    if not request.user.profile.is_service_provider:
        return redirect('profile')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.service_provider = request.user.serviceprovider
            service.save()
            return redirect('profile')
    else:
        form = ServiceForm()
    
    return render(request, 'scheduler/create_service.html', {'form': form})
###########################################################################################################################################
@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.service_provider = request.user.serviceprovider  
            service.save()
            return redirect('profile')  
    else:
        form = ServiceForm()
    
    return render(request, 'scheduler/add_service.html', {'form': form})