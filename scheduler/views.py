from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ServiceProviderForm

# Create your views here
def home(request):
    return render(request, 'scheduler/home.html')

def register(request):
    if request.method == 'POST':
        print ("POST request received")
        user_form = UserRegistrationForm(request.POST)
        provider_form = ServiceProviderForm(request.POST)
        if user_form.is_valid() and provider_form.is_valid():
            print("Details receivd successfully")
            user = user_form.save()
            service_provider = provider_form.save(commit=False)
            service_provider.user = user
            service_provider.save()
            return redirect('login')
            
        else:
            print("Wrong input.")
            user_form = UserRegistrationForm()
            provider_form = ServiceProviderForm()
    return render(request, 'scheduler/register.html', {'user_form': user_form, 'provider_form': provider_form})

@login_required
def profile(request):
    return render(request, 'scheduler/profile.html')