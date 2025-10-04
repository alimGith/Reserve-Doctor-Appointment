from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default='12345678')
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"