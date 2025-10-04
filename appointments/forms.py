from django import forms
from .models import AvailableSlot, Appointment, ImageModel, Prescreption_Model

class AvailableSlotForm(forms.ModelForm):
    class Meta:
        model = AvailableSlot
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_time',]

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان تصویر'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class PrescreptionModelForm(forms.ModelForm):
    class Meta:
        model = Prescreption_Model
        fields = ['title','text',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان نسخه'}),
            #'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'text' : forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }