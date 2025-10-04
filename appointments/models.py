from django.db import models
from django.contrib.auth.models import User
from users.models import Doctor
from django.utils import timezone

# Create your models here.
'''
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.user.username} - {self.date} {self.time}"
'''
class AvailableSlot(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='available_slots', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)  # فیلد جدید برای مشخص کردن وضعیت رزرو

    def __str__(self):
        return f"{self.doctor.user.username}: {self.start_time} - {self.end_time} ({'Booked' if self.is_booked else 'Available'})"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    available_slot = models.ForeignKey(AvailableSlot, related_name='appointments', on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField(default=timezone.now)  # تعیین مقدار پیش‌فرض
    notes = models.TextField(blank=True, null=True)  # یادداشت‌های قرار

    def __str__(self):
        return f"Appointment with {self.doctor.user.username} on {self.appointment_time}"

class ImageModel(models.Model):
    patient = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, related_name='uploaded_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='patient_images/')
    title = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image {self.title} uploaded by Dr. {self.uploaded_by.username} for {self.patient.username}'
class Prescreption_Model(models.Model):
    patient = models.ForeignKey(User, related_name='prescriptions', on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, related_name='uploaded_prescriptions', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)