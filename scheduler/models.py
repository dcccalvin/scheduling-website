from django.db import models
from django.contrib.auth.models import User
# django.contrib.auth.models
# Create your models here.
CATEGORY_CHOICES = [
('doctor', 'Doctor'),
('hotel', 'Hotel/Restaurant'),
('teacher', 'Teacher'),
('trainer', 'Trainer/Gym'),
('saloon', 'Saloon/Barbershop'),
('church', 'Church'),
]
class ServiceProvider(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)               

def __str__(self):
        return self.name

class Service(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()

def __str__(self):
        return self.name
