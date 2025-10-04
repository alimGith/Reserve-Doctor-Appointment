from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'appointment_time']  # جایگزینی 'date' و 'time' با 'appointment_time'
    list_filter = ['doctor', 'appointment_time']  # جایگزینی 'date' با 'appointment_time'

admin.site.register(Appointment, AppointmentAdmin)

#admin.site.register(Appointment)
